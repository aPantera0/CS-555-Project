# MySQL schema

ID_DATA_TYPE = "varchar(200)"
NAME_DATA_TYPE = "varchar(200)"

TABLES = {}
COLUMNS = {}
CONSTRAINTS = []

TABLES['individuals'] = f"""CREATE TABLE IF NOT EXISTS `individuals` (
    `iid` {ID_DATA_TYPE} NOT NULL UNIQUE,
    `name` {NAME_DATA_TYPE},
    `gender` CHAR,
    `birthday` DATE,
    `age` SMALLINT,
    `alive` varchar(5) DEFAULT 'True',
    `death` DATE,
    `parentmarriage` {ID_DATA_TYPE},
    PRIMARY KEY (`iid`, `name`)
    ) ENGINE=InnoDB
    """
COLUMNS['individuals'] = ("iid", "name", "gender", "birthday", "age",
    "alive", "death", "parentmarriage")

TABLES['marriages'] = f"""CREATE TABLE IF NOT EXISTS `marriages` (
    `mid` {ID_DATA_TYPE} NOT NULL UNIQUE,
    `marrydate` DATE,
    `divorced` varchar(5) DEFAULT 'False',
    `divorcedate` DATE,
    `hid` {ID_DATA_TYPE},
    `wid` {ID_DATA_TYPE},
    PRIMARY KEY (`mid`),
    FOREIGN KEY (`hid`) REFERENCES individuals (`iid`),
    FOREIGN KEY (`wid`) REFERENCES individuals (`iid`)
    ) ENGINE=InnoDB
    """
# In order for these to be foreign keys, the name column would need to be unique in the individuals table. 
# We can get all this data from a join, we dont need to store it twice
    # `hname` {NAME_DATA_TYPE},
    # `wname` {NAME_DATA_TYPE},
    # FOREIGN KEY (`hname`) REFERENCES individuals (`name`),
    # FOREIGN KEY (`wname`) REFERENCES individuals (`name`)

COLUMNS['marriages'] = ("mid", "marrydate", "divorced", "divorcedate",
    "hid", "wid")

CONSTRAINTS.append(
    f"ALTER TABLE individuals ADD CONSTRAINT `fk_parentmarriage` FOREIGN KEY (`parentmarriage`) REFERENCES `marriages` (`mid`)"
)