import streamlit as st

def generarMenu():
    """Genera el menú lateral."""
    with st.sidebar:
        nombre = st.session_state.get('nombre', 'Usuario')  
        st.write(f"Hola **:blue-background[{nombre}]** ")
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        st.subheader("Tableros")
        st.page_link("pages/pagina1.py", label="Ventas", icon=":material/sell:")
        st.page_link("pages/pagina2.py", label="Compras", icon=":material/shopping_cart:")
        st.page_link("pages/pagina3.py", label="Personal", icon=":material/group:")    
        st.page_link("pages/pm40.py", label="PM40", icon=":material/data_thresholding:")
        st.page_link("pages/cncf.py", label="CNCF", icon=":material/data_thresholding:")
        st.page_link("pages/diario.py", label="Diario", icon=":material/data_thresholding:")
        
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            st.rerun()
