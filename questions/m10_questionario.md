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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/githubactions/githubactions-original.svg"
     alt="GitHub Actions"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 10: Questionário
> Workflow End-to-End

---

**Questão 1**

O que é um **smoke test** no contexto do pipeline de CI deste módulo?

- a) Um teste de carga que simula centenas de requisições simultâneas para verificar a estabilidade da API
- b) Um teste unitário que valida a lógica matemática do modelo de regressão
- c) Uma verificação mínima que confirma se a API subiu e está respondendo a requisições, sem testar lógica de negócio
- d) Um script que compara as métricas do novo modelo com o modelo em produção antes de promovê-lo

<details>
<summary>Resposta</summary>

**c)** O smoke test faz o mínimo necessário para saber se "a fumaça saiu"  ou seja, se o sistema está de pé. No pipeline do módulo 10, isso significa subir o container de serving e verificar que `GET /health` retorna `{"status": "ok"}` e que `POST /predict/*` responde sem erro. Se o smoke test passar, o código é publicado.

</details>

---

**Questão 2**

Qual é o propósito do `Makefile` neste módulo?

- a) Substituir o Docker Compose como ferramenta de orquestração de containers
- b) Centralizar os comandos mais usados do projeto (build, treino, serving, testes) em targets de fácil execução
- c) Automatizar a geração do workflow YAML do GitHub Actions
- d) Definir as variáveis de ambiente de produção de forma segura

<details>
<summary>Resposta</summary>

**b)** O `Makefile` funciona como um "menu de comandos" do projeto. Em vez de lembrar e digitar `docker compose -f docker-compose.yml up --build`, o desenvolvedor executa `make up`. Isso reduz erros, facilita o onboarding e garante que todos na equipe usem os mesmos comandos com os mesmos parâmetros.

</details>

---

**Questão 3**

Considerando o pipeline completo do módulo 10, qual é a sequência correta de eventos após um `git push origin main`?

- a) Push ao Docker Hub → build das imagens → testes de integração → smoke test da API
- b) Build das imagens (paralelo) → testes de integração + smoke test → push ao Docker Hub
- c) Testes unitários → build das imagens → smoke test da API → push ao Docker Hub
- d) Build das imagens (paralelo) → push ao Docker Hub → testes de integração → smoke test da API

<details>
<summary>Resposta</summary>

**b)** A ordem importa: primeiro as imagens são construídas em paralelo (com cache do GHA), depois os testes são executados  incluindo o smoke test da API. Somente após todos os testes passarem é que as imagens são publicadas no Docker Hub. Publicar antes de testar criaria o risco de colocar código quebrado em produção.

</details>
