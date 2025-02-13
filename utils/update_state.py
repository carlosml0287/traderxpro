import streamlit as st

def nav(page):
    st.session_state.current_page = page
    # (Opcional) Mensaje de depuración; puedes comentarlo en producción
    st.text(f"MI SESION ACTUAL ES: {page}")
    # Utilizamos setTimeout para dar un pequeño retardo (50ms) antes de redirigir
    st.markdown(
        f"""
        <script>
            setTimeout(function() {{
                window.location.href = window.location.pathname + '?page={page}';
            }}, 50);
        </script>
        """,
        unsafe_allow_html=True
    )
    st.stop()
