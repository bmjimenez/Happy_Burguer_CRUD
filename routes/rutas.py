"""
Módulo de rutas en Flask para Happy Burger.
Este programa define las rutas para manejar clientes, menú y pedidos
utilizando las clases definidas en los modelos individuales de clases clientes, menú y pedidos.
Cada ruta maneja las operaciones CRUD y la generación de tickets para pedidos.
Proyecto Happy Burguer para la clase de Python Avanzado del curso de Fullstack developer de TecMilenio.
Autor: Jose Bernardo Moya Jimenez
Fecha: 2024-12-4
email: bmjimenez@hotmail.com

"""
#Importaciones
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db
from models.clientes import Cliente
from models.menu import Menu
from models.pedido import Pedido

# Calcular ruta a la carpeta templates en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "clave_secreta_happy_burger"

# Inicializar base de datos
init_db()


# Ruta principal que muestra el panel con clientes, menú y pedidos.
@app.route("/")
def index():
    clientes = Cliente.listar_todos()
    menus = Menu.listar_todos()
    pedidos = Pedido.listar_todos()

    """
    pestaña activa: viene por querystring ?tab=..., 
    Se hace para que se mantenga en la misma pestaña del frontend al hacer operaciones"""
    
    tab_activa = request.args.get("tab", "pedidos")  # Se define por defecto el tab 'pedidos' en el frontend

    # Para consulta individual de pedido
    id_pedido_buscar = request.args.get("id_pedido")
    pedido_buscado = None
    if id_pedido_buscar:
        pedido_buscado = Pedido.consultar_pedido(id_pedido_buscar)
        # NO forzamos tab aquí, respetamos el tab recibido (normalmente 'pedidos' definido arriba)

    return render_template(
        "index.html",
        clientes=clientes,
        menus=menus,
        pedidos=pedidos,
        pedido_buscado=pedido_buscado,
        tab_activa=tab_activa,
    )


# ------------------ CLIENTES ------------------ #
"""Ruta para agregar un cliente."""
@app.route("/clientes/agregar", methods=["POST"])
def agregar_cliente():
    tab = request.form.get("tab", "clientes")
    try:
        Cliente.agregar_cliente(
            request.form["id_cliente"],
            request.form["nombre"],
            request.form["direccion"],
            request.form["correo"],
            request.form["telefono"],
        )
        flash("Cliente agregado correctamente.") #mensaje de exito

    except sqlite3.IntegrityError as e:
        # ID duplicado en la tabla Clientes
        if "UNIQUE constraint failed: Clientes.IdCliente" in str(e):
            flash("Error al agregar cliente: El ID de cliente ya existe")
        else:
            flash(f"Error al agregar cliente: {e}")

    except Exception as e:
        flash(f"Error al agregar cliente: {e}")

    return redirect(url_for("index", tab=tab))



@app.route("/clientes/actualizar", methods=["POST"])
def actualizar_cliente():
    """Ruta para actualizar un cliente."""
    tab = request.form.get("tab", "clientes")
    try:
        Cliente.actualizar_cliente(
            request.form["id_cliente"],
            request.form["nombre"],
            request.form["direccion"],
            request.form["correo"],
            request.form["telefono"],
        )
        flash("Cliente actualizado correctamente.")
    except Exception as e:
        flash(f"Error al actualizar cliente: {e}")

    return redirect(url_for("index", tab=tab))


@app.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar_cliente(id_cliente):
    """Ruta para eliminar un cliente."""
    tab = request.form.get("tab", "clientes")
    try:
        Cliente.eliminar_cliente(id_cliente)
        flash("Cliente eliminado correctamente.")
    except Exception as e:
        flash(f"Error al eliminar cliente: {e}")

    return redirect(url_for("index", tab=tab))


# ------------------ MENÚ ------------------ #

@app.route("/menu/agregar", methods=["POST"])
def agregar_producto():
    """Ruta para agregar un producto al menú."""
    tab = request.form.get("tab", "menu")
    try:
        Menu.crear_producto(
            request.form["id_menu"],
            request.form["nombre_menu"],
            request.form["precio"],
        )
        flash("Producto agregado correctamente.")
    except Exception as e:
        flash(f"Error al agregar producto: {e}")

    return redirect(url_for("index", tab=tab))


@app.route("/menu/actualizar", methods=["POST"])
def actualizar_producto():
    """Ruta para actualizar un producto del menú."""
    tab = request.form.get("tab", "menu")
    try:
        Menu.actualizar_producto(
            request.form["id_menu"],
            request.form["nombre_menu"],
            request.form["precio"],
        )
        flash("Producto actualizado correctamente.")
    except Exception as e:
        flash(f"Error al actualizar producto: {e}")

    return redirect(url_for("index", tab=tab))


@app.route("/menu/eliminar/<int:id_menu>", methods=["POST"])
def eliminar_producto(id_menu):
    """Ruta para eliminar un producto del menú."""
    tab = request.form.get("tab", "menu")
    try:
        Menu.eliminar_producto(id_menu)
        flash("Producto eliminado correctamente.")
    except Exception as e:
        flash(f"Error al eliminar producto: {e}")

    return redirect(url_for("index", tab=tab))


# ------------------ PEDIDOS ------------------ #

@app.route("/pedidos/agregar", methods=["POST"])
def agregar_pedido():
    """Ruta para crear un pedido."""
    import sqlite3  # Asegúrate de tener este import

    tab = request.form.get("tab", "pedidos")

    try:
        Pedido.crear_pedido(
            request.form["id_pedido"],
            request.form["id_cliente_pedido"],
            request.form["id_menu_pedido"],
        )
        flash("Pedido creado correctamente. Ticket generado en carpeta 'tickets'.")
    
    except sqlite3.IntegrityError as e:
        # Error específico cuando un IdPedido ya existe
        if "UNIQUE constraint failed: Pedido.IdPedido" in str(e):
            flash("Error al crear pedido: el numerode pedido ya existe")
        else:
            flash(f"Error al crear pedido: {e}")

    except Exception as e:
        flash(f"Error al crear pedido: {e}")

    return redirect(url_for("index", tab=tab))


@app.route("/pedidos/actualizar", methods=["POST"])
def actualizar_pedido():
    """Ruta para actualizar un pedido (snapshot de cliente, producto y precio)."""
    tab = request.form.get("tab", "pedidos")
    try:
        Pedido.actualizar_pedido(
            request.form["id_pedido"],
            request.form["cliente"],
            request.form["producto"],
            request.form["precio"],
        )
        flash("Pedido actualizado correctamente.")
    except Exception as e:
        flash(f"Error al actualizar pedido: {e}")

    return redirect(url_for("index", tab=tab))


@app.route("/pedidos/eliminar/<int:id_pedido>", methods=["POST"])
def eliminar_pedido(id_pedido):
    """Ruta para eliminar un pedido."""
    tab = request.form.get("tab", "pedidos")
    try:
        Pedido.eliminar_pedido(id_pedido)
        flash("Pedido eliminado correctamente.")
    except Exception as e:
        flash(f"Error al eliminar pedido: {e}")

    return redirect(url_for("index", tab=tab))


if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)       # Para evitar DB locks y se levanten 2 procesos (reloader y app)