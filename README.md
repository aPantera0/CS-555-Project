# CS-555-Project

Nick Guo
Simrun Heir
Michael Yap
Andrew Pantera

## Purpose of the program

Ingest GEDCOM file into a database. Query the database for the data we want to display.

The data we want to display:

A list of all the individuals found. 

A list of all the families

Other lists defined in the user stories

## Structure

This system will be run from the command line with one command line parameter: the name of the GEDCOM file to parse. It will then process the data, and display errors, anomalies, and other lists defined in the user stories. 

1. Ingest

Every person and family is read into the SQL tables. Error checking, Anomaly checking, and user stories are not implemented here.

2. Display

The SQL tables for the individuals and families are displayed. Each user story is called. 

## First time setup

Ubuntu 20

```shell
  $ sudo apt update
  $ sudo apt-get install python3 python3-pip mysql-server
  $ pip3 install mysql-connector-python prettytable python-dotenv
  $ sudo service mysql start
  $ sudo mysql_secure_installation
  $ sudo mysql
  mysql> CREATE USER 'GEDCOM'@'localhost' IDENTIFIED BY 'create-a-password';
  mysql> GRANT ALL PRIVILEGES ON * . * TO 'GEDCOM'@'localhost';
  mysql> FLUSH PRIVILEGES;
  mysql> quit
  $ echo "MYSQL_PASSWORD=create-a-password" >> .env
```

## How to run

```shell
  $ python3 GEDCOMvalidator.py path-to-GEDCOM-file 
```

