-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: rpg_database
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ability`
--

DROP TABLE IF EXISTS `ability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ability` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `max_level` int(11) DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `castable` tinyint(1) DEFAULT NULL,
  `_current` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_next` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sanctity_cost` int(11) DEFAULT NULL,
  `endurance_cost` int(11) DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hidden` tinyint(1) DEFAULT NULL,
  `learnable` tinyint(1) DEFAULT NULL,
  `tree` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tree_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ability_hero_id_hero` (`hero_id`),
  CONSTRAINT `fk_ability_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ability`
--

LOCK TABLES `ability` WRITE;
/*!40000 ALTER TABLE `ability` DISABLE KEYS */;
INSERT INTO `ability` VALUES (1,'IgnoreTest4',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest4',0,1,'Basic','None','ability_icon_IgnoreTest4',1),(2,'Strider',0,3,'(BROKEN)Traveling on the map requires less endurance.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Strider',0,1,'Archetype','Survivalist','ability_icon_Strider',1),(3,'Charmer',0,3,'(BROKEN)You are more likely to succeed when choosing charm dialogues.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Charmer',0,1,'Archetype','Opportunist','ability_icon_Charmer',1),(4,'Scholar',0,3,'Gain experience faster.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Scholar',0,1,'Archetype','Philosopher','ability_icon_Scholar',1),(5,'Relentless',0,5,'Gain maximum health. Master this ability to unlock the Brute archetype.',0,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',0,0,'Relentless',0,1,'Basic','None','ability_icon_Relentless',1),(6,'VampiricAura',0,3,'You steal life per hit',0,'Amount stolen: {{ (level) * 1 }}','Amount stolen: {{ (level + 1) * 1 }}',0,0,'VampiricAura',0,1,'Basic','None','ability_icon_VampiricAura',1),(7,'IgnoreTest5',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest5',0,1,'Basic','None','ability_icon_IgnoreTest5',1),(8,'IgnoreTest6',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest6',0,1,'Basic','None','ability_icon_IgnoreTest6',1),(9,'FameBombTest',0,3,'Spend 2 sanctity to gain instant fame with this silly test spell.',1,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',2,0,'FameBombTest',0,1,'Basic','None','ability_icon_FameBombTest',1),(10,'IgnoreTest7',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest7',0,1,'Basic','None','ability_icon_IgnoreTest7',1),(11,'IgnoreTest3',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest3',0,1,'Basic','None','ability_icon_IgnoreTest3',1),(12,'Poet',0,5,'Gain renown faster. Master this ability to unlock the Opportunist archetype.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Poet',0,1,'Basic','None','ability_icon_Poet',1),(13,'Arcanum',0,5,'Gain maximum sanctity. Master this ability to unlock the Philosopher archetype.',0,'{{ (level) * 2 }}','{{ (level + 1) * 2 }}',0,0,'Arcanum',0,1,'Basic','None','ability_icon_Arcanum',1),(14,'IgnoreTest2',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest2',0,1,'Basic','None','ability_icon_IgnoreTest2',1),(15,'Trickster',0,5,'Become harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.',0,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',0,0,'Trickster',0,1,'Basic','None','ability_icon_Trickster',1),(16,'Apprentice',0,3,'You are capable of learning additional spells.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Apprentice',0,1,'Archetype','Ascetic','ability_icon_Apprentice',1),(17,'Vigilance',0,3,'(BROKEN)You are less likely to be ambushed.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Vigilance',0,1,'Archetype','Survivalist','ability_icon_Vigilance',1),(18,'IgnoreTest1',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest1',0,1,'Basic','None','ability_icon_IgnoreTest1',1),(19,'Bash',0,3,'(BROKEN)You deal more damage with blunt weapons.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Bash',0,1,'Archetype','Brute','ability_icon_Bash',1),(20,'Skinner',0,3,'(BROKEN)You have a chance of obtaining a usable fur after kiling a beast.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Skinner',0,1,'Archetype','Survivalist','ability_icon_Skinner',1),(21,'Backstab',0,3,'You are more likely to attack first in combat.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Backstab',0,1,'Archetype','Scoundrel','ability_icon_Backstab',1),(22,'Haggler',0,3,'Prices at shops are cheaper.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Haggler',0,1,'Archetype','Opportunist','ability_icon_Haggler',1),(23,'VirtueBombTest',0,3,'Spend 1 endurance to gain instant virtue with this silly spell for testing purposes.',1,'{{ (level) * 2 }}','{{ (level + 1) * 2 }}',0,1,'VirtueBombTest',0,1,'Basic','None','ability_icon_VirtueBombTest',1),(24,'Traveler',0,5,'Reveal more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Traveler',0,1,'Basic','None','ability_icon_Traveler',1),(25,'Lifeleech',0,3,'You steal life based on how much damage you deal in combat',0,'Percent of damage dealt: {{ (level) * 5 }}','Percent of damage dealt: {{ (level + 1) * 5 }}',0,0,'Lifeleech',0,1,'Basic','None','ability_icon_Lifeleech',1),(26,'Discipline',0,5,'Gain devotion faster. Master this ability to unlock the Ascetic archetype.',0,'{{ (level) * 1 }}%','{{ (level + 1) * 1 }}%',0,0,'Discipline',0,1,'Basic','None','ability_icon_Discipline',1),(27,'Student',0,3,'(BROKEN)You are capable of learning additional spells.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Student',0,1,'Archetype','Philosopher','ability_icon_Student',1),(28,'Blackhearted',0,3,'(BROKEN)Lose virtue faster.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Blackhearted',0,1,'Archetype','Scoundrel','ability_icon_Blackhearted',1),(29,'MartialArts',0,3,'You deal more damage in combat.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'MartialArts',0,1,'Archetype','Ascetic','ability_icon_MartialArts',1),(30,'Meditation',0,3,'Regenerate sanctity per day.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Meditation',0,1,'Archetype','Ascetic','ability_icon_Meditation',1),(31,'IgnoreTest4',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest4',0,1,'Basic','None','ability_icon_IgnoreTest4',2),(32,'Strider',0,3,'(BROKEN)Traveling on the map requires less endurance.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Strider',0,1,'Archetype','Survivalist','ability_icon_Strider',2),(33,'Charmer',0,3,'(BROKEN)You are more likely to succeed when choosing charm dialogues.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Charmer',0,1,'Archetype','Opportunist','ability_icon_Charmer',2),(34,'Scholar',0,3,'Gain experience faster.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Scholar',0,1,'Archetype','Philosopher','ability_icon_Scholar',2),(35,'Relentless',0,5,'Gain maximum health. Master this ability to unlock the Brute archetype.',0,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',0,0,'Relentless',0,1,'Basic','None','ability_icon_Relentless',2),(36,'VampiricAura',0,3,'You steal life per hit',0,'Amount stolen: {{ (level) * 1 }}','Amount stolen: {{ (level + 1) * 1 }}',0,0,'VampiricAura',0,1,'Basic','None','ability_icon_VampiricAura',2),(37,'IgnoreTest5',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest5',0,1,'Basic','None','ability_icon_IgnoreTest5',2),(38,'IgnoreTest6',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest6',0,1,'Basic','None','ability_icon_IgnoreTest6',2),(39,'FameBombTest',0,3,'Spend 2 sanctity to gain instant fame with this silly test spell.',1,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',2,0,'FameBombTest',0,1,'Basic','None','ability_icon_FameBombTest',2),(40,'IgnoreTest7',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest7',0,1,'Basic','None','ability_icon_IgnoreTest7',2),(41,'IgnoreTest3',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest3',0,1,'Basic','None','ability_icon_IgnoreTest3',2),(42,'Poet',0,5,'Gain renown faster. Master this ability to unlock the Opportunist archetype.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Poet',0,1,'Basic','None','ability_icon_Poet',2),(43,'Arcanum',0,5,'Gain maximum sanctity. Master this ability to unlock the Philosopher archetype.',0,'{{ (level) * 2 }}','{{ (level + 1) * 2 }}',0,0,'Arcanum',0,1,'Basic','None','ability_icon_Arcanum',2),(44,'IgnoreTest2',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest2',0,1,'Basic','None','ability_icon_IgnoreTest2',2),(45,'Trickster',0,5,'Become harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.',0,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',0,0,'Trickster',0,1,'Basic','None','ability_icon_Trickster',2),(46,'Apprentice',0,3,'You are capable of learning additional spells.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Apprentice',0,1,'Archetype','Ascetic','ability_icon_Apprentice',2),(47,'Vigilance',0,3,'(BROKEN)You are less likely to be ambushed.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Vigilance',0,1,'Archetype','Survivalist','ability_icon_Vigilance',2),(48,'IgnoreTest1',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest1',0,1,'Basic','None','ability_icon_IgnoreTest1',2),(49,'Bash',0,3,'(BROKEN)You deal more damage with blunt weapons.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Bash',0,1,'Archetype','Brute','ability_icon_Bash',2),(50,'Skinner',0,3,'(BROKEN)You have a chance of obtaining a usable fur after kiling a beast.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Skinner',0,1,'Archetype','Survivalist','ability_icon_Skinner',2),(51,'Backstab',0,3,'You are more likely to attack first in combat.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Backstab',0,1,'Archetype','Scoundrel','ability_icon_Backstab',2),(52,'Haggler',0,3,'Prices at shops are cheaper.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Haggler',0,1,'Archetype','Opportunist','ability_icon_Haggler',2),(53,'VirtueBombTest',0,3,'Spend 1 endurance to gain instant virtue with this silly spell for testing purposes.',1,'{{ (level) * 2 }}','{{ (level + 1) * 2 }}',0,1,'VirtueBombTest',0,1,'Basic','None','ability_icon_VirtueBombTest',2),(54,'Traveler',0,5,'Reveal more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Traveler',0,1,'Basic','None','ability_icon_Traveler',2),(55,'Lifeleech',0,3,'You steal life based on how much damage you deal in combat',0,'Percent of damage dealt: {{ (level) * 5 }}','Percent of damage dealt: {{ (level + 1) * 5 }}',0,0,'Lifeleech',0,1,'Basic','None','ability_icon_Lifeleech',2),(56,'Discipline',0,5,'Gain devotion faster. Master this ability to unlock the Ascetic archetype.',0,'{{ (level) * 1 }}%','{{ (level + 1) * 1 }}%',0,0,'Discipline',0,1,'Basic','None','ability_icon_Discipline',2),(57,'Student',0,3,'(BROKEN)You are capable of learning additional spells.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Student',0,1,'Archetype','Philosopher','ability_icon_Student',2),(58,'Blackhearted',0,3,'(BROKEN)Lose virtue faster.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Blackhearted',0,1,'Archetype','Scoundrel','ability_icon_Blackhearted',2),(59,'MartialArts',0,3,'You deal more damage in combat.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'MartialArts',0,1,'Archetype','Ascetic','ability_icon_MartialArts',2),(60,'Meditation',0,3,'Regenerate sanctity per day.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Meditation',0,1,'Archetype','Ascetic','ability_icon_Meditation',2),(61,'IgnoreTest4',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest4',0,1,'Basic','None','ability_icon_IgnoreTest4',3),(62,'Strider',0,3,'(BROKEN)Traveling on the map requires less endurance.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Strider',0,1,'Archetype','Survivalist','ability_icon_Strider',3),(63,'Charmer',0,3,'(BROKEN)You are more likely to succeed when choosing charm dialogues.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Charmer',0,1,'Archetype','Opportunist','ability_icon_Charmer',3),(64,'Scholar',3,3,'Gain experience faster.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Scholar',0,1,'Archetype','Philosopher','ability_icon_Scholar',3),(65,'Relentless',0,5,'Gain maximum health. Master this ability to unlock the Brute archetype.',0,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',0,0,'Relentless',0,1,'Basic','None','ability_icon_Relentless',3),(66,'VampiricAura',0,3,'You steal life per hit',0,'Amount stolen: {{ (level) * 1 }}','Amount stolen: {{ (level + 1) * 1 }}',0,0,'VampiricAura',0,1,'Basic','None','ability_icon_VampiricAura',3),(67,'IgnoreTest5',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest5',0,1,'Basic','None','ability_icon_IgnoreTest5',3),(68,'IgnoreTest6',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest6',0,1,'Basic','None','ability_icon_IgnoreTest6',3),(69,'FameBombTest',0,3,'Spend 2 sanctity to gain instant fame with this silly test spell.',1,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',2,0,'FameBombTest',0,1,'Basic','None','ability_icon_FameBombTest',3),(70,'IgnoreTest7',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest7',0,1,'Basic','None','ability_icon_IgnoreTest7',3),(71,'IgnoreTest3',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest3',0,1,'Basic','None','ability_icon_IgnoreTest3',3),(72,'Poet',0,5,'Gain renown faster. Master this ability to unlock the Opportunist archetype.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Poet',0,1,'Basic','None','ability_icon_Poet',3),(73,'Arcanum',0,5,'Gain maximum sanctity. Master this ability to unlock the Philosopher archetype.',0,'{{ (level) * 2 }}','{{ (level + 1) * 2 }}',0,0,'Arcanum',0,1,'Basic','None','ability_icon_Arcanum',3),(74,'IgnoreTest2',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest2',0,1,'Basic','None','ability_icon_IgnoreTest2',3),(75,'Trickster',0,5,'Become harder to detect when performing stealthy activities. Master this ability to unlock the Scoundrel archetype.',0,'{{ (level) * 3 }}','{{ (level + 1) * 3 }}',0,0,'Trickster',0,1,'Basic','None','ability_icon_Trickster',3),(76,'Apprentice',0,3,'You are capable of learning additional spells.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Apprentice',0,1,'Archetype','Ascetic','ability_icon_Apprentice',3),(77,'Vigilance',0,3,'(BROKEN)You are less likely to be ambushed.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Vigilance',0,1,'Archetype','Survivalist','ability_icon_Vigilance',3),(78,'IgnoreTest1',0,3,'Irrelevant',1,'Irrelevant','Irrelevant',0,0,'IgnoreTest1',0,1,'Basic','None','ability_icon_IgnoreTest1',3),(79,'Bash',0,3,'(BROKEN)You deal more damage with blunt weapons.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Bash',0,1,'Archetype','Brute','ability_icon_Bash',3),(80,'Skinner',0,3,'(BROKEN)You have a chance of obtaining a usable fur after kiling a beast.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Skinner',0,1,'Archetype','Survivalist','ability_icon_Skinner',3),(81,'Backstab',0,3,'You are more likely to attack first in combat.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Backstab',0,1,'Archetype','Scoundrel','ability_icon_Backstab',3),(82,'Haggler',0,3,'Prices at shops are cheaper.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Haggler',0,1,'Archetype','Opportunist','ability_icon_Haggler',3),(83,'VirtueBombTest',0,3,'Spend 1 endurance to gain instant virtue with this silly spell for testing purposes.',1,'{{ (level) * 2 }}','{{ (level + 1) * 2 }}',0,1,'VirtueBombTest',0,1,'Basic','None','ability_icon_VirtueBombTest',3),(84,'Traveler',0,5,'Reveal more of the map when exploring new places. Master this ability to unlock the Survivalist archetype.',0,'{{ (level) * 1 }}','{{ (level + 1) * 1 }}',0,0,'Traveler',0,1,'Basic','None','ability_icon_Traveler',3),(85,'Lifeleech',0,3,'You steal life based on how much damage you deal in combat',0,'Percent of damage dealt: {{ (level) * 5 }}','Percent of damage dealt: {{ (level + 1) * 5 }}',0,0,'Lifeleech',0,1,'Basic','None','ability_icon_Lifeleech',3),(86,'Discipline',4,5,'Gain devotion faster. Master this ability to unlock the Ascetic archetype.',0,'{{ (level) * 1 }}%','{{ (level + 1) * 1 }}%',0,0,'Discipline',0,1,'Basic','None','ability_icon_Discipline',3),(87,'Student',0,3,'(BROKEN)You are capable of learning additional spells.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Student',0,1,'Archetype','Philosopher','ability_icon_Student',3),(88,'Blackhearted',0,3,'(BROKEN)Lose virtue faster.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Blackhearted',0,1,'Archetype','Scoundrel','ability_icon_Blackhearted',3),(89,'MartialArts',0,3,'You deal more damage in combat.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'MartialArts',0,1,'Archetype','Ascetic','ability_icon_MartialArts',3),(90,'Meditation',0,3,'Regenerate sanctity per day.',0,'{{ (level) * 5 }}','{{ (level + 1) * 5 }}',0,0,'Meditation',0,1,'Archetype','Ascetic','ability_icon_Meditation',3);
/*!40000 ALTER TABLE `ability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `achievement`
--

DROP TABLE IF EXISTS `achievement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `achievement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `achievements_id` int(11) DEFAULT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_level` int(11) DEFAULT NULL,
  `next_level` int(11) DEFAULT NULL,
  `experience` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_achievement_achievements_id_achievements` (`achievements_id`),
  CONSTRAINT `fk_achievement_achievements_id_achievements` FOREIGN KEY (`achievements_id`) REFERENCES `achievements` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievement`
--

LOCK TABLES `achievement` WRITE;
/*!40000 ALTER TABLE `achievement` DISABLE KEYS */;
INSERT INTO `achievement` VALUES (1,1,NULL,'Wolf kills',0,1,50),(2,2,NULL,'Wolf kills',0,1,50),(3,3,NULL,'Wolf kills',0,1,50);
/*!40000 ALTER TABLE `achievement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `achievements`
--

DROP TABLE IF EXISTS `achievements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `achievements` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `journal_id` int(11) DEFAULT NULL,
  `deepest_dungeon_floor` int(11) DEFAULT NULL,
  `current_dungeon_floor` int(11) DEFAULT NULL,
  `current_dungeon_floor_progress` int(11) DEFAULT NULL,
  `player_kills` int(11) DEFAULT NULL,
  `monster_kills` int(11) DEFAULT NULL,
  `deaths` int(11) DEFAULT NULL,
  `wolf_kills` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_achievements_journal_id_journal` (`journal_id`),
  CONSTRAINT `fk_achievements_journal_id_journal` FOREIGN KEY (`journal_id`) REFERENCES `journal` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achievements`
--

LOCK TABLES `achievements` WRITE;
/*!40000 ALTER TABLE `achievements` DISABLE KEYS */;
INSERT INTO `achievements` VALUES (1,1,0,0,0,0,0,0,0),(2,2,0,0,0,0,0,0,0),(3,3,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `achievements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adjacent_location_association`
--

DROP TABLE IF EXISTS `adjacent_location_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adjacent_location_association` (
  `out_adjacent_id` int(11) DEFAULT NULL,
  `in_adjacent_id` int(11) DEFAULT NULL,
  KEY `fk_adjacent_location_association_out_adjacent_id_location` (`out_adjacent_id`),
  KEY `fk_adjacent_location_association_in_adjacent_id_location` (`in_adjacent_id`),
  CONSTRAINT `fk_adjacent_location_association_in_adjacent_id_location` FOREIGN KEY (`in_adjacent_id`) REFERENCES `location` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_adjacent_location_association_out_adjacent_id_location` FOREIGN KEY (`out_adjacent_id`) REFERENCES `location` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjacent_location_association`
--

LOCK TABLES `adjacent_location_association` WRITE;
/*!40000 ALTER TABLE `adjacent_location_association` DISABLE KEYS */;
INSERT INTO `adjacent_location_association` VALUES (9,8),(10,7),(11,7),(11,8),(5,2),(5,6),(6,5),(7,2),(7,3),(7,8),(7,10),(7,11),(2,3),(2,5),(2,7),(3,2),(3,4),(3,7),(8,7),(8,9),(8,11),(4,3);
/*!40000 ALTER TABLE `adjacent_location_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attribute`
--

DROP TABLE IF EXISTS `attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attribute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_attribute_hero_id_hero` (`hero_id`),
  CONSTRAINT `fk_attribute_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute`
--

LOCK TABLES `attribute` WRITE;
/*!40000 ALTER TABLE `attribute` DISABLE KEYS */;
INSERT INTO `attribute` VALUES (1,'Survivalism','Survivalism','A measure of how well you can adapt to your surroundings.',1,1),(2,'Fortuity','Fortuity','A measure of your luck.',1,1),(3,'Divinity','Divinity','A measure of your connection with the spirit world.',1,1),(4,'Pathfinding','Pathfinding','A measure of your ability to traverse the world.',1,1),(5,'Willpower','Willpower','A measure of how disciplined you are.',1,1),(6,'Resilience','Resilience','A measure of how tough you are.',1,1),(7,'Agility','Agility','A measure of how skilfully you can move.',1,1),(8,'Brawn','Brawn','A measure of how strong you are.',1,1),(9,'Charisma','Charisma','A measure of how well you interact with other people',1,1),(10,'Vitality','Vitality','A measure of how healthy you are.',1,1),(11,'Quickness','Quickness','A measure of how fast you can move.',1,1),(12,'Intellect','Intellect','A measure of your mental prowess and knowledge.',1,1),(13,'Survivalism','Survivalism','A measure of how well you can adapt to your surroundings.',1,2),(14,'Fortuity','Fortuity','A measure of your luck.',1,2),(15,'Divinity','Divinity','A measure of your connection with the spirit world.',1,2),(16,'Pathfinding','Pathfinding','A measure of your ability to traverse the world.',1,2),(17,'Willpower','Willpower','A measure of how disciplined you are.',1,2),(18,'Resilience','Resilience','A measure of how tough you are.',1,2),(19,'Agility','Agility','A measure of how skilfully you can move.',1,2),(20,'Brawn','Brawn','A measure of how strong you are.',1,2),(21,'Charisma','Charisma','A measure of how well you interact with other people',1,2),(22,'Vitality','Vitality','A measure of how healthy you are.',1,2),(23,'Quickness','Quickness','A measure of how fast you can move.',1,2),(24,'Intellect','Intellect','A measure of your mental prowess and knowledge.',1,2),(25,'Survivalism','Survivalism','A measure of how well you can adapt to your surroundings.',1,3),(26,'Fortuity','Fortuity','A measure of your luck.',1,3),(27,'Divinity','Divinity','A measure of your connection with the spirit world.',1,3),(28,'Pathfinding','Pathfinding','A measure of your ability to traverse the world.',1,3),(29,'Willpower','Willpower','A measure of how disciplined you are.',2,3),(30,'Resilience','Resilience','A measure of how tough you are.',1,3),(31,'Agility','Agility','A measure of how skilfully you can move.',1,3),(32,'Brawn','Brawn','A measure of how strong you are.',3,3),(33,'Charisma','Charisma','A measure of how well you interact with other people',1,3),(34,'Vitality','Vitality','A measure of how healthy you are.',1,3),(35,'Quickness','Quickness','A measure of how fast you can move.',1,3),(36,'Intellect','Intellect','A measure of your mental prowess and knowledge.',1,3);
/*!40000 ALTER TABLE `attribute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `board` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forum_id` int(11) DEFAULT NULL,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_board_forum_id_forum` (`forum_id`),
  CONSTRAINT `fk_board_forum_id_forum` FOREIGN KEY (`forum_id`) REFERENCES `forum` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board`
--

LOCK TABLES `board` WRITE;
/*!40000 ALTER TABLE `board` DISABLE KEYS */;
INSERT INTO `board` VALUES (1,1,'General');
/*!40000 ALTER TABLE `board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `condition`
--

DROP TABLE IF EXISTS `condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hero_attribute` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comparison` varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `condition_attribute` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `code` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_condition_location_id_location` (`location_id`),
  CONSTRAINT `fk_condition_location_id_location` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condition`
--

LOCK TABLES `condition` WRITE;
/*!40000 ALTER TABLE `condition` DISABLE KEYS */;
INSERT INTO `condition` VALUES (1,'current_location','==','location','hero.current_location.id == self.location.id',14);
/*!40000 ALTER TABLE `condition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `condition_to_trigger`
--

DROP TABLE IF EXISTS `condition_to_trigger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condition_to_trigger` (
  `condition_id` int(11) DEFAULT NULL,
  `trigger_id` int(11) DEFAULT NULL,
  KEY `fk_condition_to_trigger_condition_id_condition` (`condition_id`),
  KEY `fk_condition_to_trigger_trigger_id_trigger` (`trigger_id`),
  CONSTRAINT `fk_condition_to_trigger_condition_id_condition` FOREIGN KEY (`condition_id`) REFERENCES `condition` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_condition_to_trigger_trigger_id_trigger` FOREIGN KEY (`trigger_id`) REFERENCES `trigger` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condition_to_trigger`
--

LOCK TABLES `condition_to_trigger` WRITE;
/*!40000 ALTER TABLE `condition_to_trigger` DISABLE KEYS */;
INSERT INTO `condition_to_trigger` VALUES (1,2),(1,1);
/*!40000 ALTER TABLE `condition_to_trigger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `display`
--

DROP TABLE IF EXISTS `display`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `display` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `page_heading` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `page_image` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `paragraph` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_display_location_id_location` (`location_id`),
  CONSTRAINT `fk_display_location_id_location` FOREIGN KEY (`location_id`) REFERENCES `location` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `display`
--

LOCK TABLES `display` WRITE;
/*!40000 ALTER TABLE `display` DISABLE KEYS */;
INSERT INTO `display` VALUES (1,'Location0','You are in Location0','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',2),(2,'Location1','You are in Location1','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',3),(3,'Shadowy Cave','You are outside Shadowy Cave','generic_cave_entrance.jpg','There are many scary places to die within the cave. Have a look!',4),(4,'Location3','You are in Location3','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',5),(5,'Location4','You are in Location4','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',6),(6,'Blacksmith','You are in Blacksmith','store.jpg','There are many places to visit within the store.jpg. Have a look!',14),(7,'Sparring Room','You are in Spar','spar.jpg','There are many places to visit within the spar.jpg. Have a look!',20),(8,'Arena','You are in Arena','arena.jpg','There are many places to visit within the arena.jpg. Have a look!',21),(9,'Barracks','You are in Barracks','barracks.jpg','There are many places to visit within the barracks.jpg. Have a look!',15),(10,'Marketplace','You are in Marketplace','store.jpg','There are many places to visit within the store.jpg. Have a look!',16),(11,'Red Dragon Inn','You are in Red Dragon Inn','tavern.jpg','There are many places to visit within the tavern.jpg. Have a look!',17),(12,'Village Gate','You are in Village Gate','gate.jpg','There are many places to visit within the gate.jpg. Have a look!',18),(13,'Thornwall','You are in Thornwall','town.jpg','There are many places to visit within the town. Have a look!',7),(14,'Location6','You are in Location6','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',8),(15,'Old Man\'s Hut','Old Man\'s Hut','hut.jpg','Nice to see you again kid. What do you need?',9),(16,'Exploring','You are in Explore Dungeon','explore_dungeon.jpg','There are many places to visit within the explore_dungeon.jpg. Have a look!',22),(17,'Dungeon Entrance','You are in Dungeon Entrance','generic_cave_entrance2.jpg','There are many places to visit within the dungeon_entrance.jpg. Have a look!',19),(18,'Dark Forest','You are outside Dark Forest','generic_forest_entrance.jpg','There are many scary places to die within the forest. Have a look!',10),(19,'Location9','You are in Location9','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',11),(20,'Location10','You are in Location10','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',12),(21,'Location11','You are in Location11','explorable.jpg','There are many places to visit within the explorable.jpg. Have a look!',13),(22,'Htrae','You are wandering in the world','htrae.jpg','Be safe',1);
/*!40000 ALTER TABLE `display` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entry`
--

DROP TABLE IF EXISTS `entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `position` int(11) DEFAULT NULL,
  `info` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `journal_id` int(11) DEFAULT NULL,
  `_beast` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_person` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_place` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `_quest_path_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_entry_journal_id_journal` (`journal_id`),
  KEY `fk_entry__quest_path_id_quest_path` (`_quest_path_id`),
  CONSTRAINT `fk_entry__quest_path_id_quest_path` FOREIGN KEY (`_quest_path_id`) REFERENCES `quest_path` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_entry_journal_id_journal` FOREIGN KEY (`journal_id`) REFERENCES `journal` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry`
--

LOCK TABLES `entry` WRITE;
/*!40000 ALTER TABLE `entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `when` datetime DEFAULT NULL,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum`
--

DROP TABLE IF EXISTS `forum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum`
--

LOCK TABLES `forum` WRITE;
/*!40000 ALTER TABLE `forum` DISABLE KEYS */;
INSERT INTO `forum` VALUES (1,'Basic');
/*!40000 ALTER TABLE `forum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `handler`
--

DROP TABLE IF EXISTS `handler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `handler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `_master` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trigger_id` int(11) DEFAULT NULL,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_handler_trigger_id_trigger` (`trigger_id`),
  KEY `fk_handler_hero_id_hero` (`hero_id`),
  CONSTRAINT `fk_handler_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_handler_trigger_id_trigger` FOREIGN KEY (`trigger_id`) REFERENCES `trigger` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `handler`
--

LOCK TABLES `handler` WRITE;
/*!40000 ALTER TABLE `handler` DISABLE KEYS */;
/*!40000 ALTER TABLE `handler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hero`
--

DROP TABLE IF EXISTS `hero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_phase` tinyint(1) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `background` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `house` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `experience` int(11) DEFAULT NULL,
  `experience_maximum` int(11) DEFAULT NULL,
  `gold` int(11) DEFAULT NULL,
  `basic_ability_points` int(11) DEFAULT NULL,
  `archetype_ability_points` int(11) DEFAULT NULL,
  `calling_ability_points` int(11) DEFAULT NULL,
  `pantheon_ability_points` int(11) DEFAULT NULL,
  `attribute_points` int(11) DEFAULT NULL,
  `proficiency_points` int(11) DEFAULT NULL,
  `current_terrain` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `random_encounter_monster` tinyint(1) DEFAULT NULL,
  `spellbook_page` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `last_login` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `login_alerts` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `map_id` int(11) DEFAULT NULL,
  `current_location_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `last_city_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_hero_user_id_user` (`user_id`),
  KEY `fk_hero_map_id_location` (`map_id`),
  KEY `fk_hero_current_location_id_location` (`current_location_id`),
  KEY `fk_hero_city_id_location` (`city_id`),
  KEY `fk_hero_last_city_id_location` (`last_city_id`),
  CONSTRAINT `fk_hero_city_id_location` FOREIGN KEY (`city_id`) REFERENCES `location` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_hero_current_location_id_location` FOREIGN KEY (`current_location_id`) REFERENCES `location` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_hero_last_city_id_location` FOREIGN KEY (`last_city_id`) REFERENCES `location` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_hero_map_id_location` FOREIGN KEY (`map_id`) REFERENCES `location` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_hero_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hero`
--

LOCK TABLES `hero` WRITE;
/*!40000 ALTER TABLE `hero` DISABLE KEYS */;
INSERT INTO `hero` VALUES (1,NULL,'Haldon','',8,NULL,2,15,5000,6,1,0,0,1,1,'city',NULL,1,'2018-03-06 00:28:55','2018-04-09','',1,1,7,7,7),(2,NULL,'Admin','',7,NULL,3,10,5000,5,0,0,0,0,0,'city',NULL,1,'2018-03-22 04:27:36','2018-03-22','',2,1,7,7,7),(3,NULL,'Tntdj360','Barbarian',9,NULL,15,20,47,0,2,0,0,0,0,'none',0,1,'2018-03-06 01:13:04','2018-03-06','',3,1,21,7,7);
/*!40000 ALTER TABLE `hero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inbox`
--

DROP TABLE IF EXISTS `inbox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inbox` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_inbox_user_id_user` (`user_id`),
  CONSTRAINT `fk_inbox_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inbox`
--

LOCK TABLES `inbox` WRITE;
/*!40000 ALTER TABLE `inbox` DISABLE KEYS */;
INSERT INTO `inbox` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `inbox` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_inventory_hero_id_hero` (`hero_id`),
  CONSTRAINT `fk_inventory_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template` tinyint(1) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `buy_price` int(11) DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broken` tinyint(1) DEFAULT NULL,
  `consumable` tinyint(1) DEFAULT NULL,
  `consumed` tinyint(1) DEFAULT NULL,
  `item_rating` int(11) DEFAULT NULL,
  `garment` tinyint(1) DEFAULT NULL,
  `weapon` tinyint(1) DEFAULT NULL,
  `jewelry` tinyint(1) DEFAULT NULL,
  `max_durability` int(11) DEFAULT NULL,
  `wearable` tinyint(1) DEFAULT NULL,
  `affinity` int(11) DEFAULT NULL,
  `inventory_id` int(11) DEFAULT NULL,
  `equipped` tinyint(1) DEFAULT NULL,
  `ring_position` int(11) DEFAULT NULL,
  `unequipped_position` int(11) DEFAULT NULL,
  `style` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `one_handed_weapon` tinyint(1) DEFAULT NULL,
  `shield` tinyint(1) DEFAULT NULL,
  `two_handed_weapon` tinyint(1) DEFAULT NULL,
  `head_armour` tinyint(1) DEFAULT NULL,
  `shoulder_armour` tinyint(1) DEFAULT NULL,
  `chest_armour` tinyint(1) DEFAULT NULL,
  `leg_armour` tinyint(1) DEFAULT NULL,
  `foot_armour` tinyint(1) DEFAULT NULL,
  `arm_armour` tinyint(1) DEFAULT NULL,
  `hand_armour` tinyint(1) DEFAULT NULL,
  `ring` tinyint(1) DEFAULT NULL,
  `healing_amount` int(11) DEFAULT NULL,
  `sanctity_amount` int(11) DEFAULT NULL,
  `quest_item` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_item_inventory_id_inventory` (`inventory_id`),
  CONSTRAINT `fk_item_inventory_id_inventory` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,1,'Cloth Tunic',NULL,18,'ChestArmour','A simple cloth tunic.',0,NULL,NULL,10,1,0,0,3,1,0,NULL,NULL,NULL,NULL,'leather',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,1,'Gnarled Staff',NULL,13,'TwoHandedWeapon','An old, simple walking stick.',0,NULL,NULL,10,0,1,0,3,1,0,NULL,NULL,NULL,NULL,'leather',0,0,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,1,'Small Shield',NULL,25,'Shield','A simple wooden shield.',0,NULL,NULL,10,0,1,0,3,1,0,NULL,NULL,NULL,NULL,'leather',1,1,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,1,'Rusted Dagger',NULL,23,'OneHandedWeapon','A rusted dagger in poor condition.',0,NULL,NULL,10,0,1,0,3,1,0,NULL,NULL,NULL,NULL,'leather',1,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,1,'Silver Ring',NULL,35,'Ring','A silver ring with no markings. Nothing seems special about it.',0,NULL,NULL,10,0,0,1,3,1,0,NULL,NULL,NULL,NULL,'silver',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL),(6,1,'Minor Health Potion',NULL,3,'Consumable','A small item.',NULL,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL),(7,1,'Major Health Potion',NULL,6,'Consumable','A small item.',NULL,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL),(8,1,'Major Faith Potion',NULL,6,'Consumable','A small item.',NULL,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL),(9,1,'Major Awesome Max Potion',NULL,6000,'Consumable','A small item.',NULL,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL),(10,0,'Major Faith Potion',NULL,6,'Consumable','A small item.',NULL,1,0,NULL,NULL,NULL,NULL,NULL,NULL,0,3,0,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,50,NULL);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journal`
--

DROP TABLE IF EXISTS `journal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `journal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_journal_hero_id_hero` (`hero_id`),
  CONSTRAINT `fk_journal_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal`
--

LOCK TABLES `journal` WRITE;
/*!40000 ALTER TABLE `journal` DISABLE KEYS */;
INSERT INTO `journal` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `journal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `terrain` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_location_name` (`name`),
  KEY `fk_location_parent_id_location` (`parent_id`),
  CONSTRAINT `fk_location_parent_id_location` FOREIGN KEY (`parent_id`) REFERENCES `location` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (1,NULL,'Htrae','/map/Htrae','map','none'),(2,1,'Location0','/explorable/Location0','explorable','none'),(3,1,'Location1','/explorable/Location1','explorable','none'),(4,1,'Shadowy Cave','/dungeon/Shadowy%20Cave','dungeon','cave'),(5,1,'Location3','/explorable/Location3','explorable','none'),(6,1,'Location4','/explorable/Location4','explorable','none'),(7,1,'Thornwall','/town/Thornwall','town','city'),(8,1,'Location6','/explorable/Location6','explorable','none'),(9,1,'Old Man\'s Hut','/building/Old%20Man\'s%20Hut','building','none'),(10,1,'Dark Forest','/dungeon/Dark%20Forest','dungeon','forest'),(11,1,'Location9','/explorable/Location9','explorable','none'),(12,1,'Location10','/explorable/Location10','explorable','none'),(13,1,'Location11','/explorable/Location11','explorable','none'),(14,7,'Blacksmith','/store/Blacksmith','store','none'),(15,7,'Barracks','/barracks/Barracks','barracks','none'),(16,7,'Marketplace','/store/Marketplace','store','none'),(17,7,'Red Dragon Inn','/tavern/Red%20Dragon%20Inn','tavern','none'),(18,7,'Village Gate','/gate/Village%20Gate','gate','none'),(19,10,'Dungeon Entrance','/dungeon_entrance/Dungeon%20Entrance','dungeon_entrance','none'),(20,15,'Spar','/spar/Spar','spar','none'),(21,15,'Arena','/arena/Arena','arena','none'),(22,19,'Explore Dungeon','/explore_dungeon/Explore%20Dungeon/False','explore_dungeon','none');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unread` tinyint(1) DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `timestamp` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_message_sender_id_inbox` (`sender_id`),
  KEY `fk_message_receiver_id_inbox` (`receiver_id`),
  CONSTRAINT `fk_message_receiver_id_inbox` FOREIGN KEY (`receiver_id`) REFERENCES `inbox` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_message_sender_id_inbox` FOREIGN KEY (`sender_id`) REFERENCES `inbox` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monster_template`
--

DROP TABLE IF EXISTS `monster_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monster_template` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `species` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `species_plural` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `level_min` int(11) DEFAULT NULL,
  `level_max` int(11) DEFAULT NULL,
  `experience_rewarded` int(11) DEFAULT NULL,
  `city` tinyint(1) DEFAULT NULL,
  `forest` tinyint(1) DEFAULT NULL,
  `cave` tinyint(1) DEFAULT NULL,
  `level_modifier` int(11) DEFAULT NULL,
  `agility` int(11) DEFAULT NULL,
  `charisma` int(11) DEFAULT NULL,
  `divinity` int(11) DEFAULT NULL,
  `resilience` int(11) DEFAULT NULL,
  `fortuity` int(11) DEFAULT NULL,
  `pathfinding` int(11) DEFAULT NULL,
  `quickness` int(11) DEFAULT NULL,
  `willpower` int(11) DEFAULT NULL,
  `brawn` int(11) DEFAULT NULL,
  `survivalism` int(11) DEFAULT NULL,
  `vitality` int(11) DEFAULT NULL,
  `intellect` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monster_template`
--

LOCK TABLES `monster_template` WRITE;
/*!40000 ALTER TABLE `monster_template` DISABLE KEYS */;
INSERT INTO `monster_template` VALUES (1,'Sewer Rat','Rat','Rats',1,10,1,1,0,1,1,2,0,0,1,1,1,2,1,1,1,1,0),(2,'Rabid Dog','Dog','Dogs',1,20,2,0,1,0,1,2,0,0,2,1,1,2,1,2,1,1,0);
/*!40000 ALTER TABLE `monster_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_post_thread_id_thread` (`thread_id`),
  KEY `fk_post_user_id_user` (`user_id`),
  CONSTRAINT `fk_post_thread_id_thread` FOREIGN KEY (`thread_id`) REFERENCES `thread` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_post_user_id_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,1,3,'nevermind i just died to a dog\r\n','2018-03-06 01:03:39');
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proficiency`
--

DROP TABLE IF EXISTS `proficiency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proficiency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template` tinyint(1) DEFAULT NULL,
  `hero_id` int(11) DEFAULT NULL,
  `ability_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `base` int(11) DEFAULT NULL,
  `modifier` float DEFAULT NULL,
  `type_` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `attribute_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reason_for_zero` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current` int(11) DEFAULT NULL,
  `hidden` tinyint(1) DEFAULT NULL,
  `error` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_proficiency_hero_id_hero` (`hero_id`),
  KEY `fk_proficiency_ability_id_ability` (`ability_id`),
  KEY `fk_proficiency_item_id_item` (`item_id`),
  CONSTRAINT `fk_proficiency_ability_id_ability` FOREIGN KEY (`ability_id`) REFERENCES `ability` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_proficiency_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_proficiency_item_id_item` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proficiency`
--

LOCK TABLES `proficiency` WRITE;
/*!40000 ALTER TABLE `proficiency` DISABLE KEYS */;
INSERT INTO `proficiency` VALUES (1,1,NULL,NULL,1,0,5,0,'Defence','Resilience','Your ability to take physical damage. This combines with your armour to reduce all physical damaged received.',NULL,5,NULL,'You do not have enough Resilience'),(2,1,NULL,NULL,2,0,15,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,15,NULL,'You do not have enough Brawn'),(3,1,NULL,NULL,2,0,1,10,'Combat','Brawn','Your proficiency in fighting. The greater combat proficiency you have then the more damage you do on each attack.',NULL,1,NULL,'You do not have enough Brawn'),(4,1,NULL,NULL,3,0,25,0,'Block','Resilience','Skill with a shield. If a shield is equipped then the amount of damage blocked is increased.',NULL,25,NULL,'You do not have enough Resilience'),(5,1,NULL,NULL,3,0,15,0,'BlockAmount','None','Amount of damage absorbed when a shield successfully blocks',NULL,15,NULL,'You do not have enough None'),(6,1,NULL,NULL,4,0,5,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,5,NULL,'You do not have enough Brawn'),(7,1,NULL,NULL,4,0,1,0,'Speed','Quickness','How quickly you can attack in combat.',NULL,1,NULL,'You do not have enough Quickness'),(8,1,NULL,NULL,5,0,1,0,'Luck','Fortuity','A bonus chance of having incredibly good luck.',NULL,1,NULL,'You do not have enough Fortuity'),(9,1,NULL,NULL,6,0,10,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,10,NULL,'You do not have enough Vitality'),(10,1,NULL,NULL,7,0,50,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,50,NULL,'You do not have enough Vitality'),(11,1,NULL,NULL,8,0,50,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,50,NULL,'You do not have enough Divinity'),(12,1,NULL,NULL,9,0,50,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,50,NULL,'You do not have enough Divinity'),(13,0,NULL,1,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(14,0,NULL,1,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(15,0,NULL,2,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(16,0,NULL,2,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(17,0,NULL,3,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(18,0,NULL,3,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(19,0,NULL,4,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(20,0,NULL,5,NULL,0,3,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,3,NULL,'You do not have enough Vitality'),(21,0,NULL,5,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(22,0,NULL,6,NULL,0,1,0,'LifestealStatic','None','Amount of life stolen per hit',NULL,1,NULL,'You do not have enough None'),(23,0,NULL,6,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(24,0,NULL,7,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(25,0,NULL,7,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(26,0,NULL,8,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(27,0,NULL,8,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(28,0,NULL,9,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(29,0,NULL,9,NULL,0,0,0,'Renown','None','How famous you are',NULL,0,NULL,'You do not have enough None'),(30,0,NULL,10,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(31,0,NULL,10,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(32,0,NULL,11,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(33,0,NULL,11,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(34,0,NULL,12,NULL,0,1,0,'Reputation','Charisma','The magnitutde of which your actions affect your renown.',NULL,1,NULL,'You do not have enough Charisma'),(35,0,NULL,12,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(36,0,NULL,13,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(37,0,NULL,13,NULL,0,2,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,2,NULL,'You do not have enough Divinity'),(38,0,NULL,14,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(39,0,NULL,14,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(40,0,NULL,15,NULL,0,3,0,'Stealth','Agility','Chance to avoid detection when attempting to stay concealed.',NULL,3,NULL,'You do not have enough Agility'),(41,0,NULL,15,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(42,0,NULL,16,NULL,0,1,0,'SpellLimit','None','How many spells you may know.',NULL,1,NULL,'You do not have enough None'),(43,0,NULL,16,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(44,0,NULL,17,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(45,0,NULL,17,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(46,0,NULL,18,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(47,0,NULL,18,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(48,0,NULL,19,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(49,0,NULL,19,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(50,0,NULL,20,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(51,0,NULL,20,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(52,0,NULL,21,NULL,0,5,0,'FirstStrike','Quickness','Increases the likelihood that you will attack first in combat.',NULL,5,NULL,'You do not have enough Quickness'),(53,0,NULL,21,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(54,0,NULL,22,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(55,0,NULL,22,NULL,0,5,0,'Bartering','Charisma','Your skill at negotiating prices. It reduces the price you pay when buying any item from a vendor.',NULL,5,NULL,'You do not have enough Charisma'),(56,0,NULL,23,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(57,0,NULL,23,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(58,0,NULL,24,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(59,0,NULL,24,NULL,0,1,0,'Vision','None','How much of the map is revealed.',NULL,1,NULL,'You do not have enough None'),(60,0,NULL,25,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(61,0,NULL,25,NULL,0,5,0,'LifestealPercent','None','Amount of life stolen per hit as percent of damage dealt',NULL,5,NULL,'You do not have enough None'),(62,0,NULL,26,NULL,0,1,0,'Piety','None','How quickly you are able to gain the devotion of a god.',NULL,1,NULL,'You do not have enough None'),(63,0,NULL,26,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(64,0,NULL,27,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(65,0,NULL,27,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(66,0,NULL,28,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(67,0,NULL,28,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(68,0,NULL,29,NULL,0,5,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,5,NULL,'You do not have enough Brawn'),(69,0,NULL,29,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(70,0,NULL,30,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(71,0,NULL,30,NULL,0,5,0,'Redemption','Divinity','For each two levels of redemption you recover one sanctity each day.',NULL,5,NULL,'You do not have enough Divinity'),(72,0,1,NULL,NULL,0,0,0,'Adventuring','Fortuity','Your skill at exploring new places. This increases your likelihood of finding items when exploring',NULL,0,NULL,'You do not have enough Fortuity'),(73,0,1,NULL,NULL,0,0,0,'Parry','Quickness','The likelihood that you can parry an incoming attack.',NULL,0,NULL,'You do not have enough Quickness'),(74,0,1,NULL,NULL,0,0,0,'Reputation','Charisma','The magnitutde of which your actions affect your renown.',NULL,0,NULL,'You do not have enough Charisma'),(75,0,1,NULL,NULL,0,0,0,'ResistFlame','Resilience','Ability to resist flame damage',NULL,0,NULL,'You do not have enough Resilience'),(76,0,1,NULL,NULL,0,1,0,'Stamina','Resilience','For each four levels of stamina you recover one additional endurance each day.',NULL,1,NULL,'You do not have enough Resilience'),(77,0,1,NULL,NULL,0,1,0,'Woodsman','Pathfinding','Modifier for forest movement.',NULL,1,NULL,'You do not have enough Pathfinding'),(78,0,1,NULL,NULL,0,0,0,'Block','Resilience','Skill with a shield. If a shield is equipped then the amount of damage blocked is increased.',NULL,0,NULL,'You do not have enough Resilience'),(79,0,1,NULL,NULL,0,0,0,'ResistShadow','Resilience','Ability to resist shadow damage',NULL,0,NULL,'You do not have enough Resilience'),(80,0,1,NULL,NULL,0,0,0,'Redemption','Divinity','For each two levels of redemption you recover one sanctity each day.',NULL,0,NULL,'You do not have enough Divinity'),(81,0,1,NULL,NULL,0,0,0,'Courage','Willpower','How capable you are of overcoming your fears. The greater your courage then the greater the obstacles you will be capable of facing.',NULL,0,NULL,'You do not have enough Willpower'),(82,0,1,NULL,NULL,0,10,0,'Storage','Brawn','The amount of weight that you can carry.',NULL,10,NULL,'You do not have enough Brawn'),(83,0,1,NULL,NULL,0,0,0,'Logistics','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(84,0,1,NULL,NULL,0,0,0,'Faith','Divinity','Adds a bonus to how effective your spells are.',NULL,0,NULL,'You do not have enough Divinity'),(85,0,1,NULL,NULL,0,5,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,5,NULL,'You do not have enough Vitality'),(86,0,1,NULL,NULL,0,0,0,'Blunt','None','Skill with blunt weapons',NULL,0,NULL,'You do not have enough None'),(87,0,1,NULL,NULL,0,0,0,'ResistBlunt','Resilience','Ability to resist blunt damage',NULL,0,NULL,'You do not have enough Resilience'),(88,0,1,NULL,NULL,0,0,0,'Trustworthiness','Charisma','UNUSED',NULL,0,NULL,'You do not have enough Charisma'),(89,0,1,NULL,NULL,0,0,0,'Piety','None','How quickly you are able to gain the devotion of a god.',NULL,0,NULL,'You do not have enough None'),(90,0,1,NULL,NULL,0,0,0,'Riposte','Agility','UNUSED',NULL,0,NULL,'You do not have enough Agility'),(91,0,1,NULL,NULL,0,0,0,'Charm','Charisma','How likeable you are. It increases the speed of how quickly people begin to trust you.',NULL,0,NULL,'You do not have enough Charisma'),(92,0,1,NULL,NULL,0,0,0,'Recovery','Vitality','How quickly you recover from poisons and the negative effects of different ailments.',NULL,0,NULL,'You do not have enough Vitality'),(93,0,1,NULL,NULL,0,0,0,'Bartering','Charisma','Your skill at negotiating prices. It reduces the price you pay when buying any item from a vendor.',NULL,0,NULL,'You do not have enough Charisma'),(94,0,1,NULL,NULL,0,0,0,'FirstStrike','Quickness','Increases the likelihood that you will attack first in combat.',NULL,0,NULL,'You do not have enough Quickness'),(95,0,1,NULL,NULL,0,0,0,'LifestealPercent','None','Amount of life stolen per hit as percent of damage dealt',NULL,0,NULL,'You do not have enough None'),(96,0,1,NULL,NULL,0,0,0,'Stealth','Agility','Chance to avoid detection when attempting to stay concealed.',NULL,0,NULL,'You do not have enough Agility'),(97,0,1,NULL,NULL,0,0,0,'ResistFrost','Resilience','Ability to resist frost damage',NULL,0,NULL,'You do not have enough Resilience'),(98,0,1,NULL,NULL,0,1,0,'Speed','Quickness','How quickly you can attack in combat.',NULL,1,NULL,'You do not have enough Quickness'),(99,0,1,NULL,NULL,0,0,0,'Explorer','Survivalism','Reveals additional optional tasks which can be performed while exploring.',NULL,0,NULL,'You do not have enough Survivalism'),(100,0,1,NULL,NULL,0,0,0,'BlockAmount','None','Amount of damage absorbed when a shield successfully blocks',NULL,0,NULL,'You do not have enough None'),(101,0,1,NULL,NULL,0,0,0,'Dualism','None','How quickly you are able to change your virtue.',NULL,0,NULL,'You do not have enough None'),(102,0,1,NULL,NULL,0,0,0,'CautionLevel','None','How much detail is revealed of a location before you visit it.',NULL,0,NULL,'You do not have enough None'),(103,0,1,NULL,NULL,0,0,0,'Slashing','None','Skill with slashing weapons',NULL,0,NULL,'You do not have enough None'),(104,0,1,NULL,NULL,0,0,0,'Fatigue','Resilience','Reduces the speed at which you become exhausted in combat.',NULL,0,NULL,'You do not have enough Resilience'),(105,0,1,NULL,NULL,0,5,0,'Endurance','Resilience','Number of actions you can perform each day.',NULL,5,NULL,'You do not have enough Resilience'),(106,0,1,NULL,NULL,0,0,0,'Renown','None','How famous you are',NULL,0,NULL,'You do not have enough None'),(107,0,1,NULL,NULL,0,0,0,'Precision','Agility','Chance to critically hit enemies. A critical hit always hits for maximum damage and then applies your killshot multiplier to that value.',NULL,0,NULL,'You do not have enough Agility'),(108,0,1,NULL,NULL,0,0,0,'ResistHoly','Divinity','Ability to resist holy damage',NULL,0,NULL,'You do not have enough Divinity'),(109,0,1,NULL,NULL,0,0,0,'Survivalist','Survivalism','UNUSED',NULL,0,NULL,'You do not have enough Survivalism'),(110,0,1,NULL,NULL,0,0,0,'ResistPiercing','Resilience','Ability to resist piercing damage',NULL,0,NULL,'You do not have enough Resilience'),(111,0,1,NULL,NULL,0,0,0,'Accuracy','Agility','How accurately you attack. This gives a bonus chance to successfully striking your opponent in combat.',NULL,0,NULL,'You do not have enough Agility'),(112,0,1,NULL,NULL,0,0,0,'Encumbrance','Brawn','Your ability to fight in combat while carrying cumbersome gear.',NULL,0,NULL,'You do not have enough Brawn'),(113,0,1,NULL,NULL,0,0,0,'Mountaineering','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(114,0,1,NULL,NULL,0,0,0,'Huntsman','Survivalism','The amount of information that you can learn from defeated enemies.',NULL,0,NULL,'You do not have enough Survivalism'),(115,0,1,NULL,NULL,0,1,0,'Regeneration','Vitality','For each two levels of regeneration you recover one additional health each day.',NULL,1,NULL,'You do not have enough Vitality'),(116,0,1,NULL,NULL,0,0,0,'Evade','Quickness','Your ability to dodge enemy attacks. Gives a bonus chance for enemies to miss their close combat attacks.',NULL,0,NULL,'You do not have enough Quickness'),(117,0,1,NULL,NULL,0,0,0,'Literacy','Intellect','UNUSED',NULL,0,NULL,'You do not have enough Intellect'),(118,0,1,NULL,NULL,0,1,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,1,NULL,'You do not have enough Brawn'),(119,0,1,NULL,NULL,0,0,0,'Oration','Charisma','UNUSED',NULL,0,NULL,'You do not have enough Charisma'),(120,0,1,NULL,NULL,0,0,0,'LifestealStatic','None','Amount of life stolen per hit',NULL,0,NULL,'You do not have enough None'),(121,0,1,NULL,NULL,0,0,0,'Devotion','None','How religious you are',NULL,0,NULL,'You do not have enough None'),(122,0,1,NULL,NULL,0,1,0,'Combat','Brawn','Your proficiency in fighting. The greater combat proficiency you have then the more damage you do on each attack.',NULL,1,NULL,'You do not have enough Brawn'),(123,0,1,NULL,NULL,0,0,0,'ResistSlashing','Resilience','Ability to resist slashing damage',NULL,0,NULL,'You do not have enough Resilience'),(124,0,1,NULL,NULL,0,0,0,'Sanity','Willpower','Your ability to resist mind altering affects.',NULL,0,NULL,'You do not have enough Willpower'),(125,0,1,NULL,NULL,0,0,0,'Vision','None','How much of the map is revealed.',NULL,0,NULL,'You do not have enough None'),(126,0,1,NULL,NULL,0,0,0,'Detection','Survivalism','Determines the chance that you will uncover enemy traps and ambushes.',NULL,0,NULL,'You do not have enough Survivalism'),(127,0,1,NULL,NULL,0,0,0,'Piercing','None','Skill with piercing weapons',NULL,0,NULL,'You do not have enough None'),(128,0,1,NULL,NULL,0,0,0,'Knowledge','Intellect','UNUSED',NULL,0,NULL,'You do not have enough Intellect'),(129,0,1,NULL,NULL,0,0,0,'Defence','Resilience','Your ability to take physical damage. This combines with your armour to reduce all physical damaged received.',NULL,0,NULL,'You do not have enough Resilience'),(130,0,1,NULL,NULL,0,0,0,'Navigator','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(131,0,1,NULL,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(132,0,1,NULL,NULL,0,0,0,'Pickpocketing','Agility','Increases the chance that you will successfully pickpocket someone.',NULL,0,NULL,'You do not have enough Agility'),(133,0,1,NULL,NULL,0,0,0,'Luck','Fortuity','A bonus chance of having incredibly good luck.',NULL,0,NULL,'You do not have enough Fortuity'),(134,0,1,NULL,NULL,0,0,0,'WeaponAffinity','None','How accustomed to your current weapon you are',NULL,0,NULL,'You do not have enough None'),(135,0,1,NULL,NULL,0,0,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,0,NULL,'You do not have enough Divinity'),(136,0,1,NULL,NULL,0,0,0,'SpellLimit','None','How many spells you may know.',NULL,0,NULL,'You do not have enough None'),(137,0,1,NULL,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(138,0,1,NULL,NULL,0,0,0,'Flee','Quickness','Increases the chance that you can successful escape from a battle.',NULL,0,NULL,'You do not have enough Quickness'),(139,0,1,NULL,NULL,0,1,0,'Killshot','Agility','Damage multiplier added when performing a critical hit.',NULL,1,NULL,'You do not have enough Agility'),(140,0,1,NULL,NULL,0,0,0,'ClimbingAbility','None','The higher your climbing skill then the more difficult mountains you may climb.',NULL,0,NULL,'You do not have enough None'),(141,0,1,NULL,NULL,0,0,0,'ResistPoison','Resilience','Ability to resist poison damage',NULL,0,NULL,'You do not have enough Resilience'),(142,0,NULL,31,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(143,0,NULL,31,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(144,0,NULL,32,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(145,0,NULL,32,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(146,0,NULL,33,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(147,0,NULL,33,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(148,0,NULL,34,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(149,0,NULL,35,NULL,0,3,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,3,NULL,'You do not have enough Vitality'),(150,0,NULL,35,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(151,0,NULL,36,NULL,0,1,0,'LifestealStatic','None','Amount of life stolen per hit',NULL,1,NULL,'You do not have enough None'),(152,0,NULL,36,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(153,0,NULL,37,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(154,0,NULL,37,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(155,0,NULL,38,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(156,0,NULL,38,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(157,0,NULL,39,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(158,0,NULL,39,NULL,0,0,0,'Renown','None','How famous you are',NULL,0,NULL,'You do not have enough None'),(159,0,NULL,40,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(160,0,NULL,40,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(161,0,NULL,41,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(162,0,NULL,41,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(163,0,NULL,42,NULL,0,1,0,'Reputation','Charisma','The magnitutde of which your actions affect your renown.',NULL,1,NULL,'You do not have enough Charisma'),(164,0,NULL,42,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(165,0,NULL,43,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(166,0,NULL,43,NULL,0,2,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,2,NULL,'You do not have enough Divinity'),(167,0,NULL,44,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(168,0,NULL,44,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(169,0,NULL,45,NULL,0,3,0,'Stealth','Agility','Chance to avoid detection when attempting to stay concealed.',NULL,3,NULL,'You do not have enough Agility'),(170,0,NULL,45,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(171,0,NULL,46,NULL,0,1,0,'SpellLimit','None','How many spells you may know.',NULL,1,NULL,'You do not have enough None'),(172,0,NULL,46,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(173,0,NULL,47,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(174,0,NULL,47,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(175,0,NULL,48,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(176,0,NULL,48,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(177,0,NULL,49,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(178,0,NULL,49,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(179,0,NULL,50,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(180,0,NULL,50,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(181,0,NULL,51,NULL,0,5,0,'FirstStrike','Quickness','Increases the likelihood that you will attack first in combat.',NULL,5,NULL,'You do not have enough Quickness'),(182,0,NULL,51,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(183,0,NULL,52,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(184,0,NULL,52,NULL,0,5,0,'Bartering','Charisma','Your skill at negotiating prices. It reduces the price you pay when buying any item from a vendor.',NULL,5,NULL,'You do not have enough Charisma'),(185,0,NULL,53,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(186,0,NULL,53,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(187,0,NULL,54,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(188,0,NULL,54,NULL,0,1,0,'Vision','None','How much of the map is revealed.',NULL,1,NULL,'You do not have enough None'),(189,0,NULL,55,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(190,0,NULL,55,NULL,0,5,0,'LifestealPercent','None','Amount of life stolen per hit as percent of damage dealt',NULL,5,NULL,'You do not have enough None'),(191,0,NULL,56,NULL,0,1,0,'Piety','None','How quickly you are able to gain the devotion of a god.',NULL,1,NULL,'You do not have enough None'),(192,0,NULL,56,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(193,0,NULL,57,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(194,0,NULL,57,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(195,0,NULL,58,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(196,0,NULL,58,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(197,0,NULL,59,NULL,0,5,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,5,NULL,'You do not have enough Brawn'),(198,0,NULL,59,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(199,0,NULL,60,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(200,0,NULL,60,NULL,0,5,0,'Redemption','Divinity','For each two levels of redemption you recover one sanctity each day.',NULL,5,NULL,'You do not have enough Divinity'),(201,0,2,NULL,NULL,0,0,0,'Adventuring','Fortuity','Your skill at exploring new places. This increases your likelihood of finding items when exploring',NULL,0,NULL,'You do not have enough Fortuity'),(202,0,2,NULL,NULL,0,0,0,'Parry','Quickness','The likelihood that you can parry an incoming attack.',NULL,0,NULL,'You do not have enough Quickness'),(203,0,2,NULL,NULL,0,0,0,'Reputation','Charisma','The magnitutde of which your actions affect your renown.',NULL,0,NULL,'You do not have enough Charisma'),(204,0,2,NULL,NULL,0,0,0,'ResistFlame','Resilience','Ability to resist flame damage',NULL,0,NULL,'You do not have enough Resilience'),(205,0,2,NULL,NULL,0,1,0,'Stamina','Resilience','For each four levels of stamina you recover one additional endurance each day.',NULL,1,NULL,'You do not have enough Resilience'),(206,0,2,NULL,NULL,0,1,0,'Woodsman','Pathfinding','Modifier for forest movement.',NULL,1,NULL,'You do not have enough Pathfinding'),(207,0,2,NULL,NULL,0,0,0,'Block','Resilience','Skill with a shield. If a shield is equipped then the amount of damage blocked is increased.',NULL,0,NULL,'You do not have enough Resilience'),(208,0,2,NULL,NULL,0,0,0,'ResistShadow','Resilience','Ability to resist shadow damage',NULL,0,NULL,'You do not have enough Resilience'),(209,0,2,NULL,NULL,0,0,0,'Redemption','Divinity','For each two levels of redemption you recover one sanctity each day.',NULL,0,NULL,'You do not have enough Divinity'),(210,0,2,NULL,NULL,0,0,0,'Courage','Willpower','How capable you are of overcoming your fears. The greater your courage then the greater the obstacles you will be capable of facing.',NULL,0,NULL,'You do not have enough Willpower'),(211,0,2,NULL,NULL,0,10,0,'Storage','Brawn','The amount of weight that you can carry.',NULL,10,NULL,'You do not have enough Brawn'),(212,0,2,NULL,NULL,0,0,0,'Logistics','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(213,0,2,NULL,NULL,0,0,0,'Faith','Divinity','Adds a bonus to how effective your spells are.',NULL,0,NULL,'You do not have enough Divinity'),(214,0,2,NULL,NULL,0,5,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,5,NULL,'You do not have enough Vitality'),(215,0,2,NULL,NULL,0,0,0,'Blunt','None','Skill with blunt weapons',NULL,0,NULL,'You do not have enough None'),(216,0,2,NULL,NULL,0,0,0,'ResistBlunt','Resilience','Ability to resist blunt damage',NULL,0,NULL,'You do not have enough Resilience'),(217,0,2,NULL,NULL,0,0,0,'Trustworthiness','Charisma','UNUSED',NULL,0,NULL,'You do not have enough Charisma'),(218,0,2,NULL,NULL,0,0,0,'Piety','None','How quickly you are able to gain the devotion of a god.',NULL,0,NULL,'You do not have enough None'),(219,0,2,NULL,NULL,0,0,0,'Riposte','Agility','UNUSED',NULL,0,NULL,'You do not have enough Agility'),(220,0,2,NULL,NULL,0,0,0,'Charm','Charisma','How likeable you are. It increases the speed of how quickly people begin to trust you.',NULL,0,NULL,'You do not have enough Charisma'),(221,0,2,NULL,NULL,0,0,0,'Recovery','Vitality','How quickly you recover from poisons and the negative effects of different ailments.',NULL,0,NULL,'You do not have enough Vitality'),(222,0,2,NULL,NULL,0,0,0,'Bartering','Charisma','Your skill at negotiating prices. It reduces the price you pay when buying any item from a vendor.',NULL,0,NULL,'You do not have enough Charisma'),(223,0,2,NULL,NULL,0,0,0,'FirstStrike','Quickness','Increases the likelihood that you will attack first in combat.',NULL,0,NULL,'You do not have enough Quickness'),(224,0,2,NULL,NULL,0,0,0,'LifestealPercent','None','Amount of life stolen per hit as percent of damage dealt',NULL,0,NULL,'You do not have enough None'),(225,0,2,NULL,NULL,0,0,0,'Stealth','Agility','Chance to avoid detection when attempting to stay concealed.',NULL,0,NULL,'You do not have enough Agility'),(226,0,2,NULL,NULL,0,0,0,'ResistFrost','Resilience','Ability to resist frost damage',NULL,0,NULL,'You do not have enough Resilience'),(227,0,2,NULL,NULL,0,1,0,'Speed','Quickness','How quickly you can attack in combat.',NULL,1,NULL,'You do not have enough Quickness'),(228,0,2,NULL,NULL,0,0,0,'Explorer','Survivalism','Reveals additional optional tasks which can be performed while exploring.',NULL,0,NULL,'You do not have enough Survivalism'),(229,0,2,NULL,NULL,0,0,0,'BlockAmount','None','Amount of damage absorbed when a shield successfully blocks',NULL,0,NULL,'You do not have enough None'),(230,0,2,NULL,NULL,0,0,0,'Dualism','None','How quickly you are able to change your virtue.',NULL,0,NULL,'You do not have enough None'),(231,0,2,NULL,NULL,0,0,0,'CautionLevel','None','How much detail is revealed of a location before you visit it.',NULL,0,NULL,'You do not have enough None'),(232,0,2,NULL,NULL,0,0,0,'Slashing','None','Skill with slashing weapons',NULL,0,NULL,'You do not have enough None'),(233,0,2,NULL,NULL,0,0,0,'Fatigue','Resilience','Reduces the speed at which you become exhausted in combat.',NULL,0,NULL,'You do not have enough Resilience'),(234,0,2,NULL,NULL,0,5,0,'Endurance','Resilience','Number of actions you can perform each day.',NULL,5,NULL,'You do not have enough Resilience'),(235,0,2,NULL,NULL,0,0,0,'Renown','None','How famous you are',NULL,0,NULL,'You do not have enough None'),(236,0,2,NULL,NULL,0,0,0,'Precision','Agility','Chance to critically hit enemies. A critical hit always hits for maximum damage and then applies your killshot multiplier to that value.',NULL,0,NULL,'You do not have enough Agility'),(237,0,2,NULL,NULL,0,0,0,'ResistHoly','Divinity','Ability to resist holy damage',NULL,0,NULL,'You do not have enough Divinity'),(238,0,2,NULL,NULL,0,0,0,'Survivalist','Survivalism','UNUSED',NULL,0,NULL,'You do not have enough Survivalism'),(239,0,2,NULL,NULL,0,0,0,'ResistPiercing','Resilience','Ability to resist piercing damage',NULL,0,NULL,'You do not have enough Resilience'),(240,0,2,NULL,NULL,0,0,0,'Accuracy','Agility','How accurately you attack. This gives a bonus chance to successfully striking your opponent in combat.',NULL,0,NULL,'You do not have enough Agility'),(241,0,2,NULL,NULL,0,0,0,'Encumbrance','Brawn','Your ability to fight in combat while carrying cumbersome gear.',NULL,0,NULL,'You do not have enough Brawn'),(242,0,2,NULL,NULL,0,0,0,'Mountaineering','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(243,0,2,NULL,NULL,0,0,0,'Huntsman','Survivalism','The amount of information that you can learn from defeated enemies.',NULL,0,NULL,'You do not have enough Survivalism'),(244,0,2,NULL,NULL,0,1,0,'Regeneration','Vitality','For each two levels of regeneration you recover one additional health each day.',NULL,1,NULL,'You do not have enough Vitality'),(245,0,2,NULL,NULL,0,0,0,'Evade','Quickness','Your ability to dodge enemy attacks. Gives a bonus chance for enemies to miss their close combat attacks.',NULL,0,NULL,'You do not have enough Quickness'),(246,0,2,NULL,NULL,0,0,0,'Literacy','Intellect','UNUSED',NULL,0,NULL,'You do not have enough Intellect'),(247,0,2,NULL,NULL,0,1,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,1,NULL,'You do not have enough Brawn'),(248,0,2,NULL,NULL,0,0,0,'Oration','Charisma','UNUSED',NULL,0,NULL,'You do not have enough Charisma'),(249,0,2,NULL,NULL,0,0,0,'LifestealStatic','None','Amount of life stolen per hit',NULL,0,NULL,'You do not have enough None'),(250,0,2,NULL,NULL,0,0,0,'Devotion','None','How religious you are',NULL,0,NULL,'You do not have enough None'),(251,0,2,NULL,NULL,0,1,0,'Combat','Brawn','Your proficiency in fighting. The greater combat proficiency you have then the more damage you do on each attack.',NULL,1,NULL,'You do not have enough Brawn'),(252,0,2,NULL,NULL,0,0,0,'ResistSlashing','Resilience','Ability to resist slashing damage',NULL,0,NULL,'You do not have enough Resilience'),(253,0,2,NULL,NULL,0,0,0,'Sanity','Willpower','Your ability to resist mind altering affects.',NULL,0,NULL,'You do not have enough Willpower'),(254,0,2,NULL,NULL,0,0,0,'Vision','None','How much of the map is revealed.',NULL,0,NULL,'You do not have enough None'),(255,0,2,NULL,NULL,0,0,0,'Detection','Survivalism','Determines the chance that you will uncover enemy traps and ambushes.',NULL,0,NULL,'You do not have enough Survivalism'),(256,0,2,NULL,NULL,0,0,0,'Piercing','None','Skill with piercing weapons',NULL,0,NULL,'You do not have enough None'),(257,0,2,NULL,NULL,0,0,0,'Knowledge','Intellect','UNUSED',NULL,0,NULL,'You do not have enough Intellect'),(258,0,2,NULL,NULL,0,0,0,'Defence','Resilience','Your ability to take physical damage. This combines with your armour to reduce all physical damaged received.',NULL,0,NULL,'You do not have enough Resilience'),(259,0,2,NULL,NULL,0,0,0,'Navigator','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(260,0,2,NULL,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(261,0,2,NULL,NULL,0,0,0,'Pickpocketing','Agility','Increases the chance that you will successfully pickpocket someone.',NULL,0,NULL,'You do not have enough Agility'),(262,0,2,NULL,NULL,0,0,0,'Luck','Fortuity','A bonus chance of having incredibly good luck.',NULL,0,NULL,'You do not have enough Fortuity'),(263,0,2,NULL,NULL,0,0,0,'WeaponAffinity','None','How accustomed to your current weapon you are',NULL,0,NULL,'You do not have enough None'),(264,0,2,NULL,NULL,0,0,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,0,NULL,'You do not have enough Divinity'),(265,0,2,NULL,NULL,0,0,0,'SpellLimit','None','How many spells you may know.',NULL,0,NULL,'You do not have enough None'),(266,0,2,NULL,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(267,0,2,NULL,NULL,0,0,0,'Flee','Quickness','Increases the chance that you can successful escape from a battle.',NULL,0,NULL,'You do not have enough Quickness'),(268,0,2,NULL,NULL,0,1,0,'Killshot','Agility','Damage multiplier added when performing a critical hit.',NULL,1,NULL,'You do not have enough Agility'),(269,0,2,NULL,NULL,0,0,0,'ClimbingAbility','None','The higher your climbing skill then the more difficult mountains you may climb.',NULL,0,NULL,'You do not have enough None'),(270,0,2,NULL,NULL,0,0,0,'ResistPoison','Resilience','Ability to resist poison damage',NULL,0,NULL,'You do not have enough Resilience'),(271,0,NULL,61,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(272,0,NULL,61,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(273,0,NULL,62,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(274,0,NULL,62,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(275,0,NULL,63,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(276,0,NULL,63,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(277,0,NULL,64,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(278,0,NULL,65,NULL,0,3,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,3,NULL,'You do not have enough Vitality'),(279,0,NULL,65,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(280,0,NULL,66,NULL,0,1,0,'LifestealStatic','None','Amount of life stolen per hit',NULL,1,NULL,'You do not have enough None'),(281,0,NULL,66,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(282,0,NULL,67,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(283,0,NULL,67,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(284,0,NULL,68,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(285,0,NULL,68,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(286,0,NULL,69,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(287,0,NULL,69,NULL,0,0,0,'Renown','None','How famous you are',NULL,0,NULL,'You do not have enough None'),(288,0,NULL,70,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(289,0,NULL,70,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(290,0,NULL,71,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(291,0,NULL,71,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(292,0,NULL,72,NULL,0,1,0,'Reputation','Charisma','The magnitutde of which your actions affect your renown.',NULL,1,NULL,'You do not have enough Charisma'),(293,0,NULL,72,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(294,0,NULL,73,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(295,0,NULL,73,NULL,0,2,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,2,NULL,'You do not have enough Divinity'),(296,0,NULL,74,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(297,0,NULL,74,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(298,0,NULL,75,NULL,0,3,0,'Stealth','Agility','Chance to avoid detection when attempting to stay concealed.',NULL,3,NULL,'You do not have enough Agility'),(299,0,NULL,75,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(300,0,NULL,76,NULL,0,1,0,'SpellLimit','None','How many spells you may know.',NULL,1,NULL,'You do not have enough None'),(301,0,NULL,76,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(302,0,NULL,77,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(303,0,NULL,77,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(304,0,NULL,78,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(305,0,NULL,78,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(306,0,NULL,79,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(307,0,NULL,79,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(308,0,NULL,80,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(309,0,NULL,80,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(310,0,NULL,81,NULL,0,5,0,'FirstStrike','Quickness','Increases the likelihood that you will attack first in combat.',NULL,5,NULL,'You do not have enough Quickness'),(311,0,NULL,81,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(312,0,NULL,82,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(313,0,NULL,82,NULL,0,5,0,'Bartering','Charisma','Your skill at negotiating prices. It reduces the price you pay when buying any item from a vendor.',NULL,5,NULL,'You do not have enough Charisma'),(314,0,NULL,83,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(315,0,NULL,83,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(316,0,NULL,84,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(317,0,NULL,84,NULL,0,1,0,'Vision','None','How much of the map is revealed.',NULL,1,NULL,'You do not have enough None'),(318,0,NULL,85,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(319,0,NULL,85,NULL,0,5,0,'LifestealPercent','None','Amount of life stolen per hit as percent of damage dealt',NULL,5,NULL,'You do not have enough None'),(320,0,NULL,86,NULL,0,0,0,'Piety','None','How quickly you are able to gain the devotion of a god.',NULL,1,NULL,'You do not have enough None'),(321,0,NULL,86,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(322,0,NULL,87,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(323,0,NULL,87,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(324,0,NULL,88,NULL,0,0,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,0,NULL,'You do not have enough Vitality'),(325,0,NULL,88,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(326,0,NULL,89,NULL,0,5,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,5,NULL,'You do not have enough Brawn'),(327,0,NULL,89,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(328,0,NULL,90,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(329,0,NULL,90,NULL,0,5,0,'Redemption','Divinity','For each two levels of redemption you recover one sanctity each day.',NULL,5,NULL,'You do not have enough Divinity'),(330,0,3,NULL,NULL,0,0,0,'Adventuring','Fortuity','Your skill at exploring new places. This increases your likelihood of finding items when exploring',NULL,0,NULL,'You do not have enough Fortuity'),(331,0,3,NULL,NULL,0,0,0,'Parry','Quickness','The likelihood that you can parry an incoming attack.',NULL,0,NULL,'You do not have enough Quickness'),(332,0,3,NULL,NULL,0,0,0,'Reputation','Charisma','The magnitutde of which your actions affect your renown.',NULL,0,NULL,'You do not have enough Charisma'),(333,0,3,NULL,NULL,0,0,0,'ResistFlame','Resilience','Ability to resist flame damage',NULL,0,NULL,'You do not have enough Resilience'),(334,0,3,NULL,NULL,0,1,0,'Stamina','Resilience','For each four levels of stamina you recover one additional endurance each day.',NULL,1,NULL,'You do not have enough Resilience'),(335,0,3,NULL,NULL,0,1,0,'Woodsman','Pathfinding','Modifier for forest movement.',NULL,1,NULL,'You do not have enough Pathfinding'),(336,0,3,NULL,NULL,0,0,0,'Block','Resilience','Skill with a shield. If a shield is equipped then the amount of damage blocked is increased.',NULL,0,NULL,'You do not have enough Resilience'),(337,0,3,NULL,NULL,0,0,0,'ResistShadow','Resilience','Ability to resist shadow damage',NULL,0,NULL,'You do not have enough Resilience'),(338,0,3,NULL,NULL,0,0,0,'Redemption','Divinity','For each two levels of redemption you recover one sanctity each day.',NULL,0,NULL,'You do not have enough Divinity'),(339,0,3,NULL,NULL,0,0,0,'Courage','Willpower','How capable you are of overcoming your fears. The greater your courage then the greater the obstacles you will be capable of facing.',NULL,0,NULL,'You do not have enough Willpower'),(340,0,3,NULL,NULL,0,10,0,'Storage','Brawn','The amount of weight that you can carry.',NULL,10,NULL,'You do not have enough Brawn'),(341,0,3,NULL,NULL,0,0,0,'Logistics','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(342,0,3,NULL,NULL,0,0,0,'Faith','Divinity','Adds a bonus to how effective your spells are.',NULL,0,NULL,'You do not have enough Divinity'),(343,0,3,NULL,NULL,0,5,0,'Health','Vitality','Determines the number of health points you have. When your health reahes zero then you fall unconscious.',NULL,5,NULL,'You do not have enough Vitality'),(344,0,3,NULL,NULL,0,0,0,'Blunt','None','Skill with blunt weapons',NULL,0,NULL,'You do not have enough None'),(345,0,3,NULL,NULL,0,0,0,'ResistBlunt','Resilience','Ability to resist blunt damage',NULL,0,NULL,'You do not have enough Resilience'),(346,0,3,NULL,NULL,0,0,0,'Trustworthiness','Charisma','UNUSED',NULL,0,NULL,'You do not have enough Charisma'),(347,0,3,NULL,NULL,0,0,0,'Piety','None','How quickly you are able to gain the devotion of a god.',NULL,0,NULL,'You do not have enough None'),(348,0,3,NULL,NULL,0,0,0,'Riposte','Agility','UNUSED',NULL,0,NULL,'You do not have enough Agility'),(349,0,3,NULL,NULL,0,0,0,'Charm','Charisma','How likeable you are. It increases the speed of how quickly people begin to trust you.',NULL,0,NULL,'You do not have enough Charisma'),(350,0,3,NULL,NULL,0,0,0,'Recovery','Vitality','How quickly you recover from poisons and the negative effects of different ailments.',NULL,0,NULL,'You do not have enough Vitality'),(351,0,3,NULL,NULL,0,0,0,'Bartering','Charisma','Your skill at negotiating prices. It reduces the price you pay when buying any item from a vendor.',NULL,0,NULL,'You do not have enough Charisma'),(352,0,3,NULL,NULL,0,0,0,'FirstStrike','Quickness','Increases the likelihood that you will attack first in combat.',NULL,0,NULL,'You do not have enough Quickness'),(353,0,3,NULL,NULL,0,0,0,'LifestealPercent','None','Amount of life stolen per hit as percent of damage dealt',NULL,0,NULL,'You do not have enough None'),(354,0,3,NULL,NULL,0,0,0,'Stealth','Agility','Chance to avoid detection when attempting to stay concealed.',NULL,0,NULL,'You do not have enough Agility'),(355,0,3,NULL,NULL,0,0,0,'ResistFrost','Resilience','Ability to resist frost damage',NULL,0,NULL,'You do not have enough Resilience'),(356,0,3,NULL,NULL,0,1,0,'Speed','Quickness','How quickly you can attack in combat.',NULL,1,NULL,'You do not have enough Quickness'),(357,0,3,NULL,NULL,0,0,0,'Explorer','Survivalism','Reveals additional optional tasks which can be performed while exploring.',NULL,0,NULL,'You do not have enough Survivalism'),(358,0,3,NULL,NULL,0,0,0,'BlockAmount','None','Amount of damage absorbed when a shield successfully blocks',NULL,0,NULL,'You do not have enough None'),(359,0,3,NULL,NULL,0,0,0,'Dualism','None','How quickly you are able to change your virtue.',NULL,0,NULL,'You do not have enough None'),(360,0,3,NULL,NULL,0,0,0,'CautionLevel','None','How much detail is revealed of a location before you visit it.',NULL,0,NULL,'You do not have enough None'),(361,0,3,NULL,NULL,0,0,0,'Slashing','None','Skill with slashing weapons',NULL,0,NULL,'You do not have enough None'),(362,0,3,NULL,NULL,0,0,0,'Fatigue','Resilience','Reduces the speed at which you become exhausted in combat.',NULL,0,NULL,'You do not have enough Resilience'),(363,0,3,NULL,NULL,0,5,0,'Endurance','Resilience','Number of actions you can perform each day.',NULL,5,NULL,'You do not have enough Resilience'),(364,0,3,NULL,NULL,0,0,0,'Renown','None','How famous you are',NULL,0,NULL,'You do not have enough None'),(365,0,3,NULL,NULL,0,0,0,'Precision','Agility','Chance to critically hit enemies. A critical hit always hits for maximum damage and then applies your killshot multiplier to that value.',NULL,0,NULL,'You do not have enough Agility'),(366,0,3,NULL,NULL,0,0,0,'ResistHoly','Divinity','Ability to resist holy damage',NULL,0,NULL,'You do not have enough Divinity'),(367,0,3,NULL,NULL,0,0,0,'Survivalist','Survivalism','UNUSED',NULL,0,NULL,'You do not have enough Survivalism'),(368,0,3,NULL,NULL,0,0,0,'ResistPiercing','Resilience','Ability to resist piercing damage',NULL,0,NULL,'You do not have enough Resilience'),(369,0,3,NULL,NULL,0,0,0,'Accuracy','Agility','How accurately you attack. This gives a bonus chance to successfully striking your opponent in combat.',NULL,0,NULL,'You do not have enough Agility'),(370,0,3,NULL,NULL,0,0,0,'Encumbrance','Brawn','Your ability to fight in combat while carrying cumbersome gear.',NULL,0,NULL,'You do not have enough Brawn'),(371,0,3,NULL,NULL,0,0,0,'Mountaineering','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(372,0,3,NULL,NULL,0,0,0,'Huntsman','Survivalism','The amount of information that you can learn from defeated enemies.',NULL,0,NULL,'You do not have enough Survivalism'),(373,0,3,NULL,NULL,0,1,0,'Regeneration','Vitality','For each two levels of regeneration you recover one additional health each day.',NULL,1,NULL,'You do not have enough Vitality'),(374,0,3,NULL,NULL,0,0,0,'Evade','Quickness','Your ability to dodge enemy attacks. Gives a bonus chance for enemies to miss their close combat attacks.',NULL,0,NULL,'You do not have enough Quickness'),(375,0,3,NULL,NULL,0,0,0,'Literacy','Intellect','UNUSED',NULL,0,NULL,'You do not have enough Intellect'),(376,0,3,NULL,NULL,1,1,0,'Damage','Brawn','Your capability of inflicting damage through melee. This is added to your combat skill and determines the greatest posssible damage you can deal in a single blow.',NULL,1,NULL,'You do not have enough Brawn'),(377,0,3,NULL,NULL,0,0,0,'Oration','Charisma','UNUSED',NULL,0,NULL,'You do not have enough Charisma'),(378,0,3,NULL,NULL,0,0,0,'LifestealStatic','None','Amount of life stolen per hit',NULL,0,NULL,'You do not have enough None'),(379,0,3,NULL,NULL,0,0,0,'Devotion','None','How religious you are',NULL,0,NULL,'You do not have enough None'),(380,0,3,NULL,NULL,0,1,0,'Combat','Brawn','Your proficiency in fighting. The greater combat proficiency you have then the more damage you do on each attack.',NULL,1,NULL,'You do not have enough Brawn'),(381,0,3,NULL,NULL,0,0,0,'ResistSlashing','Resilience','Ability to resist slashing damage',NULL,0,NULL,'You do not have enough Resilience'),(382,0,3,NULL,NULL,1,0,0,'Sanity','Willpower','Your ability to resist mind altering affects.',NULL,0,NULL,'You do not have enough Willpower'),(383,0,3,NULL,NULL,0,0,0,'Vision','None','How much of the map is revealed.',NULL,0,NULL,'You do not have enough None'),(384,0,3,NULL,NULL,0,0,0,'Detection','Survivalism','Determines the chance that you will uncover enemy traps and ambushes.',NULL,0,NULL,'You do not have enough Survivalism'),(385,0,3,NULL,NULL,0,0,0,'Piercing','None','Skill with piercing weapons',NULL,0,NULL,'You do not have enough None'),(386,0,3,NULL,NULL,0,0,0,'Knowledge','Intellect','UNUSED',NULL,0,NULL,'You do not have enough Intellect'),(387,0,3,NULL,NULL,0,0,0,'Defence','Resilience','Your ability to take physical damage. This combines with your armour to reduce all physical damaged received.',NULL,0,NULL,'You do not have enough Resilience'),(388,0,3,NULL,NULL,0,0,0,'Navigator','Pathfinding','UNUSED',NULL,0,NULL,'You do not have enough Pathfinding'),(389,0,3,NULL,NULL,0,0,0,'Understanding','Intellect','How much more quickly you level up.',NULL,0,NULL,'You do not have enough Intellect'),(390,0,3,NULL,NULL,0,0,0,'Pickpocketing','Agility','Increases the chance that you will successfully pickpocket someone.',NULL,0,NULL,'You do not have enough Agility'),(391,0,3,NULL,NULL,0,0,0,'Luck','Fortuity','A bonus chance of having incredibly good luck.',NULL,0,NULL,'You do not have enough Fortuity'),(392,0,3,NULL,NULL,0,0,0,'WeaponAffinity','None','How accustomed to your current weapon you are',NULL,0,NULL,'You do not have enough None'),(393,0,3,NULL,NULL,0,0,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,0,NULL,'You do not have enough Divinity'),(394,0,3,NULL,NULL,0,0,0,'SpellLimit','None','How many spells you may know.',NULL,0,NULL,'You do not have enough None'),(395,0,3,NULL,NULL,0,0,0,'Virtue','None','How good or evil you are',NULL,0,NULL,'You do not have enough None'),(396,0,3,NULL,NULL,0,0,0,'Flee','Quickness','Increases the chance that you can successful escape from a battle.',NULL,0,NULL,'You do not have enough Quickness'),(397,0,3,NULL,NULL,0,1,0,'Killshot','Agility','Damage multiplier added when performing a critical hit.',NULL,1,NULL,'You do not have enough Agility'),(398,0,3,NULL,NULL,0,0,0,'ClimbingAbility','None','The higher your climbing skill then the more difficult mountains you may climb.',NULL,0,NULL,'You do not have enough None'),(399,0,3,NULL,NULL,0,0,0,'ResistPoison','Resilience','Ability to resist poison damage',NULL,0,NULL,'You do not have enough Resilience'),(400,0,NULL,NULL,10,0,50,0,'Sanctity','Divinity','Amount of sanctity you can have.',NULL,50,NULL,'You do not have enough Divinity');
/*!40000 ALTER TABLE `proficiency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quest`
--

DROP TABLE IF EXISTS `quest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reward_experience` int(11) DEFAULT NULL,
  `position` int(11) DEFAULT NULL,
  `trigger_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_quest_trigger_id_trigger` (`trigger_id`),
  CONSTRAINT `fk_quest_trigger_id_trigger` FOREIGN KEY (`trigger_id`) REFERENCES `trigger` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quest`
--

LOCK TABLES `quest` WRITE;
/*!40000 ALTER TABLE `quest` DISABLE KEYS */;
INSERT INTO `quest` VALUES (1,'Go talk to the blacksmith','Find the blacksmith in Thornwall and enter his shop.',3,0,2),(2,'Buy your first item','Buy any item from the blacksmith.',4,1,1),(3,'Equip an item','Equip any item in your inventory.',3,0,4),(4,'Unequip an item','Unequip any item in your inventory.',3,1,3);
/*!40000 ALTER TABLE `quest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quest_path`
--

DROP TABLE IF EXISTS `quest_path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quest_path` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template` tinyint(1) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reward_experience` int(11) DEFAULT NULL,
  `stage` int(11) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  `journal_id` int(11) DEFAULT NULL,
  `handler_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_quest_path_journal_id_journal` (`journal_id`),
  KEY `fk_quest_path_handler_id_handler` (`handler_id`),
  CONSTRAINT `fk_quest_path_handler_id_handler` FOREIGN KEY (`handler_id`) REFERENCES `handler` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_quest_path_journal_id_journal` FOREIGN KEY (`journal_id`) REFERENCES `journal` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quest_path`
--

LOCK TABLES `quest_path` WRITE;
/*!40000 ALTER TABLE `quest_path` DISABLE KEYS */;
INSERT INTO `quest_path` VALUES (1,1,'Get Acquainted with the Blacksmith','Find the blacksmith and buy something from him.',5,0,0,0,NULL,NULL),(2,1,'Learn how your inventory works','Practice equipping an unequipping.',5,0,1,0,NULL,NULL);
/*!40000 ALTER TABLE `quest_path` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quest_path_to_quest_association`
--

DROP TABLE IF EXISTS `quest_path_to_quest_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quest_path_to_quest_association` (
  `quest_path_id` int(11) DEFAULT NULL,
  `quest_id` int(11) DEFAULT NULL,
  KEY `fk_quest_path_to_quest_association_quest_path_id_quest_path` (`quest_path_id`),
  KEY `fk_quest_path_to_quest_association_quest_id_quest` (`quest_id`),
  CONSTRAINT `fk_quest_path_to_quest_association_quest_id_quest` FOREIGN KEY (`quest_id`) REFERENCES `quest` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_quest_path_to_quest_association_quest_path_id_quest_path` FOREIGN KEY (`quest_path_id`) REFERENCES `quest_path` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quest_path_to_quest_association`
--

LOCK TABLES `quest_path_to_quest_association` WRITE;
/*!40000 ALTER TABLE `quest_path_to_quest_association` DISABLE KEYS */;
INSERT INTO `quest_path_to_quest_association` VALUES (1,1),(1,2),(2,4),(2,3);
/*!40000 ALTER TABLE `quest_path_to_quest_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specialization`
--

DROP TABLE IF EXISTS `specialization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `specialization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template` tinyint(1) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `requirements` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `attrib_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hero_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_specialization_hero_id_hero` (`hero_id`),
  CONSTRAINT `fk_specialization_hero_id_hero` FOREIGN KEY (`hero_id`) REFERENCES `hero` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specialization`
--

LOCK TABLES `specialization` WRITE;
/*!40000 ALTER TABLE `specialization` DISABLE KEYS */;
INSERT INTO `specialization` VALUES (1,1,'Ascetic','Archetype','A character who focuses on disciplining mind and body. They use a combination of combat and intellect.','10 Errands Complete, Virtue of 100, Willpower of 4','ascetic',NULL),(2,1,'Brute','Archetype','A character who uses strength and combat to solve problems. Proficient with many types of weapons.','Brawn of 6, Any Weapon Talent ~ 10','brute',NULL),(3,1,'Opportunist','Archetype','A character who solves problems using speech and dialogue.','Charisma of 7, Fame of 200','opportunist',NULL),(4,1,'Philosopher','Archetype','A character who uses intellect to solve problems. Excels at any task requiring powers of the mind.','Intellect of 7, Books Read of 10','philosopher',NULL),(5,1,'Scoundrel','Archetype','A character who uses deception and sneakiness to accomplish their goals. Excels at stealth attacks and thievery.','Dagger Talent of 6, Virtue of -100','scoundrel',NULL),(6,1,'Survivalist','Archetype','A character who utilizes their environment to adapt and thrive. Excellent at long ranged weaponry and exploration.','5 Locations Discovered, 10 Animals in Bestiary','survivalist',NULL),(7,1,'TestCalling','Calling','A blacksmith dude.','Be a dude ... who likes hitting hot metal.','test_calling',NULL),(8,1,'TestPantheon','Pantheon','A fire god dude.','Be a Pyro ... and a dude.','test_pantheon',NULL);
/*!40000 ALTER TABLE `specialization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thread`
--

DROP TABLE IF EXISTS `thread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `board_id` int(11) DEFAULT NULL,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `creator` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_thread_board_id_board` (`board_id`),
  CONSTRAINT `fk_thread_board_id_board` FOREIGN KEY (`board_id`) REFERENCES `board` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thread`
--

LOCK TABLES `thread` WRITE;
/*!40000 ALTER TABLE `thread` DISABLE KEYS */;
INSERT INTO `thread` VALUES (1,1,'Enemies only missing ','Tntdj360','you need to make it so the enemies actually hit people so they have to decide when they want to fight and when they want to leave','General','2018-03-06 01:02:35');
/*!40000 ALTER TABLE `thread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trigger`
--

DROP TABLE IF EXISTS `trigger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trigger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `extra_info_for_humans` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `completed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trigger`
--

LOCK TABLES `trigger` WRITE;
/*!40000 ALTER TABLE `trigger` DISABLE KEYS */;
INSERT INTO `trigger` VALUES (1,'buy_event','Should activate when buy code runs and hero.current_location.id == id of the blacksmith.',0),(2,'move_event','Should activate when the hero.current_location.id == the id of the blacksmith object.',0),(3,'unequip_event','Should activate when unequip_event spawns.',0),(4,'equip_event','Should activate when equip_event spawns.',0);
/*!40000 ALTER TABLE `trigger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reset_key` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `inbox_alert` tinyint(1) DEFAULT NULL,
  `prestige` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'marlen','$2a$10$6b13zuj8ZfUgxACEKeXsuevrVXoY5iEbXegtDn/.cCFgOhTCwGGNG','',NULL,'2018-02-15 02:49:17',1,0,309),(2,'admin','21232f297a57a5a743894a0e4a801fc3','','1','2018-02-15 02:49:17',1,0,371),(3,'TnTDj360','2aec35054c713ceb7aa64c680fed20a0','','1','2018-03-06 00:53:56',0,0,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-08 17:44:53
