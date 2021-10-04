# Read command line paramaters, call ingest and display

import Ingest
import Database
import argparse
import functools
import Display

def validate_file(filename):
    # Validates a GEDCOM file
    db = Database.Database()
    Ingest.ingest_file(db, filename)
    Display.display(db)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate a GEDCOM file")
    parser.add_argument("filename", type=str, help="Path to a GEDCOM text file")
    args = parser.parse_args()
    validate_file(args.filename)

# run with python3 GEDCOMvalidator.py TestGEDCOM1.ged > out.txt
