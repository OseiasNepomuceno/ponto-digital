import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Sistema de Ponto Digital", page_icon="📸")

st.title("📸 Registro de Ponto via Selfie")
st.subheader("Administração & Automação Inteligente")

# 1. Captura da Foto via Navegador
foto_capturada = st.camera_input("Tire sua foto para bater o ponto")

if foto_capturada:
    # Converter a imagem para um formato que o OpenCV entenda
    bytes_data = foto_capturada.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Detectar se há um rosto (Garantia básica)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    rostos = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(rostos) > 0:
        st.success("✅ Rosto identificado com sucesso!")

        # 2. Seleção do Tipo de Ponto
        opcao = st.selectbox("Selecione o tipo de marcação:",
                             ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída Final"])

        if st.button("Confirmar Registro"):
            # 3. Lógica de Gravação
            agora = datetime.now()
            registro = {
                "Data": agora.strftime("%d/%m/%Y"),
                "Hora": agora.strftime("%H:%M:%S"),
                "Funcionário": "Oseias_Nepomuceno",  # Aqui viria o login
                "Tipo": opcao,
                "Local": "-23.5505, -46.6333"  # Simulando GPS do navegador
            }

            df = pd.DataFrame([registro])
            arquivo = "registro_ponto_web.csv"
            df.to_csv(arquivo, mode='a', index=False, header=not os.path.exists(arquivo))

            st.balloons()  # Efeito visual de sucesso
            st.info(f"Ponto de {opcao} registrado às {agora.strftime('%H:%M:%S')}")
    else:
        st.error("⚠️ Nenhum rosto detectado. Por favor, centralize seu rosto na câmera.")

# Visualização da Tabela de Registros (Apenas para o Gestor)
if st.checkbox("Ver histórico de hoje"):
    if os.path.exists("registro_ponto_web.csv"):
        df_historico = pd.read_csv("registro_ponto_web.csv")
        st.dataframe(df_historico.tail(10))