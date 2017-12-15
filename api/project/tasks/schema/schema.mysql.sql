CREATE TABLE `tasks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `author_id` int(11) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `status` varchar(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` tinytext NOT NULL,
  `last_update` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_employee_lists` (`employee_id`,`status`,`id`),
  KEY `idx_employer_lists` (`author_id`,`status`,`id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4;
