
Proyecto Happy Burguer para la clase de Python Avanzado del curso de Fullstack developer de TecMilenio.

Autor: Jose Bernardo Moya Jimenez

Fecha: 2024-12-6

email: bmjimenez@hotmail.com

Este proyecto utiliza una DB en SQLite, y es un CRUD de fullstack, para demostrar habilidades en backend development avanzado con Programacion orientada a objetos + Flask en Python


--Para correr el proyecto,crear el venv:
python -m venv venv 
source venv/bin/activate

-Instalar las dependencias de Python que vienen en el archivo requirements.txt
pip install -r requirements.txt   

-Ejecutar desde raiz del proyecto el comando: 
python3 -m app (usando Macos en este caso)

La estructura del proyecto es asi:
.
├── app.py
├── db
│   ├── __init__.py
│   └── db.py
├── dbSqlite.db
├── models
│   ├── __init__.py
│   ├── clientes.py
│   ├── menu.py
│   └── pedido.py
├── README.md
├── render.yaml
├── requirements.txt
├── routes
│   ├── __init__.py
│   └── rutas.py
├── templates
│   ├── ayuda.html
│   ├── corte_caja.html
│   ├── index.html
│   └── ticket.html
└── tickets
    ├── ticket_1.txt
    ├── ticket_10.txt
    ├── ticket_2.txt
    ├── ticket_3.txt
    ├── ticket_4.txt
 

NOTAS IMPORTANTES :
app.py es el archivo principal del proyecto y de ahi se llama a Routes/rutas.py 

Para actualizar datos de los registros simplemente modifique los datos en las cajas de texto con los campos desplegados en la pagina web y haga click en ACTUALIZAR, aparecera un mensaje en la parte superior indicando el resultado de la operacion.

El mismo caso aplica para eliminar registros, haga click en el boton ELIMINAR que aparece al final del registro y aparecera un mensaje indicando si la operacion fue exitosa. 

Se generan tickets en archivos .txt en el directorio /tickets para simular la impresion de un recibo de compra.





