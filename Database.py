import mysql.connector
from dotenv import load_dotenv
import os
import schema

class Database:
    def __init__(self, verbose: bool = False, rebuild = True):
       
        load_dotenv()

        # Initialize mysql database cursor
        self.db = mysql.connector.connect(
            host='localhost',
            user='GEDCOM',
            password=os.getenv('MYSQL_PASSWORD')
        )
        self.cursor = self.db.cursor()

        if rebuild:
            try:
                self.cursor.execute("DROP DATABASE GEDCOM")
            except mysql.connector.errors.DatabaseError:
                pass

            # Create database and tables in mysql
            self.cursor.execute("CREATE DATABASE GEDCOM")

        self.cursor.execute("USE GEDCOM")
        for table_name, build_sql in schema.TABLES.items():
            if verbose:
                print(f"Creating table {table_name}...")
            self.cursor.execute(build_sql)
    
    def query(self, query_string):
        self.cursor.execute(query_string)
        return self.cursor.fetchall()

    def constrain(self):
        for constraint in schema.CONSTRAINTS:
            self.cursor.execute(constraint)


    def teardown(self):
        self.cursor.execute("DROP DATABASE GEDCOM")

    def commit(self):
        self.db.commit()