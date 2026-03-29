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

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 03: Questionário
> Treino e Inferência Separados

---

**Questão 1**

Qual mecanismo Docker permite que o container de inferência acesse o `model.pkl` gerado pelo container de treino?

- a) O Docker copia automaticamente arquivos entre containers na mesma rede
- b) Um volume montado no host, compartilhado entre os dois containers via flag `-v`
- c) O `COPY` no Dockerfile do container de inferência busca o modelo do container de treino
- d) Variáveis de ambiente transmitem o conteúdo binário do modelo entre containers

<details>
<summary>Resposta</summary>

**b)** Um volume Docker monta um diretório do host dentro do container. O treino escreve `model.pkl` em `/app/models` (mapeado para `./models` no host); a inferência lê do mesmo mapeamento. O modelo persiste no host e é acessível por qualquer container que monte o mesmo diretório.

</details>

---

**Questão 2**

Por que `sqlalchemy` foi removido do `requirements-inference.txt`, mas permanece no `requirements-train.txt`?

- a) `sqlalchemy` é incompatível com a imagem base `python:3.11-slim`
- b) O container de inferência lê o modelo via pickle, sem precisar acessar o banco de dados
- c) `sqlalchemy` causa conflito de versão com `scikit-learn` na inferência
- d) É uma preferência de estilo; tecnicamente poderia estar em ambos

<details>
<summary>Resposta</summary>

**b)** O container de treino precisa do `sqlalchemy` para ler os dados do banco SQLite. O container de inferência recebe apenas o modelo serializado via volume  ele nunca acessa o banco. Remover dependências desnecessárias reduz o tamanho da imagem e diminui a superfície de ataque.

</details>

---

**Questão 3**

Em um cenário de produção, qual é o principal problema de rodar treino e inferência no **mesmo** container?

- a) O Docker não permite executar dois scripts Python na mesma imagem
- b) O `model.pkl` fica exposto na imagem, criando risco de segurança
- c) Treino e inferência têm ciclos de vida diferentes, o que impede escala independente e força rebuild da imagem de serving a cada re-treino
- d) A imagem unificada não consegue usar variáveis de ambiente distintas para cada processo

<details>
<summary>Resposta</summary>

**c)** Em produção, o treino acontece periodicamente (re-treino com novos dados) enquanto a inferência precisa estar disponível continuamente. Se estiverem na mesma imagem, qualquer atualização do modelo exige rebuildar e redeployar toda a imagem de serving  além de tornar impossível escalar os dois processos de forma independente.

</details>
