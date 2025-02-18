import streamlit as st



def generarMenu():
    """Genera el menú lateral común solo una vez y retorna un placeholder para widgets específicos."""
    # Si ya se generó el sidebar, retornamos el placeholder almacenado
    if "sidebar_generated" in st.session_state:
        return 
    with st.sidebar:
        nombre = st.session_state.get('nombre', 'Usuario')  
        st.write(f"""<h3 >Hola <span style="background-color:#a1a1b4; color:#fff; padding:0px 4px; border-radius:4px">{nombre}</span></h3>""",unsafe_allow_html=True)
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        
        # PUEDE ACCEDER CUALQUIER USUARIO
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.expander("### Historical",expanded=True):
            st.page_link("pages/pm40.py", label="PM40", icon=":material/data_thresholding:")
            st.page_link("pages/cncf.py", label="CNCF", icon=":material/data_thresholding:")
            st.page_link("pages/diario.py", label="Diario", icon=":material/data_thresholding:")
        
        
        # RESTRINGIDO, SOLO PARA USUARIOS REGISTRADOS
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.expander("### Real Time",expanded=False):
            st.page_link("pages/pm40.py", label="PM40", icon=":material/data_thresholding:")
            st.page_link("pages/cncf.py", label="CNCF", icon=":material/data_thresholding:")
            st.page_link("pages/diario.py", label="Diario", icon=":material/data_thresholding:")
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.expander("### Login",expanded=False):
            st.page_link("pages/login.py", label="Login", icon=":material/data_thresholding:")
            st.page_link("pages/signup.py", label="Sign Up", icon=":material/data_thresholding:")

# Exportamos el placeholder para que pueda ser usado en otras páginas
#placeholder_sidebar = generarMenu()