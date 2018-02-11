#!/bin/bash
rm -rf catalog.db
python catalog_database_setup.py
python catalog_database_create.py
