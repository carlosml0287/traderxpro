import functools
from components.header_menu import generar_header
from components.sidebar import generarMenu

def aplicar_layout():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            generar_header()  # Se muestra el header en la parte superior
            return func(*args, **kwargs)
        return wrapper
    return decorator



def aplicar_layout_con_sidebar():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            generar_header()    # Muestra el header en la parte superior
            generarMenu()   # Muestra el sidebar
            return func(*args, **kwargs)
        return wrapper
    return decorator