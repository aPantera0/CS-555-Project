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

    def test_US01(self):
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

    def tearDown(self) -> None:
        sys.stdout = sys.__stdout__  # Un-redirect stdout

if __name__ == '__main__':
    unittest.main()
