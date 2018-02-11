# Logs Analysis Project

Logs Analysis Project is the third project of the Udacity Fullstack Web Developer Nanodegree. 
The project runs three queries on a given database (intialised with newsdata.sql).
The database contains three tables articles, authors and log. 
It is queried via the python file log_analyser.py using psycopg2 for establishing the connection to the database.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Usage

Python2.7 and PostgreSQL are needed to run this code.
Initialise database by running:

```
$ psql -d news -f newsdata.sql
```

Once the database is initialised you can run the three predefined queries by:
```
$ python log_analyser.py
```

This will run the queries defined in the python program and show the formatted result in the terminal. 
