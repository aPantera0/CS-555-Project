# MySQL schema

ID_DATA_TYPE = "varchar(200)"


TABLES['Individual'] = f"""CREATE TABLE IF NOT EXISTS `gtfs` (
    `feed_id` {ID_DATA_TYPE} NOT NULL,
    `gtfs_timestamp` datetime NOT NULL UNIQUE,
    `file` longblob NOT NULL,
    `gtfs_url` text NOT NULL,
    `parsed` boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (`feed_id`, `gtfs_timestamp`),
    FOREIGN KEY (`feed_id`) REFERENCES feeds (`feed_id`)
    ) ENGINE=InnoDB
    """