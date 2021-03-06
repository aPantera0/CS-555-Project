# Unit tests to cover every user story starting with sprint 2

from os import truncate
import unittest
import datetime
import Database
import json
import schema
import Display
import io
import sys
import Ingest

# Our unit tests print to console, our methodology for testing console prints was found here https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print

class Tester(unittest.TestCase): 
    def setUp(self) -> None:
        self.capturedOutput = io.StringIO()  
        sys.stdout = self.capturedOutput # here we redirect stdout to our capturedOutput object
        # We can now query what was printed with capturedOutput.getvalue()
        self.db = Database.Database() # Initialize database

    def example_test_US01(self):
        # This test case will not be run because it doesnt start with the word 'test'
        """For each user story we need to 
        1. build a database object with our test gedcom information, 
        2. run the user story on it, and 
        3. see if the standard prints are what we expect them to be given that gedcom data
        """
        self.db.build(rebuild=True) # Drop all the tables from the db and re-add them, empty
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2035
            1 FAMS @F1@
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.datesBeforeCurrent(self.db)
        self.db.commit() # we need this because if the test fails, it will hang on the database connection, this closes it. 
        self.assertEqual("Error US01: Lisa /Wilson/ (@I2@) 's death comes after today's date!\n", self.capturedOutput.getvalue())

    def test_US09(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1982
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 7 JUL 1986
            1 FAMS @F1@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 11 JUL 1983
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I2@
            1 WIFE @I1@
            1 CHIL @I3@
            1 _CURRENT Y
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.birthBeforeParentDeath(self.db)
        expectedPrintout = """Anomaly US09: Mother Lisa /Wilson/ (@I1@) died before her child Daniel /Glasgow/ (@I3@) of family @F1@ was born\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US10(self):
        self.db.build(rebuild=True) 
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2110
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1932
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2005
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Annabelle /Glasgow/
            2 GIVN Annabelle
            2 SURN Glasgow
            2 _MARNM Edison
            1 SEX F
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Elizabeth /Redington/
            2 GIVN Elizabeth
            2 SURN Redington
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 6 DEC 1968
            1 DEAT Y
            2 DATE 30 Dec 2000
            1 FAMS @F4@
            0 @I6@ INDI
            1 NAME Michael /Glasgow/
            2 GIVN Michael
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 6 OCT 2000
            1 FAMC @F4@
            0 @I7@ INDI
            1 NAME Jennifer /Broome/
            2 GIVN Jennifer
            2 SURN Broome
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 9 OCT 1985
            1 FAMS @F3@
            0 @I8@ INDI
            1 NAME Maryann /Glasgow/
            2 GIVN Maryann
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 13 DEC 2002
            1 FAMC @F3@
            0 @I9@ INDI
            1 NAME Robert /Griffith/
            2 GIVN Robert
            2 SURN Griffith
            2 _MARNM Griffith
            1 SEX M
            1 BIRT
            2 DATE 8 JUL 1985
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I9@
            1 WIFE @I2@
            1 MARR
            2 DATE 2 OCT 2019
            1 _CURRENT Y
            0 @F3@ FAM
            1 HUSB @I3@
            1 WIFE @I7@
            1 CHIL @I8@
            1 MARR
            2 DATE 4 NOV 2003
            1 DIV
            2 DATE 12 MAR 1999
            1 _CURRENT N
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @I5@
            1 CHIL @I6@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2032
            1 _CURRENT N
            0 NOTE information about Emily Smith
            0 @L01@ INDI
            1 NAME Emily /Smith/
            1 BIRT
            2 DATE 06 JUN 1935
            1 SEX F
            1 FAMS @M01@
            0 NOTE information about France Smith
            0 @L02@ INDI
            1 NAME France /Smith/
            1 BIRT
            2 DATE 23 AUG 1933
            1 SEX M
            1 FAMS @M01@
            0 NOTE information about Jack Smith (2nd generation remarried)
            0 @L03@ INDI
            1 NAME Jack /Smith/
            1 BIRT
            2 DATE 14 JUL 1960
            1 SEX M
            1 FAMC @M01@
            1 FAMS @M03@
            0 NOTE information about Jane Smith (3rd generation)
            0 @L04@ INDI
            1 NAME Jane /Smith/
            1 BIRT
            2 DATE 22 JAN 1992
            1 SEX F
            1 FAMC @M03@
            0 NOTE information about Maria Smith (2nd generation died)
            0 @L05@ INDI
            1 NAME Maria /Smith/
            1 BIRT
            2 DATE 28 JUN 1964
            1 SEX F
            1 FAMS @M02@
            1 DEAT
            2 DATE 15 MAY 1994
            0 NOTE information about Stephanie Smith (2nd generation remarried)
            0 @L06@ INDI
            1 NAME Stephanie /Smith/ (3rd generation)
            1 BIRT
            2 DATE 03 FEB 1963
            1 SEX F
            1 FAMS @M03@
            0 NOTE information about Nick Smith
            0 @L07@ INDI
            1 NAME Nick /Leson/
            1 BIRT
            2 DATE 17 AUG 1995
            1 SEX M
            1 FAMC @M03@
            0 NOTE information about James Leson
            0 @L08@ INDI
            1 NAME James /Leson/
            1 BIRT
            2 DATE 30 SEP 1965
            1 SEX M
            1 FAMS @M04@
            0 NOTE family information
            0 @M01@ FAM
            1 MARR
            2 DATE 14 APR 1958
            1 HUSB @L02@
            1 WIFE @L01@
            1 CHIL @L03@
            0 NOTE end of @M01@
            0 @M02@ FAM
            1 MARR
            2 DATE 18 JUN 1989
            2 TYPE Death of Spouse
            1 HUSB @L03@
            1 WIFE @L05@
            1 CHIL @L04@
            0 NOTE end of @M02@
            0 @M03@ FAM
            1 MARR
            2 DATE 25 MAR 1997
            1 HUSB @L03@
            1 WIFE @L06@
            1 CHIL @L04@
            1 CHIL @L07@
            0 NOTE end of @M03@
            0 @M04@ FAM
            1 MARR
            2 DATE 13 OCT 1990
            1 HUSB @L08@
            1 WIFE @L06@
            1 CHIL @L07@
            1 DIV
            2 DATE 12 FEB 1996
            0 NOTE end of @M04@
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.marriageAfter14(self.db)
        self.db.commit()
        self.assertEqual("Anomaly US10: Marriage age of Daniel /Glasgow/ (@I3@) and Jennifer /Broome/ (@I7@) occurs before Daniel /Glasgow/ (@I3@) is 14.\nAnomaly US10: Marriage age of Daniel /Glasgow/ (@I3@) and Elizabeth /Redington/ (@I5@) occurs before Daniel /Glasgow/ (@I3@) is 14.\n", self.capturedOutput.getvalue())

    def test_US11(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2110
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1932
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2005
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Annabelle /Glasgow/
            2 GIVN Annabelle
            2 SURN Glasgow
            2 _MARNM Edison
            1 SEX F
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Elizabeth /Redington/
            2 GIVN Elizabeth
            2 SURN Redington
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 6 DEC 1968
            1 DEAT Y
            2 DATE 30 Dec 2000
            1 FAMS @F4@
            0 @I6@ INDI
            1 NAME Michael /Glasgow/
            2 GIVN Michael
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 6 OCT 2000
            1 FAMC @F4@
            0 @I7@ INDI
            1 NAME Jennifer /Broome/
            2 GIVN Jennifer
            2 SURN Broome
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 9 OCT 1985
            1 FAMS @F3@
            0 @I8@ INDI
            1 NAME Maryann /Glasgow/
            2 GIVN Maryann
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 13 DEC 2002
            1 FAMC @F3@
            0 @I9@ INDI
            1 NAME Robert /Griffith/
            2 GIVN Robert
            2 SURN Griffith
            2 _MARNM Griffith
            1 SEX M
            1 BIRT
            2 DATE 8 JUL 1985
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I9@
            1 WIFE @I2@
            1 MARR
            2 DATE 2 OCT 2019
            1 _CURRENT Y
            0 @F3@ FAM
            1 HUSB @I3@
            1 WIFE @I7@
            1 CHIL @I8@
            1 MARR
            2 DATE 4 NOV 2003
            1 DIV
            2 DATE 12 MAR 1999
            1 _CURRENT N
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @I5@
            1 CHIL @I6@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2032
            1 _CURRENT N"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.noBigamy(self.db)
        expectedPrintout = """Anomaly US11: Lisa /Wilson/(@I2@) has marriage during marriage to another spouse.\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US12(self):
        self.db.build(rebuild=True) 
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2035
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.parentsNotTooOld(self.db)
        expectedPrintout = """Anomaly US12: Father Mark /Glasgow/ (@I1@) is more than 80 years (232) older than his child Daniel /Glasgow/ (@I3@) of family @F1@.\nAnomaly US12: Mother Lisa /Wilson/ (@I2@) is more than 60 years (232) older than his child Daniel /Glasgow/ (@I3@) of family @F1@.\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US13(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1982
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 7 JUL 1986
            1 FAMS @F1@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 11 JUL 1973
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Thomas /Glasgow/
            2 GIVN Thomas
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 15 MAY 1973
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I2@
            1 WIFE @I1@
            1 CHIL @I3@
            1 CHIL @I4@
            1 _CURRENT Y
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.siblingSpacing(self.db)
        expectedPrintout = """Anomaly US13: Siblings Daniel /Glasgow/ (@I3@) and Thomas /Glasgow/ (@I4@) were born within 7 months of each other and are not twins.\nAnomaly US13: Siblings Thomas /Glasgow/ (@I4@) and Daniel /Glasgow/ (@I3@) were born within 7 months of each other and are not twins.\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())
        
    def test_US14(self):
        self.db.build(rebuild=True) 
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2035
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Ryan /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I6@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I7@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I8@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I9@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I10@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I11@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I12@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I13@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I14@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I15@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I16@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I17@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I18@ INDI
            1 NAME Nick /Smith/
            2 GIVN Nick
            2 SURN Smith
            2 _MARNM Smith
            1 SEX F
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F2@
            0 @I19@ INDI
            1 NAME Kewn /Lewis/
            2 GIVN Kwen
            2 SURN Lewis
            2 _MARNM Lewis
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 CHIL @I5@
            1 CHIL @I6@
            1 CHIL @I7@
            1 CHIL @I8@
            1 CHIL @I9@
            1 CHIL @I10@
            1 CHIL @I11@
            1 CHIL @I12@
            1 CHIL @I13@
            1 CHIL @I14@
            1 CHIL @I15@
            1 CHIL @I16@
            1 CHIL @I17@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I18@
            1 WIFE @I2@
            1 CHIL @I19@
            1 MARR
            2 DATE 3 AUG 2000
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.multipleBirthsLessEquals5(self.db)
        self.db.commit()
        self.assertEqual("Anomaly US14: Marriage (@F1@) has more than 5 multiple births.\n", self.capturedOutput.getvalue())

    def test_US15(self):
        self.db.build(rebuild=True) 
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2035
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Ryan /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I6@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I7@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I8@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I9@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I10@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I11@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I12@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I13@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I14@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I15@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I16@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I17@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F1@
            0 @I18@ INDI
            1 NAME Nick /Smith/
            2 GIVN Nick
            2 SURN Smith
            2 _MARNM Smith
            1 SEX F
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F2@
            0 @I19@ INDI
            1 NAME Kewn /Lewis/
            2 GIVN Kwen
            2 SURN Lewis
            2 _MARNM Lewis
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMC @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 CHIL @I5@
            1 CHIL @I6@
            1 CHIL @I7@
            1 CHIL @I8@
            1 CHIL @I9@
            1 CHIL @I10@
            1 CHIL @I11@
            1 CHIL @I12@
            1 CHIL @I13@
            1 CHIL @I14@
            1 CHIL @I15@
            1 CHIL @I16@
            1 CHIL @I17@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I18@
            1 WIFE @I2@
            1 CHIL @I19@
            1 MARR
            2 DATE 3 AUG 2000
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.fewerThanFifteenSiblings(self.db)       
        expectedPrintout = "Anomaly US15: Family @F1@ has 15 or more siblings\n"  
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US16(self):
        self.db.build(rebuild=True) 
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2035
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2173
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.maleLastNames(self.db)
        expectedPrintout = "Anomaly US16: Son Daniel /Lewis/ (@I3@) doesn't have the same last name as his father Mark /Glasgow/ (@I1@) of family @F1@.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US17(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2020
            1 FAMS @F1@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 1972
            1 FAMC @F1@
            1 FAMC @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I1@
            1 WIFE @I3@
            1 MARR
            2 DATE 3 AUG 1981
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        expectedPrintout = "Anomaly US17: Marriage (@F2@) occurs between a parent and their descendent Daniel /Glasgow/ (@I3@).\n"
        Display.noDescendentMarriage(self.db)
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())
        #self.assertEqual(True, True)

    def test_US18(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2021
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 1972
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Ryan /Lewis/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 18 OCT 1973
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 1972
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 CHIL @I5@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I5@
            1 WIFE @I4@
            1 MARR
            2 DATE 3 AUG 2000
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        expectedPrintout = "Anomaly US18: Marriage (@F2@) occurs between siblings Daniel /Glasgow/ (@I5@) and Ryan /Lewis/ (@I4@).\n"
        Display.noSiblingMarriage(self.db)
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())
        #self.assertEqual(True, True)

    def test_US19(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2110
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1932
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 2005
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Annabelle /Glasgow/
            2 GIVN Annabelle
            2 SURN Glasgow
            2 _MARNM Edison
            1 SEX F
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Elizabeth /Redington/
            2 GIVN Elizabeth
            2 SURN Redington
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 6 DEC 1968
            1 DEAT Y
            2 DATE 30 Dec 2000
            1 FAMS @F4@
            0 @I6@ INDI
            1 NAME Michael /Glasgow/
            2 GIVN Michael
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 6 OCT 2000
            1 FAMC @F4@
            0 @I7@ INDI
            1 NAME Jennifer /Broome/
            2 GIVN Jennifer
            2 SURN Broome
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 9 OCT 1985
            1 FAMS @F3@
            0 @I8@ INDI
            1 NAME Maryann /Glasgow/
            2 GIVN Maryann
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 13 DEC 2002
            1 FAMC @F3@
            0 @I9@ INDI
            1 NAME Robert /Griffith/
            2 GIVN Robert
            2 SURN Griffith
            2 _MARNM Griffith
            1 SEX M
            1 BIRT
            2 DATE 8 JUL 1985
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I9@
            1 WIFE @I2@
            1 MARR
            2 DATE 2 OCT 2019
            1 _CURRENT Y
            0 @F3@ FAM
            1 HUSB @I3@
            1 WIFE @I7@
            1 CHIL @I8@
            1 MARR
            2 DATE 4 NOV 2003
            1 DIV
            2 DATE 12 MAR 1999
            1 _CURRENT N
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @I5@
            1 CHIL @I6@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2032
            1 _CURRENT N
            0 NOTE information about Emily Smith
            0 @L01@ INDI
            1 NAME Emily /Smith/
            1 BIRT
            2 DATE 06 JUN 1935
            1 SEX F
            1 FAMS @M01@
            0 NOTE information about France Smith
            0 @L02@ INDI
            1 NAME France /Smith/
            1 BIRT
            2 DATE 23 AUG 1933
            1 SEX M
            1 FAMS @M01@
            0 NOTE information about Jack Smith (2nd generation remarried)
            0 @L03@ INDI
            1 NAME Jack /Smith/
            1 BIRT
            2 DATE 14 JUL 1960
            1 SEX M
            1 FAMC @M01@
            1 FAMS @M03@
            0 NOTE information about Jane Smith (3rd generation)
            0 @L04@ INDI
            1 NAME Jane /Smith/
            1 BIRT
            2 DATE 22 JAN 1992
            1 SEX F
            1 FAMC @M03@
            0 NOTE information about Maria Smith (2nd generation died)
            0 @L05@ INDI
            1 NAME Maria /Smith/
            1 BIRT
            2 DATE 28 JUN 1964
            1 SEX F
            1 FAMS @M02@
            1 DEAT
            2 DATE 15 MAY 1994
            0 NOTE information about Stephanie Smith (2nd generation remarried)
            0 @L06@ INDI
            1 NAME Stephanie /Smith/ (3rd generation)
            1 BIRT
            2 DATE 03 FEB 1963
            1 SEX F
            0 NOTE information about Nick Smith
            0 @L07@ INDI
            1 NAME Nick /Leson/
            1 BIRT
            2 DATE 17 AUG 1995
            1 SEX M
            1 FAMC @M03@
            0 NOTE information about James Leson
            0 @L08@ INDI
            1 NAME James /Leson/
            1 BIRT
            2 DATE 30 SEP 1965
            1 SEX M
            1 FAMS @M04@
            0 NOTE family information
            0 @M01@ FAM
            1 MARR
            2 DATE 14 APR 1958
            1 HUSB @L02@
            1 WIFE @L01@
            1 CHIL @L03@
            0 NOTE end of @M01@
            0 @M02@ FAM
            1 MARR
            2 DATE 18 JUN 1989
            2 TYPE Death of Spouse
            1 HUSB @L03@
            1 WIFE @L05@
            1 CHIL @L04@
            0 NOTE end of @M02@
            0 @M03@ FAM
            1 MARR
            2 DATE 25 MAR 1997
            1 HUSB @L03@
            1 WIFE @L06@
            1 CHIL @L04@
            1 CHIL @L07@
            0 NOTE end of @M03@
            0 @M04@ FAM
            1 MARR
            2 DATE 13 OCT 1990
            1 HUSB @L08@
            1 WIFE @I4@
            1 CHIL @L07@
            1 DIV
            2 DATE 12 FEB 1996
            0 NOTE end of @M04@
            0 NOTE information of test1
            0 @L09@ INDI
            1 NAME Maria /Smith/
            1 BIRT
            2 DATE 28 JUN 1964
            1 SEX F
            1 FAMS @M05@
            1 FAMC @M04@
            1 DEAT
            2 DATE 15 MAY 1994
            0 NOTE end
            0 NOTE information of test2
            0 @L10@ INDI
            1 NAME JOne /Smith/
            1 BIRT
            2 DATE 28 JUN 1964
            1 SEX M
            1 FAMS @M05@
            1 FAMC @F4@
            1 DEAT
            2 DATE 15 MAY 1994
            0 NOTE end
            0 @M05@ FAM
            1 MARR
            2 DATE 20 AUG 2010
            1 HUSB @L10@
            1 WIFE @L09@
            0 NOTE end
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.cousinsNotMarry(self.db)
        expectedPrintout = "Anomaly US19: Marraige: Marriage (@M05@) occurs between first counsins JOne /Smith/ (@L10@) and Maria /Smith/ (@L09@)\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())
    
    def test_US20(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2021
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 1973
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Annabelle /Glasgow/
            2 GIVN Annabelle
            2 SURN Glasgow
            2 _MARNM Edison
            1 SEX F
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Elizabeth /Redington/
            2 GIVN Elizabeth
            2 SURN Redington
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 6 DEC 1968
            1 FAMS @F4@
            0 @I6@ INDI
            1 NAME Michael /Glasgow/
            2 GIVN Michael
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 6 OCT 2000
            1 FAMC @F4@
            0 @I7@ INDI
            1 NAME Jennifer /Broome/
            2 GIVN Jennifer
            2 SURN Broome
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 9 OCT 1985
            1 FAMS @F3@
            0 @I8@ INDI
            1 NAME Maryann /Glasgow/
            2 GIVN Maryann
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 13 DEC 2002
            1 FAMC @F3@
            0 @I9@ INDI
            1 NAME Robert /Griffith/
            2 GIVN Robert
            2 SURN Griffith
            2 _MARNM Griffith
            1 SEX M
            1 BIRT
            2 DATE 8 JUL 1985
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I9@
            1 WIFE @I2@
            1 MARR
            2 DATE 2 OCT 2019
            1 _CURRENT Y
            0 @F3@ FAM
            1 HUSB @I3@
            1 WIFE @I7@
            1 CHIL @I8@
            1 MARR
            2 DATE 4 NOV 2003
            1 _CURRENT Y
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @I5@
            1 CHIL @I6@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2002
            1 _CURRENT N
            0 @F5@ FAM
            1 HUSB @I4@
            1 WIFE @I8@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2002
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.auntsAndUncles(self.db)
        expectedPrintout = "Anomaly US20: Aunt/Uncle Annabelle /Glasgow/ (@I4@) married their niece/nephew Maryann /Glasgow/ (@I8@).\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US21(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2020
            1 FAMS @F1@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.genderRole(self.db)
        expectedPrintout = "Anomaly US21: Husband Mark /Glasgow/ (@I1@) has gender F.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US22(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2020
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        expectedPrintout = "Anomaly US 22: Individual ID (@I1@) is not unique.\nAnomaly US 22: Family ID (@F1@) is not unique.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_23(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2110
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2110
            1 FAMS @F1@
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.uniqueNameAndBTD(self.db)
        expectedPrintout = """Anomaly US23: Individual @I2@ has the same name and birth date as Individual @I1@ with name Mark /Glasgow/ and birth date 1942-05-03\nAnomaly US23: Individual @I1@ has the same name and birth date as Individual @I2@ with name Mark /Glasgow/ and birth date 1942-05-03\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US24(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2021
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F2@
            0 @I4@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2021
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I3@
            1 WIFE @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.uniqueFamilySpouses(self.db)
        expectedPrintout = "Anomaly US24: Husband Mark /Glasgow/ (@I3@) and wife Lisa /Wilson/ (@I4@) were married on date 1961-08-03 more than once.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US25(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1982
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 7 JUL 1986
            1 FAMS @F1@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 11 JUL 1973
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 11 JUL 1973
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I2@
            1 WIFE @I1@
            1 CHIL @I3@
            1 CHIL @I4@
            1 _CURRENT Y
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.uniqueFirstNames(self.db)
        expectedPrintout = "Anomaly US25: Child Daniel /Glasgow/ appears more than once in the same family.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US26(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME First /Last/
            2 GIVN First
            2 SURN Last
            2 _MARNM Last
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F4@
            0 @I4@ INDI
            1 NAME First2 /Last2/
            2 GIVN First2
            2 SURN Last2
            2 _MARNM Last
            1 SEX F
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F5@
            0 @I5@ INDI
            1 NAME Second /Test/
            2 GIVN Second
            2 SURN Test
            2 _MARNM Test
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F7@
            0 @I6@ INDI
            1 NAME Second2 /Test2/
            2 GIVN Second2
            2 SURN Test2
            2 _MARNM Test2
            1 SEX F
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F7@
            0 @I7@ INDI
            1 NAME Child /Noparent/
            2 GIVN Child
            2 SURN Noparent
            2 _MARNM Noparent
            1 SEX F
            1 BIRT
            2 DATE 3 MAY 2000
            1 FAMS @F8@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE 
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB 
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F3@ FAM
            1 HUSB 
            1 WIFE 
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @L1@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F5@ FAM
            1 HUSB @L1@
            1 WIFE @I4@ 
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F6@ FAM
            1 HUSB @L1@
            1 WIFE @L2@  
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F7@ FAM
            1 HUSB @I5@
            1 WIFE @I6@
            1 CHIL @L7@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.correspondingEntries(self.db)
        expectedPrintout = "Anomaly US 22: Family ID (@F4@) is not unique.\nAnomaly US 22: Family ID (@F5@) is not unique.\nAnomaly US 22: Family ID (@F6@) is not unique.\nAnomaly US26: Marriage (@F1@) between husband (@I1@) and wife (None) has only one individual.\nAnomaly US26: Marriage (@F2@) between husband (None) and wife (@I2@) has only one individual.\nAnomaly US26: Marriage (@F3@) between husband (None) and wife (None) has only one individual.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US27(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        #Display.individualAges(self.db)
        expectedPrintout = ""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US28(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2021
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 18 OCT 1973
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Annabelle /Glasgow/
            2 GIVN Annabelle
            2 SURN Glasgow
            2 _MARNM Edison
            1 SEX F
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Elizabeth /Redington/
            2 GIVN Elizabeth
            2 SURN Redington
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 6 DEC 1968
            1 FAMS @F4@
            0 @I6@ INDI
            1 NAME Michael /Glasgow/
            2 GIVN Michael
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 6 OCT 2000
            1 FAMC @F4@
            0 @I7@ INDI
            1 NAME Jennifer /Broome/
            2 GIVN Jennifer
            2 SURN Broome
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 9 OCT 1985
            1 FAMS @F3@
            0 @I8@ INDI
            1 NAME Maryann /Glasgow/
            2 GIVN Maryann
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 13 DEC 2002
            1 FAMC @F3@
            0 @I9@ INDI
            1 NAME Robert /Griffith/
            2 GIVN Robert
            2 SURN Griffith
            2 _MARNM Griffith
            1 SEX M
            1 BIRT
            2 DATE 8 JUL 1985
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I9@
            1 WIFE @I2@
            1 MARR
            2 DATE 2 OCT 2019
            1 _CURRENT Y
            0 @F3@ FAM
            1 HUSB @I3@
            1 WIFE @I7@
            1 CHIL @I8@
            1 MARR
            2 DATE 4 NOV 2003
            1 _CURRENT Y
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @I5@
            1 CHIL @I6@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2002
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.orderSiblingsAge(self.db)
        expectedPrintout = """US28 - List of siblings in families by decreasing age:\n    Family @F1@\n        Annabelle /Glasgow/ (@I4@) age 53\n        Daniel /Glasgow/ (@I3@) age 49\n    Family @F3@\n        Maryann /Glasgow/ (@I8@) age 19\n    Family @F4@\n        Michael /Glasgow/ (@I6@) age 22\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US29(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 1982
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 7 JUL 1986
            1 FAMS @F1@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 11 JUL 1973
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Thomas /Glasgow/
            2 GIVN Thomas
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 15 MAY 1973
            1 FAMC @F1@
            0 @F1@ FAM
            1 HUSB @I2@
            1 WIFE @I1@
            1 CHIL @I3@
            1 CHIL @I4@
            1 _CURRENT Y
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.listDeceased(self.db)
        expectedPrintout = "US29 - List of all deceased individuals: \nLisa /Wilson/ (@I1@)\nMark /Glasgow/ (@I2@)\nEnd of US29.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US30(self):
        self.db.build(rebuild=True)
        ged_lines = """0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 FAMS @F1@
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.listLivingMarried(self.db)
        expectedPrintout = "US30 - List of all living married individuals:\nMark /Glasgow/ (@I1@)\nLisa /Wilson/ (@I2@)\nEnd of US30.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US31(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
1 GEDC
2 VERS 5.5.1
0 @I1@ INDI
1 NAME Mark /Glasgow/
2 GIVN Mark
2 SURN Glasgow
2 _MARNM Glasgow
1 SEX M
1 BIRT
2 DATE 3 MAY 1942
1 DEAT Y
2 DATE 5 DEC 2110
1 FAMS @F1@
0 @I2@ INDI
1 NAME Mark /Glasgow/
2 GIVN Mark
2 SURN Glasgow
2 _MARNM Glasgow
1 SEX M
1 BIRT
2 DATE 3 MAY 2090
1 DEAT Y
2 DATE 5 DEC 2110
1 FAMS @F1@
0 TRLR
        """
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        #Display.listLivingSingle(self.db)
        expectedPrintout = "US-31 - List of all living people over 30 who have never been married:\nMark /Glasgow/ (@I1@)\nEnd of US31.\n"
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US32(self):
        self.db.build(rebuild=True)
        ged_lines = """0 NOTE https://github.com/aPantera0/CS-555-Project
            1 GEDC
            2 VERS 5.5.1
            0 @I1@ INDI
            1 NAME Mark /Glasgow/
            2 GIVN Mark
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 3 MAY 1942
            1 DEAT Y
            2 DATE 5 DEC 2010
            1 FAMS @F1@
            0 @I2@ INDI
            1 NAME Lisa /Wilson/
            2 GIVN Lisa
            2 SURN Wilson
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 8 APR 1942
            1 DEAT Y
            2 DATE 12 JAN 2021
            1 FAMS @F1@
            1 FAMS @F2@
            0 @I3@ INDI
            1 NAME Daniel /Glasgow/
            2 GIVN Daniel
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMS @F3@
            1 FAMS @F4@
            1 FAMC @F1@
            0 @I4@ INDI
            1 NAME Annabelle /Glasgow/
            2 GIVN Annabelle
            2 SURN Glasgow
            2 _MARNM Edison
            1 SEX F
            1 BIRT
            2 DATE 30 JUL 1969
            1 FAMC @F1@
            0 @I5@ INDI
            1 NAME Elizabeth /Redington/
            2 GIVN Elizabeth
            2 SURN Redington
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 6 DEC 1968
            1 FAMS @F4@
            0 @I6@ INDI
            1 NAME Michael /Glasgow/
            2 GIVN Michael
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX M
            1 BIRT
            2 DATE 6 OCT 2000
            1 FAMC @F4@
            0 @I7@ INDI
            1 NAME Jennifer /Broome/
            2 GIVN Jennifer
            2 SURN Broome
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 9 OCT 1985
            1 FAMS @F3@
            0 @I8@ INDI
            1 NAME Maryann /Glasgow/
            2 GIVN Maryann
            2 SURN Glasgow
            2 _MARNM Glasgow
            1 SEX F
            1 BIRT
            2 DATE 13 DEC 2002
            1 FAMC @F3@
            0 @I9@ INDI
            1 NAME Robert /Griffith/
            2 GIVN Robert
            2 SURN Griffith
            2 _MARNM Griffith
            1 SEX M
            1 BIRT
            2 DATE 8 JUL 1985
            1 FAMS @F2@
            0 @F1@ FAM
            1 HUSB @I1@
            1 WIFE @I2@
            1 CHIL @I3@
            1 CHIL @I4@
            1 MARR
            2 DATE 3 AUG 1961
            1 EVEN
            2 TYPE Ending
            1 _CURRENT N
            0 @F2@ FAM
            1 HUSB @I9@
            1 WIFE @I2@
            1 MARR
            2 DATE 2 OCT 2019
            1 _CURRENT Y
            0 @F3@ FAM
            1 HUSB @I3@
            1 WIFE @I7@
            1 CHIL @I8@
            1 MARR
            2 DATE 4 NOV 2003
            1 _CURRENT Y
            0 @F4@ FAM
            1 HUSB @I3@
            1 WIFE @I5@
            1 CHIL @I6@
            1 MARR
            2 DATE 9 SEP 1995
            1 DIV
            2 DATE 8 OCT 2002
            1 _CURRENT N
            0 TRLR"""
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.listMultipleBirths(self.db)
        expectedPrintout = """US32 - List of multiple births:\n    Family @F1@ had multiple birth at 1969-07-30:\n        Daniel /Glasgow/ (@I3@)\n        Annabelle /Glasgow/ (@I4@)\n"""
        self.db.commit()
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

if __name__ == '__main__':
    unittest.main()
