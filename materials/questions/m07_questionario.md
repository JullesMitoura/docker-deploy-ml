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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/githubactions/githubactions-original.svg"
     alt="GitHub Actions"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 07: Questionário
> Publicando no Docker Hub

---

**Questão 1**

Por que o workflow é configurado para **não** fazer push ao Docker Hub quando o evento é um Pull Request?

- a) Pull Requests não têm acesso às Actions configuradas no repositório
- b) PRs de forks não têm acesso a secrets do repositório, e publicar código ainda não revisado polui o registry com imagens de desenvolvimento
- c) O Docker Hub bloqueia automaticamente pushes originados de Pull Requests
- d) A `docker/build-push-action` não suporta execução em contexto de PR

<details>
<summary>Resposta</summary>

**b)** São dois motivos combinados: segurança (PRs de forks não acessam secrets como `DOCKERHUB_TOKEN`) e higiene do registry (não queremos imagens de branches em revisão misturadas com as versões publicadas). O código só vai ao Docker Hub após ser revisado e mergeado em `main`.

</details>

---

**Questão 2**

Por que a tag `:latest` não é suficiente para identificar a versão de uma imagem em produção?

- a) A tag `:latest` só é gerada para versões semver; branches não a recebem
- b) `:latest` é uma tag mutável que aponta para a versão mais recente do push  ela pode mudar sem que o ambiente de produção seja atualizado explicitamente
- c) O Docker Hub limita o número de pulls da tag `:latest` em contas gratuitas
- d) Orquestradores como Kubernetes ignoram a tag `:latest` por padrão

<details>
<summary>Resposta</summary>

**b)** Em produção, rastreabilidade é essencial. A tag `:latest` muda a cada push em `main`  se dois ambientes fazem `docker pull :latest` em momentos diferentes, podem estar rodando versões distintas sem saber. Tags imutáveis como `:{sha}` ou `:v1.2.3` garantem que você sabe exatamente o que está em execução.

</details>

---

**Questão 3**

O que a `docker/metadata-action` faz no workflow de CD?

- a) Gera o `Dockerfile` automaticamente com base no código-fonte do projeto
- b) Autentica no Docker Hub usando os secrets do repositório
- c) Gera automaticamente tags e labels para a imagem com base no contexto do git (branch, SHA, tag semver)
- d) Verifica se a imagem já existe no registry antes de fazer o push

<details>
<summary>Resposta</summary>

**c)** A `metadata-action` lê o contexto do git (qual branch, qual SHA, se há uma tag semver) e produz a lista de tags para a imagem. Um push em `main` gera `:latest`, `:main` e `:{sha}`; uma tag `v1.2.3` gera `:v1.2.3`, `:1.2`, `:1` e `:latest`  tudo automaticamente, sem hardcode no YAML.

</details>
