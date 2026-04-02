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

## Módulo 03: Treino e Inferência Separados
> **Entrega**: dois containers com responsabilidades claras

---

No módulo anterior, treino e inferência coexistiam na mesma imagem  uma solução funcional, mas que mistura responsabilidades distintas. Este módulo aplica um dos princípios mais importantes de engenharia de software ao contexto de ML: **responsabilidade única**.

Treinar um modelo e servir um modelo são etapas com ciclos de vida completamente diferentes. O treino acontece periodicamente, consome recursos intensivamente e produz um artefato. A inferência roda continuamente, precisa ser leve e rápida, e consome o artefato produzido pelo treino. Misturá-los em um único container cria dependências desnecessárias e dificulta a evolução independente de cada parte.

### O que você vai aprender

- Como separar `Dockerfile.train` e `Dockerfile.inference` com propósitos distintos
- Gerenciamento de `requirements` separados para cada contexto
- Uso de volumes Docker para compartilhar o modelo treinado entre containers
- Por que a separação de responsabilidades facilita escala, manutenção e rastreabilidade

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| `Dockerfile.train` | Imagem com tudo necessário para treinar o modelo |
| `Dockerfile.inference` | Imagem enxuta focada apenas em gerar predições |
| Volume Docker | Mecanismo para persistir e compartilhar dados entre containers |
| Responsabilidade única | Cada container faz uma coisa e faz bem |

### A comunicação entre containers

O elo entre treino e inferência é o artefato de modelo (`model.pkl`). O container de treino o escreve em um volume; o container de inferência o lê do mesmo volume. Essa separação via sistema de arquivos é simples, explícita e auditável  qualquer pessoa pode inspecionar o artefato gerado sem precisar entrar no processo de treino.
