"""
Módulo de definicion de la clase Cliente y sus operaciones CRUD con la base de datos.

Proyecto Happy Burguer para la clase de Python Avanzado del curso de Fullstack developer de TecMilenio.
Autor: Jose Bernardo Moya Jimenez
Fecha: 2024-12-4
email: bmjimenez@hotmail.com

"""
#Importaciones
from db import get_connection

"""Clase que representa a un cliente y sus operaciones en base de datos."""
class Cliente:
   
    def __init__(self, id_cliente, nombre, direccion, correo_electronico, telefono):
        """Constructor de la clase Cliente."""
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        
    """Agrega un cliente a la tabla Clientes."""
    @staticmethod
    def agregar_cliente(id_cliente, nombre, direccion, correo_electronico, telefono):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Clientes (IdCliente, nombre, direccion, correo_electronico, telefono)
                VALUES (?, ?, ?, ?, ?);
                """,
                (int(id_cliente), nombre, direccion, correo_electronico, telefono),
            )
            conn.commit()
            cur.close()
            
    """Consulta un cliente por su IdCliente y regresa un registro."""
    @staticmethod
    def consultar_cliente(id_cliente):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM Clientes WHERE IdCliente = ?;",
                (int(id_cliente),),
            )
            row = cur.fetchone()
            cur.close()
        return row

    """Elimina un cliente de la tabla Clientes por su IdCliente."""
    @staticmethod
    def eliminar_cliente(id_cliente):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM Clientes WHERE IdCliente = ?;",
                (int(id_cliente),),
            )
            conn.commit()
            cur.close()


    """Actualiza los datos de un cliente existente."""
    @staticmethod
    def actualizar_cliente(id_cliente, nombre, direccion, correo_electronico, telefono):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE Clientes
                SET nombre = ?, direccion = ?, correo_electronico = ?, telefono = ?
                WHERE IdCliente = ?;
                """,
                (nombre, direccion, correo_electronico, telefono, int(id_cliente)),
            )
            conn.commit()
            cur.close()

    """Lista todos los clientes de la tabla Clientes."""
    @staticmethod
    def listar_todos():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Clientes ORDER BY IdCliente;")
            rows = cur.fetchall()
            cur.close()
        return rows
