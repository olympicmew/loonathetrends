CREATE TABLE IF NOT EXISTS "video_stats"
(
	tstamp   DATE NOT NULL,
	video_id TEXT NOT NULL,
	views    INTEGER,
	likes    INTEGER,
	dislikes INTEGER,
	comments INTEGER,
	PRIMARY KEY(video_id, tstamp)
);

CREATE TABLE IF NOT EXISTS "videos"
(
	video_id     TEXT NOT NULL UNIQUE,
	title        TEXT NOT NULL,
	published_at DATE,
	description  TEXT,
	moon_phase   REAL,
	PRIMARY KEY(video_id)
);

CREATE TABLE IF NOT EXISTS "followers"
(
	tstamp      DATE NOT NULL,
	site        TEXT NOT NULL,
	resource_id TEXT NOT NULL,
	count       INTEGER NOT NULL,
	PRIMARY KEY(site, resource_id, tstamp)
);

CREATE TABLE IF NOT EXISTS "spotify_popularity"
(
	tstamp     DATE NOT NULL,
	artist_id  TEXT NOT NULL,
	popularity INTEGER,
	PRIMARY KEY(tstamp, artist_id)
);

CREATE TABLE IF NOT EXISTS "registry"
(
	key   TEXT PRIMARY KEY,
	value TEXT
);