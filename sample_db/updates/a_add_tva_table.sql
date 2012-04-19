SET character_set_client = utf8;
CREATE TABLE IF NOT EXISTS `coop_tva` (
    `id` int(2) NOT NULL auto_increment,
    `name` varchar(8) NOT NULL,
    `value` int(5),
    PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
LOCK TABLES `coop_tva` WRITE;
/*!40000 ALTER TABLE `coop_tva` DISABLE KEYS */;
INSERT INTO `coop_tva` VALUES (1, 'N.A', '-1'),(2, '0%', '0'), (3,'5.5%','550'),(4,'7%', '700'), (5, '19.6%', '1960');
/*!40000 ALTER TABLE `coop_tva` ENABLE KEYS */;
UNLOCK TABLES;
