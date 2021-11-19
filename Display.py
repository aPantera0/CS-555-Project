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

def monthsBetween(startDate: datetime.datetime, endDate: datetime.datetime = datetime.datetime.today().date()):
    return abs((endDate.year - startDate.year) * 12 + (endDate.month - startDate.month))


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

def birthBeforeParentDeath(db):
    #US09
    # Child should be born before death of mother
    # and before 9 months after death of father
    query = """
    SELECT
        c.birthday as child_bday, h.death as father_death, w.death as mother_death, h.iid as hid, w.iid as wid, h.name as hname, w.name as wname, c.iid as cid, c.name as cname, m.mid
    FROM marriages m LEFT JOIN
        individuals c ON c.parentmarriage=m.mid
    LEFT JOIN 
        individuals h on m.hid=h.iid 
    LEFT JOIN 
        individuals w on m.wid=w.iid 
    WHERE c.birthday IS NOT NULL
    """
    for i in db.query(query):
        person = dict(zip(['child_bday', 'father_death', 'mother_death', 'hid', 'wid', 'hname', 'wname', 'cid', 'cname', 'mid'], i))
        if person['father_death'] and person['father_death'] < person['child_bday'] and monthsBetween(person['father_death'], person['child_bday']) > 8:
            print(f"Anomaly US09: Father {person['hname']} ({person['hid']}) died more than 8 months before his child {person['cname']} ({person['cid']}) of family {person['mid']}.")
        if person['mother_death'] and person['child_bday'] > person['mother_death']:
            print(f"Anomaly US09: Mother {person['wname']} ({person['wid']}) died before her child {person['cname']} ({person['cid']}) of family {person['mid']} was born")

def marriageAfter14(db):
    #US10: Marriage after 14
    #Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
    
    #gets info from marriages and then goes back to individuals to get names and birthdates of husband and wife
    query = """
    WITH
        base AS (SELECT mid, marrydate, hid, wid FROM marriages),
        hbirth AS (
            SELECT mid, marrydate, hid, name hname, birthday hbirthday, wid
            FROM base, individuals
            WHERE hid = iid
        )
        SELECT mid, marrydate, hid, hname, hbirthday, wid, name wname, birthday wbirthday
        FROM hbirth, individuals
        WHERE wid = iid
    """
    for i in db.query(query):
        #operates on couples instead of individuals
        couple = dict(zip(['mid','marrydate','hid', 'hname','hbirthday','wid', 'wname', 'wbirthday'], i))
        #both are under 14
        #relative delta from relativedelta import from dateutil library, .years sets difference in terms of years
        if yearsBetween(couple['hbirthday'], couple['marrydate']) < 14 and yearsBetween(couple['wbirthday'], couple['marrydate']) < 14:
            print(f"Anomaly US10: Marriage age of {couple['hname']} ({couple['hid']}) and {couple['wname']} ({couple['wid']}) occurs before {couple['hname']} ({couple['hid']}) and {couple['wname']} ({couple['wid']}) are 14.")
        #husband is under 14
        if yearsBetween(couple['hbirthday'], couple['marrydate']) < 14:
            print(f"Anomaly US10: Marriage age of {couple['hname']} ({couple['hid']}) and {couple['wname']} ({couple['wid']}) occurs before {couple['hname']} ({couple['hid']}) is 14.")
        #wife is under 14
        # if relativedelta.relativedelta(couple['marrydate'],couple['wbirthday']).years < 14:
        if yearsBetween(couple['wbirthday'], couple['marrydate']) < 14:
            print(f"Anomaly US10: Marriage age of {couple['hname']} ({couple['hid']}) and {couple['wname']} ({couple['wid']}) occurs before {couple['wname']} ({couple['wid']}) is 14.")

def noBigamy(db):
    #US11
    # Marriage should not occur during marriage to another spouse
    query = """
    SELECT
        i.iid, i.name, i.birthday, i.death, m.marrydate, m.divorcedate
    FROM individuals i LEFT JOIN
        marriages m ON i.iid=m.hid OR i.iid=m.wid
    """
    spouces = {}
    people = {}
    for i in db.query(query):
        person = dict(zip(['iid', 'name', 'birthday', 'death', 'marrydate', 'divorcedate'], i))
        people[person['iid']] = person
        # populate the people database with keys of the persons ids, and values of tuples of each marry date and divorce date
        if person['iid'] in spouces:
            spouces[person['iid']].append((person['marrydate'], person['divorcedate'], person))
        else:
            spouces[person['iid']] = [(person['marrydate'], person['divorcedate'], person)]
        
    reportedIIDs = set()
    for p in spouces:
        marriages = spouces[p]
        if len(marriages) < 2:
            continue # they can't commit biagamy if they were married less than twice

        for mi, m in enumerate(marriages):
            valid = True
            for m2i, m2 in enumerate(marriages):
                if mi != m2i:
                    if m[0] < m2[0]: # If this marriage starts before the next one
                        if not (m[1] and m[1] < m2[0]): # It must also end before the next one (this one must also have ended)
                            valid = False
                            break
                    else: # If this marriage stars after the next one starts
                        if not (m2[1] and m[0] > m2[1]): # it must also start after the next one ends (the next one must also have ended)
                            valid = False
                            break

            if not valid and m[2]['iid'] not in reportedIIDs:
                print(f"Anomaly US11: {m[2]['name']}({m[2]['iid']}) has marriage during marriage to another spouse.")
                reportedIIDs.add(m[2]['iid']) # we don't want to report the same anomoly twice

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

def siblingSpacing(db):
    #US13
    # Birth dates of siblings should be >8 months apart
    # or <2 days apart (twins may be born 1 day apart
    # e.g. 11:59 PM and 12:02 AM the following calendar day
    query = """
    SELECT
        m.mid, i.iid, i.birthday, i.parentmarriage, i.name
    FROM individuals i LEFT JOIN
        marriages m ON i.parentmarriage=m.mid
    """
    siblings = dict()
    marriages = []
    for i in db.query(query):
        #get all siblings into one unit of data, dict{mid:[(iid1,birthday1),(iid2,birthday2),...]}?
        person = dict(zip(['mid','iid','birthday', 'parentmarriage', 'name'], i))
        if person['mid'] not in siblings.keys():
            siblings[person['mid']] = [person]
            marriages.append(person['mid'])
        else:
            siblings[person['mid']].append(person)
    for j in range(len(marriages)):
        curSiblings = siblings[marriages[j]]
        for k in curSiblings:
            for l in curSiblings:
                if k['iid'] != l['iid'] and abs(monthsBetween(k['birthday'], l['birthday'])) < 8 and abs(monthsBetween(k['birthday'], l['birthday'])) > 1:
                    print(f"Anomaly US13: Siblings {k['name']} ({k['iid']}) and {l['name']} ({l['iid']}) were born within 7 months of each other and are not twins.")

def multipleBirthsLessEquals5(db):
    #US14
    #No more than five siblings should be born at the same time
    query = """
        SELECT mid, iid, birthday
        FROM marriages, individuals
        WHERE mid = parentmarriage
    """
    #dictionary to hold all siblings
    siblings = dict()
    #list to hold all mids
    marriages = []
    #for loop populates siblings and marriages
    for i in db.query(query):
        person = dict(zip(['mid','iid','birthday'], i))
        if person['mid'] not in siblings.keys():
            siblings[person['mid']] = [person['birthday']]
            marriages.append(person['mid'])
        else:
            siblings[person['mid']].append(person['birthday'])
    #goes through all mids
    for j in marriages:
        #finds all siblings of current mid
        curSiblings = siblings[j]
        if len(curSiblings) > 5:
            invalidBirthdays = []
            for k in curSiblings:
                #counts number of duplicate birthdays, number of multiple births
                if curSiblings.count(k) > 5 and k not in invalidBirthdays:
                    print(f"Anomaly US14: Marriage ({j}) has more than 5 multiple births.")
                    invalidBirthdays.append(k)

def fewerThanFifteenSiblings(db):
    # US15
    # There should be fewer than 15 siblings in a family.
    # query = """
    #     SELECT i.iid, i.name,j.iid,j.name
    #     FROM individuals i JOIN marriages m JOIN individuals j
    #     WHERE i.parentmarriage = m.mid AND i.iid<>j.iid AND j.iid IN
    #     (
    #         SELECT k.iid
    #         FROM individuals k INNER JOIN marriages l on k.parentmarriage = l.mid
    #         WHERE m.hid = l.hid OR m.wid = l.wid
    #     )
    # """
    # result = {}
    # for i in db.query(query):
    #     indis = result.keys()
    #     person = dict(zip(['iid','name','sid','sname'],i))
    #     #print(person)
    #     if person['iid'] in indis:
    #         result[person['iid']]['siblings'] += 1
    #     else:
    #         data = {
    #             'name':person['name'],
    #             'siblings': 1
    #         }
    #         result[person['iid']] = data
    # # print(result)
    # keys = result.keys()
    # for key in keys:
    #     name = result[key]['name']
    #     siblings = result[key]['siblings']
    #     if siblings >= 15:
    #         print(f"Anomaly US15: {name} ({key}) has 15 or more siblings.")

    query = """
        SELECT f.mid
        FROM individuals i, marriages f
        WHERE i.parentmarriage = f.mid
        GROUP BY f.mid
        HAVING COUNT(*)>=15
    """
    for i in db.query(query):
        fam = dict(zip(['mid'],i))
        if fam['mid']:
            print(f"Anomaly US15: Family {fam['mid']} has 15 or more siblings")

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

def noDescendentMarriage(db):
    #US 17
    #Parents should not marry any of their descendents
    query1 = """
        SELECT h.name, h.iid, w.name, w.iid, m.mid
        FROM marriages m LEFT JOIN individuals h on m.hid=h.iid
            LEFT JOIN individuals w on m.wid=w.iid
        WHERE h.name IS NOT NULL AND w.name IS NOT NULL
    """
    query2 = """
        SELECT c.name, c.iid, c.parentmarriage, h.name, h.iid, w.name, w.iid
        FROM individuals c LEFT JOIN marriages m on c.parentmarriage=m.mid
            LEFT JOIN individuals h on h.iid=m.hid
            LEFT JOIN individuals w on w.iid=m.wid
        WHERE c.name IS NOT NULL AND h.name IS NOT NULL AND w.name IS NOT NULL AND w.iid IS NOT NULL
    """
    for i in db.query(query1):
        marriage = dict(zip(['hname', 'hid', 'wname', 'wid', 'mid'], i))
        for j in db.query(query2):
            child = dict(zip(['cname', 'cid', 'cpm', 'fname', 'fid', 'mname', 'mmid'], j))
            #print(marriage)
            #print(child)
            if ((child['cid'] == marriage['hid'] or child['cid'] == marriage['wid']) and (child['fid'] == marriage['hid']) or child['mmid'] == marriage['wid']):
                print(f"Anomaly US17: Marriage ({marriage['mid']}) occurs between a parent and their descendent {child['cname']} ({child['cid']}).")

def noSiblingMarriage(db):
    #US 18
    #No siblings should be married to each other

    #returns all marriages where husband and wife have same father or mother
    #of form (mid, hid husband, hid.name hname, wid wife, wid.name wname)
    query = """
        WITH husbands as (
            SELECT m.mid, m.hid husband, i.name hname, p.hid hpa, p.wid hma, m.wid wife
            FROM marriages m, individuals i, marriages p
            WHERE m.hid = iid AND i.parentmarriage = p.mid
        ), wifes as (
            SELECT  h.mid, husband, hname, hpa, hma, wife, i.name wname, p.hid wpa, p.wid wma
            FROM husbands h, individuals i, marriages p
            WHERE h.wife = iid AND i.parentmarriage = p.mid
        )
        SELECT mid, husband, hname, wife, wname
        FROM wifes m
        WHERE hpa = wpa OR hma = wma
    """
    #outputs all marriages between siblings
    for i in db.query(query):
        marriage = dict(zip(['mid', 'husband', 'hname', 'wife', 'wname'], i))
        print(f"Anomaly US18: Marriage ({marriage['mid']}) occurs between siblings {marriage['hname']} ({marriage['husband']}) and {marriage['wname']} ({marriage['wife']}).")

def cousinsNotMarry(db):
    # US 19
    # First cousins should not marry one another
    query = """
    WITH siblings as (
        SELECT i.iid i1, i.name i1name, j.iid i2, j.name i2name, i.parentmarriage
        FROM individuals i, individuals j
        WHERE i.parentmarriage = j.parentmarriage AND i.iid <> j.iid
    )
        SELECT a.iid, a.name, b.iid, b.name, f.mid
        FROM individuals a, marriages f, individuals b, siblings s, marriages q, marriages w
        WHERE f.hid = a.iid and b.iid = f.wid and q.mid = a.parentmarriage and w.mid = b.parentmarriage and ((q.hid = s.i1 or q.wid = s.i1) AND (w.hid = s.i2 or w.wid = s.i2))
    """
    for i in db.query(query):
        marriage = dict(zip(['hid', 'hname', 'wid', 'wname', 'mid'], i))
        print(f"Anomaly US19: Marraige: Marriage ({marriage['mid']}) occurs between first counsins {marriage['hname']} ({marriage['hid']}) and {marriage['wname']} ({marriage['wid']})")

def auntsAndUncles(db):
    #US20
    # Aunts and uncles should not marry their nieces or nephews
    # First we get all possible triplets of grandparent, parent, and child, and then
    # Then, For each grandparent, 
    #   For each of of that grandparents kids
    #       For each of their kids
    #           If that kid is married to any of the grandparents' other kids
    #               throw the anomoly 

    # Get triplets
    tripletsQuery = """SELECT
        grand.name as Grandparent, grand.iid, parent.name as Parent, parent.iid, child.name as Child, child.iid
    FROM 
        individuals grand 
    LEFT JOIN 
        marriages mg ON mg.hid=grand.iid OR mg.wid=grand.iid 
    LEFT JOIN 
        individuals parent ON parent.parentmarriage = mg.mid
    LEFT JOIN 
        marriages mp ON mp.hid=parent.iid OR mp.wid=parent.iid 
    LEFT JOIN 
        individuals child ON child.parentmarriage = mp.mid"""
    triplets = []
    grandparents = {} # a mapping of grandparent iids to lists of triplets
    for triplet in db.query(tripletsQuery):
        # triplet = dict(zip(['gname', 'gid', 'pname', 'pid', 'cname', 'cid'], i))
        triplets.append(triplet)
        if triplet[1] in grandparents:
            grandparents[triplet[1]] = grandparents[triplet[1]] + [triplet]
        else:
            grandparents[triplet[1]] = [triplet]
    
    # Get marriages
    marriagesQuery = """SELECT
        h.iid, w.iid
    FROM 
        marriages m
    LEFT JOIN 
        individuals h on m.hid=h.iid
    LEFT JOIN 
        individuals w on m.wid=w.iid"""
    marriages = {} # a mapping of hisband ids to a list of wife ids, and from wife ids to a list of husband ids
    for hid, wid in db.query(marriagesQuery):
        if hid and wid:
            if hid in marriages:
                marriages[hid] = marriages[hid] + [wid]
            else:
                marriages[hid] = [wid]
            if wid in marriages:
                marriages[wid] = marriages[wid] + [hid]
            else:
                marriages[wid] = [hid]

    anomalies = set()
    for gname, gid, pname, pid, cname, cid in triplets:
        for _, _, auncleName, auncleId, _, _ in grandparents[gid]:
            if auncleId != pid:
                if (auncleId in marriages and cid in marriages[auncleId]) or (cid in marriages and auncleId in marriages[cid]):
                    anomalies.add(f"Anomaly US20: Aunt/Uncle {auncleName} ({auncleId}) married their niece/nephew {cname} ({cid}).")

    list(map(print, anomalies))

def genderRole(db):
    #US 21
    #Correct gender for role
    #ex. husband in family should be male, wife should be female
    query = """
        SELECT h.name, h.iid, h.gender, w.name, w.iid, w.gender, m.mid
        FROM marriages m LEFT JOIN individuals h on m.hid=h.iid
            LEFT JOIN individuals w on m.wid=w.iid
        WHERE h.name IS NOT NULL AND w.name IS NOT NULL
    """
    for i in db.query(query):
        marriage = dict(zip(['hname', 'hid', 'hgender', 'wname', 'wid', 'wgender', 'mid'], i))
        if (marriage['hgender'] == 'F'):
            print(f"Anomaly US21: Husband {marriage['hname']} ({marriage['hid']}) has gender F.")
        if (marriage['wgender'] == 'M'):
            print(f"Anomaly US21: Wife {marriage['wname']} ({marriage['wid']}) has gender M.")

def uniqueIDs(db):
    # US 22 
    # Implemented upon ingest in ingest.py
    pass

def uniqueNameAndBTD(db):
    #US 23
    #No more than one individual with the same name and birth date should appear in a GEDCOM file

    query = """
        SELECT i.iid, i.name, i.birthday, j.iid, j.name, j.birthday
        FROM individuals i, individuals j
        WHERE i.name = j.name AND i.birthday = j.birthday AND i.iid <> j.iid
    """
    for i in db.query(query):
        person = dict(zip(['iid1', 'name1', 'birthday1', 'iid2', 'name2', 'birthday2'], i))
        print(f"Anomaly US23: Individual {person['iid1']} has the same name and birth date as Individual {person['iid2']} with name {person['name1']} and birth date {person['birthday1']}")
    

def uniqueFamilySpouses(db):
    #US 24
    # No more than one family with the same spouses by name 
    # and the same marriage date should appear in the GEDCOM file
    # the marriages table is keyed by the IDs, so that shouldn't conflict with this user story 
    query = """
        SELECT 
            h.name, h.iid, w.name, w.iid, m.mid, m.marrydate
        FROM 
            marriages m 
        LEFT JOIN 
            individuals h on m.hid=h.iid
        LEFT JOIN 
            individuals w on m.wid=w.iid
        WHERE 
            h.name IS NOT NULL AND w.name IS NOT NULL"""
    # hname, hiid, wname, wiid, mmid, mmarrydate
    marriages = set()
    for hname, hiid, wname, wiid, mmid, marrydate in db.query(query):
        key = (hname, wname, marrydate)
        if key in marriages:
            print(f"Anomaly US24: Husband {hname} ({hiid}) and wife {wname} ({wiid}) were married on date {marrydate} more than once.")
        else:
            marriages.add(key)



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

    # Run user stories...
    # Sprint 2
    birthBeforeParentDeath(db)
    marriageAfter14(db)
    noBigamy(db)
    parentsNotTooOld(db)
    siblingSpacing(db)
    multipleBirthsLessEquals5(db)
    fewerThanFifteenSiblings(db)
    maleLastNames(db)

    #Run user stories...
    #Sprint 3
    noDescendentMarriage(db) #US17 No marriages to descendants
    noSiblingMarriage(db) #US18 No marriages to siblings
    cousinsNotMarry(db) #US19 First cousins should not marry   
    auntsAndUncles(db) # US20 
    genderRole(db) #US21
    #US22 implemented in ingest.py
    uniqueNameAndBTD(db) #US 23 Unique name and birth date
    uniqueFamilySpouses(db) #US 24 Unique families by spouses

if __name__ == "__main__":
    db = Database.Database(rebuild=False)
    display(db)
