Configuración
=============

Linux/Ubuntu:
-------------

Asegurese de tener instalado libpq-dev para el correcto funcionamiento del driver de postgresql en django

```sh
sudo apt-get install libpq-dev
```

Instale el requiriment
```sh
python3 -m pip install -r requirements.txt
```

Database:

Cree la base de datos y usuario que usara el proyecto:

```sh
$ sudo su - postgres
$ psql

CREATE DATABASE chrdb;
CREATE USER chr_user WITH ENCRYPTED PASSWORD '1q2w3e4r5t';
GRANT ALL PRIVILEGES ON DATABASE chrdb TO chr_user;
```

El proyecto cuenta con variables de entorno en el archivo .env, se debe cambiar el archivo de .env.example para que el proyecto tome las variables desde ese archivo:

```sh
$ mv chr/.env.example chr/.env
```

Cree el superusuario para el django admin:

```sh
$ python manage.py createsuperuser
email: admin@yopmail.com
user: admin
pass: 1q2w3e4r5t
```

Tarea 1
=======

Que se hizo:
------------

1. Comando para consultar el api rest y guardar la info en base de datos, ejecutar en la consola con:
```sh
# Advertencia: Solo si se usa un virtualenv, activar primero con:
$ source $PATH_TO_VIRTUALENV/bin/active

# Luego ejecutar:
$ python manage.py requestapi
```
2. Habilitado el admin para consultar los datos y agregar otros manualmente
3. Para no complicar el manejo de los id alfanuméricos de los objetos en la API se usó el ID autoincrement de django, pero adicional a eso se agregó un campo external_id para almacenar el ID proveniente del API.
4. Se asumió que listas como payment y company son listados de objetos, por lo tanto, se crearon modelos para que se puedan agregar nuevos desde el admin o ejecutando el comando que lee la API.