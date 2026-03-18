import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim

# 1. Configuração de Conexão (Usa os Secrets que você salvou)
conn = st.connection("gsheets", type=GSheetsConnection)
geolocator = Nominatim(user_agent="ponto_digital_oseias")

st.title("📸 Ponto Digital Facial - Cloud")

# --- Interface de Login na Sidebar ---
st.sidebar.title("🔐 Login")
matricula = st.sidebar.text_input("Matrícula:")
funcionarios = {"123": "Oseias Nepomuceno", "456": "João Silva"} # Exemplo

if matricula in funcionarios:
    nome_usuario = funcionarios[matricula]
    st.sidebar.success(f"Conectado: {nome_usuario}")

    # --- Captura da Foto ---
    foto = st.camera_input("Tire a selfie para o ponto")

    if foto:
        tipo = st.selectbox("Tipo:", ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída"])
        
        if st.button("Confirmar Registro"):
            # 2. Preparar os Dados
            agora = datetime.now()
            novo_registro = pd.DataFrame([{
                "Data": agora.strftime("%d/%m/%Y"),
                "Hora": agora.strftime("%H:%M:%S"),
                "Funcionario": nome_usuario,
                "Tipo": tipo,
                "Localizacao": "Sao Paulo - SP" # Aqui depois integraremos o GPS real
            }])

            try:
                # 3. Ler dados atuais e enviar novos (O pulo do gato!)
                # ttl=0 garante que ele não use "cache" e pegue a planilha sempre atualizada
                dados_atuais = conn.read(worksheet="Página1", ttl=0)
                dados_finais = pd.concat([dados_atuais, novo_registro], ignore_index=True)
                
                conn.update(worksheet="Página1", data=dados_finais)
                
                st.balloons()
                st.success(f"✅ Ponto de {tipo} gravado no Google Sheets!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
else:
    st.info("Aguardando login para liberar a câmera...")
