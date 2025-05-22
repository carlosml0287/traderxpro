import streamlit as st

def generarSidebar():
    st.markdown("""
                <style>
                    .stButton > button{
                        width: 100%;
                        margin:0px;
                        border-color: #57cc99;
                    }
                    
                    .stButton > button:hover{
                        box-shadow: 0px 0px 5px #80ed99;
                    }
                    .stButton > button p{
                        font-size:18px;
                        color: #57cc99;
                    }
                    
                    .st-emotion-cache-1oou9d  > p{
                        color: #fff;
                        padding-bottom: 5px;  
                        font-size:12px;  
                    }
                    .st-emotion-cache-1w3omjh {
                        font-size: 18px !important;  /* Aumenta el tamaño del texto */
                        font-weight: bold !important; /* Hace que el texto sea más grueso */
                    }
                    .sidebar-separador{
                        border: 0;
                        height: 1px;
                        background-color: #c7f9cc !important;
                        margin: 2px 0px !important;
                    }

                </style>
                """,unsafe_allow_html=True)
    # Sección Historical en la sidebar con expander
    
    with st.sidebar.expander("📜 Estrategias"):
        #st.page_link("pages/pm40.py", label="PM40", icon="⚙️")
        st.page_link("pages/visitante.py", label="Ϟ Ruptura Bajista")
        st.page_link("pages/visitante.py", label="⩏ Caida Normal")
        st.page_link("pages/visitante.py", label="⩚ Promedio Movil")
        #st.page_link("pages/rsi_bollinger.py", label="RSI + Bollinger", icon="📈")

    st.sidebar.markdown("<hr class='sidebar-separador'>", unsafe_allow_html=True)

    # Sección Time Real en la sidebar con expander (bloqueada si es visitante)
    """
    with st.sidebar.expander("⏳ Real Time", expanded=False):
        if st.session_state.modo != "visitante":
            time_real = st.radio(
                "Selecciona un indicador:",
                ["Indicador_1", "Indicador_2"],
                index=None,
                key="indicador_time_real"
            )
            if time_real:
                st.write("📡 Indicador seleccionado en Time Real:", time_real)
        else:
            st.warning("⚠️ **Acceso Restringido**\n\nPara acceder a Real Time, es necesario Iniciar Sesión.")
            if st.button("🔑 Iniciar Sesión", key="iniciar_sesion_real_time"):
                st.session_state.modo = "usuario"
                st.rerun()
    """

    #st.sidebar.markdown("<hr class='sidebar-separador'>", unsafe_allow_html=True)
