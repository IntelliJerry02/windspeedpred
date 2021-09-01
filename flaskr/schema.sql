------ 创建表
-- 在 SQLite 中，数据储存在 表 和 列 中。在储存和调取数据之前需要先创建它们。 
-- Flaskr 会把用户数据储存在 user 表中，把博客内容储存在 post 表中。
-- 下面 创建一个文件储存用于创建空表的 SQL 命令：

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS frame;
DROP TABLE IF EXISTS dataset;
DROP TABLE IF EXISTS algorithm_execute;
DROP TABLE IF EXISTS computer_configuration;
DROP TABLE IF EXISTS arguments;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  usertype TEXT NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO user VALUES (1, 'admin1', '管理员', '123456');

CREATE TABLE frame (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  directory TEXT NOT NULL,
  argument_number INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE algorithm_execute (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  algorithm_id INTEGER NOT NULL,
  dataset_id INTEGER NOT NULL,
  config_id INTEGER NOT NULL,
  arguments_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  execute_time REAL NOT NULL,
  mse REAL NOT NULL,
  rmse REAL NOT NULL,
  directory TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (algorithm_id) REFERENCES frame (id),
  FOREIGN KEY (dataset_id) REFERENCES dataset (id),
  FOREIGN KEY (config_id) REFERENCES computer_configuration (id),
  FOREIGN KEY (arguments_id) REFERENCES arguments (id)
);

CREATE TABLE dataset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT,
  directory TEXT NOT NULL,
  dataset_type TEXT NOT NULL,
  time_interval REAL NOT NULL,
  space_interval REAL NOT NULL,
  source TEXT NOT NULL,
  data_number INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

INSERT INTO dataset VALUES (1, 2, CURRENT_TIMESTAMP, 'dataset1', '123/456', '仅时间', 5, 5, 'nuist', 100000);

CREATE TABLE computer_configuration (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  cpu TEXT NOT NULL,
  gpu TEXT NOT NULL,
  memory TEXT NOT NULL
);

CREATE TABLE arguments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  alpha REAL NOT NULL,
  tau REAL NOT NULL,
  k REAL NOT NULL,
  dc REAL NOT NULL,
  filter_cnn REAL NOT NULL,
  kernel_size REAL NOT NULL
);

-- 在 db.py 文件中添加 Python 函数 init_db() ，用于运行这个 SQL 命令