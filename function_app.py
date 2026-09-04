import os
import json
from datetime import datetime, timezone

import azure.functions as func
from bson import ObjectId
from pymongo import MongoClient

# 4 Azure Functions (modelo Python v2) - CRUD contra o MongoDB Atlas.
# Rotas iguais as da versao Node, entao o frontend nao muda:
#   POST   /api/insert     PUT    /api/alterar
#   GET    /api/pesquisar  DELETE /api/excluir

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

_client = None


def get_collection():
    """Conexao reutilizavel com o Atlas (uma vez por instancia)."""
    global _client
    uri = os.environ.get("MONGO_URI")
    if not uri:
        raise RuntimeError("Variavel MONGO_URI nao configurada.")
    db_name = os.environ.get("MONGO_DB", "pjbl")
    coll = os.environ.get("MONGO_COLLECTION", "itens")
    if _client is None:
        _client = MongoClient(uri)
    return _client[db_name][coll]


def resp(status, body):
    return func.HttpResponse(
        json.dumps(body, default=str),
        status_code=status,
        mimetype="application/json",
    )


@app.route(route="insert", methods=["POST"])
def insert(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        data = {}
    nome = (data or {}).get("nome")
    if not nome:
        return resp(400, {"erro": "O campo 'nome' e obrigatorio."})
    doc = {
        "nome": nome,
        "descricao": (data.get("descricao") or ""),
        "criadoEm": datetime.now(timezone.utc),
    }
    result = get_collection().insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return resp(201, {"mensagem": "Item inserido com sucesso.", "id": str(result.inserted_id), "item": doc})


@app.route(route="pesquisar", methods=["GET"])
def pesquisar(req: func.HttpRequest) -> func.HttpResponse:
    col = get_collection()
    item_id = req.params.get("id")
    nome = req.params.get("nome")
    filtro = {}
    if item_id:
        if not ObjectId.is_valid(item_id):
            return resp(400, {"erro": "id invalido."})
        filtro = {"_id": ObjectId(item_id)}
    elif nome:
        filtro = {"nome": {"$regex": nome, "$options": "i"}}
    itens = list(col.find(filtro).sort("criadoEm", -1).limit(100))
    for it in itens:
        it["_id"] = str(it["_id"])
    return resp(200, {"total": len(itens), "itens": itens})


@app.route(route="alterar", methods=["PUT"])
def alterar(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except ValueError:
        data = {}
    item_id = (data or {}).get("id")
    if not item_id or not ObjectId.is_valid(item_id):
        return resp(400, {"erro": "Um 'id' valido e obrigatorio."})
    campos = {}
    if "nome" in data:
        campos["nome"] = data["nome"]
    if "descricao" in data:
        campos["descricao"] = data["descricao"]
    if not campos:
        return resp(400, {"erro": "Nada para alterar."})
    result = get_collection().update_one({"_id": ObjectId(item_id)}, {"$set": campos})
    if result.matched_count == 0:
        return resp(404, {"erro": "Item nao encontrado."})
    return resp(200, {"mensagem": "Item alterado com sucesso.", "modificados": result.modified_count})


@app.route(route="excluir", methods=["DELETE"])
def excluir(req: func.HttpRequest) -> func.HttpResponse:
    item_id = req.params.get("id")
    if not item_id:
        try:
            item_id = (req.get_json() or {}).get("id")
        except ValueError:
            item_id = None
    if not item_id or not ObjectId.is_valid(item_id):
        return resp(400, {"erro": "Um 'id' valido e obrigatorio (query ?id= ou body)."})
    result = get_collection().delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        return resp(404, {"erro": "Item nao encontrado."})
    return resp(200, {"mensagem": "Item excluido com sucesso."})
