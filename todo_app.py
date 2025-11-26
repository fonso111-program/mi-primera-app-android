import flet as ft
import sqlite3
from datetime import datetime

class BaseDatos:
    def __init__(self, nombre_db="tareas.db"):
        self.nombre_db = nombre_db
        self.crear_tabla()
    
    def crear_conexion(self):
        conexion = sqlite3.connect(self.nombre_db)
        return conexion
    
    def crear_tabla(self):
        conexion = self.crear_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                completada INTEGER DEFAULT 0,
                fecha_creacion TEXT
            )
        ''')
        conexion.commit()
        conexion.close()
    
    def agregar_tarea(self, titulo):
        conexion = self.crear_conexion()
        cursor = conexion.cursor()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO tareas (titulo, completada, fecha_creacion)
            VALUES (?, ?, ?)
        ''', (titulo, 0, fecha_actual))
        conexion.commit()
        conexion.close()
        return True
    
    def obtener_tareas(self):
        conexion = self.crear_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM tareas ORDER BY id DESC')
        tareas = cursor.fetchall()
        conexion.close()
        return tareas
    
    def marcar_completada(self, id_tarea, completada):
        conexion = self.crear_conexion()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE tareas 
            SET completada = ? 
            WHERE id = ?
        ''', (completada, id_tarea))
        conexion.commit()
        conexion.close()
    
    def eliminar_tarea(self, id_tarea):
        conexion = self.crear_conexion()
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM tareas WHERE id = ?', (id_tarea,))
        conexion.commit()
        conexion.close()


def main(page: ft.Page):
    page.title = "Mi Lista de Tareas"
    page.padding = 20
    page.bgcolor = "#1a1a2e"
    page.scroll = ft.ScrollMode.AUTO
    
    db = BaseDatos()
    
    titulo = ft.Text(
        "📝 Mis Tareas",
        size=36,
        weight="bold",
        color="#eee",
        text_align=ft.TextAlign.CENTER
    )
    
    campo_nueva_tarea = ft.TextField(
        hint_text="¿Qué necesitas hacer?",
        expand=True,
        border_color="#16f4d0",
        focused_border_color="#4ecca3",
        color="#ffffff",
        bgcolor="#16213e",
        text_size=18,
        cursor_color="#4ecca3",
        hint_style=ft.TextStyle(
            color="#6c757d",
            size=16
        ),
        border_radius=10,
        content_padding=15
    )
    
    texto_error = ft.Text(
        "",
        size=14,
        color="#ff6b6b",
        text_align=ft.TextAlign.CENTER
    )
    
    texto_contador = ft.Text(
        "0 tareas",
        size=16,
        color="#aaa",  # ← Color más claro para mejor visibilidad
        text_align=ft.TextAlign.CENTER
    )
    
    lista_tareas = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
    
    def crear_item_tarea(id_tarea, titulo, completada):
        """
        Crea un elemento visual para una tarea.
        """
        
        def cambiar_estado(e):
            nuevo_estado = 1 if e.control.value else 0
            db.marcar_completada(id_tarea, nuevo_estado)
            cargar_tareas()
        
        def eliminar(e):
            db.eliminar_tarea(id_tarea)
            cargar_tareas()
        
        checkbox = ft.Checkbox(
            value=bool(completada),
            on_change=cambiar_estado,
            fill_color="#4ecca3",
            check_color="#ffffff"  # ← Check blanco más visible
        )
        
        # Texto con o sin tachado según estado
        if completada:
            texto_tarea = ft.Text(
                titulo,
                size=16,
                color="#999999",  # ← Gris más claro para completadas
                weight="normal",
                expand=True,
                style=ft.TextStyle(
                    decoration=ft.TextDecoration.LINE_THROUGH,
                    decoration_color="#999999"
                )
            )
        else:
            texto_tarea = ft.Text(
                titulo,
                size=16,
                color="#ffffff",  # ← Blanco puro para pendientes
                weight="bold",
                expand=True
            )
        
        boton_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color="#ff6b6b",
            icon_size=22,
            on_click=eliminar,
            tooltip="Eliminar tarea"
        )
        
        # ✅ COLORES MEJORADOS - MUY VISIBLE
        return ft.Container(
            content=ft.Row(
                [checkbox, texto_tarea, boton_eliminar],
                alignment=ft.MainAxisAlignment.START
            ),
            bgcolor="#2d3561",              # ← Azul más claro que el fondo
            border_radius=12,
            padding=18,
            border=ft.border.all(2, "#3d4a7a"),  # ← Borde visible
            margin=ft.margin.only(bottom=5),     # ← Espacio entre items
            animate=ft.Animation(300, "easeInOut")
        )
    
    def cargar_tareas():
        """
        Carga todas las tareas desde la base de datos y las muestra.
        """
        lista_tareas.controls.clear()
        tareas = db.obtener_tareas()
        
        total = len(tareas)
        completadas = sum(1 for t in tareas if t[2] == 1)
        texto_contador.value = f"{total} tarea{'s' if total != 1 else ''} ({completadas} completada{'s' if completadas != 1 else ''})"
        
        if tareas:
            for tarea in tareas:
                id_tarea = tarea[0]
                titulo = tarea[1]
                completada = tarea[2]
                item = crear_item_tarea(id_tarea, titulo, completada)
                lista_tareas.controls.append(item)
        else:
            lista_tareas.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No hay tareas aún.\n¡Añade tu primera tarea arriba!",
                        size=16,
                        color="#888",
                        text_align=ft.TextAlign.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )
        
        page.update()
    
    def agregar_tarea(e):
        """
        Añade una nueva tarea a la base de datos.
        """
        titulo = campo_nueva_tarea.value.strip()
        
        if not titulo:
            texto_error.value = "⚠️ Escribe una tarea"
            page.update()
            return
        
        texto_error.value = ""
        db.agregar_tarea(titulo)
        campo_nueva_tarea.value = ""
        cargar_tareas()
    
    def presionar_enter(e):
        """
        Permite añadir tareas presionando Enter.
        """
        if campo_nueva_tarea.value.strip():
            agregar_tarea(e)
    
    campo_nueva_tarea.on_submit = presionar_enter
    
    boton_agregar = ft.ElevatedButton(
        "Añadir Tarea",
        on_click=agregar_tarea,
        bgcolor="#4ecca3",
        color="white",
        height=50,
        elevation=3
    )
    
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    titulo,
                    ft.Container(height=10),
                    ft.Row(
                        [campo_nueva_tarea, boton_agregar],
                        spacing=10
                    ),
                    texto_error,
                    ft.Container(height=10),
                    texto_contador,
                    ft.Container(height=20),
                    ft.Container(
                        content=lista_tareas,
                        expand=True
                    )
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True
        )
    )
    
    cargar_tareas()

ft.app(target=main)