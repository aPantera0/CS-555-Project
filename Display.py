# The database tables are displayed, each user story is called

import Database
import schema
import datetime
from prettytable import PrettyTable


def userStory():
    print("This is a user story")

def populateAge(db):
    for i in db.query("SELECT * FROM individuals"):
        person = dict(zip(schema.COLUMNS['individuals'], i))
        # person is a dictionary, keys are the field names in schema.py, and the values are the values in the database for that person
        if not person['age']:
            birth = person['birthday']
            if not person['alive']:
                death = person['death']
            else:
                death = datetime.datetime.today().date()
            age = death.year - birth.year
            if death.month > birth.month:
                age += 1
            elif death.month == birth.month and death.day > birth.day:
                age += 1
            db.cursor.execute(f"UPDATE individuals SET age={age} WHERE iid='{person['iid']}'") # has to be a better way to do this
    db.commit()


def displaySQLTables(db):
    sentinceCase = lambda x: x[0].upper() + x[1:].lower()
    fConversions = {
        'iid': 'ID',
        'mid': 'ID',
        'parentmarriage': 'Child',
        'marrydate': 'Married',
        'divorcedate': 'Divorce Date',
        'hid': 'Husband ID',
        'wid': 'Wife ID'
    }
    convertFNs = lambda fn: sentinceCase(fn) if fn not in fConversions else fConversions[fn]

    it = PrettyTable()

    it.field_names = list(map(
        convertFNs, 
        schema.COLUMNS['individuals']
    ))
    it.add_rows(db.query("SELECT * FROM individuals ORDER BY iid"))

    mt = PrettyTable()
    mt.field_names = ['ID', 'Married', 'Divorced', 'Divorce Date', 'Wife ID',
        'Wife Name', 'Husband Id', 'Husband Name']
    marriagesQuery = """
    SELECT 
        m.mid AS ID, m.marrydate AS Married, m.divorced AS Divorced, 
        m.divorcedate AS 'Divorce Date', m.wid AS 'Wife ID', i1.name AS 'Wife Name', 
        m.hid AS 'Husband Id', i2.name AS 'Husband Name'
    FROM marriages m LEFT JOIN 
        individuals i1 ON m.wid=i1.iid LEFT JOIN
        individuals i2 ON m.hid=i2.iid"""
    mt.add_rows(db.query(marriagesQuery))
    print('Individuals', it, 'Families', mt, sep='\n')

def birthBeforeMarriage(db):
    # We want a list of people, with the day they were born, and the day they were married
    marriagesQuery = """
    SELECT 
        i.iid, i.birthday, i.alive, i.death, m.marrydate, m.divorcedate
    FROM individuals i LEFT JOIN 
        marriages m ON i.iid=m.hid OR i.iid=m.wid
    """
    for i in db.query(marriagesQuery):
        person = dict(zip(['iid', 'birthday', 'alive', 'death', 'marrydate', 'divorcedate'], i))
        print(person)

def display(db):
    # Display SQL tables...
    # populateAge(db)
    # displaySQLTables(db)
    birthBeforeMarriage(db)
    # userStory()

if __name__ == "__main__":
    db = Database.Database(rebuild=False)
    display(db)