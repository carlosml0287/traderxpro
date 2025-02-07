import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("assets/fondo.png")

# Guarda el resultado en un archivo CSS
with open("styles.css", "w") as f:
    f.write(f"""
    [data-testid="stAppViewContainer"] {{
        position: relative;
        height: 100vh;
        width: 100vw;
        background: url("data:image/png;base64,{image_base64}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}
    """)
