import streamlit as st
from utils.custom_style import load_css

# Configuración de la página
st.set_page_config(page_title="Mi Aplicación", layout="wide")
load_css("styles/style.css")

def mostrar_inicio():
    st.markdown("<div class='title_header'>Trading Project <span>Web</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='p_descripcion'>Esta es la descripción de mi proyecto. Elige una opción para continuar.</div>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            if st.button("👤 Iniciar como Visitante"):
                st.session_state.modo = "visitante"
                st.rerun()
        with button_col2:
            if st.button("🔑 Iniciar Sesión"):
                st.session_state.modo = "usuario"
                st.rerun()

def main():
    if "modo" not in st.session_state:
        mostrar_inicio()
    elif st.session_state.modo == "visitante":
        from pages.visitante import app_visitante
        print(st.session_state.modo)
        app_visitante()
        st.stop()
    elif st.session_state.modo == "usuario":
        from pages.autenticacion import login
        login()
        st.stop()

if __name__ == "__main__":
    main()
