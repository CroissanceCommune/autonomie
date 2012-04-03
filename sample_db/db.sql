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
) ENGINE=MyISAM AUTO_INCREMENT=315 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=23143 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=11594 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=24055 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=4098 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=4807 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=3033 DEFAULT CHARSET=utf8;
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
) ENGINE=MyISAM AUTO_INCREMENT=8189 DEFAULT CHARSET=utf8;
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
-- Table structure for table `egw_access_log`
--

DROP TABLE IF EXISTS `egw_access_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_access_log` (
  `sessionid` varchar(128) NOT NULL,
  `loginid` varchar(64) NOT NULL,
  `ip` varchar(40) NOT NULL,
  `li` int(11) NOT NULL,
  `lo` int(11) DEFAULT '0',
  `account_id` int(11) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=MyISAM AUTO_INCREMENT=1040 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_acl`
--

DROP TABLE IF EXISTS `egw_acl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_acl` (
  `acl_appname` varchar(50) NOT NULL,
  `acl_location` varchar(255) NOT NULL,
  `acl_account` int(11) NOT NULL,
  `acl_rights` int(11) DEFAULT NULL,
  PRIMARY KEY (`acl_appname`,`acl_location`,`acl_account`),
  KEY `egw_acl_account` (`acl_account`),
  KEY `egw_acl_location_account` (`acl_location`,`acl_account`),
  KEY `egw_acl_appname_account` (`acl_appname`,`acl_account`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_addressbook`
--

DROP TABLE IF EXISTS `egw_addressbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_addressbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lid` varchar(32) DEFAULT NULL,
  `tid` varchar(1) DEFAULT NULL,
  `owner` bigint(20) DEFAULT NULL,
  `access` varchar(7) DEFAULT NULL,
  `cat_id` varchar(32) DEFAULT NULL,
  `fn` varchar(64) DEFAULT NULL,
  `n_family` varchar(64) DEFAULT NULL,
  `n_given` varchar(64) DEFAULT NULL,
  `n_middle` varchar(64) DEFAULT NULL,
  `n_prefix` varchar(64) DEFAULT NULL,
  `n_suffix` varchar(64) DEFAULT NULL,
  `sound` varchar(64) DEFAULT NULL,
  `bday` varchar(32) DEFAULT NULL,
  `note` text,
  `tz` varchar(8) DEFAULT NULL,
  `geo` varchar(32) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  `pubkey` text,
  `org_name` varchar(64) DEFAULT NULL,
  `org_unit` varchar(64) DEFAULT NULL,
  `title` varchar(64) DEFAULT NULL,
  `adr_one_street` varchar(64) DEFAULT NULL,
  `adr_one_locality` varchar(64) DEFAULT NULL,
  `adr_one_region` varchar(64) DEFAULT NULL,
  `adr_one_postalcode` varchar(64) DEFAULT NULL,
  `adr_one_countryname` varchar(64) DEFAULT NULL,
  `adr_one_type` varchar(32) DEFAULT NULL,
  `label` text,
  `adr_two_street` varchar(64) DEFAULT NULL,
  `adr_two_locality` varchar(64) DEFAULT NULL,
  `adr_two_region` varchar(64) DEFAULT NULL,
  `adr_two_postalcode` varchar(64) DEFAULT NULL,
  `adr_two_countryname` varchar(64) DEFAULT NULL,
  `adr_two_type` varchar(32) DEFAULT NULL,
  `tel_work` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_home` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_voice` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_fax` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_msg` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_cell` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_pager` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_bbs` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_modem` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_car` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_isdn` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_video` varchar(40) NOT NULL DEFAULT '+1 (000) 000-0000',
  `tel_prefer` varchar(32) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `email_type` varchar(32) DEFAULT 'INTERNET',
  `email_home` varchar(64) DEFAULT NULL,
  `email_home_type` varchar(32) DEFAULT 'INTERNET',
  `last_mod` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `egw_addressbook_tid_owner_access_n_family_n_given_email` (`tid`,`owner`,`access`,`n_family`,`n_given`,`email`),
  KEY `egw_addressbook_tid_cat_id_owner_access_n_family_n_given_email` (`tid`,`cat_id`,`owner`,`access`,`n_family`,`n_given`,`email`)
) ENGINE=MyISAM AUTO_INCREMENT=48454 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_addressbook_extra`
--

DROP TABLE IF EXISTS `egw_addressbook_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_addressbook_extra` (
  `contact_id` int(11) NOT NULL,
  `contact_owner` bigint(20) DEFAULT NULL,
  `contact_name` varchar(255) NOT NULL,
  `contact_value` text,
  PRIMARY KEY (`contact_id`,`contact_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_api_content_history`
--

DROP TABLE IF EXISTS `egw_api_content_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_api_content_history` (
  `sync_appname` varchar(60) NOT NULL,
  `sync_contentid` varchar(60) NOT NULL,
  `sync_added` datetime DEFAULT NULL,
  `sync_modified` datetime DEFAULT NULL,
  `sync_deleted` datetime DEFAULT NULL,
  `sync_id` int(11) NOT NULL AUTO_INCREMENT,
  `sync_guid` varchar(120) NOT NULL,
  `sync_changedby` int(11) NOT NULL,
  PRIMARY KEY (`sync_id`),
  KEY `egw_api_content_history_sync_added` (`sync_added`),
  KEY `egw_api_content_history_sync_modified` (`sync_modified`),
  KEY `egw_api_content_history_sync_deleted` (`sync_deleted`),
  KEY `egw_api_content_history_sync_guid` (`sync_guid`),
  KEY `egw_api_content_history_sync_changedby` (`sync_changedby`),
  KEY `egw_api_content_history_sync_appname_sync_contentid` (`sync_appname`,`sync_contentid`)
) ENGINE=MyISAM AUTO_INCREMENT=14402 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_app_sessions`
--

DROP TABLE IF EXISTS `egw_app_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_app_sessions` (
  `sessionid` varchar(128) NOT NULL,
  `loginid` int(11) NOT NULL,
  `app` varchar(25) NOT NULL,
  `location` varchar(128) NOT NULL,
  `content` longtext,
  `session_dla` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sessionid`,`loginid`,`app`,`location`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_applications`
--

DROP TABLE IF EXISTS `egw_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_applications` (
  `app_id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(25) NOT NULL,
  `app_enabled` int(11) NOT NULL,
  `app_order` int(11) NOT NULL,
  `app_tables` text,
  `app_version` varchar(20) NOT NULL DEFAULT '0.0',
  PRIMARY KEY (`app_id`),
  UNIQUE KEY `egw_applications_name` (`app_name`),
  KEY `egw_applications_enabled_order` (`app_enabled`,`app_order`)
) ENGINE=MyISAM AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_async`
--

DROP TABLE IF EXISTS `egw_async`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_async` (
  `async_id` varchar(255) NOT NULL,
  `async_next` int(11) NOT NULL,
  `async_times` varchar(255) NOT NULL,
  `async_method` varchar(80) NOT NULL,
  `async_data` text,
  `async_account_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`async_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_bookmarks`
--

DROP TABLE IF EXISTS `egw_bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_bookmarks` (
  `bm_id` int(11) NOT NULL AUTO_INCREMENT,
  `bm_owner` int(11) DEFAULT NULL,
  `bm_access` varchar(255) DEFAULT NULL,
  `bm_url` varchar(255) DEFAULT NULL,
  `bm_name` varchar(255) DEFAULT NULL,
  `bm_desc` text,
  `bm_keywords` varchar(255) DEFAULT NULL,
  `bm_category` int(11) DEFAULT NULL,
  `bm_rating` int(11) DEFAULT NULL,
  `bm_info` varchar(255) DEFAULT NULL,
  `bm_visits` int(11) DEFAULT NULL,
  PRIMARY KEY (`bm_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_cal`
--

DROP TABLE IF EXISTS `egw_cal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_cal` (
  `cal_id` int(11) NOT NULL AUTO_INCREMENT,
  `cal_uid` varchar(255) NOT NULL,
  `cal_owner` int(11) NOT NULL,
  `cal_category` varchar(30) DEFAULT NULL,
  `cal_modified` bigint(20) DEFAULT NULL,
  `cal_priority` smallint(6) NOT NULL DEFAULT '2',
  `cal_public` smallint(6) NOT NULL DEFAULT '1',
  `cal_title` varchar(255) NOT NULL DEFAULT '1',
  `cal_description` text,
  `cal_location` varchar(255) DEFAULT NULL,
  `cal_reference` int(11) NOT NULL DEFAULT '0',
  `cal_modifier` int(11) DEFAULT NULL,
  `cal_non_blocking` smallint(6) DEFAULT '0',
  PRIMARY KEY (`cal_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9744 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_cal_dates`
--

DROP TABLE IF EXISTS `egw_cal_dates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_cal_dates` (
  `cal_id` int(11) NOT NULL,
  `cal_start` bigint(20) NOT NULL,
  `cal_end` bigint(20) NOT NULL,
  PRIMARY KEY (`cal_id`,`cal_start`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_cal_extra`
--

DROP TABLE IF EXISTS `egw_cal_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_cal_extra` (
  `cal_id` int(11) NOT NULL,
  `cal_extra_name` varchar(40) NOT NULL,
  `cal_extra_value` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`cal_id`,`cal_extra_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_cal_holidays`
--

DROP TABLE IF EXISTS `egw_cal_holidays`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_cal_holidays` (
  `hol_id` int(11) NOT NULL AUTO_INCREMENT,
  `hol_locale` varchar(2) NOT NULL,
  `hol_name` varchar(50) NOT NULL,
  `hol_mday` bigint(20) NOT NULL DEFAULT '0',
  `hol_month_num` bigint(20) NOT NULL DEFAULT '0',
  `hol_occurence` bigint(20) NOT NULL DEFAULT '0',
  `hol_dow` bigint(20) NOT NULL DEFAULT '0',
  `hol_observance_rule` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`hol_id`),
  KEY `egw_cal_holidays_hol_locale` (`hol_locale`)
) ENGINE=MyISAM AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_cal_repeats`
--

DROP TABLE IF EXISTS `egw_cal_repeats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_cal_repeats` (
  `cal_id` int(11) NOT NULL,
  `recur_type` smallint(6) NOT NULL,
  `recur_enddate` bigint(20) DEFAULT NULL,
  `recur_interval` smallint(6) DEFAULT '1',
  `recur_data` smallint(6) DEFAULT '1',
  `recur_exception` text,
  PRIMARY KEY (`cal_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_cal_user`
--

DROP TABLE IF EXISTS `egw_cal_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_cal_user` (
  `cal_id` int(11) NOT NULL DEFAULT '0',
  `cal_recur_date` bigint(20) NOT NULL DEFAULT '0',
  `cal_user_type` varchar(1) NOT NULL DEFAULT 'u',
  `cal_user_id` int(11) NOT NULL DEFAULT '0',
  `cal_status` varchar(1) DEFAULT 'A',
  `cal_quantity` int(11) DEFAULT '1',
  PRIMARY KEY (`cal_id`,`cal_recur_date`,`cal_user_type`,`cal_user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_categories`
--

DROP TABLE IF EXISTS `egw_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_categories` (
  `cat_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_main` int(11) NOT NULL DEFAULT '0',
  `cat_parent` int(11) NOT NULL DEFAULT '0',
  `cat_level` smallint(6) NOT NULL DEFAULT '0',
  `cat_owner` int(11) NOT NULL DEFAULT '0',
  `cat_access` varchar(7) DEFAULT NULL,
  `cat_appname` varchar(50) NOT NULL,
  `cat_name` varchar(150) NOT NULL,
  `cat_description` varchar(255) NOT NULL,
  `cat_data` text,
  `last_mod` bigint(20) NOT NULL,
  PRIMARY KEY (`cat_id`),
  KEY `egw_categories_appname_owner_parent_level` (`cat_appname`,`cat_owner`,`cat_parent`,`cat_level`)
) ENGINE=MyISAM AUTO_INCREMENT=452 DEFAULT CHARSET=utf8;
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
  PRIMARY KEY (`config_app`,`config_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_contentmap`
--

DROP TABLE IF EXISTS `egw_contentmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_contentmap` (
  `map_id` varchar(128) NOT NULL,
  `map_guid` varchar(100) NOT NULL,
  `map_locuid` varchar(100) NOT NULL,
  `map_timestamp` datetime NOT NULL,
  `map_expired` tinyint(4) NOT NULL,
  PRIMARY KEY (`map_id`,`map_guid`,`map_locuid`),
  KEY `egw_contentmap_map_expired` (`map_expired`),
  KEY `egw_contentmap_map_id_map_locuid` (`map_id`,`map_locuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_emailadmin`
--

DROP TABLE IF EXISTS `egw_emailadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_emailadmin` (
  `ea_profile_id` int(11) NOT NULL AUTO_INCREMENT,
  `ea_smtp_server` varchar(80) DEFAULT NULL,
  `ea_smtp_type` int(11) DEFAULT NULL,
  `ea_smtp_port` int(11) DEFAULT NULL,
  `ea_smtp_auth` varchar(3) DEFAULT NULL,
  `ea_editforwardingaddress` varchar(3) DEFAULT NULL,
  `ea_smtp_ldap_server` varchar(80) DEFAULT NULL,
  `ea_smtp_ldap_basedn` varchar(200) DEFAULT NULL,
  `ea_smtp_ldap_admindn` varchar(200) DEFAULT NULL,
  `ea_smtp_ldap_adminpw` varchar(30) DEFAULT NULL,
  `ea_smtp_ldap_use_default` varchar(3) DEFAULT NULL,
  `ea_imap_server` varchar(80) DEFAULT NULL,
  `ea_imap_type` int(11) DEFAULT NULL,
  `ea_imap_port` int(11) DEFAULT NULL,
  `ea_imap_login_type` varchar(20) DEFAULT NULL,
  `ea_imap_tsl_auth` varchar(3) DEFAULT NULL,
  `ea_imap_tsl_encryption` varchar(3) DEFAULT NULL,
  `ea_imap_enable_cyrus` varchar(3) DEFAULT NULL,
  `ea_imap_admin_user` varchar(40) DEFAULT NULL,
  `ea_imap_admin_pw` varchar(40) DEFAULT NULL,
  `ea_imap_enable_sieve` varchar(3) DEFAULT NULL,
  `ea_imap_sieve_server` varchar(80) DEFAULT NULL,
  `ea_imap_sieve_port` int(11) DEFAULT NULL,
  `ea_description` varchar(200) DEFAULT NULL,
  `ea_default_domain` varchar(100) DEFAULT NULL,
  `ea_organisation_name` varchar(100) DEFAULT NULL,
  `ea_user_defined_accounts` varchar(3) DEFAULT NULL,
  `ea_imapoldcclient` varchar(3) DEFAULT NULL,
  `ea_order` int(11) DEFAULT NULL,
  `ea_appname` varchar(80) DEFAULT NULL,
  `ea_group` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`ea_profile_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_etemplate`
--

DROP TABLE IF EXISTS `egw_etemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_etemplate` (
  `et_name` varchar(80) NOT NULL,
  `et_template` varchar(20) NOT NULL DEFAULT '',
  `et_lang` varchar(5) NOT NULL DEFAULT '',
  `et_group` int(11) NOT NULL DEFAULT '0',
  `et_version` varchar(20) NOT NULL DEFAULT '',
  `et_data` text,
  `et_size` varchar(128) DEFAULT NULL,
  `et_style` text,
  `et_modified` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`et_name`,`et_template`,`et_lang`,`et_group`,`et_version`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_felamimail_cache`
--

DROP TABLE IF EXISTS `egw_felamimail_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_felamimail_cache` (
  `fmail_accountid` int(11) NOT NULL,
  `fmail_hostname` varchar(60) NOT NULL,
  `fmail_accountname` varchar(128) NOT NULL,
  `fmail_foldername` varchar(128) NOT NULL,
  `fmail_uid` int(11) NOT NULL,
  `fmail_subject` text,
  `fmail_striped_subject` text,
  `fmail_sender_name` varchar(120) DEFAULT NULL,
  `fmail_sender_address` varchar(120) DEFAULT NULL,
  `fmail_to_name` varchar(120) DEFAULT NULL,
  `fmail_to_address` varchar(120) DEFAULT NULL,
  `fmail_date` bigint(20) DEFAULT NULL,
  `fmail_size` int(11) DEFAULT NULL,
  `fmail_attachments` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`fmail_accountid`,`fmail_hostname`,`fmail_accountname`,`fmail_foldername`,`fmail_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_felamimail_displayfilter`
--

DROP TABLE IF EXISTS `egw_felamimail_displayfilter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_felamimail_displayfilter` (
  `fmail_filter_accountid` int(11) NOT NULL,
  `fmail_filter_data` text,
  PRIMARY KEY (`fmail_filter_accountid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_felamimail_folderstatus`
--

DROP TABLE IF EXISTS `egw_felamimail_folderstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_felamimail_folderstatus` (
  `fmail_accountid` int(11) NOT NULL,
  `fmail_hostname` varchar(60) NOT NULL,
  `fmail_accountname` varchar(128) NOT NULL,
  `fmail_foldername` varchar(128) NOT NULL,
  `fmail_messages` int(11) DEFAULT NULL,
  `fmail_recent` int(11) DEFAULT NULL,
  `fmail_unseen` int(11) DEFAULT NULL,
  `fmail_uidnext` int(11) DEFAULT NULL,
  `fmail_uidvalidity` int(11) DEFAULT NULL,
  PRIMARY KEY (`fmail_accountid`,`fmail_hostname`,`fmail_accountname`,`fmail_foldername`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_history_log`
--

DROP TABLE IF EXISTS `egw_history_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_history_log` (
  `history_id` int(11) NOT NULL AUTO_INCREMENT,
  `history_record_id` int(11) NOT NULL,
  `history_appname` varchar(64) NOT NULL,
  `history_owner` int(11) NOT NULL,
  `history_status` varchar(2) NOT NULL,
  `history_new_value` text,
  `history_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `history_old_value` text,
  PRIMARY KEY (`history_id`),
  KEY `egw_history_log_appname_record_id_status_timestamp` (`history_appname`,`history_record_id`,`history_status`,`history_timestamp`)
) ENGINE=MyISAM AUTO_INCREMENT=1515 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_hooks`
--

DROP TABLE IF EXISTS `egw_hooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_hooks` (
  `hook_id` int(11) NOT NULL AUTO_INCREMENT,
  `hook_appname` varchar(255) DEFAULT NULL,
  `hook_location` varchar(255) DEFAULT NULL,
  `hook_filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`hook_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3401 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_infolog`
--

DROP TABLE IF EXISTS `egw_infolog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_infolog` (
  `info_id` int(11) NOT NULL AUTO_INCREMENT,
  `info_type` varchar(40) NOT NULL DEFAULT 'task',
  `info_from` varchar(255) DEFAULT NULL,
  `info_addr` varchar(255) DEFAULT NULL,
  `info_subject` varchar(255) DEFAULT NULL,
  `info_des` text,
  `info_owner` int(11) NOT NULL,
  `info_responsible` varchar(255) NOT NULL DEFAULT '0',
  `info_access` varchar(10) DEFAULT 'public',
  `info_cat` int(11) NOT NULL DEFAULT '0',
  `info_datemodified` bigint(20) NOT NULL,
  `info_startdate` bigint(20) NOT NULL DEFAULT '0',
  `info_enddate` bigint(20) NOT NULL DEFAULT '0',
  `info_id_parent` int(11) NOT NULL DEFAULT '0',
  `info_planned_time` int(11) NOT NULL DEFAULT '0',
  `info_used_time` int(11) NOT NULL DEFAULT '0',
  `info_status` varchar(40) DEFAULT 'done',
  `info_confirm` varchar(10) DEFAULT 'not',
  `info_modifier` int(11) NOT NULL DEFAULT '0',
  `info_link_id` int(11) NOT NULL DEFAULT '0',
  `info_priority` smallint(6) DEFAULT '1',
  `pl_id` int(11) DEFAULT NULL,
  `info_price` double DEFAULT NULL,
  `info_percent` smallint(6) DEFAULT '0',
  `info_datecompleted` bigint(20) DEFAULT NULL,
  `info_location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`info_id`),
  KEY `egw_infolog_owner_responsible_status_startdate` (`info_owner`,`info_responsible`,`info_status`,`info_startdate`),
  KEY `egw_infolog_id_parent_owner_responsible_status_startdate` (`info_id_parent`,`info_owner`,`info_responsible`,`info_status`,`info_startdate`)
) ENGINE=MyISAM AUTO_INCREMENT=321 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_infolog_extra`
--

DROP TABLE IF EXISTS `egw_infolog_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_infolog_extra` (
  `info_id` int(11) NOT NULL,
  `info_extra_name` varchar(32) NOT NULL,
  `info_extra_value` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`info_id`,`info_extra_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_interserv`
--

DROP TABLE IF EXISTS `egw_interserv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_interserv` (
  `server_id` int(11) NOT NULL AUTO_INCREMENT,
  `server_name` varchar(64) DEFAULT NULL,
  `server_host` varchar(255) DEFAULT NULL,
  `server_url` varchar(255) DEFAULT NULL,
  `trust_level` int(11) DEFAULT NULL,
  `trust_rel` int(11) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `admin_name` varchar(255) DEFAULT NULL,
  `admin_email` varchar(255) DEFAULT NULL,
  `server_mode` varchar(16) NOT NULL DEFAULT 'xmlrpc',
  `server_security` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`server_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_lang`
--

DROP TABLE IF EXISTS `egw_lang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_lang` (
  `lang` varchar(5) NOT NULL DEFAULT '',
  `app_name` varchar(32) NOT NULL DEFAULT 'common',
  `message_id` varchar(128) NOT NULL DEFAULT '',
  `content` text,
  PRIMARY KEY (`lang`,`app_name`,`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_languages`
--

DROP TABLE IF EXISTS `egw_languages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_languages` (
  `lang_id` varchar(5) NOT NULL,
  `lang_name` varchar(50) NOT NULL,
  PRIMARY KEY (`lang_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_links`
--

DROP TABLE IF EXISTS `egw_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_links` (
  `link_id` int(11) NOT NULL AUTO_INCREMENT,
  `link_app1` varchar(25) NOT NULL,
  `link_id1` varchar(50) NOT NULL,
  `link_app2` varchar(25) NOT NULL,
  `link_id2` varchar(50) NOT NULL,
  `link_remark` varchar(100) DEFAULT NULL,
  `link_lastmod` int(11) NOT NULL,
  `link_owner` int(11) NOT NULL,
  PRIMARY KEY (`link_id`),
  KEY `egw_links_app1_id1_lastmod` (`link_app1`,`link_id1`,`link_lastmod`),
  KEY `egw_links_app2_id2_lastmod` (`link_app2`,`link_id2`,`link_lastmod`)
) ENGINE=MyISAM AUTO_INCREMENT=121 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_log`
--

DROP TABLE IF EXISTS `egw_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `log_date` datetime NOT NULL,
  `log_user` int(11) NOT NULL,
  `log_app` varchar(50) NOT NULL,
  `log_severity` varchar(1) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2147 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_log_msg`
--

DROP TABLE IF EXISTS `egw_log_msg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_log_msg` (
  `log_msg_log_id` int(11) NOT NULL,
  `log_msg_seq_no` int(11) NOT NULL,
  `log_msg_date` datetime NOT NULL,
  `log_msg_tx_fid` varchar(4) DEFAULT NULL,
  `log_msg_tx_id` varchar(4) DEFAULT NULL,
  `log_msg_severity` varchar(1) NOT NULL,
  `log_msg_code` varchar(30) NOT NULL,
  `log_msg_msg` text,
  `log_msg_parms` text,
  `log_msg_file` varchar(255) NOT NULL,
  `log_msg_line` int(11) NOT NULL,
  PRIMARY KEY (`log_msg_log_id`,`log_msg_seq_no`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_news`
--

DROP TABLE IF EXISTS `egw_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_news` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `news_date` bigint(20) DEFAULT NULL,
  `news_subject` varchar(255) DEFAULT NULL,
  `news_submittedby` varchar(255) DEFAULT NULL,
  `news_content` longblob,
  `news_begin` bigint(20) NOT NULL DEFAULT '0',
  `news_end` bigint(20) DEFAULT NULL,
  `news_cat` int(11) DEFAULT NULL,
  `news_teaser` varchar(255) DEFAULT NULL,
  `is_html` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`news_id`),
  KEY `egw_news_date` (`news_date`),
  KEY `egw_news_subject` (`news_subject`)
) ENGINE=MyISAM AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_news_export`
--

DROP TABLE IF EXISTS `egw_news_export`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_news_export` (
  `cat_id` int(11) NOT NULL,
  `export_type` smallint(6) DEFAULT NULL,
  `export_itemsyntax` smallint(6) DEFAULT NULL,
  `export_title` varchar(255) DEFAULT NULL,
  `export_link` varchar(255) DEFAULT NULL,
  `export_description` text,
  `export_img_title` varchar(255) DEFAULT NULL,
  `export_img_url` varchar(255) DEFAULT NULL,
  `export_img_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_nextid`
--

DROP TABLE IF EXISTS `egw_nextid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_nextid` (
  `id` int(11) DEFAULT NULL,
  `appname` varchar(25) NOT NULL,
  PRIMARY KEY (`appname`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_constraints`
--

DROP TABLE IF EXISTS `egw_pm_constraints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_constraints` (
  `pm_id` int(11) NOT NULL,
  `pe_id_end` int(11) NOT NULL,
  `pe_id_start` int(11) NOT NULL,
  `ms_id` int(11) NOT NULL,
  PRIMARY KEY (`pm_id`,`pe_id_end`,`pe_id_start`,`ms_id`),
  KEY `egw_pm_constraints_id_pe_id_start` (`pm_id`,`pe_id_start`),
  KEY `egw_pm_constraints_id_ms_id` (`pm_id`,`ms_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_elements`
--

DROP TABLE IF EXISTS `egw_pm_elements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_elements` (
  `pm_id` int(11) NOT NULL,
  `pe_id` int(11) NOT NULL,
  `pe_title` varchar(255) NOT NULL,
  `pe_completion` smallint(6) DEFAULT NULL,
  `pe_planned_time` int(11) DEFAULT NULL,
  `pe_used_time` int(11) DEFAULT NULL,
  `pe_planned_budget` decimal(20,2) DEFAULT NULL,
  `pe_used_budget` decimal(20,2) DEFAULT NULL,
  `pe_planned_start` bigint(20) DEFAULT NULL,
  `pe_real_start` bigint(20) DEFAULT NULL,
  `pe_planned_end` bigint(20) DEFAULT NULL,
  `pe_real_end` bigint(20) DEFAULT NULL,
  `pe_overwrite` int(11) NOT NULL DEFAULT '0',
  `pl_id` int(11) NOT NULL DEFAULT '0',
  `pe_synced` bigint(20) DEFAULT NULL,
  `pe_modified` bigint(20) NOT NULL,
  `pe_modifier` int(11) NOT NULL,
  `pe_status` varchar(8) NOT NULL DEFAULT 'new',
  `pe_unitprice` decimal(20,2) DEFAULT NULL,
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `pe_share` int(11) DEFAULT NULL,
  `pe_health` smallint(6) DEFAULT NULL,
  `pe_resources` varchar(255) DEFAULT NULL,
  `pe_details` text,
  `pe_planned_quantity` double DEFAULT NULL,
  `pe_used_quantity` double DEFAULT NULL,
  PRIMARY KEY (`pm_id`,`pe_id`),
  KEY `egw_pm_elements_id_pe_status` (`pm_id`,`pe_status`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_extra`
--

DROP TABLE IF EXISTS `egw_pm_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_extra` (
  `pm_id` int(11) NOT NULL,
  `pm_extra_name` varchar(40) NOT NULL,
  `pm_extra_value` text,
  PRIMARY KEY (`pm_id`,`pm_extra_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_members`
--

DROP TABLE IF EXISTS `egw_pm_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_members` (
  `pm_id` int(11) NOT NULL,
  `member_uid` int(11) NOT NULL,
  `role_id` int(11) DEFAULT '0',
  `member_availibility` double DEFAULT '100',
  PRIMARY KEY (`pm_id`,`member_uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_milestones`
--

DROP TABLE IF EXISTS `egw_pm_milestones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_milestones` (
  `ms_id` int(11) NOT NULL AUTO_INCREMENT,
  `pm_id` int(11) NOT NULL,
  `ms_date` bigint(20) NOT NULL,
  `ms_title` varchar(255) DEFAULT NULL,
  `ms_description` text,
  PRIMARY KEY (`ms_id`),
  KEY `egw_pm_milestones_id` (`pm_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_pricelist`
--

DROP TABLE IF EXISTS `egw_pm_pricelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_pricelist` (
  `pl_id` int(11) NOT NULL AUTO_INCREMENT,
  `pl_title` varchar(255) NOT NULL,
  `pl_description` text,
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `pl_unit` varchar(20) NOT NULL,
  PRIMARY KEY (`pl_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_prices`
--

DROP TABLE IF EXISTS `egw_pm_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_prices` (
  `pm_id` int(11) NOT NULL DEFAULT '0',
  `pl_id` int(11) NOT NULL,
  `pl_validsince` bigint(20) NOT NULL DEFAULT '0',
  `pl_price` double DEFAULT NULL,
  `pl_modifier` int(11) NOT NULL,
  `pl_modified` bigint(20) NOT NULL,
  `pl_customertitle` varchar(255) DEFAULT NULL,
  `pl_billable` smallint(6) DEFAULT '1',
  PRIMARY KEY (`pm_id`,`pl_id`,`pl_validsince`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_projects`
--

DROP TABLE IF EXISTS `egw_pm_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_projects` (
  `pm_id` int(11) NOT NULL AUTO_INCREMENT,
  `pm_number` varchar(64) NOT NULL,
  `pm_title` varchar(255) NOT NULL,
  `pm_description` text,
  `pm_creator` int(11) NOT NULL,
  `pm_created` bigint(20) NOT NULL,
  `pm_modifier` int(11) DEFAULT NULL,
  `pm_modified` bigint(20) DEFAULT NULL,
  `pm_planned_start` bigint(20) DEFAULT NULL,
  `pm_planned_end` bigint(20) DEFAULT NULL,
  `pm_real_start` bigint(20) DEFAULT NULL,
  `pm_real_end` bigint(20) DEFAULT NULL,
  `cat_id` int(11) DEFAULT '0',
  `pm_access` varchar(7) DEFAULT 'public',
  `pm_priority` smallint(6) DEFAULT '1',
  `pm_status` varchar(9) DEFAULT 'active',
  `pm_completion` smallint(6) DEFAULT '0',
  `pm_used_time` int(11) DEFAULT NULL,
  `pm_planned_time` int(11) DEFAULT NULL,
  `pm_used_budget` decimal(20,2) DEFAULT NULL,
  `pm_planned_budget` decimal(20,2) DEFAULT NULL,
  `pm_overwrite` int(11) DEFAULT '0',
  `pm_accounting_type` varchar(10) DEFAULT 'times',
  PRIMARY KEY (`pm_id`),
  UNIQUE KEY `egw_pm_projects_number` (`pm_number`),
  KEY `egw_pm_projects_title` (`pm_title`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_pm_roles`
--

DROP TABLE IF EXISTS `egw_pm_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_pm_roles` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `pm_id` int(11) DEFAULT '0',
  `role_title` varchar(80) NOT NULL,
  `role_description` varchar(255) DEFAULT NULL,
  `role_acl` int(11) NOT NULL,
  PRIMARY KEY (`role_id`),
  KEY `egw_pm_roles_id` (`pm_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_preferences`
--

DROP TABLE IF EXISTS `egw_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_preferences` (
  `preference_owner` int(11) NOT NULL,
  `preference_app` varchar(25) NOT NULL,
  `preference_value` text,
  PRIMARY KEY (`preference_owner`,`preference_app`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_reg_accounts`
--

DROP TABLE IF EXISTS `egw_reg_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_reg_accounts` (
  `reg_id` varchar(32) NOT NULL,
  `reg_lid` varchar(255) NOT NULL,
  `reg_info` text,
  `reg_dla` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_reg_fields`
--

DROP TABLE IF EXISTS `egw_reg_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_reg_fields` (
  `field_name` varchar(255) NOT NULL,
  `field_text` text,
  `field_type` varchar(255) NOT NULL,
  `field_values` text,
  `field_required` varchar(1) NOT NULL,
  `field_order` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_resources`
--

DROP TABLE IF EXISTS `egw_resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_resources` (
  `res_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `short_description` varchar(100) DEFAULT NULL,
  `cat_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT '1',
  `useable` int(11) DEFAULT '1',
  `location` varchar(100) DEFAULT NULL,
  `bookable` varchar(1) DEFAULT NULL,
  `buyable` varchar(1) DEFAULT NULL,
  `prize` varchar(200) DEFAULT NULL,
  `long_description` text,
  `picture_src` varchar(20) DEFAULT NULL,
  `accessory_of` int(11) DEFAULT '-1',
  `storage_info` varchar(200) DEFAULT NULL,
  `inventory_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`res_id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_resources_extra`
--

DROP TABLE IF EXISTS `egw_resources_extra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_resources_extra` (
  `extra_id` int(11) NOT NULL,
  `extra_name` varchar(40) NOT NULL,
  `extra_owner` int(11) NOT NULL DEFAULT '-1',
  `extra_value` varchar(255) NOT NULL,
  PRIMARY KEY (`extra_id`,`extra_name`,`extra_owner`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sessions`
--

DROP TABLE IF EXISTS `egw_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sessions` (
  `session_id` varchar(128) NOT NULL,
  `session_lid` varchar(128) DEFAULT NULL,
  `session_ip` varchar(40) DEFAULT NULL,
  `session_logintime` bigint(20) DEFAULT NULL,
  `session_dla` bigint(20) DEFAULT NULL,
  `session_action` varchar(255) DEFAULT NULL,
  `session_flags` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`session_id`),
  KEY `egw_sessions_session_flags_session_dla` (`session_flags`,`session_dla`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_active_modules`
--

DROP TABLE IF EXISTS `egw_sitemgr_active_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_active_modules` (
  `area` varchar(50) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `module_id` int(11) NOT NULL,
  PRIMARY KEY (`area`,`cat_id`,`module_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_blocks`
--

DROP TABLE IF EXISTS `egw_sitemgr_blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_blocks` (
  `block_id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(50) DEFAULT NULL,
  `cat_id` int(11) DEFAULT NULL,
  `page_id` int(11) DEFAULT NULL,
  `module_id` int(11) NOT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `viewable` int(11) DEFAULT NULL,
  PRIMARY KEY (`block_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_blocks_lang`
--

DROP TABLE IF EXISTS `egw_sitemgr_blocks_lang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_blocks_lang` (
  `block_id` int(11) NOT NULL,
  `lang` varchar(5) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`block_id`,`lang`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_categories_lang`
--

DROP TABLE IF EXISTS `egw_sitemgr_categories_lang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_categories_lang` (
  `cat_id` int(11) NOT NULL,
  `lang` varchar(5) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cat_id`,`lang`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_categories_state`
--

DROP TABLE IF EXISTS `egw_sitemgr_categories_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_categories_state` (
  `cat_id` int(11) NOT NULL,
  `state` smallint(6) DEFAULT NULL,
  `index_page_id` int(11) DEFAULT '0',
  PRIMARY KEY (`cat_id`),
  KEY `egw_sitemgr_categories_state_cat_id_state` (`cat_id`,`state`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_content`
--

DROP TABLE IF EXISTS `egw_sitemgr_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_content` (
  `version_id` int(11) NOT NULL AUTO_INCREMENT,
  `block_id` int(11) NOT NULL,
  `arguments` text,
  `state` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`version_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_content_lang`
--

DROP TABLE IF EXISTS `egw_sitemgr_content_lang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_content_lang` (
  `version_id` int(11) NOT NULL,
  `lang` varchar(5) NOT NULL,
  `arguments_lang` text,
  PRIMARY KEY (`version_id`,`lang`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_modules`
--

DROP TABLE IF EXISTS `egw_sitemgr_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_modules` (
  `module_id` int(11) NOT NULL AUTO_INCREMENT,
  `module_name` varchar(25) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`module_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_notifications`
--

DROP TABLE IF EXISTS `egw_sitemgr_notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_notifications` (
  `notification_id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `site_language` varchar(3) NOT NULL DEFAULT 'all',
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`notification_id`),
  KEY `egw_sitemgr_notifications_email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_notify_messages`
--

DROP TABLE IF EXISTS `egw_sitemgr_notify_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_notify_messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` int(11) NOT NULL,
  `language` varchar(3) DEFAULT NULL,
  `message` text,
  `subject` text,
  PRIMARY KEY (`message_id`),
  UNIQUE KEY `egw_sitemgr_notify_messages_id_language` (`site_id`,`language`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_pages`
--

DROP TABLE IF EXISTS `egw_sitemgr_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_pages` (
  `page_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL,
  `hide_page` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `state` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`page_id`),
  KEY `egw_sitemgr_pages_cat_id` (`cat_id`),
  KEY `egw_sitemgr_pages_state_cat_id_sort_order` (`state`,`cat_id`,`sort_order`),
  KEY `egw_sitemgr_pages_name_cat_id` (`name`,`cat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_pages_lang`
--

DROP TABLE IF EXISTS `egw_sitemgr_pages_lang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_pages_lang` (
  `page_id` int(11) NOT NULL,
  `lang` varchar(5) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `subtitle` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`page_id`,`lang`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_properties`
--

DROP TABLE IF EXISTS `egw_sitemgr_properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_properties` (
  `area` varchar(50) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `module_id` int(11) NOT NULL,
  `properties` text,
  PRIMARY KEY (`area`,`cat_id`,`module_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_sitemgr_sites`
--

DROP TABLE IF EXISTS `egw_sitemgr_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_sitemgr_sites` (
  `site_id` int(11) NOT NULL,
  `site_name` varchar(255) DEFAULT NULL,
  `site_url` varchar(255) DEFAULT NULL,
  `site_dir` varchar(255) DEFAULT NULL,
  `themesel` varchar(50) DEFAULT NULL,
  `site_languages` varchar(50) DEFAULT NULL,
  `home_page_id` int(11) DEFAULT NULL,
  `anonymous_user` varchar(50) DEFAULT NULL,
  `anonymous_passwd` varchar(50) DEFAULT NULL,
  `upload_dir` varchar(255) DEFAULT NULL,
  `upload_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`site_id`),
  KEY `egw_sitemgr_sites_url` (`site_url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_syncmldevinfo`
--

DROP TABLE IF EXISTS `egw_syncmldevinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_syncmldevinfo` (
  `dev_id` varchar(255) NOT NULL,
  `dev_dtdversion` varchar(10) NOT NULL,
  `dev_numberofchanges` tinyint(4) NOT NULL,
  `dev_largeobjs` tinyint(4) NOT NULL,
  `dev_swversion` varchar(100) NOT NULL,
  `dev_oem` varchar(100) NOT NULL,
  `dev_model` varchar(100) NOT NULL,
  `dev_manufacturer` varchar(100) NOT NULL,
  `dev_devicetype` varchar(100) NOT NULL,
  `dev_deviceid` varchar(100) NOT NULL,
  `dev_datastore` text,
  PRIMARY KEY (`dev_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_syncmlsummary`
--

DROP TABLE IF EXISTS `egw_syncmlsummary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_syncmlsummary` (
  `dev_id` varchar(255) NOT NULL,
  `sync_path` varchar(100) NOT NULL,
  `sync_serverts` varchar(20) NOT NULL,
  `sync_clientts` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_timesheet`
--

DROP TABLE IF EXISTS `egw_timesheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_timesheet` (
  `ts_id` int(11) NOT NULL AUTO_INCREMENT,
  `ts_project` varchar(80) DEFAULT NULL,
  `ts_title` varchar(80) NOT NULL,
  `ts_description` text,
  `ts_start` bigint(20) NOT NULL,
  `ts_duration` bigint(20) NOT NULL DEFAULT '0',
  `ts_quantity` double NOT NULL,
  `ts_unitprice` double DEFAULT NULL,
  `cat_id` int(11) DEFAULT '0',
  `ts_owner` int(11) NOT NULL,
  `ts_modified` bigint(20) NOT NULL,
  `ts_modifier` int(11) NOT NULL,
  `pl_id` int(11) DEFAULT '0',
  PRIMARY KEY (`ts_id`),
  KEY `egw_timesheet_ts_project` (`ts_project`),
  KEY `egw_timesheet_ts_owner` (`ts_owner`)
) ENGINE=MyISAM AUTO_INCREMENT=121 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_vfs`
--

DROP TABLE IF EXISTS `egw_vfs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_vfs` (
  `vfs_file_id` int(11) NOT NULL AUTO_INCREMENT,
  `vfs_owner_id` int(11) NOT NULL,
  `vfs_createdby_id` int(11) DEFAULT NULL,
  `vfs_modifiedby_id` int(11) DEFAULT NULL,
  `vfs_created` date NOT NULL DEFAULT '1970-01-01',
  `vfs_modified` date DEFAULT NULL,
  `vfs_size` int(11) DEFAULT NULL,
  `vfs_mime_type` varchar(64) DEFAULT NULL,
  `vfs_deleteable` varchar(1) DEFAULT 'Y',
  `vfs_comment` varchar(255) DEFAULT NULL,
  `vfs_app` varchar(25) DEFAULT NULL,
  `vfs_directory` varchar(233) DEFAULT NULL,
  `vfs_name` varchar(100) NOT NULL,
  `vfs_link_directory` varchar(255) DEFAULT NULL,
  `vfs_link_name` varchar(128) DEFAULT NULL,
  `vfs_version` varchar(30) NOT NULL DEFAULT '0.0.0.0',
  `vfs_content` text,
  PRIMARY KEY (`vfs_file_id`),
  KEY `egw_vfs_directory_name` (`vfs_directory`,`vfs_name`)
) ENGINE=MyISAM AUTO_INCREMENT=1085 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_activities`
--

DROP TABLE IF EXISTS `egw_wf_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_activities` (
  `wf_activity_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_name` varchar(80) DEFAULT NULL,
  `wf_normalized_name` varchar(80) DEFAULT NULL,
  `wf_p_id` int(11) NOT NULL,
  `wf_type` varchar(25) DEFAULT NULL,
  `wf_is_autorouted` varchar(1) DEFAULT NULL,
  `wf_flow_num` int(11) DEFAULT NULL,
  `wf_is_interactive` varchar(1) DEFAULT NULL,
  `wf_last_modif` int(11) DEFAULT NULL,
  `wf_description` text,
  `wf_default_user` varchar(200) DEFAULT '*',
  PRIMARY KEY (`wf_activity_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_activity_agents`
--

DROP TABLE IF EXISTS `egw_wf_activity_agents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_activity_agents` (
  `wf_activity_id` int(11) NOT NULL,
  `wf_agent_id` int(11) NOT NULL,
  `wf_agent_type` varchar(15) NOT NULL,
  PRIMARY KEY (`wf_activity_id`,`wf_agent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_activity_roles`
--

DROP TABLE IF EXISTS `egw_wf_activity_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_activity_roles` (
  `wf_activity_id` int(11) NOT NULL,
  `wf_role_id` int(11) NOT NULL,
  `wf_readonly` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`wf_activity_id`,`wf_role_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_agent_mail_smtp`
--

DROP TABLE IF EXISTS `egw_wf_agent_mail_smtp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_agent_mail_smtp` (
  `wf_agent_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_to` varchar(255) NOT NULL DEFAULT '%roles%',
  `wf_cc` varchar(255) DEFAULT NULL,
  `wf_bcc` varchar(255) DEFAULT NULL,
  `wf_from` varchar(255) DEFAULT '%user%',
  `wf_replyTo` varchar(255) DEFAULT '%user%',
  `wf_subject` varchar(255) DEFAULT NULL,
  `wf_message` text,
  `wf_send_mode` int(11) DEFAULT '0',
  PRIMARY KEY (`wf_agent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_instance_activities`
--

DROP TABLE IF EXISTS `egw_wf_instance_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_instance_activities` (
  `wf_instance_id` int(11) NOT NULL,
  `wf_activity_id` int(11) NOT NULL,
  `wf_started` int(11) NOT NULL,
  `wf_ended` int(11) DEFAULT NULL,
  `wf_user` varchar(200) DEFAULT NULL,
  `wf_status` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`wf_instance_id`,`wf_activity_id`),
  KEY `egw_wf_instance_activities_activity_id` (`wf_activity_id`),
  KEY `egw_wf_instance_activities_id` (`wf_instance_id`),
  KEY `egw_wf_instance_activities_user` (`wf_user`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_instance_supplements`
--

DROP TABLE IF EXISTS `egw_wf_instance_supplements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_instance_supplements` (
  `wf_supplement_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_supplement_type` varchar(50) DEFAULT NULL,
  `wf_supplement_name` varchar(100) DEFAULT NULL,
  `wf_supplement_value` text,
  `wf_workitem_id` int(11) DEFAULT NULL,
  `wf_supplement_blob` longblob,
  PRIMARY KEY (`wf_supplement_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_instances`
--

DROP TABLE IF EXISTS `egw_wf_instances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_instances` (
  `wf_instance_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_p_id` int(11) NOT NULL,
  `wf_started` int(11) DEFAULT NULL,
  `wf_owner` varchar(200) DEFAULT NULL,
  `wf_next_activity` longblob,
  `wf_next_user` varchar(200) DEFAULT NULL,
  `wf_ended` int(11) DEFAULT NULL,
  `wf_status` varchar(25) DEFAULT NULL,
  `wf_priority` int(11) DEFAULT '0',
  `wf_properties` longblob,
  `wf_name` varchar(120) DEFAULT NULL,
  `wf_category` int(11) DEFAULT NULL,
  PRIMARY KEY (`wf_instance_id`),
  KEY `egw_wf_instances_owner` (`wf_owner`),
  KEY `egw_wf_instances_status` (`wf_status`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_process_config`
--

DROP TABLE IF EXISTS `egw_wf_process_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_process_config` (
  `wf_p_id` int(11) NOT NULL,
  `wf_config_name` varchar(255) NOT NULL,
  `wf_config_value` text,
  `wf_config_value_int` int(11) DEFAULT NULL,
  PRIMARY KEY (`wf_p_id`,`wf_config_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_processes`
--

DROP TABLE IF EXISTS `egw_wf_processes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_processes` (
  `wf_p_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_name` varchar(80) DEFAULT NULL,
  `wf_is_valid` varchar(1) DEFAULT NULL,
  `wf_is_active` varchar(1) DEFAULT NULL,
  `wf_version` varchar(12) DEFAULT NULL,
  `wf_description` text,
  `wf_last_modif` int(11) DEFAULT NULL,
  `wf_normalized_name` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`wf_p_id`),
  KEY `egw_wf_processes_id_is_active` (`wf_p_id`,`wf_is_active`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_roles`
--

DROP TABLE IF EXISTS `egw_wf_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_roles` (
  `wf_role_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_p_id` int(11) NOT NULL,
  `wf_last_modif` int(11) DEFAULT NULL,
  `wf_name` varchar(80) DEFAULT NULL,
  `wf_description` text,
  PRIMARY KEY (`wf_role_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_transitions`
--

DROP TABLE IF EXISTS `egw_wf_transitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_transitions` (
  `wf_p_id` int(11) NOT NULL,
  `wf_act_from_id` int(11) NOT NULL,
  `wf_act_to_id` int(11) NOT NULL,
  PRIMARY KEY (`wf_act_from_id`,`wf_act_to_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_user_roles`
--

DROP TABLE IF EXISTS `egw_wf_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_user_roles` (
  `wf_role_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_p_id` int(11) NOT NULL,
  `wf_user` varchar(200) NOT NULL,
  `wf_account_type` varchar(1) NOT NULL DEFAULT 'u',
  PRIMARY KEY (`wf_role_id`,`wf_user`,`wf_account_type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wf_workitems`
--

DROP TABLE IF EXISTS `egw_wf_workitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wf_workitems` (
  `wf_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `wf_instance_id` int(11) NOT NULL,
  `wf_order_id` int(11) NOT NULL,
  `wf_properties` longblob,
  `wf_activity_id` int(11) NOT NULL,
  `wf_started` int(11) DEFAULT NULL,
  `wf_ended` int(11) DEFAULT NULL,
  `wf_user` varchar(200) DEFAULT NULL,
  `wf_note` text,
  `wf_action` text,
  PRIMARY KEY (`wf_item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wiki_interwiki`
--

DROP TABLE IF EXISTS `egw_wiki_interwiki`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wiki_interwiki` (
  `wiki_id` int(11) NOT NULL DEFAULT '0',
  `interwiki_prefix` varchar(80) NOT NULL,
  `wiki_name` varchar(80) NOT NULL,
  `wiki_lang` varchar(5) NOT NULL,
  `interwiki_url` varchar(255) NOT NULL,
  PRIMARY KEY (`wiki_id`,`interwiki_prefix`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wiki_links`
--

DROP TABLE IF EXISTS `egw_wiki_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wiki_links` (
  `wiki_id` smallint(6) NOT NULL DEFAULT '0',
  `wiki_name` varchar(80) NOT NULL,
  `wiki_lang` varchar(5) NOT NULL,
  `wiki_link` varchar(80) NOT NULL,
  `wiki_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`wiki_id`,`wiki_name`,`wiki_lang`,`wiki_link`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wiki_pages`
--

DROP TABLE IF EXISTS `egw_wiki_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wiki_pages` (
  `wiki_id` smallint(6) NOT NULL DEFAULT '0',
  `wiki_name` varchar(80) NOT NULL,
  `wiki_lang` varchar(5) NOT NULL,
  `wiki_version` int(11) NOT NULL DEFAULT '1',
  `wiki_time` int(11) DEFAULT NULL,
  `wiki_supercede` int(11) DEFAULT NULL,
  `wiki_readable` int(11) NOT NULL DEFAULT '0',
  `wiki_writable` int(11) NOT NULL DEFAULT '0',
  `wiki_username` varchar(80) DEFAULT NULL,
  `wiki_hostname` varchar(80) NOT NULL,
  `wiki_comment` varchar(80) NOT NULL,
  `wiki_title` varchar(80) DEFAULT NULL,
  `wiki_body` text,
  PRIMARY KEY (`wiki_id`,`wiki_name`,`wiki_lang`,`wiki_version`),
  KEY `egw_wiki_pages_title` (`wiki_title`),
  FULLTEXT KEY `egw_wiki_pages_body` (`wiki_body`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wiki_rate`
--

DROP TABLE IF EXISTS `egw_wiki_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wiki_rate` (
  `wiki_rate_ip` varchar(20) NOT NULL,
  `wiki_rate_time` int(11) DEFAULT NULL,
  `wiki_rate_viewLimit` smallint(6) DEFAULT NULL,
  `wiki_rate_searchLimit` smallint(6) DEFAULT NULL,
  `wiki_rate_editLimit` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`wiki_rate_ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wiki_remote_pages`
--

DROP TABLE IF EXISTS `egw_wiki_remote_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wiki_remote_pages` (
  `wiki_remote_page` varchar(80) NOT NULL,
  `wiki_remote_site` varchar(80) NOT NULL,
  PRIMARY KEY (`wiki_remote_page`,`wiki_remote_site`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `egw_wiki_sisterwiki`
--

DROP TABLE IF EXISTS `egw_wiki_sisterwiki`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `egw_wiki_sisterwiki` (
  `wiki_id` int(11) NOT NULL DEFAULT '0',
  `sisterwiki_prefix` varchar(80) NOT NULL,
  `wiki_name` varchar(80) NOT NULL,
  `wiki_lang` varchar(5) NOT NULL,
  `sisterwiki_url` varchar(255) NOT NULL,
  PRIMARY KEY (`wiki_id`,`sisterwiki_prefix`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `migration_version`
--

DROP TABLE IF EXISTS `migration_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `migration_version` (
  `version` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_articles`
--

DROP TABLE IF EXISTS `phpgw_kb_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_articles` (
  `art_id` int(11) NOT NULL AUTO_INCREMENT,
  `q_id` bigint(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `topic` varchar(255) NOT NULL,
  `text` text,
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `published` smallint(6) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL DEFAULT '0',
  `views` int(11) NOT NULL DEFAULT '0',
  `created` int(11) DEFAULT NULL,
  `modified` int(11) DEFAULT NULL,
  `modified_user_id` int(11) NOT NULL,
  `votes_1` int(11) NOT NULL,
  `votes_2` int(11) NOT NULL,
  `votes_3` int(11) NOT NULL,
  `votes_4` int(11) NOT NULL,
  `votes_5` int(11) NOT NULL,
  PRIMARY KEY (`art_id`)
) ENGINE=MyISAM AUTO_INCREMENT=398 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_comment`
--

DROP TABLE IF EXISTS `phpgw_kb_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_comment` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `comment` text,
  `entered` int(11) DEFAULT NULL,
  `art_id` int(11) NOT NULL,
  `published` smallint(6) NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `phpgw_kb_comment_art_id` (`art_id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_files`
--

DROP TABLE IF EXISTS `phpgw_kb_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_files` (
  `art_id` int(11) NOT NULL,
  `art_file` varchar(255) NOT NULL,
  `art_file_comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`art_id`,`art_file`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_questions`
--

DROP TABLE IF EXISTS `phpgw_kb_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_questions` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `summary` text,
  `details` text,
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `creation` int(11) DEFAULT NULL,
  `published` smallint(6) NOT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_ratings`
--

DROP TABLE IF EXISTS `phpgw_kb_ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_ratings` (
  `user_id` int(11) NOT NULL,
  `art_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`art_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_related_art`
--

DROP TABLE IF EXISTS `phpgw_kb_related_art`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_related_art` (
  `art_id` int(11) NOT NULL,
  `related_art_id` int(11) NOT NULL,
  PRIMARY KEY (`art_id`,`related_art_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_search`
--

DROP TABLE IF EXISTS `phpgw_kb_search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_search` (
  `keyword` varchar(30) NOT NULL,
  `art_id` int(11) NOT NULL,
  `score` bigint(20) NOT NULL,
  PRIMARY KEY (`keyword`,`art_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_kb_urls`
--

DROP TABLE IF EXISTS `phpgw_kb_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_kb_urls` (
  `art_id` int(11) NOT NULL,
  `art_url` varchar(255) NOT NULL,
  `art_url_title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`art_id`,`art_url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_ACLs`
--

DROP TABLE IF EXISTS `phpgw_mydms_ACLs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_ACLs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target` int(11) NOT NULL DEFAULT '0',
  `targetType` smallint(6) NOT NULL DEFAULT '0',
  `userID` int(11) NOT NULL DEFAULT '-1',
  `groupID` int(11) NOT NULL DEFAULT '-1',
  `mode` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_DocumentContent`
--

DROP TABLE IF EXISTS `phpgw_mydms_DocumentContent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_DocumentContent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document` int(11) DEFAULT '0',
  `version` smallint(6) DEFAULT '0',
  `comment` text,
  `date` bigint(20) DEFAULT '0',
  `createdBy` int(11) DEFAULT '0',
  `dir` varchar(10) NOT NULL DEFAULT ' ',
  `orgFileName` varchar(150) NOT NULL DEFAULT ' ',
  `fileType` varchar(10) NOT NULL DEFAULT ' ',
  `mimeType` varchar(70) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_DocumentLinks`
--

DROP TABLE IF EXISTS `phpgw_mydms_DocumentLinks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_DocumentLinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `document` int(11) NOT NULL DEFAULT '0',
  `target` int(11) NOT NULL DEFAULT '0',
  `userID` int(11) NOT NULL DEFAULT '0',
  `public` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Documents`
--

DROP TABLE IF EXISTS `phpgw_mydms_Documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Documents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `comment` text,
  `date` bigint(20) DEFAULT '0',
  `expires` bigint(20) DEFAULT '0',
  `owner` int(11) DEFAULT '0',
  `folder` int(11) DEFAULT '0',
  `inheritAccess` tinyint(4) NOT NULL DEFAULT '1',
  `defaultAccess` smallint(6) NOT NULL DEFAULT '0',
  `locked` int(11) NOT NULL DEFAULT '-1',
  `keywords` text,
  `sequence` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Folders`
--

DROP TABLE IF EXISTS `phpgw_mydms_Folders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Folders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(70) DEFAULT NULL,
  `parent` int(11) DEFAULT '0',
  `comment` text,
  `owner` int(11) DEFAULT '0',
  `inheritAccess` tinyint(4) NOT NULL DEFAULT '1',
  `defaultAccess` smallint(6) NOT NULL DEFAULT '0',
  `sequence` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_GroupMembers`
--

DROP TABLE IF EXISTS `phpgw_mydms_GroupMembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_GroupMembers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupID` int(11) NOT NULL DEFAULT '0',
  `userID` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Groups`
--

DROP TABLE IF EXISTS `phpgw_mydms_Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_KeywordCategories`
--

DROP TABLE IF EXISTS `phpgw_mydms_KeywordCategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_KeywordCategories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `owner` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Keywords`
--

DROP TABLE IF EXISTS `phpgw_mydms_Keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` int(11) NOT NULL DEFAULT '0',
  `keywords` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Notify`
--

DROP TABLE IF EXISTS `phpgw_mydms_Notify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Notify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target` int(11) NOT NULL DEFAULT '0',
  `targetType` int(11) NOT NULL DEFAULT '0',
  `userID` int(11) NOT NULL DEFAULT '-1',
  `groupID` int(11) NOT NULL DEFAULT '-1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Sessions`
--

DROP TABLE IF EXISTS `phpgw_mydms_Sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Sessions` (
  `id` varchar(50) NOT NULL,
  `userID` int(11) NOT NULL DEFAULT '0',
  `lastAccess` int(11) NOT NULL DEFAULT '0',
  `theme` varchar(30) NOT NULL,
  `language` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_UserImages`
--

DROP TABLE IF EXISTS `phpgw_mydms_UserImages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_UserImages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) NOT NULL DEFAULT '0',
  `image` longblob,
  `mimeType` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_mydms_Users`
--

DROP TABLE IF EXISTS `phpgw_mydms_Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_mydms_Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(50) DEFAULT NULL,
  `pwd` varchar(50) DEFAULT NULL,
  `fullName` varchar(100) DEFAULT NULL,
  `email` varchar(70) DEFAULT NULL,
  `comment` text,
  `isAdmin` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_polls_data`
--

DROP TABLE IF EXISTS `phpgw_polls_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_polls_data` (
  `poll_id` int(11) NOT NULL,
  `option_text` varchar(100) NOT NULL,
  `option_count` int(11) NOT NULL,
  `vote_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_polls_desc`
--

DROP TABLE IF EXISTS `phpgw_polls_desc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_polls_desc` (
  `poll_id` int(11) NOT NULL AUTO_INCREMENT,
  `poll_title` varchar(100) NOT NULL,
  `poll_timestamp` int(11) NOT NULL,
  PRIMARY KEY (`poll_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_polls_settings`
--

DROP TABLE IF EXISTS `phpgw_polls_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_polls_settings` (
  `setting_name` varchar(255) DEFAULT NULL,
  `setting_value` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_polls_user`
--

DROP TABLE IF EXISTS `phpgw_polls_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_polls_user` (
  `poll_id` int(11) NOT NULL,
  `vote_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `vote_timestamp` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_customfields`
--

DROP TABLE IF EXISTS `phpgw_vfs2_customfields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_customfields` (
  `customfield_id` int(11) NOT NULL AUTO_INCREMENT,
  `customfield_name` varchar(60) NOT NULL,
  `customfield_description` varchar(255) DEFAULT NULL,
  `customfield_type` varchar(20) NOT NULL,
  `customfield_precision` int(11) DEFAULT NULL,
  `customfield_active` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`customfield_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_customfields_data`
--

DROP TABLE IF EXISTS `phpgw_vfs2_customfields_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_customfields_data` (
  `file_id` int(11) NOT NULL,
  `customfield_id` int(11) NOT NULL,
  `data` text,
  PRIMARY KEY (`file_id`,`customfield_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_files`
--

DROP TABLE IF EXISTS `phpgw_vfs2_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_files` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `mime_id` int(11) DEFAULT NULL,
  `owner_id` int(11) NOT NULL,
  `createdby_id` int(11) DEFAULT NULL,
  `modifiedby_id` int(11) DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `modified` datetime DEFAULT NULL,
  `size` bigint(20) DEFAULT NULL,
  `deleteable` varchar(1) DEFAULT 'Y',
  `comment` varchar(255) DEFAULT NULL,
  `app` varchar(25) DEFAULT NULL,
  `directory` varchar(255) DEFAULT NULL,
  `name` varchar(64) NOT NULL,
  `link_directory` varchar(255) DEFAULT NULL,
  `link_name` varchar(128) DEFAULT NULL,
  `version` varchar(30) NOT NULL DEFAULT '0.0.0.0',
  `content` text,
  `is_backup` varchar(1) NOT NULL DEFAULT 'N',
  `shared` varchar(1) NOT NULL DEFAULT 'N',
  `proper_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`file_id`),
  KEY `phpgw_vfs2_files_directory_name` (`directory`,`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_mimetypes`
--

DROP TABLE IF EXISTS `phpgw_vfs2_mimetypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_mimetypes` (
  `mime_id` int(11) NOT NULL AUTO_INCREMENT,
  `extension` varchar(10) NOT NULL,
  `mime` varchar(50) NOT NULL,
  `mime_magic` varchar(255) DEFAULT NULL,
  `friendly` varchar(50) NOT NULL,
  `image` longblob,
  `proper_id` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`mime_id`)
) ENGINE=MyISAM AUTO_INCREMENT=149 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_prefixes`
--

DROP TABLE IF EXISTS `phpgw_vfs2_prefixes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_prefixes` (
  `prefix_id` int(11) NOT NULL AUTO_INCREMENT,
  `prefix` varchar(8) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `prefix_description` varchar(30) DEFAULT NULL,
  `prefix_type` varchar(1) NOT NULL DEFAULT 'p',
  PRIMARY KEY (`prefix_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_quota`
--

DROP TABLE IF EXISTS `phpgw_vfs2_quota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_quota` (
  `account_id` int(11) NOT NULL,
  `quota` int(11) NOT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_shares`
--

DROP TABLE IF EXISTS `phpgw_vfs2_shares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_shares` (
  `account_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  `acl_rights` int(11) NOT NULL,
  PRIMARY KEY (`account_id`,`file_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phpgw_vfs2_versioning`
--

DROP TABLE IF EXISTS `phpgw_vfs2_versioning`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `phpgw_vfs2_versioning` (
  `version_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL,
  `operation` int(11) NOT NULL,
  `modifiedby_id` int(11) NOT NULL,
  `modified` datetime NOT NULL,
  `version` varchar(30) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  `backup_file_id` int(11) DEFAULT NULL,
  `backup_content` text,
  `src` varchar(255) DEFAULT NULL,
  `dest` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`version_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `portpara_newsletter`
--

DROP TABLE IF EXISTS `portpara_newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `portpara_newsletter` (
  `id_newsletter` int(11) NOT NULL AUTO_INCREMENT,
  `sujet_newsletter` varchar(75) NOT NULL,
  `text_newsletter` text,
  `footer_newsletter` text,
  PRIMARY KEY (`id_newsletter`)
) ENGINE=MyISAM AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `portpara_nl_user`
--

DROP TABLE IF EXISTS `portpara_nl_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `portpara_nl_user` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `email_user` varchar(45) NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=MyISAM AUTO_INCREMENT=339 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symf_administrateurs`
--

DROP TABLE IF EXISTS `symf_administrateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symf_administrateurs` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint(20) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symf_correspondance_compta`
--

DROP TABLE IF EXISTS `symf_correspondance_compta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symf_correspondance_compta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `compagnie_id` bigint(20) DEFAULT NULL,
  `compta_id` text COLLATE utf8_unicode_ci,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=162 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symf_facture_manuelle`
--

DROP TABLE IF EXISTS `symf_facture_manuelle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symf_facture_manuelle` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sequence_id` bigint(20) NOT NULL,
  `libelle` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `montant_ht` decimal(18,2) DEFAULT NULL,
  `tva` decimal(18,2) DEFAULT NULL,
  `paiement_ok` tinyint(1) DEFAULT NULL,
  `paiement_date` date DEFAULT NULL,
  `paiement_comment` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `client_id` varchar(5) CHARACTER SET utf8 NOT NULL,
  `date_emission` date DEFAULT NULL,
  `compagnie_id` bigint(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `symf_operation_treso`
--

DROP TABLE IF EXISTS `symf_operation_treso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `symf_operation_treso` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `montant` decimal(18,2) DEFAULT NULL,
  `charge` tinyint(1) DEFAULT NULL,
  `compagnie_id` bigint(20) NOT NULL,
  `date` date DEFAULT NULL,
  `libelle` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `annee` bigint(20) DEFAULT NULL,
  `type` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1131 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `vue_client`
--

DROP TABLE IF EXISTS `vue_client`;
/*!50001 DROP VIEW IF EXISTS `vue_client`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vue_client` (
  `id` varchar(4),
  `name` varchar(255),
  `compagny_id` int(11),
  `adresse` varchar(255),
  `code_postal` varchar(20),
  `ville` varchar(255),
  `telephone` varchar(50),
  `email` varchar(255)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vue_compagny`
--

DROP TABLE IF EXISTS `vue_compagny`;
/*!50001 DROP VIEW IF EXISTS `vue_compagny`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vue_compagny` (
  `id` int(11),
  `name` varchar(150),
  `object` varchar(255),
  `email` varchar(255)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vue_facture`
--

DROP TABLE IF EXISTS `vue_facture`;
/*!50001 DROP VIEW IF EXISTS `vue_facture`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vue_facture` (
  `id` bigint(20),
  `official_id` bigint(20),
  `sequence_id` bigint(20),
  `tache_id` bigint(20),
  `description` text,
  `number` varchar(100),
  `project_id` bigint(20),
  `compagnie_id` bigint(20),
  `compagnie_lib` varchar(150),
  `montant_ht` double,
  `tva` decimal(18,2),
  `date_emission` date,
  `annee` varchar(20),
  `date_estimation` date,
  `client_id` varchar(4),
  `client_lib` varchar(255),
  `paiement_etat` varchar(10),
  `paiement_ok` bigint(4),
  `paiement_comment` text,
  `paiement_date` date
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vue_facture_manuelle`
--

DROP TABLE IF EXISTS `vue_facture_manuelle`;
/*!50001 DROP VIEW IF EXISTS `vue_facture_manuelle`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vue_facture_manuelle` (
  `number` int(11),
  `annee` int(4),
  `date_emission` datetime,
  `description` varchar(255)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `vue_utilisateur`
--

DROP TABLE IF EXISTS `vue_utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vue_utilisateur` (
  `id` int(11) DEFAULT NULL,
  `libelle` varchar(101) DEFAULT NULL,
  `login` varchar(64) DEFAULT NULL,
  `pass` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vue_utilisateur_compagny`
--

DROP TABLE IF EXISTS `vue_utilisateur_compagny`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vue_utilisateur_compagny` (
  `company_id` int(11) DEFAULT NULL,
  `utilisateur_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `vue_client`
--

/*!50001 DROP TABLE IF EXISTS `vue_client`*/;
/*!50001 DROP VIEW IF EXISTS `vue_client`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vue_client` AS select `c`.`code` AS `id`,`c`.`name` AS `name`,`c`.`IDCompany` AS `compagny_id`,`c`.`address` AS `adresse`,`c`.`zipCode` AS `code_postal`,`c`.`city` AS `ville`,`c`.`phone` AS `telephone`,`c`.`email` AS `email` from `coop_customer` `c` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vue_compagny`
--

/*!50001 DROP TABLE IF EXISTS `vue_compagny`*/;
/*!50001 DROP VIEW IF EXISTS `vue_compagny`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vue_compagny` AS select `u`.`IDCompany` AS `id`,`u`.`name` AS `name`,`u`.`object` AS `object`,`u`.`email` AS `email` from `coop_company` `u` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vue_facture`
--

/*!50001 DROP TABLE IF EXISTS `vue_facture`*/;
/*!50001 DROP VIEW IF EXISTS `vue_facture`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vue_facture` AS select `i`.`IDTask` AS `id`,`i`.`officialNumber` AS `official_id`,`i`.`sequenceNumber` AS `sequence_id`,`i`.`IDTask` AS `tache_id`,`t`.`description` AS `description`,`i`.`number` AS `number`,`project`.`IDProject` AS `project_id`,`entrepreneur`.`id` AS `compagnie_id`,`entrepreneur`.`name` AS `compagnie_lib`,((select (sum((`line`.`cost` * `line`.`quantity`)) / 100) AS `sum(line.cost * line.quantity) / 100` from `coop_invoice_line` `line` where (`line`.`IDTask` = `i`.`IDTask`)) - (`i`.`discountHT` / 100)) AS `montant_ht`,`i`.`tva` AS `tva`,cast(concat(substr(cast(`t`.`taskDate` as char charset utf8),1,4),_utf8'-',substr(cast(`t`.`taskDate` as char charset utf8),5,2),_utf8'-',substr(cast(`t`.`taskDate` as char charset utf8),7,2)) as date) AS `date_emission`,substr(cast(`t`.`taskDate` as char charset utf8),1,4) AS `annee`,cast(concat(substr(cast(`i`.`estimationDate` as char charset utf8),1,4),_utf8'-',substr(cast(`i`.`estimationDate` as char charset utf8),5,2),_utf8'-',substr(cast(`i`.`estimationDate` as char charset utf8),7,2)) as date) AS `date_estimation`,`client`.`id` AS `client_id`,`client`.`name` AS `client_lib`,`t`.`CAEStatus` AS `paiement_etat`,if((`t`.`CAEStatus` = _utf8'paid'),1,0) AS `paiement_ok`,if((if((`t`.`CAEStatus` = _utf8'paid'),1,0) = 1),`t`.`statusComment`,NULL) AS `paiement_comment`,if((if((`t`.`CAEStatus` = _utf8'paid'),1,0) = 1),from_unixtime(`t`.`statusDate`),NULL) AS `paiement_date` from ((((`coop_invoice` `i` join `coop_task` `t` on((`t`.`IDTask` = `i`.`IDTask`))) join `coop_project` `project` on((`i`.`IDProject` = `project`.`IDProject`))) join `vue_compagny` `entrepreneur` on((`entrepreneur`.`id` = `project`.`IDCompany`))) join `vue_client` `client` on((`client`.`id` = `project`.`customerCode`))) where ((`t`.`CAEStatus` <> _utf8'aboinv') and (`t`.`CAEStatus` <> _utf8'draft') and (`t`.`CAEStatus` <> _utf8'invalid') and (`t`.`CAEStatus` <> _utf8'wait')) union all select `m`.`id` AS `id`,`m`.`sequence_id` AS `official_id`,`m`.`sequence_id` AS `sequence_id`,`m`.`sequence_id` AS `tache_id`,`m`.`libelle` AS `description`,concat(_utf8'FACT_MAN_',`m`.`sequence_id`) AS `number`,0 AS `project_id`,`m`.`compagnie_id` AS `compagnie_id`,`c1`.`name` AS `compagnie_lib`,`m`.`montant_ht` AS `montant_ht`,`m`.`tva` AS `tva`,`m`.`date_emission` AS `date_emission`,year(`m`.`date_emission`) AS `annee`,NULL AS `date_estimation`,`c2`.`id` AS `client_id`,`c2`.`name` AS `client_lib`,NULL AS `paiement_etat`,`m`.`paiement_ok` AS `paiement_ok`,_utf8'' AS `paiement_comment`,`m`.`paiement_date` AS `paiement_date` from ((`symf_facture_manuelle` `m` join `vue_compagny` `c1` on((`c1`.`id` = `m`.`compagnie_id`))) join `vue_client` `c2` on((`c2`.`id` = `m`.`client_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vue_facture_manuelle`
--

/*!50001 DROP TABLE IF EXISTS `vue_facture_manuelle`*/;
/*!50001 DROP VIEW IF EXISTS `vue_facture_manuelle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vue_facture_manuelle` AS select `i`.`number` AS `number`,year(from_unixtime(`i`.`invoiceDate`)) AS `annee`,from_unixtime(`i`.`invoiceDate`) AS `date_emission`,`i`.`description` AS `description` from `coop_internal_invoice` `i` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-02-03 16:11:15
