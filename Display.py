# The database tables are displayed, each user story is called

from typing import NoReturn
import Database
import schema
import datetime
from prettytable import PrettyTable

def yearsBetween(startDate: datetime.datetime, endDate: datetime.datetime = datetime.datetime.today().date()):
    """Returns the integer floor number of full years years between two dates.

    Args:
        startDate (datetime.datetime): The start date
        endDate (datetime.datetime, optional): The end date, if not supplied, this will be today. Defaults to datetime.datetime.today().date().
    """
    years = endDate.year - startDate.year
    if endDate.month > startDate.month:
        years += 1
    elif endDate.month == startDate.month and endDate.day > startDate.day:
        years += 1
    return years

def populateAge(db):
    for i in db.query("SELECT * FROM individuals"):
        person = dict(zip(schema.COLUMNS['individuals'], i))
        # person is a dictionary, keys are the field names in schema.py, and the values are the values in the database for that person
        if not person['age']:
            age = yearsBetween(person['birthday'], person['death'] if person['death'] else datetime.datetime.today().date())
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

def datesBeforeCurrent(db):
    #US01
    currentDate = datetime.datetime.today().date()
    query = """
    SELECT
        i.iid, i.name, i.birthday, i.death, m.marrydate, m.divorcedate
    FROM individuals i LEFT JOIN
        marriages m ON i.iid=m.hid OR i.iid=m.wid
    """
    for i in db.query(query):
        person = dict(zip(['iid', 'name', 'birthday', 'death', 'marrydate', 'divorcedate'], i))
        if (person['birthday'] and person['birthday'] > currentDate):
            print("Error US01: " + person['name'] + " (" + person['iid'] + ") 's birth comes after today's date!")
        elif (person['death'] and person['death'] > currentDate):
            print("Error US01: " + person['name'] + " (" + person['iid'] + ") 's death comes after today's date!")
        elif (person['marrydate'] and person['marrydate'] > currentDate):
            print("Error US01: " + person['name'] + " (" + person['iid'] + ") 's marriage comes after today's date!")
        elif (person['divorcedate'] and person['divorcedate'] > currentDate):
            print("Error US01: " + person['name'] + " (" + person['iid'] + ") 's divorce comes after today's date!")

def birthBeforeMarriage(db):
    #US02
    # We want a list of people, with the day they were born, and the day they were married
    marriagesQuery = """
    SELECT 
        i.iid, i.birthday, i.alive, i.death, m.marrydate, m.divorcedate, i.name, m.mid
    FROM individuals i LEFT JOIN 
        marriages m ON i.iid=m.hid OR i.iid=m.wid
    """
    for i in db.query(marriagesQuery):
        person = dict(zip(['iid', 'birthday', 'alive', 'death', 'marrydate', 'divorcedate','name','mid'], i))
        if person['birthday'] and person['marrydate']:
            if person['birthday'] > person['marrydate']:
                print(f"Error US02: Birth date of {person['name']} ({person['iid']}) occurs after his/her marriage date in family ({person['mid']}).")

def birthBeforeDeath(db):
    #US03
    #gets the data from the DB
    for i in db.query("SELECT * FROM individuals"):
        person = dict(zip(schema.COLUMNS['individuals'], i))
        #checks if birthday and death day exist, and evaluates both
        if person['birthday'] and person['death'] and person['birthday'] > person['death']:
            print("Error US03: Birth date of " + person['name'] + " (" + person['iid'] + ") occurs after their death date.")

def marriageBeforeDivorce(db):
    #US04
    for m in db.query("SELECT * FROM marriages"):
        marriage = dict(zip(schema.COLUMNS['marriages'], m))
        if marriage['marrydate'] and marriage['divorcedate'] and marriage['marrydate'] > marriage['divorcedate']:
            print(f"Error US04: Family {marriage['mid']} divorced before they married.")

def marriageBeforeDeath(db):
    #US05
    marriageanddeathquery = """
    SELECT
        i.iid, i.death, m.marrydate, i.name, m.mid
    FROM individuals i LEFT JOIN
        marriages m ON i.iid=m.hid OR i.iid=m.wid
    """
    for i in db.query(marriageanddeathquery):
        person=dict(zip(['iid','death','marrydate','name','mid'],i))
        if person['death'] and person['marrydate']:
            if person['marrydate'] > person['death']:
                print(f"Error US05: Marriage date of {person['name']}({person['iid']}) occurs after his/her death date in family ({person['mid']}).")

def divorceBeforeDeath(db):
    #US06
    divorceAndDeathQuery = """
    SELECT
        i.iid, i.death, m.marrydate, i.name, m.mid, m.divorced, m.divorcedate
    FROM individuals i LEFT JOIN
        marriages m ON i.iid=m.hid OR i.iid=m.wid
    """
    for i in db.query(divorceAndDeathQuery):
        person=dict(zip(['iid','death','marrydate','name','mid','divorced','divorcedate'],i))
        if person['divorcedate'] and person['death']:
            if person['divorcedate'] > person['death']:
                print(f"Error US06: Divorce date of {person['name']}({person['iid']}) occurs after his/her death date in family ({person['mid']}).")

def lessThan150(db):
    #US07
    currentDate = datetime.datetime.now()
    for i in db.query("SELECT * FROM individuals"):
        person = dict(zip(schema.COLUMNS['individuals'], i))
        yearsDiff = yearsBetween(person['birthday'],  person['death'] if person['death'] else datetime.datetime.today().date()) 
        if person['alive'] == 'True' and (yearsDiff > 150):
            print("Error US07: " + person['name'] + "(" + person['iid'] + ") is older than 150 years old!")
        elif (yearsDiff > 150):
            print("Error US07: " + person['name'] + "(" + person['iid'] + ") lived longer than 150 years!")

def birthBeforeMarriageOfParents(db):
    #US08
    query = """
    SELECT
        i.iid, i.name, i.birthday, m.mid, m.marrydate, i.parentmarriage
    FROM individuals i LEFT JOIN
        marriages m ON i.parentmarriage=m.mid
    """
    for i in db.query(query):
        person = dict(zip(['iid', 'name', 'birthday', 'mid', 'marrydate', 'parentmarriage'], i))
        if person['birthday'] and person['marrydate'] and person['birthday'] < person['marrydate']:
            print(f"Anomaly US08: Birth date of {person['name']} ({person['iid']}) occurs before the marriage date of their parents in Family {person['mid']}.")

def display(db):
    # Display SQL tables...
    populateAge(db)
    displaySQLTables(db)

    # Run user stories...
    # Sprint 1
    datesBeforeCurrent(db)
    birthBeforeMarriage(db)
    birthBeforeDeath(db)
    marriageBeforeDivorce(db)
    marriageBeforeDeath(db)
    divorceBeforeDeath(db)
    lessThan150(db)
    birthBeforeMarriageOfParents(db)

if __name__ == "__main__":
    db = Database.Database(rebuild=False)
    display(db)
