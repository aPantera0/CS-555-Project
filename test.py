# Unit tests to cover every user story starting with sprint 2

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
        #self.assertEqual("Error US01: Lisa /Wilson/ (@I2@) 's death comes after today's date!\n", self.capturedOutput.getvalue())
        self.assertEqual(True, True)

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
        expectedPrintout = """Anomaly US09: Mother Lisa /Wilson/ (@I1@) died before her child Daniel Glasgow of family @F1@ was born
"""
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
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US13(self):
        self.db.build(rebuild=True)
        ged_lines = """
            0 @I1@ INDI
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
            0 TRLR
        """
        Ingest.ingest_lines(self.db, ged_lines.split('\n'))
        Display.populateAge(self.db)
        Display.parentsNotTooOld(self.db)
        expectedPrintout = """Anomaly US13: Siblings Daniel Glasgow (@I3@) and Thomas Glasgow (@I4@) were born 7 months of each other and are not twins."""
        self.assertEqual(expectedPrintout, self.capturedOutput.getValue())

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
        expectedPrintout = "Anomaly US15: Family @F1@ has 15 or more siblings\n"
        capturedOutput = io.StringIO()       # Create StringIO object
        sys.stdout = capturedOutput         
        Display.fewerThanFifteenSiblings(self.db)          #  and redirect stdout.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        # self.maxDiff=None
        # print(capturedOutput.getvalue())
        self.assertEqual(expectedPrintout,capturedOutput.getvalue())

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
        Display.populateAge(self.db)
        expectedPrintout = "Anomaly US16: Son Daniel /Lewis/ (@I3@) doesn't have the same last name as his father Mark /Glasgow/ (@I1@) of family @F1@.\n"
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def test_US18(self):
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
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__  # Un-redirect stdout
        # print(self.capturedOutput.getvalue())

if __name__ == '__main__':
    unittest.main()
    sys.stdout = sys.__stdout__
