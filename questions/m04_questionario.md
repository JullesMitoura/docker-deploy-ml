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

## Módulo 04: Questionário
> Otimizando Imagens Docker

---

**Questão 1**

Num Dockerfile com multi-stage build, o que acontece com o compilador `gcc` instalado no stage `builder`?

- a) É copiado automaticamente para o stage final junto com os pacotes Python
- b) Permanece disponível no stage final para eventuais compilações em runtime
- c) Fica restrito ao stage `builder` e nunca chega à imagem final
- d) É removido explicitamente por um `RUN apt-get remove gcc` no stage final

<details>
<summary>Resposta</summary>

**c)** No multi-stage build, cada `FROM` inicia uma camada zerada. Apenas o que for explicitamente copiado com `COPY --from=builder` chega à imagem final. O `gcc`, o cache do pip e todas as ferramentas de build ficam no stage intermediário e são descartados automaticamente.

</details>

---

**Questão 2**

Um desenvolvedor editou apenas o arquivo `src/train.py` e executou `docker build` novamente. Qual das afirmações abaixo descreve corretamente o comportamento do cache?

- a) Todo o build é re-executado do zero, pois qualquer alteração invalida o cache completo
- b) A camada do `pip install` é reutilizada; apenas as camadas de cópia do código são re-executadas
- c) Apenas a camada `FROM` é cacheada; todo o restante sempre re-executa
- d) O cache é reutilizado somente se o arquivo alterado for menor que 1 KB

<details>
<summary>Resposta</summary>

**b)** O Docker invalida o cache a partir da primeira camada que mudou. Como `requirements.txt` não foi alterado, a camada `COPY requirements.txt` e a camada `RUN pip install` são reutilizadas. Somente a camada `COPY src/` (e as subsequentes) é re-executada.

</details>

---

**Questão 3**

Qual é o papel do `.dockerignore` no processo de build?

- a) Define quais arquivos o container tem permissão de ler em runtime
- b) Lista os arquivos que serão excluídos da imagem final após o build
- c) Reduz o contexto de build enviado ao daemon Docker antes do primeiro `FROM`
- d) Impede que o `COPY` dentro do Dockerfile copie arquivos sensíveis

<details>
<summary>Resposta</summary>

**c)** O `.dockerignore` atua antes mesmo de qualquer instrução do Dockerfile ser executada. O Docker CLI envia um "contexto de build" ao daemon  todos os arquivos do diretório. O `.dockerignore` exclui arquivos desse contexto, reduzindo a transferência e evitando que `.venv/`, notebooks, `.env` e outros arquivos desnecessários entrem na imagem.

</details>
