# The GEDCOM file is parsed into the SQL database

from typing import List
import datetime

valid_mid_tags = {'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'}
valid_end_tags = {'INDI', 'FAM'}

def ingest_lines(db, lines: List[str]):
    values = {}
    table = None
    prev = ("", "", "")
    for line in lines:
        line = line.strip()
        if line[-1] == '\n':
            line = line[:-1]
        line_parts = line.split(' ')
        level = line_parts[0]

        if line_parts[-1] in valid_end_tags:
            tag = line_parts[-1]
            args = ' '.join(line_parts[1:-1])
        else:
            tag = line_parts[1]
            args = ' '.join(line_parts[2:])

        if level == '0':
            if values and table: # if the values dictionary is not empty, we have some info about a previous person or family in it
                sql = f"INSERT INTO {table} ({', '.join([k for k in values])}) VALUES ({', '.join(['%s' for k in values])})"
                val = [v for k, v in values.items()]
                db.cursor.execute(sql, val)
            values = {}
            if tag == 'INDI':
                table = 'individuals'
                values['iid'] = args
            elif tag == 'FAM':
                table = 'marriages'
                values['mid'] = args
        
        # Individual tags
        elif tag == "NAME" and args:
            values['name'] = args
        elif tag == "SEX" and args:
            values['gender'] = args
        elif tag == "DATE" and prev[1] == "BIRT":
            values['birthday'] = datetime.datetime.strptime(args, '%d %b %Y')
        elif tag == "DEAT" and args == "Y":
            values['alive'] = 'False'
        elif tag == "DATE" and prev[1] == "DEAT":
            values['death'] = datetime.datetime.strptime(args, '%d %b %Y')
        elif tag == "FAMC" and args:
            values['parentmarriage'] = args

        # Family tags
        elif tag == "DATE" and prev[1] == "MARR":
            values['marrydate'] = datetime.datetime.strptime(args, '%d %b %Y')
        elif tag == "DIV":
            values['divorced'] = 'True'
        elif tag == "DATE" and prev[1] == "DIV":
            values['divorcedate'] = datetime.datetime.strptime(args, '%d %b %Y')
        elif tag == "HUSB" and args:
            values['hid'] = args
        elif tag == "WIFE" and args:
            values['wid'] = args
        prev = (level, tag, args)
    db.commit()

def ingest_file(db, path: str):
    """Reads a list of GEDCOM lines into the database.

    Args:
        path (str): Path to a GEDCOM file.
    """
    with open(path, 'r') as ged_file:
        ingest_lines(db, ged_file.readlines())
    
