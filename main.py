import flet as ft

def main(page: ft.Page):
    # Configuración
    page.title = "Mi App Android"
    page.padding = 20
    page.bgcolor = "#1a1a2e"
    page.scroll = ft.ScrollMode.AUTO
    
    # Elementos
    titulo = ft.Text(
        "¡Mi App en Android!",
        size=32,
        weight="bold",
        color="#eee",
        text_align=ft.TextAlign.CENTER
    )
    
    texto_saludo = ft.Text(
        "Escribe tu nombre",
        size=20,
        color="#16f4d0",
        text_align=ft.TextAlign.CENTER
    )
    
    texto_error = ft.Text(
        "",
        size=16,
        color="#ff6b6b",
        text_align=ft.TextAlign.CENTER
    )
    
    campo_nombre = ft.TextField(
        label="Tu nombre",
        hint_text="Escribe aquí...",
        text_align=ft.TextAlign.CENTER,
        border_color="#16f4d0",
        focused_border_color="#4ecca3",
        color="#eee",
        max_length=30
    )
    
    contador = [0]
    texto_contador = ft.Text(
        "Saludos: 0",
        size=18,
        color="#eee",
        text_align=ft.TextAlign.CENTER
    )
    
    def saludar(e):
        nombre = campo_nombre.value
        if not nombre:
            texto_error.value = "⚠️ Escribe tu nombre"
            texto_saludo.color = "#ff6b6b"
        else:
            texto_error.value = ""
            texto_saludo.value = f"¡Hola {nombre}! 👋"
            texto_saludo.color = "#4ecca3"
            contador[0] += 1
            texto_contador.value = f"Saludos: {contador[0]}"
        page.update()
    
    def despedir(e):
        nombre = campo_nombre.value
        if not nombre:
            texto_error.value = "⚠️ Escribe tu nombre"
        else:
            texto_error.value = ""
            texto_saludo.value = f"¡Adiós {nombre}! 👋"
            texto_saludo.color = "#ff9f43"
        page.update()
    
    def limpiar(e):
        campo_nombre.value = ""
        texto_saludo.value = "Escribe tu nombre"
        texto_saludo.color = "#16f4d0"
        texto_error.value = ""
        contador[0] = 0
        texto_contador.value = "Saludos: 0"
        page.update()
    
    campo_nombre.on_submit = saludar
    
    # Botones
    btn_saludar = ft.ElevatedButton(
        "👋 Saludar",
        on_click=saludar,
        height=50,
        bgcolor="#0f3460",
        color="white",
        expand=True
    )
    
    btn_despedir = ft.ElevatedButton(
        "👋 Despedir",
        on_click=despedir,
        height=50,
        bgcolor="#e94560",
        color="white",
        expand=True
    )
    
    btn_limpiar = ft.ElevatedButton(
        "🔄 Limpiar",
        on_click=limpiar,
        height=50,
        bgcolor="#4ecca3",
        color="white",
        expand=True
    )
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    titulo,
                    ft.Container(height=20),
                    texto_saludo,
                    texto_error,
                    ft.Container(height=20),
                    campo_nombre,
                    ft.Container(height=20),
                    texto_contador,
                    ft.Container(height=20),
                    btn_saludar,
                    ft.Container(height=10),
                    btn_despedir,
                    ft.Container(height=10),
                    btn_limpiar
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True
        )
    )

ft.app(target=main)