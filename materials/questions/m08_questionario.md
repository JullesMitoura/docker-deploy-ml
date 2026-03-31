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

## Módulo 08: Questionário
> Serving do Modelo via API REST

---

**Questão 1**

Por que o modelo é carregado dentro do `lifespan` do FastAPI, e não dentro da função de cada endpoint?

- a) O `lifespan` é o único contexto onde o `pickle.load` funciona corretamente
- b) Para que o modelo seja carregado uma única vez no startup, ficando em memória para todas as requisições, em vez de ser re-lido do disco a cada chamada
- c) Endpoints assíncronos não podem realizar operações de I/O como leitura de arquivos
- d) O FastAPI impede acesso ao sistema de arquivos dentro de funções de rota por questões de segurança

<details>
<summary>Resposta</summary>

**b)** Carregar um modelo do disco é uma operação relativamente lenta. Se feita a cada requisição, a latência da API seria dominada pelo I/O, não pela inferência. Com `lifespan`, o modelo é lido uma única vez durante o startup e mantido em memória  todas as requisições subsequentes usam o objeto já carregado.

</details>

---

**Questão 2**

Qual é o papel do `uvicorn` no container de serving?

- a) Substitui o FastAPI como framework de rotas e validação de dados
- b) É o servidor ASGI que recebe as conexões HTTP e executa a aplicação FastAPI
- c) Gerencia o volume Docker onde o modelo está armazenado
- d) Compila o código Python em bytecode otimizado para menor latência

<details>
<summary>Resposta</summary>

**b)** FastAPI é um framework  ele define rotas, valida dados com Pydantic e gera documentação. Mas ele não escuta conexões de rede por conta própria. O `uvicorn` é o servidor ASGI que recebe requisições HTTP, as passa para a aplicação FastAPI e retorna as respostas ao cliente.

</details>

---

**Questão 3**

Por que `sqlalchemy` não está no `requirements-serve.txt`?

- a) O FastAPI usa seu próprio ORM integrado, tornando o sqlalchemy redundante
- b) O `sqlalchemy` é incompatível com o uvicorn em modo assíncrono
- c) O container de serving nunca acessa o banco de dados; ele apenas carrega o modelo via volume e gera predições
- d) O `sqlalchemy` já vem instalado na imagem base `python:3.11-slim`

<details>
<summary>Resposta</summary>

**c)** O banco de dados (`heat_exchanger.db`) é necessário apenas no treino, para carregar os dados históricos. A API de serving recebe uma data ou eficiência como entrada, usa o modelo já carregado em memória para calcular a predição e retorna o resultado  sem nenhuma consulta ao banco.

</details>
