# Prompt utilizado (IAG)

**Ferramenta de IA generativa:** Claude (Anthropic)

O frontend deste projeto foi gerado com auxílio de IA generativa. Abaixo, o
prompt utilizado para gerar a tela que consome as Azure Functions.

## Prompt

> Crie um frontend web simples (HTML, CSS e JavaScript puro, sem framework) para
> a atividade PJBL. A tela deve executar 4 Azure Functions (CRUD) conectadas ao
> MongoDB Atlas:
>
> - Inserir — `POST /api/insert`
> - Pesquisar/Listar — `GET /api/pesquisar`
> - Alterar — `PUT /api/alterar`
> - Excluir — `DELETE /api/excluir`
>
> Requisitos da interface:
> - Campo para configurar a URL base das Azure Functions (salvo em `localStorage`).
> - Formulário de inserir (campos nome e descrição).
> - Busca por nome + botão "Listar todos", exibindo os resultados em uma tabela.
> - Botões "Editar" e "Excluir" por linha da tabela.
> - Formulário de alterar (preenchido ao clicar em Editar).
> - Um painel de log mostrando a resposta (status HTTP) de cada function chamada.
> - Tema escuro, layout responsivo e textos em português (PT-BR).
>
> As chamadas devem ser feitas com `fetch`. Trate erros de rede e exiba mensagens
> claras no log.

O resultado está em [`frontend/index.html`](frontend/index.html).
