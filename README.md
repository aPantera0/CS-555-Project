# CS-555-Project

Nick Guo
Simrun Heir
Michael Yap
Andrew Pantera

## Purpose of the program

Ingest GEDCOM file into a database. Query the database for the data we want to display.

The data we want to display:

A list of all the individuals found. 

A list of all the families

Other lists defined in the user stories

## Structure

This system will be run from the command line with one command line parameter: the name of the GEDCOM file to parse. It will then process the data, and display errors, anomalies, and other lists defined in the user stories. 

1. Ingest

This is where user stories for validation are implemented, like catching errors, catching anomalies, and enforcing rules.

2. Display

This is where the families and individuals tables are displayed, and where user stories that involve listing things like orphans are done.

## How to run

```shell
  $ python3 .\GEDCOMvalidator.py validate path-to-GEDCOM-file 
```

