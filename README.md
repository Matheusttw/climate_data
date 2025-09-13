# Análise de Dados Climáticos: Aplicação Desktop com Python

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.x-brightgreen.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-orange.svg)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-red.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

Uma aplicação desktop interativa construída com Python para analisar e visualizar dados históricos de temperatura de diversas cidades ao redor do mundo. Este projeto demonstra um pipeline de dados completo, desde a ingestão e limpeza de dados brutos até a apresentação de insights em uma interface gráfica amigável.

## Visão Geral

O objetivo deste projeto é fornecer uma ferramenta prática que permita a usuários, mesmo sem conhecimento técnico, explorar tendências climáticas e padrões sazonais. A aplicação carrega um dataset com temperaturas diárias, processa-o em tempo real e gera visualizações claras e objetivas.

### Screenshot da Aplicação
<img width="999" height="828" alt="app2" src="https://github.com/user-attachments/assets/3bbabd3f-67d5-423f-b266-80cfea5320c5" />
<img width="999" height="830" alt="app" src="https://github.com/user-attachments/assets/82fffa6c-4c7b-4d45-be52-4c7c4bfb7e84" />

## Funcionalidades Principais

* **Ingestão de Dados:** Carrega e processa um arquivo CSV de grande volume (~3 milhões de linhas).
* **Limpeza de Dados Robusta:** Trata valores ausentes, anomalias (como temperaturas de -99°F) e datas inválidas de forma programática.
* **Interface Gráfica Interativa:** Permite que o usuário selecione uma cidade de uma lista suspensa para análise.
* **Análise de Tendência:** Plota a temperatura média anual ao longo do tempo, incluindo uma linha de tendência (regressão linear) para identificar padrões de aquecimento ou resfriamento.
* **Análise de Sazonalidade:** Gera um gráfico de barras que mostra a temperatura média para cada mês do ano, destacando os períodos mais quentes e frios.

## Relevância para a Indústria de Dados

Este projeto, embora simples, toca em conceitos fundamentais para diversas áreas da tecnologia:

* **Para Cientistas e Analistas de Dados:** É um exemplo clássico de Análise Exploratória de Dados (EDA). Demonstra como extrair narrativas e insights (tendências, sazonalidade) a partir de dados brutos e comunicá-los de forma visual e eficaz.

* **Para Engenheiros de Dados:** O script `app.py` implementa um mini-pipeline de ETL (Extract, Transform, Load). A função `carregar_e_limpar_dados` é um exemplo prático de transformação de dados, lidando com problemas de qualidade comuns em fontes de dados do mundo real.

* **Para Desenvolvedores de Software:** Mostra a integração entre a lógica de backend (processamento de dados com Pandas) e o frontend (interface gráfica com Tkinter), um pilar do desenvolvimento de aplicações. A integração do Matplotlib com o Tkinter é um destaque técnico.

* **Para Profissionais de Cloud:** A lógica de análise pode ser facilmente "conteinerizada" (com Docker) e migrada para um serviço web (usando Flask/Streamlit/FastAPI) para ser executada em plataformas de nuvem como AWS, GCP ou Azure. O carregamento de dados poderia ser adaptado para ler de um Data Lake (S3, Blob Storage) em vez de um CSV local.

## Stack Tecnológica

* **Linguagem:** Python 3.9+
* **Análise de Dados:** Pandas, NumPy
* **Visualização de Dados:** Matplotlib
* **Interface Gráfica (GUI):** Tkinter (módulo `ttk`)

## Como Executar o Projeto Localmente

Siga os passos abaixo para ter a aplicação rodando em sua máquina.

### Pré-requisitos
* Python 3.9 ou superior
* Git

### 1. Clone o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git)
cd NOME_DO_SEU_REPOSITORIO
```

### 2. Crie e Ative um Ambiente Virtual (Recomendado)
```bash
# Para Windows
python -m venv venv
venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Baixe o Conjunto de Dados
Este projeto utiliza o dataset "Daily Temperature of Major Cities". Por favor, baixe o arquivo `city_temperature.csv` [deste link do Kaggle](https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities) e coloque-o na raiz do diretório do projeto.

### 5. Execute a Aplicação
```bash
python app.py
```
Uma janela gráfica deverá aparecer, pronta para uso.

## Estrutura do Projeto
```
.
├── .gitignore         # Arquivo para ignorar arquivos desnecessários no Git
├── README.md          # Documentação do projeto
├── app.py             # Código-fonte principal da aplicação
├── requirements.txt   # Lista de dependências Python
└── city_temperature.csv # Arquivo de dados (deve ser baixado manualmente)
```


## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
