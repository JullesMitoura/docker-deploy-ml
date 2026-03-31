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

## Módulo 02: Questionário
> Containerizando o Projeto

---

**Questão 1**

Por que o `requirements.txt` é copiado para dentro do container **antes** do código-fonte no Dockerfile?

- a) O Docker exige que arquivos de texto venham antes de diretórios
- b) Para que a camada do `pip install` seja cacheada e reutilizada quando apenas o código mudar
- c) Para reduzir o tamanho final da imagem
- d) O `pip install` falha se o código-fonte já estiver presente no container

<details>
<summary>Resposta</summary>

**b)** O Docker invalida o cache de uma camada quando qualquer camada anterior muda. Copiando `requirements.txt` antes de `src/`, garantimos que o `pip install` (operação lenta) só é re-executado quando as dependências mudam de fato  não a cada alteração de código.

</details>

---

**Questão 2**

Qual é a diferença entre as instruções `RUN` e `CMD` em um Dockerfile?

- a) `RUN` executa comandos em background; `CMD` executa em primeiro plano
- b) `RUN` só pode ser usado com scripts shell; `CMD` aceita qualquer executável
- c) `RUN` executa durante o **build** da imagem; `CMD` define o comando padrão executado ao iniciar o **container**
- d) Não há diferença prática; são intercambiáveis

<details>
<summary>Resposta</summary>

**c)** `RUN` transforma o sistema de arquivos da imagem durante o build (instalar pacotes, criar diretórios). `CMD` define o que o container faz quando é iniciado com `docker run`  e pode ser sobrescrito pelo usuário passando outro comando após o nome da imagem.

</details>

---

**Questão 3**

Após rodar `docker run heat-exchanger-train` (treino) e depois `docker run heat-exchanger-train python src/inference.py --date 2022-04-15` (inferência), o segundo container retorna `FileNotFoundError: Modelo não encontrado`. Por quê?

- a) O nome da imagem está errado; treino e inferência precisam de imagens separadas
- b) Containers são efêmeros: o `model.pkl` gerado no primeiro container não persiste para o segundo
- c) O `CMD` do Dockerfile sobrescreve qualquer arquivo gerado em runtime
- d) O `pip install` não incluiu o `pickle`, necessário para salvar o modelo

<details>
<summary>Resposta</summary>

**b)** Cada `docker run` cria um container isolado com seu próprio sistema de arquivos. O modelo gerado pelo primeiro container existe apenas dentro daquele container  quando ele para, os arquivos desaparecem. A solução correta é usar volumes, tema do módulo 03.

</details>
