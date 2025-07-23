import streamlit as st
import pandas as pd
from unidecode import unidecode
import time

st.set_page_config(page_title="Painel de Lideranças", layout="wide")
st.image("https://www.consilliumrig.com.br/wp-content/uploads/2022/07/02_Logotipo_Consillium-1024x218.png", width=300)
st.title("📂 Líderes da Câmara dos Deputados")
st.markdown("#### Esta ferramenta foi desenvolvida para facilitar o acesso rápido aos contatos dos líderes partidários da Câmara dos Deputados, permitindo buscas diretas por meio de perguntas no chat ou consulta detalhada na tabela.")


# === DADOS COMPLEMENTARES DE FOTO E PERFIL ===
dados_complementares = {
    "Adolfo Viana": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204560.jpg", "perfil": "https://www.camara.leg.br/deputados/204560"},
    "Antonio Brito": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160553.jpg", "perfil": "https://www.camara.leg.br/deputados/160553"},
    "Aureo Ribeiro": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160512.jpg", "perfil": "https://www.camara.leg.br/deputados/160512"},
    "Doutor Luizinho": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204450.jpg", "perfil": "https://www.camara.leg.br/deputados/204450"},
    "Fred Costa": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204494.jpg", "perfil": "https://www.camara.leg.br/deputados/204494"},
    "Gilberto Abramo": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204491.jpg", "perfil": "https://www.camara.leg.br/deputados/204491"},
    "Isnaldo Bulhões Jr.": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204436.jpg", "perfil": "https://www.camara.leg.br/deputados/204436"},
    "Lindbergh Farias": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/74858.jpg", "perfil": "https://www.camara.leg.br/deputados/74858"},
    "Luis Tibé": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/160510.jpg", "perfil": "https://www.camara.leg.br/deputados/160510"},
    "Marcel van Hattem": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/156190.jpg", "perfil": "https://www.camara.leg.br/deputados/156190"},
    "Mário Heringer": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/74158.jpg", "perfil": "https://www.camara.leg.br/deputados/74158"},
    "Neto Carletto": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220703.jpg", "perfil": "https://www.camara.leg.br/deputados/220703"},
    "Pedro Campos": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220667.jpg", "perfil": "https://www.camara.leg.br/deputados/220667"},
    "Pedro Lucas Fernandes": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/122974.jpg", "perfil": "https://www.camara.leg.br/deputados/122974"},
    "Rodrigo Gambale": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220641.jpg", "perfil": "https://www.camara.leg.br/deputados/220641"},
    "Sóstenes Cavalcante": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/178947.jpg", "perfil": "https://www.camara.leg.br/deputados/178947"},
    "Talíria Petrone": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204464.jpg", "perfil": "https://www.camara.leg.br/deputados/204464"},
    "José Guimarães": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/141470.jpg", "perfil": "https://www.camara.leg.br/deputados/141470"},
    "Arlindo Chinaglia": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/73433.jpg", "perfil": "https://www.camara.leg.br/deputados/73433"},
    "Caroline de Toni": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/204369.jpg", "perfil": "https://www.camara.leg.br/deputados/204369"},
    "Zucco": {"foto": "https://www.camara.leg.br/internet/deputado/bandep/220552.jpg", "perfil": "https://www.camara.leg.br/deputados/220552"}
}

@st.cache_data
def carregar_dados():
    df = pd.read_excel("liderancas.xlsx")
    df.columns = df.columns.str.strip()
    return df

def criar_link_whatsapp(numero):
    if pd.notna(numero) and "xxxx" not in str(numero):
        numero_limpo = str(numero).replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        return f"https://wa.me/55{numero_limpo}"
    return None

# Carrega os dados
df = carregar_dados()

# Preprocessamento
df["nome_clean"] = df["Nome_Parlamentar"].fillna("").apply(lambda x: unidecode(str(x).lower()))
df["partido_clean"] = df["Partido"].fillna("").apply(lambda x: unidecode(str(x).lower()))
df["rep_clean"] = df["Representacao"].fillna("").apply(lambda x: unidecode(str(x).lower()))

# Filtros
partidos = sorted(df["Partido"].dropna().unique())
ufs = sorted(df["Uf"].dropna().unique())
representacoes = sorted(df["Representacao"].dropna().unique())

partido_sel = st.selectbox("Filtrar por Partido", options=["Todos"] + partidos)
uf_sel = st.selectbox("Filtrar por UF", options=["Todos"] + ufs)
rep_sel = st.selectbox("Filtrar por Representação", options=["Todas"] + representacoes)
nome_busca = st.text_input("🔎 Buscar por Nome, Representação ou Partido")

# Aplicar filtros
df_filtrado = df.copy()
if partido_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Partido"] == partido_sel]
if uf_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Uf"] == uf_sel]
if rep_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Representacao"] == rep_sel]
if nome_busca:
    termo = unidecode(nome_busca.lower())
    df_filtrado = df_filtrado[
        df_filtrado["nome_clean"].str.contains(termo) |
        df_filtrado["partido_clean"].str.contains(termo) |
        df_filtrado["rep_clean"].str.contains(termo)
    ]

# Exibição dos cards individuais
st.markdown(f"### 👥 {len(df_filtrado)} líder(es) encontrado(s)")
for _, row in df_filtrado.iterrows():
    col1, col2 = st.columns([1, 4])
    with col1:
        nome = row["Nome_Parlamentar"]
        if nome in dados_complementares:
            st.image(dados_complementares[nome]["foto"], width=100)
    with col2:
        nome = row["Nome_Parlamentar"]
        if nome in dados_complementares:
            link = dados_complementares[nome]["perfil"]
            st.markdown(f"**[{nome}]({link})**")
        else:
            st.markdown(f"**{nome}**")
        st.markdown(f"{row['Representacao']} — {row['Partido']}/{row['Uf']}")
        st.markdown(f"📧 {row['Correio_Eletronico']}")
        if pd.notna(row['Celular_Deputado']):
            link_dep = criar_link_whatsapp(row['Celular_Deputado'])
            if link_dep:
                st.markdown(f"🟢 [WhatsApp Deputado]({link_dep})")
        if pd.notna(row['Celular_Assessoria']):
            link_ass = criar_link_whatsapp(row['Celular_Assessoria'])
            if link_ass:
                st.markdown(f"💬 [WhatsApp Assessoria]({link_ass})")
        if pd.notna(row['Nome_assessor']):
            st.markdown(f"👤 Assessor(a): {row['Nome_assessor']}")
        st.markdown(f"🏢 Gabinete: {row['Endereco_Gabinete']}")
        st.markdown(f"🏛️ Liderança: {row['Endereco_Lideranca']}")
        st.markdown("---")

# Tabela com endereços
st.markdown("## 🏢 Tabela de Endereços dos Líderes")
st.markdown("### 📋 Lista completa de líderes partidários na Câmara dos Deputados, com informações de contato e localização dos gabinetes.")
st.dataframe(df_filtrado[["Nome_Parlamentar", "Representacao", "Partido", "Uf", "Endereco_Gabinete", "Endereco_Lideranca"]])

from difflib import get_close_matches

# === Chat com IA — Busca Semântica via Embeddings ===
import streamlit as st
import pandas as pd

# Carrega a base com os líderes
dados = pd.read_excel("liderancas.xlsx")

# Mapeamento de representações
representacoes = {
    "governo": "José Guimarães",
    "maioria": "Arlindo Chinaglia",
    "minoria": "Caroline de Toni",
    "oposição": "Zucco",
}

# Mapeamento de federações e líderes
federacoes = {
    "psdb": "O PSDB está na Federação PSDB Cidadania, portanto seu líder é o Deputado Adolfo Viana.",
    "pt": "O PT está na Federação Brasil da Esperança - Fe Brasil, portanto seu líder é o Deputado Lindbergh Farias.",
    "psol": "O PSOL está na Federação PSOL REDE, portanto a líder é a Deputada Talíria Petrone.",
    "rede": "A REDE está na Federação PSOL REDE, portanto a líder é a Deputada Talíria Petrone.",
    "cidadania": "O Cidadania está na Federação PSDB Cidadania, portanto seu líder é o Deputado Adolfo Viana.",
    "pcdob": "O PCdoB está na Federação Brasil da Esperança - Fe Brasil, portanto seu líder é o Deputado Lindbergh Farias.",
    "pv": "O PV está na Federação Brasil da Esperança - Fe Brasil, portanto seu líder é o Deputado Lindbergh Farias."
}

# Interface do chat
st.markdown("## 🤖 Pergunte diretamente sobre os contatos dos líderes")
st.markdown("### ℹ️ Você pode perguntar no chat sobre os contatos dos líderes. Ou, se preferir, role a tela para cima para visualizar a lista completa.")
pergunta = st.text_input("Digite sua pergunta sobre os contatos os líderes:")

if pergunta:
    pergunta_lower = pergunta.lower()

    # Verifica representações (governo, minoria, etc.)
    resposta_direta = None
    for chave, nome in representacoes.items():
        if chave in pergunta_lower:
            resposta_direta = f"O líder da {chave.capitalize()} é {nome}."
            break

    # Verifica federações (PT, PSDB etc.)
    if not resposta_direta:
        for partido, resposta in federacoes.items():
            if f"líder do {partido}" in pergunta_lower or f"lider do {partido}" in pergunta_lower:
                resposta_direta = resposta
                break

    if resposta_direta:
        st.markdown(f"**{resposta_direta}**")
    else:
        resultados = dados[dados['Texto_Embedding'].str.lower().str.contains(pergunta_lower, na=False)]
        if not resultados.empty:
            for i, row in resultados.iterrows():
                st.markdown(f"**Resultado {i+1}:** {row['Texto_Embedding']}")
        else:
            st.markdown("Nenhuma informação encontrada para essa pergunta.")







