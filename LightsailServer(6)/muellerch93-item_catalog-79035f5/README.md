# AWS Item Catalog Project

AWS Item Catalog Project is the fourth project of the Udacity Fullstack Web Developer Nanodegree. 
The goal of the project was to setup an AWS server that hosts the item catalog application

## Usage
IP address: 35.158.166.30  
SSH Port: 2200 

Web application: http://35.158.166.30 OR http://35.158.166.30/catalog

## Setup AWS

Software: apache2, libapache2-mod-wsgi, postgresql, python-psycopg2, pip, git,ufw


1. Create new user and grant him root rights
2. Generate key pair using ssh-keygen and enforce key based authorization
3. Make 2200 the new ssh port (edit /etc/ssh/sshd_config, configure lightsail firewall via web app)
4. Set Locale to en_US.UTF-8
5. Config Server Firewall via UFW (deny incoming,allow outgoing, deny ssh, allow 2200/tcp, allow www, allow ntp)
6. Install Apache2 and wsgi and Postgresql
7. Install git
8. Configure Apache to handle requests using the WSGI module. edit: /etc/apache2/sites-enabled/000-default.conf
9. Create new Postgres user (catalog) and make him the owner of a new database catalog_db (used by webapp via psycopg2)


