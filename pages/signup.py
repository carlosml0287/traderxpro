# pages/signup.py
import streamlit as st
from utils.custom_style import load_css
from firebase_config import db, firebase_admin
from auth import generar_google_login
load_css("styles/style.css")


# Opciones para la lista de países y monedas
# Puedes definir una lista estática o utilizar una librería como `pycountry` para obtener una lista completa.
countries = [
    "United States", "Canada", "United Kingdom", "Australia", "Germany", "France", "Spain", "Italy", "Brazil", "Mexico"
]
currencies = [
    "USD", "CAD", "GBP", "AUD", "EUR", "CHF", "JPY", "BRL", "MXN"
]

def show():
    # Ejemplo de formulario de registro:
    with st.form("frmSignup"):
        st.markdown("""
                <div>
                    <h3 class="h-3">Register Trader <span style="color: #a1a1b4; font-size: 40px; font-weight: bold;">XPro</span></h3>
                    <p>Hey there! Ready to log in? Just enter your username and password below and you'll be back in action in no time. Let's go!</p>
                </div>
                """,
                unsafe_allow_html=True)
        # Selección del país (Country)
        country = st.selectbox("Country", countries)
        
        # Campo para el usuario
        usuario = st.text_input("User")
        
        # Campo para la contraseña
        password = st.text_input("Password", type="password")
        
        # Botón de registro
        btnRegistro = st.form_submit_button("Registrarse",use_container_width=True)
        
        # Ejemplo de manejo del registro
        if btnRegistro:
            # Aquí colocarías la lógica de validación y registro, por ejemplo:
            st.success(f"Registro exitoso para {usuario} de {country} usando la moneda {currency}.")
        
        st.markdown("""
                <div style="display: flex; align-items: center; text-align: center; width: 100%; margin: 20px 0;">
                    <hr style="flex-grow: 1; border: none; height: 1.4px; background-color: gray;">
                    <span style="padding: 0 13px; font-weight: bold; color: gray;">Register in via</span>
                    <hr style="flex-grow: 1; border: none; height: 2px; background-color: gray;">
                </div>
            """, unsafe_allow_html=True)
        google_url = generar_google_login()
        google_button = f"""
            <div class="btn-container">
                <a href="{google_url}" class="google-btn">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="24" height="24">
                </a>
            </div>
            """
          

        st.markdown(google_button, unsafe_allow_html=True)
        
        if btnRegistro:
            # Aquí iría la lógica para guardar el registro (por ejemplo, validación y conexión a la base de datos)
            st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")

if __name__ == "__main__":
    show()
