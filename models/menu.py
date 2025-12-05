"""
Módulo de definicion de clase menu y sus operaciones CRUD en la base de datos
Proyecto Happy Burguer para la clase de Python Avanzado del curso de Fullstack developer de TecMilenio.
Autor: Jose Bernardo Moya Jimenez
Fecha: 2024-12-4
email: bmjimenez@hotmail.com
"""
#Importaciones
from db import get_connection

 #Clase que representa un producto del menú y sus operaciones CRUD en base de datos.
class Menu:

    def __init__(self, id_menu, nombre, precio):
        """Constructor de la clase Menu."""
        self.id_menu = id_menu
        self.nombre = nombre
        self.precio = precio

    #Crea (agrega) un producto en la tabla Menu.
    @staticmethod
    def crear_producto(id_menu, nombre, precio):
       
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO Menu (IdMenu, nombre, precio)
                VALUES (?, ?, ?);
                """,
                (int(id_menu), nombre, float(precio)),
            )
            conn.commit()
            cur.close()
            
    #Consulta un producto del menú por IdMenu.
    @staticmethod
    def consultar_producto(id_menu):
        
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM Menu WHERE IdMenu = ?;",
                (int(id_menu),),
            )
            row = cur.fetchone()
            cur.close()
        return row

    #Elimina un producto del menú por IdMenu.
    @staticmethod
    def eliminar_producto(id_menu):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM Menu WHERE IdMenu = ?;",
                (int(id_menu),),
            )
            conn.commit()
            cur.close()
            
    #Actualiza un producto del menú por IdMenu.
    @staticmethod
    def actualizar_producto(id_menu, nombre, precio):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE Menu
                SET nombre = ?, precio = ?
                WHERE IdMenu = ?;
                """,
                (nombre, float(precio), int(id_menu)),
            )
            conn.commit()
            cur.close()
            
    #Lista todos los productos del menú.
    @staticmethod
    def listar_todos():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Menu ORDER BY IdMenu;")
            rows = cur.fetchall()
            cur.close()
        return rows
