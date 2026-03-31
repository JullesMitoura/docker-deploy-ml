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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg"
     alt="scikit-learn"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 05: Questionário
> Versionando Artefatos de Modelo

---

**Questão 1**

Por que o versionamento por timestamp (`YYYYMMDD_HHMMSS`) é preferível ao versionamento sequencial (`v1`, `v2`, `v3`) para artefatos de modelo?

- a) O timestamp ocupa menos espaço no nome do arquivo
- b) O timestamp é autoexplicativo, funciona em treinos paralelos sem risco de colisão e não requer estado externo para controlar o próximo número
- c) Ferramentas como MLflow e DVC só reconhecem o formato de timestamp
- d) Números sequenciais não são permitidos em nomes de arquivos `.pkl`

<details>
<summary>Resposta</summary>

**b)** O timestamp carrega informação por si só (você sabe quando o modelo foi treinado). Números sequenciais requerem um contador centralizado  em treinos paralelos, dois workers poderiam gerar `v3` ao mesmo tempo (colisão). O timestamp não tem esse problema.

</details>

---

**Questão 2**

O que é `model_latest.pkl` na estrutura de versionamento deste módulo?

- a) O único arquivo de modelo que deve ser commitado no git
- b) Uma cópia do artefato do treino mais recente, usada como ponteiro para a versão em produção
- c) Um link simbólico imutável gerado uma única vez na primeira execução do treino
- d) O modelo com as melhores métricas entre todos os treinos registrados

<details>
<summary>Resposta</summary>

**b)** `model_latest.pkl` é atualizado a cada treino para apontar para a versão mais recente. Ele serve como convenção de "o que está em produção agora". Os artefatos versionados (`model_20240101_143052.pkl`) são imutáveis; `model_latest.pkl` é o ponteiro mutável.

</details>

---

**Questão 3**

Como é feito o rollback para uma versão anterior do modelo sem precisar rebuildar a imagem Docker?

- a) Editando o `Dockerfile.inference` para apontar para o arquivo correto e executando `docker build`
- b) Deletando `model_latest.pkl` e renomeando o artefato antigo
- c) Passando a variável de ambiente `MODEL_VERSION` com o tag da versão desejada no `docker run`
- d) Modificando o `registry.json` manualmente para alterar o campo `"latest"`

<details>
<summary>Resposta</summary>

**c)** O container de inferência aceita `MODEL_VERSION` como variável de ambiente. Ao passar `MODEL_VERSION=20240101_143052`, o código carrega esse artefato específico do volume, sem qualquer alteração de imagem ou código. Nenhum rebuild, nenhum downtime de pipeline.

</details>
