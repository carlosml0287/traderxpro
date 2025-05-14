import streamlit as st

# Función para inyectar CSS personalizado
def aplicar_estilos():
    st.markdown("""
    <style>
        .login-container {
            background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.4);
            width: 350px;
            margin: 0 auto;
        }
        .login-title {
            text-align: center;
            font-size: 2em;
            margin-bottom: 1rem;
            color: #57cc99;
        }
        .stButton button {
            background-color: #57cc99;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 1rem;
            margin-top: 1rem;
            width: 100%;
        }
        .stTextInput > div > div > input {
            background-color: #1c1c1c;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Formulario de login
def login():
    aplicar_estilos()

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔒 Login</div>', unsafe_allow_html=True)

    with st.form(key="login_form"):
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        login_button = st.form_submit_button("Ingresar")

    st.markdown('</div>', unsafe_allow_html=True)

    if login_button:
        if usuario == "admin" and contraseña == "1234":
            st.success("✅ ¡Bienvenido!")
            st.balloons()
            return True
        else:
            st.error("❌ Usuario o contraseña incorrectos.")
            return False
    return False

if __name__ == "__main__":
    login()
