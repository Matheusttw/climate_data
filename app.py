# -*- coding: utf-8 -*-

# =============================================================================
# APLICAÇÃO DESKTOP PARA ANÁLISE DE DADOS CLIMÁTICOS
#
# Autor: (Seu Nome)
# Data: 10 de setembro de 2025
#
# Descrição:
# Esta aplicação permite ao usuário selecionar uma cidade de um conjunto
# de dados global e visualizar duas análises climáticas:
# 1. A tendência da temperatura média anual ao longo do tempo.
# 2. A sazonalidade, mostrando a temperatura média para cada mês.
#
# Utiliza as bibliotecas:
# - tkinter: para a construção da interface gráfica.
# - pandas: para manipulação e análise dos dados.
# - matplotlib: para a criação dos gráficos.
# =============================================================================


# --- 1. IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS ---
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- 2. LÓGICA DE PROCESSAMENTO E LIMPEZA DE DADOS ---

def carregar_e_limpar_dados(filepath):
    """
    Carrega o dataset de um arquivo CSV, realiza a limpeza e o pré-processamento.
    Retorna um DataFrame do Pandas pronto para análise ou None se o arquivo não for encontrado.
    """
    try:
        # Especificar os tipos de dados durante a leitura otimiza o uso de memória
        # e previne o 'DtypeWarning'. 'category' é ideal para colunas com texto repetido.
        dtypes = {
            'Region': 'category',
            'Country': 'category',
            'City': 'category',
            'AvgTemperature': float
        }
        df = pd.read_csv(filepath, dtype=dtypes)

    except FileNotFoundError:
        # Se o arquivo CSV não estiver na pasta, exibe um erro claro para o usuário.
        messagebox.showerror("Erro de Arquivo", f"Arquivo não encontrado: {filepath}\n\nPor favor, certifique-se de que 'city_temperature.csv' está na mesma pasta que a aplicação.")
        return None

    # Etapa 1: Substituir o valor sentinela (-99) por NaN (Not a Number) para que o pandas possa tratá-lo como um valor ausente.
    df['AvgTemperature'] = df['AvgTemperature'].replace(-99.0, np.nan)

    # Etapa 2: Criar uma coluna de data a partir das colunas 'Year', 'Month', 'Day'.
    # O parâmetro 'errors='coerce'' é crucial para lidar com datas inválidas no arquivo (ex: 31 de Abril).
    # Datas inválidas serão convertidas para 'NaT' (Not a Time).
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], errors='coerce')
    
    # Removemos qualquer linha em que a data não pôde ser criada (onde 'Date' é NaT).
    df.dropna(subset=['Date'], inplace=True)
    
    # Etapa 3: Converter a temperatura de Fahrenheit para Celsius para melhor interpretação.
    df['AvgTemperatureCelsius'] = (df['AvgTemperature'] - 32) * 5/9

    # Etapa 4: Preencher os valores de temperatura ausentes.
    # Agrupamos por cidade e usamos 'ffill' (forward fill) e 'bfill' (backward fill)
    # para preencher os buracos com o último ou próximo valor válido para aquela cidade.
    df['AvgTemperatureCelsius'] = df.groupby('City')['AvgTemperatureCelsius'].transform(
        lambda x: x.fillna(method='ffill').fillna(method='bfill')
    )
    # Removemos qualquer cidade que ainda tenha valores nulos (caso não tenha nenhum dado válido).
    df.dropna(subset=['AvgTemperatureCelsius'], inplace=True)
    
    print("Dados carregados e limpos com sucesso.")
    return df


# --- 3. FUNÇÕES DE ANÁLISE E PLOTAGEM ---

def plotar_tendencia_anual(ax, df_cidade):
    """
    Plota o gráfico de tendência anual de temperatura em um eixo Matplotlib (ax).
    'ax' é o subplot onde o gráfico será desenhado.
    """
    # 'resample('A')' agrupa os dados por ano ('A' de Annual) e calcula a média.
    media_anual = df_cidade['AvgTemperatureCelsius'].resample('A').mean()
    ax.plot(media_anual.index, media_anual.values, label='Média Anual', color='navy')
    
    # Adiciona uma linha de tendência (regressão linear simples) para visualizar o aquecimento/resfriamento.
    x = np.arange(len(media_anual))
    y = media_anual.values
    mask = ~np.isnan(y) # Ignora anos com dados faltantes para o cálculo da tendência
    if np.any(mask):
        m, b = np.polyfit(x[mask], y[mask], 1)
        ax.plot(media_anual.index, m*x + b, color='red', linestyle='--', label='Tendência')

    ax.set_title('Tendência da Temperatura Média Anual')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Temperatura Média (°C)')
    ax.legend()
    ax.grid(True)

def plotar_sazonalidade_mensal(ax, df_cidade):
    """
    Plota o gráfico de sazonalidade mensal em um eixo Matplotlib (ax).
    """
    # Agrupa os dados pelo número do mês (1 a 12) e calcula a média de temperatura para cada mês.
    media_mensal = df_cidade.groupby(df_cidade.index.month)['AvgTemperatureCelsius'].mean()
    nomes_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    # Cria um gráfico de barras com cores variando com a temperatura (palette coolwarm).
    ax.bar(nomes_meses, media_mensal, color=plt.cm.coolwarm(media_mensal.values / media_mensal.max()))
    ax.set_title('Sazonalidade: Temperatura Média Mensal')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Temperatura Média (°C)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)


# --- 4. CLASSE DA APLICAÇÃO GRÁFICA (GUI) ---

class AppClima(tk.Tk):
    def __init__(self, df):
        super().__init__()
        
        self.df = df
        # Obtém uma lista única e ordenada de cidades para popular o menu suspenso.
        self.cidades = sorted(self.df['City'].unique())

        # --- Configurações da Janela Principal ---
        self.title("Análise de Dados Climáticos")
        self.geometry("1000x800") # Define o tamanho inicial da janela

        # --- Widgets da Interface ---
        # Usamos 'ttk' em vez de 'tk' para um visual mais moderno.
        
        # Frame principal para organizar o conteúdo
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame superior para os controles (label, combobox, botão)
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Selecione uma Cidade:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # Variável especial do tkinter para armazenar a seleção do combobox
        self.cidade_selecionada = tk.StringVar()
        
        # Menu suspenso (Combobox) para selecionar a cidade
        self.combo_cidades = ttk.Combobox(control_frame, textvariable=self.cidade_selecionada, values=self.cidades, width=30, state="readonly")
        self.combo_cidades.pack(side=tk.LEFT, padx=5)
        if self.cidades:
            self.combo_cidades.set("Sao Paulo") # Define um valor padrão para iniciar

        # Botão que dispara a análise
        self.botao_analisar = ttk.Button(control_frame, text="Analisar", command=self.analisar_cidade)
        self.botao_analisar.pack(side=tk.LEFT, padx=10)

        # Frame inferior para exibir os gráficos
        self.plot_frame = ttk.Frame(main_frame, relief="sunken", borderwidth=2)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Placeholder para o canvas do Matplotlib
        self.canvas = None
        
        # Inicia a aplicação com a análise da cidade padrão
        self.analisar_cidade()

    def analisar_cidade(self):
        """
        Função chamada quando o botão "Analisar" é clicado.
        """
        cidade = self.cidade_selecionada.get()
        if not cidade:
            messagebox.showwarning("Aviso", "Por favor, selecione uma cidade.")
            return

        print(f"Analisando dados para: {cidade}")

        # Filtra o DataFrame principal para obter dados apenas da cidade selecionada.
        df_cidade = self.df[self.df['City'] == cidade].copy()
        df_cidade.set_index('Date', inplace=True)

        # Se já existir um gráfico, ele é destruído para dar lugar ao novo.
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Cria a figura e os subplots do Matplotlib que conterão nossos gráficos.
        # A figura terá 2 linhas e 1 coluna de gráficos.
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), dpi=100)
        fig.tight_layout(pad=4.0) # Ajusta o espaçamento para que os títulos não se sobreponham

        # Chama as funções de plotagem, passando os eixos corretos para cada gráfico.
        plotar_tendencia_anual(ax1, df_cidade)
        plotar_sazonalidade_mensal(ax2, df_cidade)

        # Esta é a parte chave da integração:
        # FigureCanvasTkAgg é a ponte entre o Matplotlib e o Tkinter.
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw() # Desenha o gráfico no canvas
        # get_tk_widget() retorna o widget do Tkinter que pode ser colocado na janela.
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# --- 5. PONTO DE ENTRADA DA APLICAÇÃO ---

if __name__ == "__main__":
    # Este bloco de código só é executado quando o script é rodado diretamente
    # (e não quando é importado por outro script).
    
    print("Iniciando carregamento de dados...")
    # 1. Carrega e limpa os dados antes de iniciar a interface gráfica.
    df_global = carregar_e_limpar_dados('city_temperature.csv')
    
    # 2. Só inicia a aplicação se os dados forem carregados com sucesso.
    if df_global is not None:
        print("Iniciando a aplicação gráfica...")
        app = AppClima(df_global)
        app.mainloop() # Inicia o loop de eventos do Tkinter, que "escuta" cliques e outras interações.
    else:
        print("Aplicação não pôde ser iniciada devido a um erro no carregamento dos dados.")