Configuración
=============

Linux Ubuntu:

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

Tarea 1
=======

Que se hizo:
------------

1. Comando para consultar el api rest y guardar la info en base de datos
2. Habilitado el admin para consultar los datos y agregar otros manualmente
3. Vista publica para visualizar los datos


Admin
=====

```sh
$ python manage.py createsuperuser
email: admin@yopmail.com
user: admin
pass: 1q2w3e4r5t
```