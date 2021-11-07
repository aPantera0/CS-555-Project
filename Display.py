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

def marriageAfter14(db):
    #US10: Marriage after 14
    #Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
    pass

def noBigAmy(db):
    #US11
    # Marriage should not occur during marriage to another spouse
    query = """
    SELECT 
        i.iid, i.name, m.mid, m.marrydate, m.divorced, m.divorcedate, m.hid, m.wid
    FROM 
        individuals i join marriages m INNER JOIN
        (SELECT
            i.iid, i.name, m.mid, m.marrydate, m.divorced, m.divorcedate, m.hid, m.wid
        FROM
            individuals i join marriages m
        WHERE 
            i.iid = m.hid OR i.iid = m.wid 
        GROUP BY
            i.iid
        HAVING
            count(i.iid)>1) mm ON mm.iid = i.iid AND (m.hid = i.iid or m.wid = i.iid)
    """
    result = {}
    for i in db.query(query):
        indis = result.keys()
        person = dict(zip(['iid','name','mid','marrydate','divorced','divorcedate','hid','wid'],i))
        #print(person)
        if person['iid'] in indis:
            result[person['iid']]['marriages'].append(person['divorced'])
        else:
            data = {
                'name':person['name'],
                'marriages':[person['divorced']]
            }
            result[person['iid']] = data
    # print(result)
    keys = result.keys()
    for key in keys:
        name = result[key]['name']
        marriages = result[key]['marriages']
        valid = 0
        for m in marriages:
            if m=='False':
                valid +=1
            else:
                valid -=1
            # print(m,valid)
        if valid > 0:
            print(f"Anomaly US11: {name}({key}) has marriage during marriage to another spouse.")

def parentsNotTooOld(db):
    #US12
    # Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
    # Creates an Error
    query = """
    SELECT
        c.birthday as child_bday, h.birthday as father_bday, w.birthday as mother_bday, h.iid as hid, w.iid as wid, h.name as hname, w.name as wname, c.iid as cid, c.name as cname, m.mid
    FROM marriages m LEFT JOIN
        individuals c ON c.parentmarriage=m.mid
    LEFT JOIN 
        individuals h on m.hid=h.iid 
    LEFT JOIN 
        individuals w on m.wid=w.iid 
    WHERE c.birthday IS NOT NULL
    """
    for i in db.query(query):
        person = dict(zip(['child_bday', 'father_bday', 'mother_bday', 'hid', 'wid', 'hname', 'wname', 'cid', 'cname', 'mid'], i))
        if person['father_bday'] and yearsBetween(person['father_bday'], person['child_bday']) > 80:
            print(f"Anomaly US12: Father {person['hname']} ({person['hid']}) is more than 80 years ({yearsBetween(person['father_bday'], person['child_bday'])}) older than his child {person['cname']} ({person['cid']}) of family {person['mid']}.")
        if person['mother_bday'] and yearsBetween(person['mother_bday'], person['child_bday']) > 60:
            print(f"Anomaly US12: Mother {person['wname']} ({person['wid']}) is more than 60 years ({yearsBetween(person['mother_bday'], person['child_bday'])}) older than his child {person['cname']} ({person['cid']}) of family {person['mid']}.")

def multipleBirthsCap(db):
    #US14
    #No more than five siblings should be born at the same time
    pass

def fewerThanFifteenSiblings(db):
    # US15
    # There should be fewer than 15 siblings in a family.
    query = """
        SELECT i.iid, i.name,j.iid,j.name
        FROM individuals i JOIN marriages m JOIN individuals j
        WHERE i.parentmarriage = m.mid AND i.iid<>j.iid AND j.iid IN
        (
            SELECT k.iid
            FROM individuals k INNER JOIN marriages l on k.parentmarriage = l.mid
            WHERE m.hid = l.hid OR m.wid = l.wid
        )
    """
    result = {}
    for i in db.query(query):
        indis = result.keys()
        person = dict(zip(['iid','name','sid','sname'],i))
        #print(person)
        if person['iid'] in indis:
            result[person['iid']]['siblings'] += 1
        else:
            data = {
                'name':person['name'],
                'siblings': 1
            }
            result[person['iid']] = data
    # print(result)
    keys = result.keys()
    for key in keys:
        name = result[key]['name']
        siblings = result[key]['siblings']
        if siblings >= 15:
            print(f"Anomaly US15: {name} ({key}) has 15 or more siblings.")

    # query = """
    #     SELECT f.mid
    #     FROM individuals i, marriages f
    #     WHERE i.parentmarriage = f.mid
    #     GROUP BY f.mid
    #     HAVING COUNT(*)>=15
    # """
    # for i in db.query(query):
    #     fam = dict(zip(['mid'],i))
    #     if fam['mid']:
    #         print(f"Anomaly US15: Family {fam['mid']} has 15 or more siblings")



def maleLastNames(db):
    #US16
    # All male members of a family should have the same last name
    # Creates an Anomoly 
    query = """
    SELECT
        c.name, c.iid, h.name, h.iid, m.mid
    FROM marriages m LEFT JOIN
        individuals c ON c.parentmarriage=m.mid
    LEFT JOIN 
        individuals h on m.hid=h.iid 
    WHERE c.gender='M' AND c.name IS NOT NULL AND h.name IS NOT NULL
    """
    for i in db.query(query):
        person = dict(zip(['son_name', 'son_id', 'father_name', 'father_id', 'mid'], i))
        son_last = person['son_name'].split('/')[1]
        father_last = person['father_name'].split('/')[1]
        if son_last != father_last:
            print(f"Anomaly US16: Son {person['son_name']} ({person['son_id']}) doesn't have the same last name as his father {person['father_name']} ({person['father_id']}) of family {person['mid']}.")


def display(db):
    # Display SQL tables...
    populateAge(db)
    displaySQLTables(db)

    # Run user stories...
    # Sprint 1
    # datesBeforeCurrent(db)
    # birthBeforeMarriage(db)
    # birthBeforeDeath(db)
    # marriageBeforeDivorce(db)
    # marriageBeforeDeath(db)
    # divorceBeforeDeath(db)
    # lessThan150(db)
    # birthBeforeMarriageOfParents(db)

    # Run user stories...
    # Sprint 2
    # parentsNotTooOld(db)
    # noBigAmy(db)
    fewerThanFifteenSiblings(db)
    # maleLastNames(db)

if __name__ == "__main__":
    db = Database.Database(rebuild=False)
    display(db)
