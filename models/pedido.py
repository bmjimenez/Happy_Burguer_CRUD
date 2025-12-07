"""
Módulo de definicion de la clase pedido para Happy Burger.
Define la clase Pedido, sus operaciones en base de datos (CRUD) y la generación de tickets.
Utiliza claves foráneas hacia Clientes y Menu.

Proyecto Happy Burguer para la clase de Python Avanzado del curso de Fullstack developer de TecMilenio.
Autor: Jose Bernardo Moya Jimenez
Fecha: 2024-12-8
email: bmjimenez@hotmail.com
"""

# Importaciones
import os
import datetime
from db import get_connection


class Pedido:
    """Clase que representa un pedido y sus operaciones en base de datos."""

    def __init__(self, id_pedido, id_cliente, id_menu, cliente, producto, precio):
        """Constructor de la clase Pedido."""
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.id_menu = id_menu
        self.cliente = cliente
        self.producto = producto
        self.precio = precio

    # Crea un pedido consultando cliente y producto, guarda snapshot y genera ticket.
    @staticmethod
    def crear_pedido(id_pedido, id_cliente, id_menu):
        """Crea un pedido en la base de datos y genera un ticket de texto."""
        # Operación en base de datos con contexto para evitar locks
        with get_connection() as conn:
            cur = conn.cursor()

            # Obtener datos del cliente
            cur.execute(
                "SELECT nombre FROM Clientes WHERE IdCliente = ?;",
                (int(id_cliente),),
            )
            cliente_row = cur.fetchone()
            if cliente_row is None:
                cur.close()
                raise ValueError("Cliente no encontrado (IdCliente inválido).")

            cliente_nombre = cliente_row["nombre"]

            # Obtener datos del producto
            cur.execute(
                "SELECT nombre, precio FROM Menu WHERE IdMenu = ?;",
                (int(id_menu),),
            )
            menu_row = cur.fetchone()
            if menu_row is None:
                cur.close()
                raise ValueError("Producto de menú no encontrado (IdMenu inválido).")

            producto_nombre = menu_row["nombre"]
            precio = float(menu_row["precio"])

            # Insertar en la tabla Pedido
            cur.execute(
                """
                INSERT INTO Pedido (IdPedido, IdCliente, IdMenu, cliente, producto, precio)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    int(id_pedido),
                    int(id_cliente),
                    int(id_menu),
                    cliente_nombre,
                    producto_nombre,
                    precio,
                ),
            )
            conn.commit()
            cur.close()

        # Fuera del contexto de BD, generamos el ticket (no bloquea la base)
        Pedido.generar_ticket(id_pedido, cliente_nombre, producto_nombre, precio)

    # Función que genera un archivo de texto simulando el ticket del pedido.
    @staticmethod
    def generar_ticket(id_pedido, cliente, producto, precio):
        """Genera un archivo .txt con la información del pedido."""
        # Obtener fecha y hora actual
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        os.makedirs("tickets", exist_ok=True)
        ruta_ticket = os.path.join("tickets", f"ticket-{id_pedido}-{fecha_hora}-{cliente}.txt")

        with open(ruta_ticket, "w", encoding="utf-8") as f:
            f.write("************************\n")
            f.write("*     Happy Burger     *\n")
            f.write("************************\n")
            f.write(f"Fecha: {fecha_hora}\n")  # fecha y hora en la línea siguiente
            f.write(f"Pedido No: {id_pedido}\n")
            f.write(f"Cliente: {cliente}\n")
            f.write(f"Producto: {producto}\n")
            f.write(f"Precio: ${precio:.2f}\n")
            f.write("------------------------\n")
            f.write("¡Gracias por su compra!\n")

    # Consulta un pedido por su IdPedido y regresa el registro completo
    @staticmethod
    def consultar_pedido(id_pedido):
        """Consulta un pedido por IdPedido."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM Pedido WHERE IdPedido = ?;",
                (int(id_pedido),),
            )
            row = cur.fetchone()
            cur.close()
        return row

    # Elimina un pedido de la tabla Pedido.
    @staticmethod
    def eliminar_pedido(id_pedido):
        """Elimina un pedido por IdPedido."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM Pedido WHERE IdPedido = ?;",
                (int(id_pedido),),
            )
            conn.commit()
            cur.close()

    # Actualiza un pedido (snapshot de cliente, producto y precio).
    @staticmethod
    def actualizar_pedido(id_pedido, cliente, producto, precio):
        """Actualiza los datos de un pedido (cliente, producto y precio)."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE Pedido
                SET cliente = ?, producto = ?, precio = ?
                WHERE IdPedido = ?;
                """,
                (cliente, producto, float(precio), int(id_pedido)),
            )
            conn.commit()
            cur.close()

    # Lista todos los pedidos de la tabla Pedido.
    @staticmethod
    def listar_todos():
        """Devuelve todos los pedidos ordenados por IdPedido."""
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Pedido ORDER BY IdPedido;")
            rows = cur.fetchall()
            cur.close()
        return rows
