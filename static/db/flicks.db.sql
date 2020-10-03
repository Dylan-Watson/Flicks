BEGIN TRANSACTION;
DROP TABLE IF EXISTS "users";
;
DROP TABLE IF EXISTS "attributes";
CREATE TABLE IF NOT EXISTS "attributes" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"groups"	TEXT,
	PRIMARY KEY("user_id")
);
DROP TABLE IF EXISTS "groups";
CREATE TABLE IF NOT EXISTS "groups" (
	"group_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"code"	TEXT NOT NULL UNIQUE,
	"users"	TEXT
);
INSERT INTO "users" VALUES (1,1,'watson','$2b$12$L7vvdR0jEzLl55opLl7dLOrOccOOfjiuPa0PoJCLPZJbXueTHQcNS','','');
INSERT INTO "attributes" VALUES (1,NULL);
COMMIT;
