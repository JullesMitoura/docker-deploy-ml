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

## Módulo 05: Versionando Artefatos de Modelo
> **Entrega**: modelo versionado fora da imagem Docker

---

Até aqui, o modelo treinado (`model.pkl`) vivia dentro do container ou em um volume sem controle de versão. Em produção, isso é um problema: como saber qual versão do modelo está em uso? Como reverter para uma versão anterior se algo der errado? Como rastrear quando cada modelo foi treinado?

Este módulo introduz **versionamento de artefatos de modelo**  uma prática essencial de MLOps que trata o modelo como um artefato de primeira classe, com identificação única, histórico e capacidade de rollback.

### O que você vai aprender

- Como nomear artefatos de modelo com timestamp para garantir unicidade (`model_{tag}.pkl`)
- Manter um `registry.json` como catálogo dos modelos disponíveis
- Usar um link simbólico `model_latest.pkl` para apontar sempre para o modelo atual
- Implementar rollback: reverter o serving para uma versão anterior do modelo

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| `model_{tag}.pkl` | Artefato versionado com identificador único por treino |
| `registry.json` | Registro dos modelos disponíveis com metadados (data, métricas, etc.) |
| `model_latest.pkl` | Ponteiro para o modelo em uso atualmente |
| Rollback | Capacidade de restaurar uma versão anterior do modelo em produção |

### Por que versionar o modelo separadamente da imagem

Embutir o modelo dentro da imagem Docker mistura dois ciclos de vida diferentes: o código (que muda raramente) e o modelo (que pode ser re-treinado frequentemente). Versioná-los separadamente permite re-treinar sem rebuildar a imagem, auditar qual modelo gerou cada predição e fazer rollback cirúrgico sem alterar o código de serving.
