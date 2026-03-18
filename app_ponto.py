import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim

# --- 1. CONFIGURAÇÕES E BANCO DE DADOS (TOP LEVEL) ---
# Movido para o topo para evitar o NameError
funcionarios = {
    "123": "Oseias Nepomuceno", 
    "456": "João Silva",
    "789": "Maria Oliveira"
}

# Conexão com o Google Sheets (Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)
geolocator = Nominatim(user_agent="ponto_digital_oseias")

st.title("📸 Ponto Digital Facial - Cloud")

# --- 2. INTERFACE DE LOGIN NA SIDEBAR ---
st.sidebar.title("🔐 Login do Colaborador")
matricula = st.sidebar.text_input("Digite sua Matrícula ou CPF:")

# --- 3. LÓGICA PRINCIPAL ---
if matricula in funcionarios:
    nome_usuario = funcionarios[matricula]
    st.sidebar.success(f"Conectado: {nome_usuario}")

    # Interface de Batida de Ponto
    st.info(f"Olá, **{nome_usuario}**. Posicione-se para a foto.")
    foto = st.camera_input("Capture sua imagem")

    if foto:
        tipo = st.selectbox("Selecione o Tipo de Registro:", 
                            ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída Final"])
        
        if st.button("Confirmar Registro no Sistema"):
            with st.spinner('Enviando dados para o Google Sheets...'):
                agora = datetime.now()
                
                # Criar o DataFrame com o novo registro
                novo_registro = pd.DataFrame([{
                    "Data": agora.strftime("%d/%m/%Y"),
                    "Hora": agora.strftime("%H:%M:%S"),
                    "Funcionario": nome_usuario,
                    "Tipo": tipo,
                    "Localizacao": "Localização via Navegador" # Placeholder para o GPS
                }])

                try:
                    # Lógica de atualização da planilha
                    dados_atuais = conn.read(worksheet="Página1", ttl=0)
                    dados_finais = pd.concat([dados_atuais, novo_registro], ignore_index=True)
                    
                    # Enviar para o Google
                    conn.update(worksheet="Página1", data=dados_finais)
                    
                    st.balloons()
                    st.success(f"✅ Sucesso! Ponto de {tipo} gravado às {agora.strftime('%H:%M:%S')}")
                except Exception as e:
                    st.error(f"Erro na conexão com a planilha: {e}")
else:
    if matricula:
        st.sidebar.warning("Matrícula não reconhecida.")
    st.info("Aguardando identificação na barra lateral para liberar a câmera.")
