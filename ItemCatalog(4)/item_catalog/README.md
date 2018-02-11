# Item Catalog Project

Item Catalog Project is the fourth project of the Udacity Fullstack Web Developer Nanodegree. 
The project consists of a Web Interface, a backend written in python and a database that stores items of predefined categories.
The user can view, add, edit and remove items via the web interface only if he is logged in.
Unauthorized users can only view the items in the catalog. The Authorization system is provided by Google


## Usage
Python2.7, PostgreSQL,sqlalchemy and Flask are needed to run this code.

Initialise database by running:

```
$ python catalog_database_setup.py
$ python catalog_database_create.py
```

This will create a catalog.db file. The catalog_database_setup.py creates the tables while the catalog_database_create.py
populates the database with sample categories and items. If you want to reset the database just delete the catalog.db file and rerun these commands.
If you can execute execute bash script simply run:

```
$ sh catalog_database_build.sh
```


Once the database is initialised you have to start the server by using:

```
$ python webapp.py
```

The application should now be hosted at port 8000 on your local machine. Use URL http://localhost:8000 to access it via your favorite browser

The project also includes an JSON Endpoint that responds with the entire item catalog: http://localhost:8000/catalog.json

