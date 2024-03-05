# Índice

- [Version Oficial V1.0](#version-oficial-v10)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Funcionalidades](#funcionalidades)
- [Tecnologías Usadas](#tecnologias-usadas)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Contacto](#contacto)
- [Autores](#autores)

## Tours & Bookings - Flask

Este proyecto es un ejemplo de una API RESTful desarrollada con Flask que permite realizar operaciones CRUD (GET,POST,PUT,DELETE) ademas se hace implementación de JWT y pruebas unitarias 


Este proyecto esta Generado en Flask 3.0.2 [Flask Micro-FrameWork](https://github.com/pallets/flask)


## Version Oficial V1.0

![image](https://github.com/Sebastian-Beltran-rincon-22/tours-flask/assets/132385582/a0877783-2fa5-4b65-82cf-1410f3e39058)


## Estructura de carpetas

![image](https://github.com/Sebastian-Beltran-rincon-22/tours-flask/assets/132385582/016d4fb2-8a49-44f3-ad1e-36f61c6c252c)


## Funcionalidades

- Se implemento `CRUD` en su primera version para navegar por las diferente rutas del proyecto a traves de los tour y reservas filtrado, eliminado y crear.
- Se implemento un `Register` con JWT para la validacion de usuarios para la creacion y seguridad de los tour
- Se implemento un `Login` con has de contraseña y JWT para mas seguridad en el logueo y peticion de datos
- Se implemento diversos `Testing` para la validacion y funcionalidad de las rutas

## Tecnologias Usadas
- PIP
- Python
- JWT (Json Web Token)
- Flask FrameWork
- MySQL
- PyTest
- SQLAlchemy

## Instalación

1 Clona el repositorio en tu maquina local
```bash
git clone https://github.com/Sebastian-Beltran-rincon-22/tours-flask.git
```

2 Navega en el directorio del proyecto 
```bash
cd tours-flask
```

3 Puedes cambiar el origen del proyecto con los siguientes comando

```bash
git remote -v
git remote remove origin
git remote add origin <nueva_url_del_repositorio>
```

4 Instalar venv (O el entorno de preferencia)

- Windows
```bash
python -m venv venv
```
- Linux/Mac
```bash
python3 -m venv venv
```

5 Inicia el entorno virtual

- Windows
```bash
venv/Scripts/activate
```
- Linux/Mac
```bash
source venv/bin/activate
```

6 Instalar las dependecias necesarias con el entorno activo
- Recuerda tener el requirements.txt en el root de la carpeta y ejecutas

```bash
pip install -r requirements.txt
```


## Configuración

> [!IMPORTANT]
>Es importante la configuracion y en MYSQL_DB asignar tu DB

1 .env Configuración

```env
SECRET_KEY=
MYSQL_HOST=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB=
JWT_KEY=
```

2 recuerda inicializar y configurar tu base de datos MySQL SQLite o en todo caso la de tu preferencia

3 Inicia la app con 
```bash
python index.py
```

4 Puedes acceder a ella desde el puerto configurado:

http://127.0.0.1:5000/

## Uso

#### iniciado el puerto puedes navegar en diferentes rutas:
- user 
```bash
http://127.0.0.1:5000/new
http://127.0.0.1:5000/login
```
- tour
```bash
http://127.0.0.1:5000/tours/newtour
http://127.0.0.1:5000/tours/update/<id>
http://127.0.0.1:5000/tours/toursdetails
http://127.0.0.1:5000/tours/delete/<id>
http://127.0.0.1:5000/tours/tourfor/<id>
```
- Bookings
```bash
http://127.0.0.1:5000/bookings/newbooking
http://127.0.0.1:5000/bookings/listbookings/<nameUser>
http://127.0.0.1:5000/bookings/deletebooking/<id>
http://127.0.0.1:5000/bookings/completebooking
```
## Contacto

Si tienes alguna pregunta o sugerencia o quieres la documentacion para desarrollar este proyecto, no dudes en contactarme en [sebastianrincon834@gmail.com](sebastianrincon834@gmail.com).

## Autores

- [@Sebastian Beltran](https://github.com/Sebastian-Beltran-rincon-22)
