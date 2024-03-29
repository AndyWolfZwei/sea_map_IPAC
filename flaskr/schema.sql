DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS path_display;
DROP TABLE IF EXISTS path_transfer;
DROP TABLE IF EXISTS states;

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE `user` (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phone TEXT NOT NULL
);

CREATE TABLE `path_display` (
  id INTEGER,
  `x` FLOAT(4,7) NOT NULL,
  `y` FLOAT(4,7) NOT NULL
);

CREATE TABLE `path_transfer` (
  id INTEGER,
  `x` FLOAT(4,7) NOT NULL,
  `y` FLOAT(4,7) NOT NULL
);

CREATE TABLE `states` (
 `state`  SMALLINT DEFAULT 0,
 `lon`  FLOAT(4,6),
 `lat`  FLOAT(4,6),
 `dir`  INTEGER,
 `speed`  SMALLINT ,
 `height` INTEGER,
 `yaw`  INTEGER
);