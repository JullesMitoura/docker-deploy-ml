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

## Módulo 08: Serving do Modelo via API REST
> **Entrega**: API de inferência rodando em Docker

---

Até aqui, a inferência era executada via linha de comando  um script que roda, imprime um resultado e encerra. Em produção, isso não é viável: outros sistemas precisam chamar o modelo sob demanda, de forma programática, via rede. Este módulo transforma o modelo em um **serviço HTTP** com FastAPI.

A diferença fundamental é o modelo de execução: em vez de um script que termina, temos um **servidor que fica em execução contínua**, aguardando requisições. O modelo é carregado uma única vez na memória ao iniciar, e cada requisição recebe uma resposta JSON em milissegundos.

### O que você vai aprender

- Como construir uma API REST de inferência com FastAPI
- Usar `uvicorn` como servidor ASGI para receber conexões HTTP
- Carregar o modelo uma única vez na inicialização com o padrão `lifespan`
- Expor endpoints REST para as duas capacidades de inferência do modelo
- Configurar `PYTHONPATH` corretamente dentro do container

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| FastAPI | Framework Python para construção de APIs REST com validação automática |
| uvicorn | Servidor ASGI que recebe conexões HTTP e executa a aplicação FastAPI |
| `lifespan` | Padrão para executar código na inicialização e encerramento do servidor |
| Endpoint REST | Rota HTTP (`GET /predict`, `POST /predict`) que recebe e retorna JSON |
| `PYTHONPATH` | Variável de ambiente que define onde o Python busca módulos |

### O que muda no fluxo

```
Antes (CLI):   docker run → script roda → resultado impresso → container encerra
Depois (API):  docker run → servidor inicia → aguarda requisições → responde JSON
```

Essa mudança é o que viabiliza integração com frontends, outros microsserviços, dashboards e qualquer cliente HTTP  tornando o modelo verdadeiramente consumível em produção.
