# PJBL - Semana 5: Frontend + Serverless

Arquitetura e Soluções Cloud - Engenharia de Software (Noite)

## Alunos
- Alander Menezes Arantes de Ávila
- Bernardo Creplive Vieira
- Emanuelle Skolut Jose
- Murilo Regnier Stange

## Solução
4 Azure Functions (CRUD) em Python + MongoDB Atlas + frontend web.

- **Function App:** `alander1` (Azure, Brazil South)
- **URL base:** https://alander1-cbewavcrdqfab2ga.brazilsouth-01.azurewebsites.net/api
- **Banco:** MongoDB Atlas — database `pjbl`, collection `itens`

### Endpoints
| Função | Método | Rota |
|---|---|---|
| inserir | POST | `/api/insert` |
| pesquisar | GET | `/api/pesquisar` |
| alterar | PUT | `/api/alterar` |
| excluir | DELETE | `/api/excluir` |

## Estrutura
- `function_app.py` — as 4 Azure Functions (modelo Python v2)
- `requirements.txt` — dependências (azure-functions, pymongo)
- `host.json` — configuração do host
- `frontend/index.html` — tela que executa as 4 functions
- `ENTREGA-Semana5.pdf` — documento de entrega com as evidências

## Configuração
As variáveis `MONGO_URI`, `MONGO_DB` e `MONGO_COLLECTION` ficam nas Application
Settings do Function App (não versionadas por segurança).

## Frontend publicado

- **URL do site (GitHub Pages):** https://aland3r.github.io/pjbl-serverless-semana5/

> **Observação sobre o Azure Static Web Apps:** a criação do recurso no Azure
> Static Web Apps foi bloqueada pela política de regiões permitidas da assinatura
> institucional (PUCPR / Grupo Marista), que barra todas as 5 regiões do serviço.
> Como alternativa funcional, o frontend foi publicado no **GitHub Pages**.

O frontend (`frontend/index.html`, também em `docs/` para o GitHub Pages) consome
as Azure Functions via `fetch`. O endpoint GET utilizado é `GET /api/pesquisar`,
que retorna dados reais do MongoDB Atlas. Não foi utilizado Apidog para mock
(os dados vêm das próprias Azure Functions).

## Grupo e IAG
- Integrantes do grupo: ver [GRUPO.md](GRUPO.md).
- Prompt de IA generativa (IAG) usado para gerar o frontend: ver [Prompt.md](Prompt.md).
