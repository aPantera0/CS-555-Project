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
        self.assertEqual("Error US01: Lisa /Wilson/ (@I2@) 's death comes after today's date!\n", self.capturedOutput.getvalue())

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
        expectedPrintout = """Anomaly US12: Father Mark /Glasgow/ (@I1@) is more than 80 years (232) older than his child Daniel /Glasgow/ (@I3@) of family @F1@.
Anomaly US12: Mother Lisa /Wilson/ (@I2@) is more than 60 years (232) older than his child Daniel /Glasgow/ (@I3@) of family @F1@.
"""
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
        Display.populateAge(self.db)
        Display.maleLastNames(self.db)
        expectedPrintout = "Anomaly US16: Son Daniel /Lewis/ (@I3@) doesn't have the same last name as his father Mark /Glasgow/ (@I1@) of family @F1@.\n"
        self.assertEqual(expectedPrintout, self.capturedOutput.getvalue())

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__  # Un-redirect stdout
        # print(self.capturedOutput.getvalue())

if __name__ == '__main__':
    unittest.main()
