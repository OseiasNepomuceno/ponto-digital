import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. CONEXÃO (Fica "solta" no início do script)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📸 Ponto Digital - Google Sheets")

# ... (Código da câmera e login aqui) ...

if st.button("Confirmar Registro"):
    # Criamos o dado que será enviado
    novo_ponto = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Funcionario": nome_usuario,
        "Tipo": tipo_ponto
    }])

    # 2. AÇÃO DE SALVAR (Dentro do botão)
    # Lemos os dados atuais da planilha
    dados_existentes = conn.read(worksheet="Página1", ttl=0) 
    
    # Juntamos o antigo com o novo
    dados_atualizados = pd.concat([dados_existentes, novo_ponto], ignore_index=True)
    
    # Enviamos de volta para o Google
    conn.update(worksheet="Página1", data=dados_atualizados)
    
    st.success("✅ Ponto salvo direto no Google Sheets!")
    st.balloons()
