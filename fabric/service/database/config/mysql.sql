
CREATE DATABASE IF NOT EXISTS flinktest;
USE flinktest;

CREATE TABLE IF NOT EXISTS Student(
    stuid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    stuname VARCHAR(10) NOT NULL,
    stuaddr VARCHAR(40) NOT NULL,
    stusex VARCHAR(10) NOT NULL
);

INSERT INTO `Student`(`stuid`, `stuname`, `stuaddr`, `stusex`) VALUES
	(1, "xiaoming",	"henan zhengzhou", 	"male"),
	(2, "xiaoqing", "shandong jinan",	"female"),
	(3, "xiaohua", 	"hebei shijizhang",	"male"),
	(4, "xiaohong", "yunnan kunming",	"female");