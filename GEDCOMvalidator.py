# Read command line paramaters, call ingest and display

import argparse
import functools

# Requirements for this script are defined as follows:
# 1) Reads each line of a GEDCOM file

# 2) Prints "--> <input line>"

# 3) Prints "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
#     <level> is the level of the input line, e.g. 0, 1, 2
#     <tag> is the tag associated with the line, e.g. 'INDI', 'FAM', 'DATE', ...
#     <valid?> has the value 'Y' if the tag is one of the supported tags or 'N' otherwise.  The set of all valid tags for our project is specified in the Project Overview document.
#     <arguments> is the rest of the line beyond the level and tag.

# Sample input:
# 0 NOTE dates after now
# 1 SOUR Family Echo
# 2 WWW http://www.familyecho.com  (Links to an external site.)
# 0 bi00 INDI
# 1 NAME Jimmy /Conners/

# Sample output:
# --> 0 NOTE dates after now
# <-- 0|NOTE|Y|dates after now
# --> 1 SOUR Family Echo
# <-- 1|SOUR|N|Family Echo
# --> 2 WWW http://www.familyecho.com (Links to an external site.) (Links to an external site.)
# <-- 2|WWW|N|http://www.familyecho.com (Links to an external site.)
# --> 0 bi00 INDI
# <-- 0|INDI|Y|bi00
# --> 1 NAME Jimmy /Conners/
# <-- 1|NAME|Y|Jimmy /Conners/

valid_mid_tags = {'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'}
valid_end_tags = {'INDI', 'FAM'}

def validate_line(line: str):
    """Process a single line of a GEDCOM file. First printing the line,
    then printing the parsed line

    Args:
        line (str): a single line of a GEDCOM file
    """
    line = line[:-1] # Each line ends with a newline character
    print_lines = [] # store lines and print them after
    print_lines.append(f"--> {line}")
    line_parts = line.split(' ')
    level = line_parts[0]

    if line_parts[-1] in valid_end_tags:
        tag = line_parts[-1]
        args = ' '.join(line_parts[1:-1])
        valid = True
    else:
        tag = line_parts[1]
        args = ' '.join(line_parts[2:])
        valid = tag in valid_mid_tags
    # Valid is defined in the spec as being determined just by the tag,
    # But it is also mentioned later in the spec DATA tags with levels of 2
    # and NAME tags with levels of 1 "we are NOT supporting", does this mean
    # that those tags would be invalid? It does not say the level affects the
    # validity of the tag
    print_lines.append(f"<-- {level}|{tag}|{'Y' if valid else 'N'}|{args}")
    return print_lines

def validate_lines(lines):
    """Validates a list of GEDCOM lines

    Args:
        lines (list): List of strings represting lines of a gedcom file

    Returns:
        [list]: list of strings represting output lines
    """
    return functools.reduce(lambda x, y: x+y, map(validate_line, lines)) # we need to cast to a list in order to execute the map


def validate_file(args):
    # Validates a GEDCOM file
    with open(args.file_path, 'r') as ged_file:
        print('\n'.join(validate_lines(ged_file.readlines())))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    validate_parser = subparsers.add_parser('validate')
    validate_parser.add_argument('file_path', help='path to the file to validate')
    validate_parser.set_defaults(func=validate_file)
    args = parser.parse_args()
    args.func(args)

# run with python3 .\GEDCOMvalidator.py validate ./My-Family-19-Sep-2021-212321671.ged > out.txt

def myFun():
    for person in personstable():
        if person is orphan:
            print the bitch


def main():
    myFun()
