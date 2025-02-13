from components.header_menu import generar_header

def aplicar_layout(nav):
    def decorator(func):
        def wrapper(*args, **kwargs):
            generar_header(nav)  # Se muestra el header en la parte superior
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
