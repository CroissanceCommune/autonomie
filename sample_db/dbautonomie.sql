-- MySQL dump 10.13  Distrib 5.5.19, for Linux (x86_64)
--
-- Host: localhost    Database: egw
-- ------------------------------------------------------
-- Server version	5.5.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `coop_company`
--

DROP TABLE IF EXISTS `coop_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_company` (
  `IDCompany` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `object` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `comments` text,
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  `active` varchar(1) NOT NULL DEFAULT 'Y',
  `IDGroup` int(11) NOT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `header` varchar(255) DEFAULT NULL,
  `logoType` varchar(255) DEFAULT NULL,
  `headerType` varchar(255) DEFAULT NULL,
  `IDEGWUser` int(11) NOT NULL,
  `RIB` varchar(255) DEFAULT NULL,
  `IBAN` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IDCompany`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_company_employee`
--

DROP TABLE IF EXISTS `coop_company_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_company_employee` (
  `IDCompany` int(11) NOT NULL,
  `IDEmployee` int(11) NOT NULL,
  `DateStart` int(11) NOT NULL,
  `DateEnd` int(11) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_customer`
--

DROP TABLE IF EXISTS `coop_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_customer` (
  `code` varchar(4) NOT NULL,
  `IDContact` int(11) DEFAULT '0',
  `comments` text,
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  `IDCompany` int(11) NOT NULL,
  `intraTVA` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `zipCode` varchar(20) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(150) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `contactLastName` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `contactFirstName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`),
  KEY `IDCompany` (`IDCompany`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_employee`
--

DROP TABLE IF EXISTS `coop_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_employee` (
  `IDEmployee` int(11) NOT NULL,
  `comments` text,
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  `IDContact` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDEmployee`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_estimation`
--

DROP TABLE IF EXISTS `coop_estimation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_estimation` (
  `IDTask` int(11) NOT NULL,
  `sequenceNumber` int(11) NOT NULL,
  `number` varchar(100) NOT NULL,
  `tva` int(11) NOT NULL DEFAULT '196',
  `discount` int(11) NOT NULL DEFAULT '0',
  `deposit` int(11) NOT NULL DEFAULT '0',
  `paymentConditions` text,
  `exclusions` text,
  `IDProject` int(11) NOT NULL,
  `manualDeliverables` tinyint(4) DEFAULT NULL,
  `course` tinyint(4) NOT NULL DEFAULT '0',
  `displayedUnits` tinyint(4) NOT NULL DEFAULT '0',
  `discountHT` int(11) NOT NULL DEFAULT '0',
  `expenses` int(11) NOT NULL DEFAULT '0',
  `paymentDisplay` varchar(20) DEFAULT 'SUMMARY',
  PRIMARY KEY (`IDTask`),
  KEY `coop_estimation_sequenceNumber` (`sequenceNumber`),
  KEY `coop_estimation_IDProject` (`IDProject`),
  KEY `IDProject` (`IDProject`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_estimation_line`
--

DROP TABLE IF EXISTS `coop_estimation_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_estimation_line` (
  `IDWorkLine` int(11) NOT NULL AUTO_INCREMENT,
  `IDTask` int(11) NOT NULL,
  `rowIndex` int(11) NOT NULL,
  `description` text,
  `cost` int(11) DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `creationDate` int(11) DEFAULT NULL,
  `updateDate` int(11) DEFAULT NULL,
  `unity` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`IDWorkLine`),
  KEY `coop_estimation_line_IDTask` (`IDTask`),
  KEY `coop_estimation_line_rowIndex` (`rowIndex`),
  KEY `IDTask` (`IDTask`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_estimation_payment`
--

DROP TABLE IF EXISTS `coop_estimation_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_estimation_payment` (
  `IDPaymentLine` int(11) NOT NULL AUTO_INCREMENT,
  `IDTask` int(11) NOT NULL,
  `rowIndex` int(11) NOT NULL,
  `description` text,
  `amount` int(11) DEFAULT NULL,
  `creationDate` int(11) DEFAULT NULL,
  `updateDate` int(11) DEFAULT NULL,
  `paymentDate` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDPaymentLine`),
  KEY `coop_estimation_payment_IDTask` (`IDTask`),
  KEY `coop_estimation_payment_rowIndex` (`rowIndex`),
  KEY `IDTask` (`IDTask`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_internal_invoice`
--

DROP TABLE IF EXISTS `coop_internal_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_internal_invoice` (
  `number` int(11) NOT NULL,
  `invoiceDate` int(11) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `account` int(11) DEFAULT NULL,
  PRIMARY KEY (`number`,`invoiceDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_invoice`
--

DROP TABLE IF EXISTS `coop_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_invoice` (
  `IDTask` int(11) NOT NULL,
  `IDEstimation` int(11) DEFAULT '0',
  `IDProject` int(11) NOT NULL,
  `sequenceNumber` int(11) NOT NULL,
  `number` varchar(100) NOT NULL,
  `tva` int(11) NOT NULL DEFAULT '196',
  `discount` int(11) NOT NULL DEFAULT '0',
  `paymentConditions` text,
  `estimationDate` int(11) DEFAULT '0',
  `estimationNumber` varchar(100) DEFAULT NULL,
  `deposit` tinyint(4) NOT NULL DEFAULT '0',
  `course` tinyint(4) NOT NULL DEFAULT '0',
  `officialNumber` int(11) DEFAULT NULL,
  `paymentMode` varchar(10) DEFAULT NULL,
  `displayedUnits` tinyint(4) NOT NULL DEFAULT '0',
  `discountHT` int(11) NOT NULL DEFAULT '0',
  `expenses` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`IDTask`),
  KEY `IDProject` (`IDProject`),
  KEY `IDEstimation` (`IDEstimation`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_invoice_line`
--

DROP TABLE IF EXISTS `coop_invoice_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_invoice_line` (
  `IDInvoiceLine` int(11) NOT NULL AUTO_INCREMENT,
  `IDTask` int(11) NOT NULL,
  `rowIndex` int(11) NOT NULL,
  `description` text,
  `cost` int(11) DEFAULT '0',
  `creationDate` int(11) DEFAULT '0',
  `updateDate` int(11) DEFAULT '0',
  `quantity` double DEFAULT '1',
  `unity` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`IDInvoiceLine`),
  KEY `IDTask` (`IDTask`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_personal_task`
--

DROP TABLE IF EXISTS `coop_personal_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_personal_task` (
  `IDPersonalTask` int(11) NOT NULL AUTO_INCREMENT,
  `IDEmployee` int(11) NOT NULL,
  `taskDate` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
  `title` varchar(255) NOT NULL,
  `contents` text,
  `IDInterviewer` int(11) DEFAULT '0',
  `document` varchar(255) DEFAULT NULL,
  `documentType` varchar(255) DEFAULT NULL,
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  `employeeTask` tinyint(4) NOT NULL DEFAULT '0',
  `inProcess` tinyint(4) NOT NULL DEFAULT '0',
  `status` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`IDPersonalTask`),
  KEY `IDEmployee` (`IDEmployee`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_phase`
--

DROP TABLE IF EXISTS `coop_phase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_phase` (
  `IDPhase` int(11) NOT NULL AUTO_INCREMENT,
  `IDProject` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `IDPreviousPhase` int(11) NOT NULL DEFAULT '0',
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  PRIMARY KEY (`IDPhase`),
  KEY `IDProject` (`IDProject`),
  KEY `IDPreviousPhase` (`IDPreviousPhase`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_project`
--

DROP TABLE IF EXISTS `coop_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_project` (
  `IDProject` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `customerCode` varchar(4) NOT NULL,
  `type` varchar(150) DEFAULT NULL,
  `code` varchar(4) NOT NULL,
  `definition` text,
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  `startingDate` int(11) DEFAULT NULL,
  `endingDate` int(11) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `IDCompany` int(11) NOT NULL,
  `dispatchType` varchar(10) NOT NULL DEFAULT 'PERCENT',
  `archived` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`IDProject`),
  KEY `IDCompany` (`IDCompany`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_project_team`
--

DROP TABLE IF EXISTS `coop_project_team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_project_team` (
  `IDProject` int(11) NOT NULL,
  `IDEmployee` int(11) NOT NULL,
  `leader` tinyint(4) NOT NULL DEFAULT '0',
  `dispatch` int(11) NOT NULL DEFAULT '0',
  `external` tinyint(4) NOT NULL DEFAULT '0',
  UNIQUE KEY `coop_project_team_IDProject_IDEmployee` (`IDProject`,`IDEmployee`),
  KEY `coop_project_team_IDProject` (`IDProject`),
  KEY `coop_project_team_IDEmployee` (`IDEmployee`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_task`
--

DROP TABLE IF EXISTS `coop_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_task` (
  `IDTask` int(11) NOT NULL AUTO_INCREMENT,
  `IDPhase` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `CAEStatus` varchar(10) DEFAULT NULL,
  `customerStatus` varchar(10) DEFAULT NULL,
  `taskDate` int(11) DEFAULT '0',
  `IDEmployee` int(11) NOT NULL,
  `document` varchar(255) DEFAULT NULL,
  `creationDate` int(11) NOT NULL,
  `updateDate` int(11) NOT NULL,
  `description` text,
  `statusComment` text,
  `documentType` varchar(255) DEFAULT NULL,
  `statusPerson` int(11) DEFAULT NULL,
  `statusDate` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  PRIMARY KEY (`IDTask`),
  KEY `IDPhase` (`IDPhase`),
  KEY `IDEmployee` (`IDEmployee`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coop_task_status`
--

DROP TABLE IF EXISTS `coop_task_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coop_task_status` (
  `IDTask` int(11) NOT NULL,
  `statusCode` varchar(10) NOT NULL,
  `statusComment` text,
  `statusPerson` int(11) DEFAULT NULL,
  `statusDate` int(11) DEFAULT NULL,
  KEY `IDTask` (`IDTask`),
  KEY `statusCode` (`statusCode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--

--
-- Table structure for table `egw_accounts`
--

DROP TABLE IF EXISTS `egw_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_accounts` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_lid` varchar(64) NOT NULL,
  `account_pwd` varchar(100) NOT NULL,
  `account_firstname` varchar(50) DEFAULT NULL,
  `account_lastname` varchar(50) DEFAULT NULL,
  `account_lastlogin` int(11) DEFAULT NULL,
  `account_lastloginfrom` varchar(255) DEFAULT NULL,
  `account_lastpwd_change` int(11) DEFAULT NULL,
  `account_status` varchar(1) NOT NULL DEFAULT 'A',
  `account_expires` int(11) DEFAULT NULL,
  `account_type` varchar(1) DEFAULT NULL,
  `person_id` int(11) DEFAULT NULL,
  `account_primary_group` int(11) NOT NULL DEFAULT '0',
  `account_email` varchar(100) DEFAULT NULL,
  `account_challenge` varchar(100) DEFAULT NULL,
  `account_response` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `egw_accounts_account_lid` (`account_lid`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_config`
--

DROP TABLE IF EXISTS `egw_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_config` (
  `config_app` varchar(50) NOT NULL,
  `config_name` varchar(255) NOT NULL,
  `config_value` text,
  PRIMARY KEY  (`config_app`,`config_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-02-03 16:11:15
