import streamlit as st

def generar_header():
    logged = st.session_state.get("logged_in", False)
    visitor = st.session_state.get("visitor", False)
    
    if logged:
        header_buttons = '<a class="header-button" href="?page=logout">Cerrar sesión</a>'
    elif visitor:
        header_buttons = (
            '<a class="header-button" href="?page=logout">Cerrar sesión</a>'
            '<a class="header-button" href="/login">Ingresar como usuario</a>'
        )
    else:
        header_buttons = (
            '<a class="header-button" href="/login">Iniciar Sesión</a>'
            '<a class="header-button" href="?page=visitor">Visitante</a>'
        )
    
    st.markdown(
        f"""
        <style>
            .header {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #1D1D1D;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 110px;
                font-size: 18px;
                font-weight: bold;
                z-index: 1000;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
            }}
            .menu-links a {{
                color: white;
                text-decoration: none;
                margin-right: 15px;
                font-weight: bold;
            }}
            .header-button {{
                background-color: #45ba73;
                color: black;
                padding: 8px 15px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
                cursor: pointer;
                margin-left: 10px;
                box-shadow: 0px 0px 10px #56E990;
            }}
            .header-button:hover {{
                background-color: transparent;
                border: 2px solid #56E990;
            }}
            .stApp {{
                margin-top: 60px;
            }}
        </style>
        <div class="header">
            <div class="menu-links">
                <a href="/">Logo</a>
            </div>
            <div class="button-container">
                {header_buttons}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
