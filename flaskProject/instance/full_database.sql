-- Users definition

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255)
, is_admin INTEGER DEFAULT (0));
INSERT INTO Users (username,email,password_hash,avatar_url,is_admin) VALUES
	 ('dennis','3109993240@qq.com','175050','123456',0),
	 ('john_doe','john@example.com','hashed_password','http://example.com/avatar.jpg',0),
	 ('testuser','testuser@example.com','scrypt:32768:8:1$mYdEzCsHZ8tKE6K3$6bf82a45d52f94057d78f8f1cad5961f1db70013700193e31dac047095048ec6475786ead06a4fe1bb1502e043f4349b29d9a721dd8f195a09700bec95ce9565',NULL,0),
	 ('1123','111@qq.com','scrypt:32768:8:1$cTUwWjF6vMqFrIT4$2c247885c9aa8195d04ef3e8ac8dbf1d6fc891282cc88c2e82a240b2bbb92cfb4ea0dd474b0b2f9274b6c0166a1e7622701eb714fb918f7a0b01ffc46d082d05',NULL,0),
	 ('123','123@qq.com','scrypt:32768:8:1$2XcKBnxuMF0RbSBn$d9d21a0b34843fb39611aa926084dea882f5c983f42548132aa6a7bf377f9c4542c48cb4b50f331434eab782377cf35ae1bc855c53a06dd6bd0fa52cc5afcde5',NULL,0),
	 ('qiuzihan','1@qq.com','scrypt:32768:8:1$yREZnWSasFIoDykl$7e43a74b187d701a1cf55ce1ee61586c1de1b2183d2bd741b96e80fb6b0d4ad16bfdb473283410b04f25b2a99fb5952d2dc8d6a95b6095666d5c67506c6d66f5',NULL,0),
	 ('1234','1243@qq.com','scrypt:32768:8:1$RpP5MVloDpKGbJif$4f12a4afe3b4e4b7ebf7fcfe8edfbb0cd7126fe8e10bc27a8759a6c1af4038f1e34e8b6ce7470cd2b54b7b6fc37c72e8f86ecfefff146141efac2c9f3a4ad1ca',NULL,0),
	 ('12345','12345@qq.com','scrypt:32768:8:1$qi9liyPmnR5LaF5m$0b4d516e1db6c989ab3991444cbb3994d6f885fe4e6b57f689688fe8b371320b919db75d1ac66d0aa394a3fe062d22cf9ca3089bbc9895d5aa9faa3de4bbcd41',NULL,0),
	 ('123456','123456@qq.com','scrypt:32768:8:1$c6wMjTTkHzN34Ulw$b85e546315fc9ea21fc27f017773fee6a52294337bc4c533cec5c9cde1bc030f8c4cfb1aac1b2901aa947b681d0feb6b615136979740793faadd6eddc10b1334',NULL,0),
	 ('1112','1112@qq.com','scrypt:32768:8:1$iDpdX792uykPzaBF$83b33f18ebf5d7eef7153d3f14012a2962abfbc57291f11b579c930ed7585e05939c4a0a568f08baa4e543f77c5443b3649655122233c00a4e6581b37d478f73',NULL,0);
INSERT INTO Users (username,email,password_hash,avatar_url,is_admin) VALUES
	 ('abc','abc@qq.com','scrypt:32768:8:1$HbH0XaCeNiwJiqxW$c5c57dd3e7c048bb47a86dc6b76c2369bb3cc9d9c7a5356bcb2a2039087406a42b03de78b83d0d8ff1224100eb5a5406187bacd4c48a6f1deddf267a7cd9da96',NULL,0),
	 ('a','a@qq.com','scrypt:32768:8:1$BcAI6sMdmJMq333p$c34d1590e5c532b6ffce1cb2c4f83105bc3ec7606d7494516e5621fb7df9640e4557d064a1bf18b1996fad0ca256590d654f80884ad8f76b0927738eb85937e4',NULL,1),
	 ('ab','abs@qq.com','scrypt:32768:8:1$yoqjojyUobhVGS3d$7359ddeb3c2c3ef659f9586d7d114191aab5c1a1ec774a6bae75b2f32a3ac82257e92b84f35bb1d29780f7d69319660e2cffb30156be0b63dd28a50f6503a315','None',1),
	 ('admin','333@qq.com','scrypt:32768:8:1$LEtAGCjDCkPnXw1X$e7f32dfa64199dd5d9b4704d8d3e20dd072b9801ac5ccc98c2c89812821a051812da49059db0b803c274526605332f646477fdf6f08bf0e2f8df82795e818d23',NULL,1),
	 ('qiuzi','qqs@qq.com','scrypt:32768:8:1$hcvwQaVYnfgRooYm$6e1e418df21222b9916270b407f6ffb35ce10bf5a1883aaede43d35d085efe0627b497450ef86e9dc4d3283dc8ec0556d016c45059a5b8fb8dfb4d84df00b0fe','None',0),
	 ('qiuzihan03','qqqqqq@qq.com','scrypt:32768:8:1$aMHz3yZELrQFrLUT$edef0d4103df91d85543a643f8bfb87d01ae2d6f5aeb773f85ce84a6f032840a1f049b05831872bf52e878f287ef9fb7b78f02ee523528c9116b8c9f78229c50','None',1);

-- Polls definition

CREATE TABLE Polls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    creator_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1, is_anonymous INTEGER DEFAULT (0), is_disabled INTEGER DEFAULT (0),
    FOREIGN KEY (creator_id) REFERENCES Users(id)
);
INSERT INTO Polls (title,description,start_time,end_time,creator_id,is_active,is_anonymous,is_disabled) VALUES
	 ('最好吃的水果','12','2025-01-26 01:12:00.000000','2025-01-31 01:12:00.000000',13,1,0,1),
	 ('哪种运动好玩','12','2025-01-17 01:13:00.000000','2025-02-01 01:13:00.000000',13,1,0,0),
	 ('春节档哪部电影最好看','12','2025-01-24 20:57:00.000000','2025-01-29 20:00:00.000000',13,1,1,0),
	 ('实例','123','2025-02-02 16:59:00.000000','2025-02-04 16:59:00.000000',13,1,1,1),
	 ('test1','123','2025-02-03 23:43:00.000000','2025-02-05 23:43:00.000000',13,1,0,1),
	 ('test2','123','2025-02-05 10:47:00.000000','2025-02-08 10:47:00.000000',13,1,0,1),
	 ('test4','123','2025-02-10 11:00:00.000000','2025-02-13 11:00:00.000000',14,1,0,0),
	 ('test5','123','2025-02-12 11:52:00.000000','2025-02-16 11:52:00.000000',10,1,1,1),
	 ('test6','12345','2025-02-14 14:07:00.000000','2025-02-18 14:07:00.000000',16,1,0,1);

-- PollOptions definition

CREATE TABLE PollOptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER NOT NULL,
    option_text VARCHAR(255) NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES Polls(id)
);
INSERT INTO PollOptions (poll_id,option_text) VALUES
	 (1,'a'),
	 (1,'b'),
	 (2,'a'),
	 (2,'b'),
	 (3,'a'),
	 (3,'b'),
	 (4,'a'),
	 (4,'b'),
	 (5,'a'),
	 (5,'b');
INSERT INTO PollOptions (poll_id,option_text) VALUES
	 (6,'a'),
	 (6,'b'),
	 (7,'苹果'),
	 (7,'梨子'),
	 (8,'足球'),
	 (8,'篮球'),
	 (9,'苹果'),
	 (9,'梨子'),
	 (9,'香蕉'),
	 (10,'足球');
INSERT INTO PollOptions (poll_id,option_text) VALUES
	 (10,'篮球'),
	 (10,'羽毛球'),
	 (11,'封神'),
	 (11,'哪吒'),
	 (11,'唐探1900'),
	 (11,'射雕英雄传'),
	 (12,'a'),
	 (12,'b'),
	 (12,'c'),
	 (12,'d');
INSERT INTO PollOptions (poll_id,option_text) VALUES
	 (12,'e'),
	 (12,'f'),
	 (13,'a'),
	 (13,'b'),
	 (13,'c'),
	 (13,'d'),
	 (14,'a'),
	 (14,'b'),
	 (14,'c'),
	 (14,'d');
INSERT INTO PollOptions (poll_id,option_text) VALUES
	 (14,'e'),
	 (14,'f'),
	 (14,'g'),
	 (15,'a'),
	 (15,'b'),
	 (15,'c'),
	 (15,'d'),
	 (16,'a'),
	 (16,'b'),
	 (16,'c');
INSERT INTO PollOptions (poll_id,option_text) VALUES
	 (16,'d'),
	 (16,'e'),
	 (17,'a'),
	 (17,'b'),
	 (17,'c'),
	 (17,'d'),
	 (17,'e'),
	 (17,'f'),
	 (17,'g');

-- Votes definition

CREATE TABLE "Votes" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    poll_id INTEGER NOT NULL,
    option_id INTEGER NOT NULL,
    vote_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (poll_id) REFERENCES Polls(id),
    FOREIGN KEY (option_id) REFERENCES PollOptions(id)
);
INSERT INTO Votes (user_id,poll_id,option_id,vote_time) VALUES
	 (13,8,15,'2025-01-27 08:44:49.127541'),
	 (13,10,20,'2025-01-28 17:13:40.992999'),
	 (5,10,21,'2025-01-28 17:14:15.399658'),
	 (13,12,28,'2025-02-03 08:59:15.627439'),
	 (14,12,28,'2025-02-04 03:01:03.069651'),
	 (5,12,32,'2025-02-04 03:01:25.623500'),
	 (13,13,34,'2025-02-04 15:43:15.361979'),
	 (5,13,34,'2025-02-04 15:43:43.785991'),
	 (13,14,37,'2025-02-06 02:47:38.414160'),
	 (14,15,46,'2025-02-11 03:00:56.537583');
INSERT INTO Votes (user_id,poll_id,option_id,vote_time) VALUES
	 (13,15,45,'2025-02-13 02:37:47.475421'),
	 (12,15,47,'2025-02-13 02:52:23.154279'),
	 (NULL,16,52,'2025-02-13 04:31:01.587128'),
	 (NULL,16,48,'2025-02-15 06:06:33.699626'),
	 (16,17,56,'2025-02-15 06:07:32.120116');
