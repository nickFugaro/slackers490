-- MySQL dump 10.13  Distrib 8.0.23, for Linux (x86_64)
--
-- Host: localhost    Database: IT490
-- ------------------------------------------------------
-- Server version	8.0.23-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Account`
--

DROP TABLE IF EXISTS `Account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Account` (
  `account_email` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `account_password` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `account_salt` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `account_id` int NOT NULL AUTO_INCREMENT,
  `account_username` varchar(100) NOT NULL,
  UNIQUE KEY `id` (`account_id`),
  UNIQUE KEY `user_email_unique` (`account_email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Account`
--

LOCK TABLES `Account` WRITE;
/*!40000 ALTER TABLE `Account` DISABLE KEYS */;
INSERT INTO `Account` VALUES ('EMAIL','7d32ea9b6fe3f5a12e66680f2698fae06c851664fe0f39501ebc35547dc68eaf14e539dfb967731a674614f2247d31b512de521d6a1f5ecfa0b739c888d37530','a915cd06-2482-41b4-b7d6-67375ef2441b',1,'email_username'),('bMAIL','e108361cafba95815397828d78d865983ce975be0cefa1afe972bf136ae1a00dfed2ec7cb9cfce0ef86cec1f0b063e8fb01210f872ec499365ac501df3709ede','7c766ad0-3235-417e-be47-90445af3fd52',2,'bmail_username'),('da354@njit.edu','3dd6a3c9e9537ac1d23b2928b364a48e99c0dcfd376bb4e976307f0acd34cd8703a0fa01acdc04239204f85f57078fd6f0dc4043a244260430526a3aa3b6409f','82bb3373-20ef-4709-b3db-af5f209eb6bb',3,'da354_username');
/*!40000 ALTER TABLE `Account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Categories`
--

DROP TABLE IF EXISTS `Categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Categories` (
  `cat_id` int NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cat_description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`cat_id`),
  UNIQUE KEY `cat_name_unique` (`cat_name`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Categories`
--

LOCK TABLES `Categories` WRITE;
/*!40000 ALTER TABLE `Categories` DISABLE KEYS */;
INSERT INTO `Categories` VALUES (1,'Category 1','Category 1 Description'),(2,'Category 2','Category 2 Description'),(3,'Category 3','Category 3 Description'),(4,'Category 4','Category 4 Description'),(5,'Category 5','Category 5 Description'),(6,'Category 6','Category 6 Description'),(7,'Category 7','Category 7 Description'),(8,'Category 8','Category 8 Description'),(9,'Category 9','Category 9 Description'),(10,'Category 10','Category 10 Description'),(16,'Category 11','Category 11 Description'),(28,'Category 12','Category 3 Description'),(29,'Category 13','Category 13 Description');
/*!40000 ALTER TABLE `Categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Posts`
--

DROP TABLE IF EXISTS `Posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Posts` (
  `post_id` int NOT NULL AUTO_INCREMENT,
  `post_content` text NOT NULL,
  `post_date` datetime NOT NULL,
  `post_topic` int NOT NULL,
  `post_by` int NOT NULL,
  PRIMARY KEY (`post_id`),
  KEY `post_topic` (`post_topic`),
  KEY `post_by` (`post_by`),
  CONSTRAINT `Posts_ibfk_1` FOREIGN KEY (`post_topic`) REFERENCES `Topics` (`topic_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Posts_ibfk_2` FOREIGN KEY (`post_by`) REFERENCES `Account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Posts`
--

LOCK TABLES `Posts` WRITE;
/*!40000 ALTER TABLE `Posts` DISABLE KEYS */;
INSERT INTO `Posts` VALUES (1,'Post Content of Topic 1','2021-02-25 15:02:36',1,2),(2,'Post Content of Topic 1','2021-02-25 15:03:28',1,2),(3,'Category 14, Topic 4, Post 1','2021-03-02 17:46:39',4,2);
/*!40000 ALTER TABLE `Posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Quiz`
--

DROP TABLE IF EXISTS `Quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Quiz` (
  `quiz_id` int NOT NULL AUTO_INCREMENT,
  `quiz_question` varchar(100) NOT NULL,
  `quiz_option_a` varchar(100) NOT NULL,
  `quiz_option_b` varchar(100) NOT NULL,
  `quiz_option_c` varchar(100) NOT NULL,
  `quiz_option_d` varchar(100) NOT NULL,
  `quiz_option_correct` varchar(1) NOT NULL,
  PRIMARY KEY (`quiz_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Quiz`
--

LOCK TABLES `Quiz` WRITE;
/*!40000 ALTER TABLE `Quiz` DISABLE KEYS */;
INSERT INTO `Quiz` VALUES (1,'Question 1 ','Q1_Option_A','Q1_Option_B','Q1_Option_C','Q1_Option_D','A'),(2,'Question 2','Q2_Option_A','Q2_Option_B','Q2_Option_C','Q2_Option_D','B'),(3,'Question 3','Q3_Option_A','Q3_Option_B','Q3_Option_C','Q3_Option_D','C'),(4,'Question 4','Q4_Option_A','Q4_Option_B','Q4_Option_C','Q4_Option_D','D'),(5,'Question 5','Q5_Option_A','Q5_Option_B','Q5_Option_C','Q5_Option_D','A'),(6,'Question 6','Q6_Option_A','Q6_Option_B','Q6_Option_C','Q6_Option_D','B'),(7,'Question 7','Q7_Option_A','Q7_Option_B','Q7_Option_C','Q7_Option_D','C'),(8,'Question 8','Q8_Option_A','Q8_Option_B','Q8_Option_C','Q8_Option_D','D'),(9,'Question 9','Q9_Option_A','Q9_Option_B','Q9_Option_C','Q9_Option_D','A'),(10,'Question 10','Q10_Option_A','Q10_Option_B','Q10_Option_C','Q10_Option_D','B');
/*!40000 ALTER TABLE `Quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `QuizHistory`
--

DROP TABLE IF EXISTS `QuizHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `QuizHistory` (
  `account_id` int NOT NULL,
  `quiz_id` int NOT NULL,
  `user_selection` varchar(100) NOT NULL,
  `correct` tinyint(1) NOT NULL,
  `date` datetime NOT NULL,
  KEY `account_id` (`account_id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `QuizHistory_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `Account` (`account_id`) ON DELETE CASCADE,
  CONSTRAINT `QuizHistory_ibfk_2` FOREIGN KEY (`quiz_id`) REFERENCES `Quiz` (`quiz_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QuizHistory`
--

LOCK TABLES `QuizHistory` WRITE;
/*!40000 ALTER TABLE `QuizHistory` DISABLE KEYS */;
INSERT INTO `QuizHistory` VALUES (2,7,'C',1,'2021-03-01 17:21:01'),(2,7,'D',0,'2021-03-01 17:21:47'),(1,7,'D',0,'2021-03-01 17:31:57'),(1,7,'D',0,'2021-03-01 17:32:02'),(1,7,'D',0,'2021-03-01 17:32:21'),(1,7,'C',1,'2021-03-01 17:32:52');
/*!40000 ALTER TABLE `QuizHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Topics`
--

DROP TABLE IF EXISTS `Topics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Topics` (
  `topic_id` int NOT NULL AUTO_INCREMENT,
  `topic_subject` varchar(255) NOT NULL,
  `topic_date` datetime NOT NULL,
  `topic_cat` int NOT NULL,
  `topic_by` int NOT NULL,
  PRIMARY KEY (`topic_id`),
  KEY `topic_cat` (`topic_cat`),
  KEY `topic_by` (`topic_by`),
  CONSTRAINT `Topics_ibfk_1` FOREIGN KEY (`topic_cat`) REFERENCES `Categories` (`cat_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Topics_ibfk_2` FOREIGN KEY (`topic_by`) REFERENCES `Account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Topics`
--

LOCK TABLES `Topics` WRITE;
/*!40000 ALTER TABLE `Topics` DISABLE KEYS */;
INSERT INTO `Topics` VALUES (1,'Topic Subject 1','2021-02-25 12:20:10',1,2),(2,'Category 1 Subject SOMETHING RANDOM','2021-03-02 17:28:08',1,2),(4,'Category 11 Subject SOMETHING RANDOM SAGA','2021-03-02 17:29:23',16,2);
/*!40000 ALTER TABLE `Topics` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-04 20:05:23
