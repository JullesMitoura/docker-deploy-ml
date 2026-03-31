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

## Módulo 06: Questionário
> CI com GitHub Actions

---

**Questão 1**

No workflow do módulo 06, qual instrução YAML garante que o job `test` só comece após os jobs `build-train` e `build-inference` concluírem com sucesso?

- a) `depends: [build-train, build-inference]`
- b) `after: build-train, build-inference`
- c) `needs: [build-train, build-inference]`
- d) `requires: [build-train, build-inference]`

<details>
<summary>Resposta</summary>

**c)** A chave `needs` no GitHub Actions define dependências entre jobs. O job `test` só é colocado na fila de execução quando todos os jobs listados em `needs` completam com status de sucesso. Se qualquer um falhar, o `test` é cancelado.

</details>

---

**Questão 2**

Jobs do GitHub Actions rodam em VMs independentes e não compartilham sistema de arquivos. Como a imagem Docker buildada no job `build-train` é disponibilizada para o job `test`?

- a) O Docker Hub atua como intermediário: o build-train faz push e o test faz pull
- b) O job build-train usa `docker save` para exportar a imagem como tarball, faz upload como artefato de CI; o job test faz download e usa `docker load` para restaurá-la
- c) O GitHub Actions mantém um cache de imagens Docker compartilhado entre todos os jobs do workflow
- d) Variáveis de ambiente transmitem o hash da imagem, e o Docker a baixa automaticamente do registry local

<details>
<summary>Resposta</summary>

**b)** Como cada job roda em uma VM zerada, `docker save` serializa a imagem em um arquivo `.tar`, que é salvo como artefato via `upload-artifact`. O job `test` baixa esse arquivo com `download-artifact` e o carrega com `docker load`, tornando a imagem disponível localmente sem precisar publicá-la em um registry.

</details>

---

**Questão 3**

No cache do GitHub Actions configurado com `type=gha,scope=train`, qual é a função do parâmetro `scope`?

- a) Define o nível de permissão de leitura e escrita no cache
- b) Isola o cache de `build-train` do cache de `build-inference`, evitando que um invalide o outro
- c) Limita o cache ao branch `main`, sem usar em feature branches
- d) Especifica quantos gigabytes de cache são reservados para o job

<details>
<summary>Resposta</summary>

**b)** Sem `scope`, os dois jobs de build compartilhariam o mesmo namespace de cache. Com scopes distintos (`scope=train` e `scope=inference`), cada imagem tem seu próprio cache independente  uma mudança nas dependências de treino não invalida o cache de inferência.

</details>
