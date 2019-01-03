BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `videos` (
	`videoid`	TEXT NOT NULL UNIQUE,
	`title`	TEXT NOT NULL,
	`published_at`	TEXT,
	`description`	TEXT,
	'moon_phase'	REAL,
	PRIMARY KEY(`videoid`)
);
CREATE TABLE IF NOT EXISTS `video_stats` (
	`tstamp`	TEXT NOT NULL,
	`videoid`	TEXT NOT NULL,
	`views`	INTEGER,
	`likes`	INTEGER,
	`dislikes`	INTEGER,
	`comments`	INTEGER,
	PRIMARY KEY(`videoid`,`tstamp`)
);
CREATE TABLE IF NOT EXISTS `followers` (
	`tstamp`	TEXT NOT NULL,
	`site`	TEXT NOT NULL,
	`count`	INTEGER NOT NULL,
	PRIMARY KEY(`site`,`tstamp`)
);
COMMIT;
