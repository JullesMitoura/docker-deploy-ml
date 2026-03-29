<div align="center">

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
     alt="Python"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg"
     alt="Docker"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg"
     alt="FastAPI"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 09: Questionário
> Ambiente de Produção com Docker Compose

---

**Questão 1**

O que a instrução `depends_on: condition: service_completed_successfully` garante no `docker-compose.yml`?

- a) Que o serviço `serve` reinicia automaticamente se o serviço `train` falhar
- b) Que o serviço `serve` só é iniciado após o serviço `train` encerrar com código de saída 0 (sucesso)
- c) Que os dois serviços compartilham o mesmo volume automaticamente
- d) Que o serviço `train` aguarda a API `serve` estar saudável antes de iniciar

<details>
<summary>Resposta</summary>

**b)** `service_completed_successfully` é mais restrito que o simples `depends_on`: ele verifica não apenas que o container iniciou, mas que encerrou com código 0. Se o treino falhar (código diferente de 0), o `serve` não sobe  garantindo que a API nunca inicialize sem um modelo válido disponível.

</details>

---

**Questão 2**

Qual é a diferença prática entre executar `docker compose up` e `docker compose -f docker-compose.yml up`?

- a) Não há diferença; ambos os comandos são equivalentes
- b) O primeiro carrega automaticamente `docker-compose.yml` + `docker-compose.override.yml` (modo dev); o segundo usa apenas o arquivo base (modo produção)
- c) O primeiro usa a versão mais recente das imagens; o segundo usa as imagens cacheadas localmente
- d) O primeiro inicia os serviços em background; o segundo em primeiro plano

<details>
<summary>Resposta</summary>

**b)** O Docker Compose carrega `docker-compose.override.yml` automaticamente quando ele existe no diretório. O override adiciona hot reload, monta o código-fonte como volume e ativa logs de debug. Para produção, passar explicitamente `-f docker-compose.yml` ignora o override e usa apenas a configuração base.

</details>

---

**Questão 3**

Para que serve o `HEALTHCHECK` definido no `Dockerfile.serve`?

- a) Bloqueia requisições externas enquanto o modelo ainda está sendo carregado
- b) Verifica periodicamente se o container está respondendo; orquestradores usam esse status para roteamento de tráfego e reinício automático
- c) Registra métricas de latência da API no log do Docker
- d) Garante que apenas requisições com header de autenticação sejam aceitas

<details>
<summary>Resposta</summary>

**b)** O Docker verifica a saúde do container no intervalo configurado fazendo uma requisição para `GET /health`. O resultado aparece em `docker ps` como `(healthy)` ou `(unhealthy)`. Orquestradores como Kubernetes usam esse status para decidir se o container deve receber tráfego  um container `unhealthy` é removido da rotação e reiniciado.

</details>
