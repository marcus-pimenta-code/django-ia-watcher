# Projeto Django + Next.js com Docker

## Como rodar o projeto (desenvolvimento)

1. Extraia o zip:
   ```bash
   unzip projeto_reestruturado_avancado.zip
   cd projeto_reestruturado_avancado
   ```

2. Suba o ambiente de desenvolvimento:
   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

3. Acessos rápidos:
   - Frontend (Next.js): http://localhost:3000
   - Backend (Django API): http://localhost:8000/api/

---

## Rodar o ambiente de produção

Para simular a produção com NGINX:
```bash
docker compose -f docker-compose.prod.yml up --build
```

Acesso pelo navegador: http://localhost

---

## Comandos úteis

| Ação | Comando |
|:---|:---|
| Parar tudo | `docker compose -f docker-compose.dev.yml down` |
| Ver containers rodando | `docker ps` |
| Ver logs do frontend | `docker logs -f projeto_frontend_1` |
| Ver logs do backend | `docker logs -f projeto_backend_1` |

---

## Observações

- Django roda com `DEBUG=True` em desenvolvimento e `DEBUG=False` na produção.
- O banco de dados SQLite está persistente em `db_data`.
- O Next.js já está configurado para consumir a API do Django usando a variável `NEXT_PUBLIC_BACKEND_URL`.
=======
