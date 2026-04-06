/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.2.2-MariaDB, for Win64 (AMD64)
--
-- Host: 10.200.10.62    Database: plataforma_mell
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Subcontractor`
--

DROP TABLE IF EXISTS `Subcontractor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Subcontractor` (
  `Subcontractor_ID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Subcontractor_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Subcontractor`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `Subcontractor` WRITE;
/*!40000 ALTER TABLE `Subcontractor` DISABLE KEYS */;
/*!40000 ALTER TABLE `Subcontractor` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `cidade`
--

DROP TABLE IF EXISTS `cidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cidade` (
  `id_cidade` int(11) NOT NULL AUTO_INCREMENT,
  `cidade` varchar(255) NOT NULL,
  `id_regional` int(11) NOT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id_cidade`),
  KEY `id_regional` (`id_regional`),
  CONSTRAINT `cidade_ibfk_1` FOREIGN KEY (`id_regional`) REFERENCES `regional` (`id_regional`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cidade`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `cidade` WRITE;
/*!40000 ALTER TABLE `cidade` DISABLE KEYS */;
/*!40000 ALTER TABLE `cidade` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `historico_comissoes`
--

DROP TABLE IF EXISTS `historico_comissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `historico_comissoes` (
  `id_historico` int(11) NOT NULL AUTO_INCREMENT,
  `vendedor_nome` varchar(255) DEFAULT NULL,
  `regional` varchar(100) DEFAULT NULL,
  `mes_referencia` int(11) DEFAULT NULL,
  `ano_referencia` int(11) DEFAULT NULL,
  `valor_pago` decimal(10,2) DEFAULT NULL,
  `status_pagamento` varchar(50) DEFAULT NULL,
  `observacao` text DEFAULT NULL,
  `data_fechamento` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_historico`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_comissoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `historico_comissoes` WRITE;
/*!40000 ALTER TABLE `historico_comissoes` DISABLE KEYS */;
INSERT INTO `historico_comissoes` VALUES
(1,'samanta ','Moc',2,2026,0.00,'RECUSADO','','2026-02-23 17:28:58'),
(2,'ANA PAULA PEREIRA ROCHA','Moc',2,2026,52065.80,'PAGO','','2026-02-23 17:28:58'),
(3,'jose aquino ','Curvelo',2,2026,0.00,'RECUSADO','','2026-02-23 17:29:31'),
(4,'jose aquino ','Curvelo',2,2026,0.00,'RECUSADO','recusado','2026-02-23 17:29:34'),
(5,'ANA PAULA PEREIRA ROCHA','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42'),
(6,'samanta ','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42'),
(7,'PEDRO HENRIQUE PEREIRA SILVA','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42');
/*!40000 ALTER TABLE `historico_comissoes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `logs_sistema`
--

DROP TABLE IF EXISTS `logs_sistema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_sistema` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `acao` varchar(100) DEFAULT NULL,
  `detalhes` text DEFAULT NULL,
  `data_hora` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=489 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_sistema`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `logs_sistema` WRITE;
/*!40000 ALTER TABLE `logs_sistema` DISABLE KEYS */;
INSERT INTO `logs_sistema` VALUES
(1,1,'LOGIN','Entrou no sistema','2026-02-24 17:01:00'),
(2,1,'LOGIN','Entrou no sistema','2026-02-24 17:10:15'),
(3,1,'LOGOUT','Saiu do sistema','2026-02-24 17:22:10'),
(4,20,'LOGIN','Entrou no sistema','2026-02-24 17:22:16'),
(5,20,'LOGIN','Entrou no sistema','2026-02-24 17:51:16'),
(6,20,'NOTIFICACAO_ENVIADA','Título: Atualização  | Para: Todos','2026-02-24 17:51:56'),
(7,2,'LOGIN','Entrou no sistema','2026-02-24 18:56:12'),
(8,2,'LOGOUT','Saiu do sistema','2026-02-24 18:57:19'),
(9,1,'LOGIN','Entrou no sistema','2026-02-24 18:57:25'),
(10,4,'LOGIN','Entrou no sistema','2026-02-24 18:58:41'),
(11,4,'LOGOUT','Saiu do sistema','2026-02-24 18:59:38'),
(12,20,'LOGIN','Entrou no sistema','2026-02-24 19:01:02'),
(13,20,'LOGOUT','Saiu do sistema','2026-02-24 19:11:52'),
(14,1,'LOGIN','Entrou no sistema','2026-02-24 19:17:30'),
(15,1,'LOGOUT','Saiu do sistema','2026-02-24 19:17:35'),
(16,1,'LOGIN','Entrou no sistema','2026-02-24 19:32:25'),
(17,1,'LOGOUT','Saiu do sistema','2026-02-24 19:32:39'),
(18,4,'LOGIN','Entrou no sistema','2026-02-24 19:32:47'),
(19,1,'LOGIN','Entrou no sistema','2026-02-24 20:25:54'),
(20,17,'LOGIN','Entrou no sistema','2026-02-24 20:30:43'),
(21,1,'LOGIN','Entrou no sistema','2026-02-24 20:31:59'),
(22,1,'LOGOUT','Saiu do sistema','2026-02-24 20:32:27'),
(23,1,'LOGIN','Entrou no sistema','2026-02-24 20:34:30'),
(24,1,'LOGIN','Entrou no sistema','2026-02-24 20:48:43'),
(25,4,'LOGIN','Entrou no sistema','2026-02-24 20:54:51'),
(26,1,'LOGIN','Entrou no sistema','2026-02-24 20:55:36'),
(27,4,'LOGIN','Entrou no sistema','2026-02-24 20:58:43'),
(28,20,'LOGIN','Entrou no sistema','2026-02-24 20:59:08'),
(29,1,'LOGIN','Entrou no sistema','2026-02-25 12:21:17'),
(30,20,'LOGIN','Entrou no sistema','2026-02-25 12:41:00'),
(31,1,'LOGIN','Entrou no sistema','2026-02-25 13:51:54'),
(32,3,'LOGIN','Entrou no sistema','2026-02-25 13:53:49'),
(33,20,'LOGIN','Entrou no sistema','2026-02-25 13:54:16'),
(34,1,'LOGIN','Entrou no sistema','2026-02-25 13:56:17'),
(35,2,'LOGIN','Entrou no sistema','2026-02-25 13:57:18'),
(36,19,'LOGIN','Entrou no sistema','2026-02-25 14:06:12'),
(37,4,'LOGIN','Entrou no sistema','2026-02-25 14:10:18'),
(38,1,'LOGIN','Entrou no sistema','2026-02-25 14:32:53'),
(39,1,'LOGIN','Entrou no sistema','2026-02-25 14:59:41'),
(40,2,'LOGIN','Entrou no sistema','2026-02-25 15:00:12'),
(41,2,'LOGIN','Entrou no sistema','2026-02-25 15:18:10'),
(42,1,'LOGIN','Entrou no sistema','2026-02-25 15:19:03'),
(43,20,'LOGIN','Entrou no sistema','2026-02-25 15:19:30'),
(44,20,'NOTIFICACAO_ENVIADA','Título: implelementaçao ','2026-02-25 15:20:46'),
(45,2,'LOGIN','Entrou no sistema','2026-02-25 15:21:43'),
(46,1,'LOGIN','Entrou no sistema','2026-02-26 11:31:02'),
(47,1,'LOGIN','Entrou no sistema','2026-02-26 17:08:23'),
(48,2,'LOGIN','Entrou no sistema','2026-02-26 17:08:54'),
(49,20,'LOGIN','Entrou no sistema','2026-02-26 17:10:41'),
(50,20,'NOTIFICACAO_ENVIADA','Título: 🚨teste de notificação 🚨','2026-02-26 17:11:49'),
(51,4,'LOGIN','Entrou no sistema','2026-02-26 17:33:12'),
(52,20,'LOGIN','Entrou no sistema','2026-02-26 18:05:00'),
(53,20,'NOTIFICACAO_ENVIADA','Título: novo teste','2026-02-26 20:28:26'),
(54,1,'LOGIN','Acesso bem sucedido','2026-02-26 20:47:17'),
(55,20,'LOGIN','Acesso bem sucedido','2026-02-26 20:47:59'),
(56,1,'LOGIN','Entrou no sistema','2026-02-27 11:10:30'),
(57,1,'LOGIN','Entrou no sistema','2026-02-27 11:16:24'),
(58,1,'LOGIN','Entrou no sistema','2026-02-27 11:24:26'),
(59,20,'LOGIN','Entrou no sistema','2026-02-27 11:53:23'),
(60,1,'LOGIN','Entrou no sistema','2026-02-27 11:53:45'),
(61,1,'LOGIN','Entrou no sistema','2026-02-27 12:49:45'),
(62,1,'LOGIN','Entrou no sistema','2026-02-27 13:52:22'),
(63,20,'LOGIN','Entrou no sistema','2026-02-27 13:53:25'),
(64,2,'LOGIN','Entrou no sistema','2026-02-27 13:53:41'),
(65,1,'LOGIN','Entrou no sistema','2026-02-27 14:12:03'),
(66,1,'LOGIN','Entrou no sistema','2026-02-27 14:27:15'),
(67,4,'LOGIN','Entrou no sistema','2026-02-27 14:55:32'),
(68,20,'LOGIN','Entrou no sistema','2026-02-27 14:56:00'),
(69,17,'LOGIN','Entrou no sistema','2026-02-27 15:20:55'),
(70,16,'LOGIN','Entrou no sistema','2026-02-27 15:21:17'),
(71,1,'LOGIN','Entrou no sistema','2026-02-27 17:50:23'),
(72,16,'LOGIN','Entrou no sistema','2026-02-27 17:51:07'),
(73,1,'LOGIN','Entrou no sistema','2026-02-27 17:51:42'),
(74,2,'LOGIN','Entrou no sistema','2026-02-27 18:01:43'),
(75,4,'LOGIN','Entrou no sistema','2026-02-27 18:02:23'),
(76,1,'LOGIN','Entrou no sistema','2026-02-27 18:13:55'),
(77,2,'LOGIN','Entrou no sistema','2026-02-27 18:15:47'),
(78,1,'LOGIN','Entrou no sistema','2026-02-27 18:17:25'),
(79,19,'LOGIN','Entrou no sistema','2026-02-27 18:18:44'),
(80,20,'LOGIN','Entrou no sistema','2026-02-27 18:19:13'),
(81,1,'LOGIN','Entrou no sistema','2026-02-27 18:30:05'),
(82,2,'LOGIN','Entrou no sistema','2026-02-27 18:35:31'),
(83,1,'LOGIN','Entrou no sistema','2026-02-27 19:11:34'),
(84,4,'LOGIN','Entrou no sistema','2026-02-27 19:12:10'),
(85,1,'LOGIN','Entrou no sistema','2026-02-27 19:16:12'),
(86,20,'LOGIN','Entrou no sistema','2026-02-27 19:17:27'),
(87,24,'LOGIN','Entrou no sistema','2026-02-27 19:30:23'),
(88,1,'LOGIN','Entrou no sistema','2026-03-02 13:23:59'),
(89,24,'LOGIN','Entrou no sistema','2026-03-02 13:35:49'),
(90,1,'LOGIN','Entrou no sistema','2026-03-02 13:39:54'),
(91,24,'LOGIN','Entrou no sistema','2026-03-02 13:45:44'),
(92,24,'LOGIN_TREINAMENTO','Acessou o portal','2026-03-02 13:49:11'),
(93,24,'LOGIN','Entrou no sistema','2026-03-02 13:51:18'),
(94,20,'LOGIN','Entrou no sistema','2026-03-02 13:53:03'),
(95,24,'LOGIN','Entrou no sistema','2026-03-02 14:00:47'),
(96,24,'LOGIN','Entrou no sistema','2026-03-02 14:02:13'),
(97,24,'LOGIN','Entrou no sistema','2026-03-02 14:10:39'),
(98,4,'LOGIN','Entrou no sistema','2026-03-02 14:12:11'),
(99,24,'LOGIN','Entrou no sistema','2026-03-02 14:13:30'),
(100,4,'LOGIN','Entrou no sistema','2026-03-02 14:15:34'),
(101,24,'LOGIN','Entrou no sistema','2026-03-02 14:16:04'),
(102,24,'LOGIN','Entrou no sistema','2026-03-02 14:31:25'),
(103,4,'LOGIN','Entrou no sistema','2026-03-02 14:32:12'),
(104,1,'LOGIN','Entrou no sistema','2026-03-02 14:32:34'),
(105,24,'LOGIN','Entrou no sistema','2026-03-02 14:33:04'),
(106,24,'LOGIN','Entrou no sistema','2026-03-02 14:34:51'),
(107,24,'LOGIN','Entrou no sistema','2026-03-02 14:42:06'),
(108,24,'LOGIN','Entrou no sistema','2026-03-02 14:44:47'),
(109,4,'LOGIN','Entrou no sistema','2026-03-02 14:47:51'),
(110,4,'LOGIN','Entrou no sistema','2026-03-02 14:48:06'),
(111,24,'LOGIN','Entrou no sistema','2026-03-02 14:48:35'),
(112,24,'LOGIN','Entrou no sistema','2026-03-02 15:07:51'),
(113,16,'LOGIN','Entrou no sistema','2026-03-02 17:37:23'),
(114,4,'LOGIN','Entrou no sistema','2026-03-02 17:44:55'),
(115,2,'LOGIN','Entrou no sistema','2026-03-02 18:02:08'),
(116,16,'LOGIN','Entrou no sistema','2026-03-02 18:06:10'),
(117,2,'LOGIN','Entrou no sistema','2026-03-02 18:07:22'),
(118,1,'LOGIN','Entrou no sistema','2026-03-02 18:08:04'),
(119,17,'LOGIN','Entrou no sistema','2026-03-02 18:08:43'),
(120,2,'LOGIN','Entrou no sistema','2026-03-02 18:10:12'),
(121,3,'LOGIN','Entrou no sistema','2026-03-02 18:10:47'),
(122,1,'LOGIN','Entrou no sistema','2026-03-02 18:11:16'),
(123,6,'LOGIN','Entrou no sistema','2026-03-02 18:18:19'),
(124,2,'LOGIN','Entrou no sistema','2026-03-02 18:20:08'),
(125,1,'LOGIN','Entrou no sistema','2026-03-02 18:20:34'),
(126,3,'LOGIN','Entrou no sistema','2026-03-02 18:20:55'),
(127,6,'LOGIN','Entrou no sistema','2026-03-02 18:23:52'),
(128,1,'LOGIN','Entrou no sistema','2026-03-02 18:29:11'),
(129,24,'LOGIN','Entrou no sistema','2026-03-02 18:30:20'),
(130,6,'LOGIN','Entrou no sistema','2026-03-02 18:51:17'),
(131,24,'LOGIN','Entrou no sistema','2026-03-02 18:51:56'),
(132,4,'LOGIN','Entrou no sistema','2026-03-02 19:01:36'),
(133,20,'LOGIN','Entrou no sistema','2026-03-02 19:18:49'),
(134,20,'NOTIFICACAO_ENVIADA','Título: teste ','2026-03-02 19:42:55'),
(135,20,'NOTIFICACAO_ENVIADA','Título: teste ','2026-03-02 19:46:35'),
(136,20,'LOGIN','Entrou no sistema','2026-03-02 19:46:50'),
(137,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-02 19:49:56'),
(138,2,'LOGIN','Perfil: supervisor','2026-03-02 19:50:08'),
(139,24,'LOGIN','Perfil: admin','2026-03-02 19:55:50'),
(140,1,'LOGIN','Entrou no sistema','2026-03-03 11:30:40'),
(141,1,'LOGIN','Perfil: admin','2026-03-03 11:32:43'),
(142,1,'LOGIN','Entrou no sistema','2026-03-03 11:58:46'),
(143,19,'LOGIN','Perfil: auditor','2026-03-03 12:18:35'),
(144,1,'LOGIN','Perfil: admin','2026-03-03 12:19:00'),
(145,24,'LOGIN','Perfil: admin','2026-03-03 12:53:44'),
(146,24,'LOGIN','Entrou no sistema','2026-03-03 12:54:17'),
(147,4,'LOGIN','Entrou no sistema','2026-03-03 12:54:59'),
(148,4,'LOGIN','Perfil: vendedor','2026-03-03 12:55:16'),
(149,1,'LOGIN','Entrou no sistema','2026-03-03 12:56:02'),
(150,1,'LOGIN','Perfil: admin','2026-03-03 12:56:30'),
(151,1,'LOGIN','Entrou no sistema','2026-03-03 12:57:06'),
(152,4,'LOGIN','Entrou no sistema','2026-03-03 12:57:52'),
(153,1,'LOGIN','Entrou no sistema','2026-03-03 12:58:16'),
(154,1,'LOGIN','Entrou no sistema','2026-03-03 14:51:02'),
(155,1,'LOGIN','Perfil: admin','2026-03-03 16:45:02'),
(156,24,'LOGIN','Perfil: admin','2026-03-03 17:08:25'),
(157,24,'LOGIN','Perfil: admin','2026-03-03 17:14:52'),
(158,2,'LOGIN','Perfil: supervisor','2026-03-03 17:20:33'),
(159,4,'LOGIN','Perfil: vendedor','2026-03-03 17:22:01'),
(160,24,'LOGIN','Perfil: admin','2026-03-03 17:23:35'),
(161,4,'LOGIN','Perfil: vendedor','2026-03-03 17:51:23'),
(162,2,'LOGIN','Perfil: supervisor','2026-03-03 17:51:52'),
(163,24,'LOGIN','Perfil: admin','2026-03-03 17:53:29'),
(164,24,'LOGIN','Perfil: admin','2026-03-03 18:43:32'),
(165,4,'LOGIN','Perfil: vendedor','2026-03-03 18:46:38'),
(166,2,'LOGIN','Perfil: supervisor','2026-03-03 18:49:51'),
(167,24,'LOGIN','Perfil: admin','2026-03-03 18:50:13'),
(168,4,'LOGIN','Perfil: vendedor','2026-03-03 19:05:32'),
(169,24,'LOGIN','Perfil: admin','2026-03-03 19:05:53'),
(170,4,'LOGIN','Perfil: vendedor','2026-03-03 19:15:27'),
(171,24,'LOGIN','Perfil: admin','2026-03-03 19:17:46'),
(172,1,'LOGIN','Perfil: admin','2026-03-03 19:18:39'),
(173,24,'LOGIN','Perfil: admin','2026-03-03 19:23:20'),
(174,20,'LOGIN','Perfil: gestor_treinamento','2026-03-03 19:34:59'),
(175,24,'LOGIN','Perfil: admin','2026-03-03 19:36:49'),
(176,20,'LOGIN','Perfil: gestor_treinamento','2026-03-03 19:37:56'),
(177,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 19:38:06'),
(178,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 19:45:44'),
(179,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 19:50:41'),
(180,24,'LOGIN','Perfil: admin','2026-03-03 20:09:24'),
(181,20,'LOGIN','Perfil: gestor_treinamento','2026-03-03 20:09:52'),
(182,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:10:17'),
(183,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:10:42'),
(184,4,'LOGIN','Perfil: vendedor','2026-03-03 20:10:53'),
(185,4,'LOGIN','Perfil: vendedor','2026-03-03 20:13:37'),
(186,20,'LOGIN','Perfil: gestor_treinamento','2026-03-03 20:15:18'),
(187,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:15:28'),
(188,4,'LOGIN','Perfil: vendedor','2026-03-03 20:15:44'),
(189,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:21:08'),
(190,24,'LOGIN','Perfil: admin','2026-03-03 20:22:16'),
(191,6,'LOGIN','Perfil: vendedor','2026-03-03 20:24:53'),
(192,2,'LOGIN','Perfil: supervisor','2026-03-03 20:26:12'),
(193,20,'LOGIN','Perfil: gestor_treinamento','2026-03-03 20:33:59'),
(194,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:34:07'),
(195,4,'LOGIN','Perfil: vendedor','2026-03-03 20:39:13'),
(196,2,'LOGIN','Perfil: supervisor','2026-03-03 20:39:33'),
(197,20,'NOTIFICACAO','Para Todos','2026-03-03 20:42:26'),
(198,1,'LOGIN','Perfil: admin','2026-03-03 20:47:08'),
(199,1,'LOGIN','Perfil: admin','2026-03-03 20:47:57'),
(200,20,'LOGIN','Perfil: gestor_treinamento','2026-03-03 20:48:14'),
(201,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:48:21'),
(202,20,'NOTIFICACAO_ENVIADA','Para: Todos','2026-03-03 20:50:33'),
(203,1,'LOGIN','Entrou no sistema','2026-03-04 11:19:12'),
(204,6,'LOGIN','Entrou no sistema','2026-03-04 11:21:05'),
(205,2,'LOGIN','Entrou no sistema','2026-03-04 11:21:19'),
(206,2,'LOGIN','Entrou no sistema','2026-03-04 11:24:06'),
(207,2,'LOGIN','Entrou no sistema','2026-03-04 11:24:46'),
(208,2,'LOGIN','Entrou no sistema','2026-03-04 11:27:18'),
(209,2,'LOGIN','Entrou no sistema','2026-03-04 12:13:11'),
(210,1,'LOGIN','Entrou no sistema','2026-03-04 12:15:37'),
(211,2,'LOGIN','Entrou no sistema','2026-03-04 12:16:05'),
(212,1,'LOGIN','Entrou no sistema','2026-03-04 12:17:22'),
(213,1,'LOGIN','Entrou no sistema','2026-03-04 12:34:44'),
(214,1,'LOGIN','Entrou no sistema','2026-03-04 12:37:22'),
(215,6,'LOGIN','Entrou no sistema','2026-03-04 12:39:33'),
(216,3,'LOGIN','Entrou no sistema','2026-03-04 12:43:37'),
(217,2,'LOGIN','Entrou no sistema','2026-03-04 12:44:10'),
(218,1,'LOGIN','Entrou no sistema','2026-03-04 12:58:51'),
(219,2,'LOGIN','Entrou no sistema','2026-03-04 13:01:18'),
(220,1,'LOGIN','Entrou no sistema','2026-03-04 13:03:23'),
(221,1,'LOGIN','Entrou no sistema','2026-03-04 13:08:32'),
(222,1,'LOGIN','Entrou no sistema','2026-03-04 13:51:31'),
(223,4,'LOGIN','Entrou no sistema','2026-03-04 13:51:49'),
(224,2,'LOGIN','Entrou no sistema','2026-03-04 13:52:10'),
(225,19,'LOGIN','Entrou no sistema','2026-03-04 13:52:50'),
(226,1,'USUÁRIO','Cadastro em massa: 2 sucessos, 0 erros','2026-03-04 15:21:16'),
(227,1,'LOGIN','Acesso realizado','2026-03-04 15:31:14'),
(228,1,'USUÁRIO','Cadastro em massa: 1 sucessos, 0 erros','2026-03-04 15:31:48'),
(229,1,'LOGIN','Acesso realizado','2026-03-04 17:11:15'),
(230,1,'LOGOUT','Saiu do sistema','2026-03-04 17:12:56'),
(231,2,'LOGIN','Acesso realizado','2026-03-04 17:14:50'),
(232,2,'LOGOUT','Saiu do sistema','2026-03-04 17:15:30'),
(233,1,'LOGIN','Acesso realizado','2026-03-04 17:15:36'),
(234,1,'USUÁRIO','Cadastrou: SUPERVISOR SERRA','2026-03-04 17:18:09'),
(235,1,'USUÁRIO','Cadastrou: SUPERVISOR SERRA','2026-03-04 17:18:26'),
(236,1,'USUÁRIO','Cadastrou: SUPERVISOR SERRA','2026-03-04 17:18:55'),
(237,1,'LOGOUT','Saiu do sistema','2026-03-04 17:21:31'),
(238,2,'LOGIN','Acesso realizado','2026-03-04 17:21:40'),
(239,2,'LOGOUT','Saiu do sistema','2026-03-04 17:21:47'),
(240,20,'LOGIN','Acesso realizado','2026-03-04 17:22:08'),
(241,20,'LOGOUT','Saiu do sistema','2026-03-04 17:22:32'),
(242,1,'LOGIN','Acesso realizado','2026-03-04 17:22:37'),
(243,1,'USUÁRIO','Alterou status de auditoria_mell para Inativo','2026-03-04 17:39:26'),
(244,1,'USUÁRIO','Alterou status de auditoria_mell para Ativo','2026-03-04 17:39:51'),
(245,1,'LOGOUT','Saiu do sistema','2026-03-04 17:40:58'),
(246,20,'LOGIN','Acesso realizado','2026-03-04 17:41:09'),
(247,20,'LOGOUT','Saiu do sistema','2026-03-04 17:51:54'),
(248,20,'LOGIN','Acesso realizado','2026-03-04 17:52:05'),
(249,20,'LOGOUT','Saiu do sistema','2026-03-04 17:57:03'),
(250,6,'LOGIN','Acesso realizado','2026-03-04 17:57:17'),
(251,6,'LOGOUT','Saiu do sistema','2026-03-04 17:57:27'),
(252,4,'LOGIN','Acesso realizado','2026-03-04 17:57:40'),
(253,4,'LOGOUT','Saiu do sistema','2026-03-04 17:57:59'),
(254,20,'LOGIN','Acesso realizado','2026-03-04 17:58:16'),
(255,20,'NOTIFICACAO_ENVIADA','Título: teste  | Para: Todos','2026-03-04 18:17:26'),
(256,20,'LOGOUT','Saiu do sistema','2026-03-04 18:18:56'),
(257,3,'LOGIN','Acesso realizado','2026-03-04 18:19:41'),
(258,3,'LOGOUT','Saiu do sistema','2026-03-04 18:19:51'),
(259,2,'LOGIN','Acesso realizado','2026-03-04 18:19:56'),
(260,2,'LOGOUT','Saiu do sistema','2026-03-04 18:32:17'),
(261,1,'LOGIN','Acesso realizado','2026-03-04 18:33:29'),
(262,1,'LOGIN','Acesso realizado','2026-03-04 18:45:28'),
(263,1,'LOGIN','Acesso realizado','2026-03-04 18:48:25'),
(264,1,'LOGIN','Acesso realizado','2026-03-04 18:54:19'),
(265,1,'LOGIN','Entrou no sistema','2026-03-04 19:06:30'),
(266,1,'LOGIN','Acesso realizado','2026-03-04 19:18:22'),
(267,1,'LOGOUT','Saiu do sistema','2026-03-04 19:19:26'),
(268,19,'LOGIN','Acesso realizado','2026-03-04 19:19:37'),
(269,19,'LOGOUT','Saiu do sistema','2026-03-04 19:20:03'),
(270,4,'LOGIN','Acesso realizado','2026-03-04 19:20:13'),
(271,4,'VENDA','Nova venda: 80835 - R$ 89.9','2026-03-04 19:20:34'),
(272,5,'LOGIN','Acesso realizado','2026-03-04 19:29:57'),
(273,4,'LOGIN','Entrou no sistema','2026-03-04 19:38:24'),
(274,5,'LOGOUT','Saiu do sistema','2026-03-04 19:43:14'),
(275,4,'LOGIN','Acesso realizado','2026-03-04 19:43:24'),
(276,4,'LOGOUT','Saiu do sistema','2026-03-04 19:51:39'),
(277,2,'LOGIN','Acesso realizado','2026-03-04 19:51:48'),
(278,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:51:53'),
(279,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:52:00'),
(280,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:52:17'),
(281,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:52:18'),
(282,2,'APROVAÇÃO','Venda 99 aprovada - R$ 89.9','2026-03-04 19:52:19'),
(283,2,'APROVAÇÃO','Venda 99 aprovada - R$ 89.9','2026-03-04 19:52:20'),
(284,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:52:21'),
(285,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:52:22'),
(286,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:52:22'),
(287,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:53:08'),
(288,2,'APROVAÇÃO','Venda 99 aprovada - R$ 89.9','2026-03-04 19:53:09'),
(289,2,'LOGOUT','Saiu do sistema','2026-03-04 19:54:15'),
(290,20,'LOGIN','Acesso realizado','2026-03-04 19:54:20'),
(291,20,'LOGOUT','Saiu do sistema','2026-03-04 19:58:14'),
(292,2,'LOGIN','Acesso realizado','2026-03-04 19:58:27'),
(293,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:58:32'),
(294,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:58:48'),
(295,2,'REPROVAÇÃO','Venda 99 reprovada','2026-03-04 19:59:51'),
(296,2,'LOGOUT','Saiu do sistema','2026-03-04 20:06:07'),
(297,1,'LOGIN','Acesso realizado','2026-03-04 20:06:13'),
(298,1,'LOGOUT','Saiu do sistema','2026-03-04 20:06:39'),
(299,1,'LOGIN','Acesso realizado','2026-03-04 20:07:09'),
(300,1,'USUÁRIO','Resetou senha de ze maria da mel ','2026-03-04 20:07:18'),
(301,1,'LOGOUT','Saiu do sistema','2026-03-04 20:07:24'),
(302,15,'LOGIN','Acesso realizado','2026-03-04 20:07:43'),
(303,15,'VENDA','Upgrade: 4306 - R$ 109.0 (anterior: R$ 89.0)','2026-03-04 20:08:05'),
(304,15,'VENDA','Venda Nova: 32t20 - R$ 89.9','2026-03-04 20:08:21'),
(305,15,'VENDA','Downgrade: 65293 - R$ 89.9 (anterior: R$ 109.9)','2026-03-04 20:08:38'),
(306,15,'LOGOUT','Saiu do sistema','2026-03-04 20:08:45'),
(307,2,'LOGIN','Acesso realizado','2026-03-04 20:09:08'),
(308,2,'LOGOUT','Saiu do sistema','2026-03-04 20:09:33'),
(309,3,'LOGIN','Acesso realizado','2026-03-04 20:09:39'),
(310,3,'APROVAÇÃO','Venda 101 aprovada - R$ 89.9','2026-03-04 20:10:03'),
(311,3,'APROVAÇÃO','Venda 100 aprovada - R$ 109.0','2026-03-04 20:10:06'),
(312,3,'APROVAÇÃO','Venda 102 aprovada - R$ 89.9','2026-03-04 20:10:14'),
(313,3,'LOGOUT','Saiu do sistema','2026-03-04 20:16:43'),
(314,2,'LOGIN','Acesso realizado','2026-03-04 20:16:47'),
(315,2,'LOGOUT','Saiu do sistema','2026-03-04 20:17:10'),
(316,2,'LOGIN','Acesso realizado','2026-03-04 20:17:22'),
(317,2,'LOGOUT','Saiu do sistema','2026-03-04 20:20:36'),
(318,16,'LOGIN','Acesso realizado','2026-03-04 20:20:42'),
(319,16,'VENDA','Downgrade: 33036 - R$ 89.9 (anterior: R$ 109.9)','2026-03-04 20:21:13'),
(320,16,'VENDA','Downgrade: 2136 - R$ 79.9 (anterior: R$ 109.9)','2026-03-04 20:21:36'),
(321,16,'LOGOUT','Saiu do sistema','2026-03-04 20:21:42'),
(322,2,'LOGIN','Acesso realizado','2026-03-04 20:21:51'),
(323,2,'APROVAÇÃO','Venda 104 aprovada - R$ 79.9','2026-03-04 20:27:55'),
(324,2,'LOGOUT','Saiu do sistema','2026-03-04 20:28:51'),
(325,16,'LOGIN','Acesso realizado','2026-03-04 20:29:13'),
(326,16,'LOGOUT','Saiu do sistema','2026-03-04 20:30:46'),
(327,2,'LOGIN','Acesso realizado','2026-03-04 20:30:56'),
(328,2,'LOGOUT','Saiu do sistema','2026-03-04 20:32:31'),
(329,17,'LOGIN','Acesso realizado','2026-03-04 20:32:39'),
(330,17,'VENDA','Upgrade: 4393 - R$ 109.0 (anterior: R$ 89.0)','2026-03-04 20:32:58'),
(331,17,'VENDA','Upgrade: 2134 - R$ 129.9 (anterior: R$ 109.0)','2026-03-04 20:33:21'),
(332,17,'VENDA','Upgrade: 00826 - R$ 109.9 (anterior: R$ 89.0)','2026-03-04 20:33:37'),
(333,17,'VENDA','Upgrade: 00826 - R$ 109.9 (anterior: R$ 89.0)','2026-03-04 20:33:40'),
(334,17,'LOGOUT','Saiu do sistema','2026-03-04 20:33:48'),
(335,3,'LOGIN','Acesso realizado','2026-03-04 20:33:57'),
(336,3,'APROVAÇÃO','Venda 108 aprovada - R$ 109.9','2026-03-04 20:34:02'),
(337,3,'APROVAÇÃO','Venda 107 aprovada - R$ 109.9','2026-03-04 20:34:06'),
(338,3,'APROVAÇÃO','Venda 105 aprovada - R$ 109.0','2026-03-04 20:34:09'),
(339,3,'REPROVAÇÃO','Venda 106 reprovada','2026-03-04 20:34:41'),
(340,3,'LOGOUT','Saiu do sistema','2026-03-04 20:34:59'),
(341,1,'LOGIN','Acesso realizado','2026-03-04 20:35:04'),
(342,1,'LOGOUT','Saiu do sistema','2026-03-04 20:35:46'),
(343,19,'LOGIN','Acesso realizado','2026-03-04 20:36:01'),
(344,19,'LOGOUT','Saiu do sistema','2026-03-04 20:36:14'),
(345,17,'LOGIN','Acesso realizado','2026-03-04 20:36:25'),
(346,17,'LOGOUT','Saiu do sistema','2026-03-04 20:39:13'),
(347,3,'LOGIN','Acesso realizado','2026-03-04 20:40:34'),
(348,17,'LOGIN','Acesso realizado','2026-03-04 20:41:04'),
(349,3,'LOGOUT','Saiu do sistema','2026-03-04 20:41:32'),
(350,1,'LOGIN','Acesso realizado','2026-03-04 20:41:40'),
(351,1,'META','Metas salvas para Geral','2026-03-04 20:45:14'),
(352,17,'VENDA','Venda Nova: 02829 - R$ 109.9','2026-03-04 20:46:23'),
(353,17,'LOGOUT','Saiu do sistema','2026-03-04 20:46:58'),
(354,4,'LOGIN','Acesso realizado','2026-03-04 20:47:06'),
(355,4,'LOGOUT','Saiu do sistema','2026-03-04 20:47:15'),
(356,2,'LOGIN','Acesso realizado','2026-03-04 20:47:20'),
(357,2,'META','Metas salvas para Moc','2026-03-04 20:47:35'),
(358,1,'LOGOUT','Saiu do sistema','2026-03-04 20:47:57'),
(359,4,'LOGIN','Acesso realizado','2026-03-04 20:48:02'),
(360,2,'LOGOUT','Saiu do sistema','2026-03-04 20:50:33'),
(361,1,'LOGIN','Acesso realizado','2026-03-04 20:50:42'),
(362,1,'META','Metas salvas para Moc','2026-03-04 20:50:54'),
(363,1,'LOGOUT','Saiu do sistema','2026-03-04 20:51:02'),
(364,2,'LOGIN','Acesso realizado','2026-03-04 20:51:14'),
(365,2,'LOGOUT','Saiu do sistema','2026-03-04 20:51:52'),
(366,1,'LOGIN','Acesso realizado','2026-03-04 20:51:57'),
(367,1,'META','Metas salvas para Moc','2026-03-04 20:52:07'),
(368,1,'META','Metas salvas para Geral','2026-03-04 20:52:27'),
(369,4,'LOGOUT','Saiu do sistema','2026-03-04 20:52:33'),
(370,4,'LOGIN','Acesso realizado','2026-03-04 20:52:54'),
(371,1,'LOGIN','Acesso realizado','2026-03-05 11:08:30'),
(372,2,'LOGIN','Acesso realizado','2026-03-05 11:09:36'),
(373,2,'LOGOUT','Saiu do sistema','2026-03-05 11:10:03'),
(374,1,'LOGIN','Acesso realizado','2026-03-05 11:10:14'),
(375,1,'LOGOUT','Saiu do sistema','2026-03-05 11:10:44'),
(376,1,'LOGIN','Acesso realizado','2026-03-05 11:11:04'),
(377,1,'USUÁRIO','Resetou senha de natasha','2026-03-05 11:11:16'),
(378,1,'LOGOUT','Saiu do sistema','2026-03-05 11:11:32'),
(379,27,'LOGIN','Acesso realizado','2026-03-05 11:11:44'),
(380,27,'LOGOUT','Saiu do sistema','2026-03-05 11:12:08'),
(381,27,'LOGIN','Acesso realizado','2026-03-05 11:12:22'),
(382,27,'LOGOUT','Saiu do sistema','2026-03-05 11:12:35'),
(383,1,'LOGIN','Acesso realizado','2026-03-05 11:12:49'),
(384,1,'USUÁRIO','Resetou senha de natasha','2026-03-05 11:13:11'),
(385,1,'USUÁRIO','Alterou status de natasha para Inativo','2026-03-05 11:13:16'),
(386,1,'USUÁRIO','Cadastrou: ludmila','2026-03-05 11:13:59'),
(387,1,'USUÁRIO','Cadastrou: ludmila','2026-03-05 11:14:42'),
(388,1,'USUÁRIO','Cadastro em massa: 1 sucessos, 2 erros','2026-03-05 11:15:28'),
(389,1,'USUÁRIO','Cadastro em massa: 0 sucessos, 3 erros','2026-03-05 11:15:36'),
(390,1,'USUÁRIO','Cadastro em massa: 3 sucessos, 0 erros','2026-03-05 11:15:55'),
(391,1,'USUÁRIO','Cadastrou: SUPERVISOR SERRA','2026-03-05 11:23:27'),
(392,1,'LOGIN','Acesso realizado','2026-03-05 11:27:18'),
(393,1,'LOGOUT','Saiu do sistema','2026-03-05 11:30:37'),
(394,4,'LOGIN','Acesso realizado','2026-03-05 11:30:49'),
(395,4,'LOGOUT','Saiu do sistema','2026-03-05 11:30:57'),
(396,6,'LOGIN','Acesso realizado','2026-03-05 11:31:20'),
(397,6,'LOGOUT','Saiu do sistema','2026-03-05 11:32:45'),
(398,4,'LOGIN','Acesso realizado','2026-03-05 11:32:55'),
(399,1,'LOGIN','Acesso realizado','2026-03-05 11:36:43'),
(400,1,'USUÁRIO','Cadastrou: SUPERVISOR SERRA','2026-03-05 11:37:29'),
(401,1,'LOGOUT','Saiu do sistema','2026-03-05 11:43:21'),
(402,39,'LOGIN','Acesso realizado','2026-03-05 11:43:33'),
(403,39,'LOGOUT','Saiu do sistema','2026-03-05 11:43:45'),
(404,1,'LOGIN','Acesso realizado','2026-03-05 11:43:59'),
(405,1,'LOGOUT','Saiu do sistema','2026-03-05 11:44:18'),
(406,26,'LOGIN','Acesso realizado','2026-03-05 11:44:23'),
(407,26,'LOGOUT','Saiu do sistema','2026-03-05 11:46:12'),
(408,39,'LOGIN','Acesso realizado','2026-03-05 11:46:25'),
(409,1,'LOGIN','Acesso realizado','2026-03-05 11:47:01'),
(410,1,'LOGOUT','Saiu do sistema','2026-03-05 11:53:14'),
(411,4,'LOGIN','Acesso realizado','2026-03-05 11:53:23'),
(412,4,'LOGOUT','Saiu do sistema','2026-03-05 11:54:18'),
(413,39,'LOGIN','Acesso realizado','2026-03-05 11:55:02'),
(414,39,'LOGOUT','Saiu do sistema','2026-03-05 12:18:55'),
(415,1,'LOGIN','Acesso realizado','2026-03-05 12:19:04'),
(416,39,'LOGOUT','Saiu do sistema','2026-03-05 12:21:54'),
(417,39,'LOGIN','Acesso realizado','2026-03-05 12:24:47'),
(418,39,'LOGOUT','Saiu do sistema','2026-03-05 12:33:16'),
(419,39,'LOGIN','Acesso realizado','2026-03-05 12:33:28'),
(420,39,'LOGOUT','Saiu do sistema','2026-03-05 12:35:05'),
(421,39,'LOGIN','Acesso realizado','2026-03-05 12:35:20'),
(422,39,'LOGIN','Acesso realizado','2026-03-05 13:11:12'),
(423,39,'LOGOUT','Saiu do sistema','2026-03-05 13:13:41'),
(424,1,'LOGIN','Acesso realizado','2026-03-05 13:13:48'),
(425,39,'LOGIN','Acesso realizado','2026-03-05 13:19:38'),
(426,39,'APROVAÇÃO','Venda 116 aprovada - R$ 310.0','2026-03-05 13:23:17'),
(427,39,'APROVAÇÃO','Venda 114 aprovada - R$ 420.0','2026-03-05 13:23:19'),
(428,39,'APROVAÇÃO','Venda 112 aprovada - R$ 280.0','2026-03-05 13:23:21'),
(429,39,'APROVAÇÃO','Venda 110 aprovada - R$ 350.0','2026-03-05 13:23:23'),
(430,39,'REPROVAÇÃO','Venda 124 reprovada','2026-03-05 13:26:43'),
(431,39,'REPROVAÇÃO','Venda 118 reprovada','2026-03-05 13:26:46'),
(432,39,'REPROVAÇÃO','Venda 122 reprovada','2026-03-05 13:26:49'),
(433,1,'LOGOUT','Saiu do sistema','2026-03-05 13:28:11'),
(434,22,'LOGIN','Acesso realizado','2026-03-05 13:28:22'),
(435,22,'VENDA','Venda Nova: 549368 - R$ 89.9','2026-03-05 13:30:46'),
(436,22,'VENDA','Venda Nova: 549368 - R$ 89.9','2026-03-05 13:33:31'),
(437,22,'VENDA','Venda Nova: 549388 - R$ 109.9','2026-03-05 13:38:22'),
(438,22,'VENDA','Downgrade: 549388 - R$ 109.9 (anterior: R$ 129.9)','2026-03-05 13:38:43'),
(439,22,'VENDA','Downgrade: t5382 - R$ 79.9 (anterior: R$ 129.9)','2026-03-05 13:41:41'),
(440,39,'APROVAÇÃO','Venda 128 aprovada - R$ 109.9','2026-03-05 13:46:53'),
(441,39,'APROVAÇÃO','Venda 129 aprovada - R$ 109.9','2026-03-05 13:46:56'),
(442,39,'APROVAÇÃO','Venda 130 aprovada - R$ 79.9','2026-03-05 13:53:23'),
(443,39,'REPROVAÇÃO','Venda 126 reprovada','2026-03-05 13:53:26'),
(444,39,'REPROVAÇÃO','Venda 127 reprovada','2026-03-05 13:53:34'),
(445,1,'LOGIN','Acesso realizado','2026-03-05 14:19:06'),
(446,1,'META','Metas salvas para Geral','2026-03-05 14:19:53'),
(447,4,'LOGIN','Acesso realizado','2026-03-05 14:40:14'),
(448,4,'VENDA','Upgrade: yo927 - R$ 89.0 (anterior: R$ 79.9)','2026-03-05 14:42:59'),
(449,4,'LOGOUT','Saiu do sistema','2026-03-05 14:43:03'),
(450,2,'LOGIN','Acesso realizado','2026-03-05 14:43:20'),
(451,2,'APROVAÇÃO','Venda 131 aprovada - R$ 89.0','2026-03-05 14:43:38'),
(452,2,'LOGOUT','Saiu do sistema','2026-03-05 14:44:06'),
(453,4,'LOGIN','Acesso realizado','2026-03-05 14:44:11'),
(454,4,'VENDA','Upgrade: y680 - R$ 89.9 (anterior: R$ 79.9)','2026-03-05 14:44:39'),
(455,4,'LOGOUT','Saiu do sistema','2026-03-05 14:44:43'),
(456,4,'LOGIN','Acesso realizado','2026-03-05 15:05:29'),
(457,4,'LOGOUT','Saiu do sistema','2026-03-05 15:08:23'),
(458,1,'USUÁRIO','Cadastrou: SUPERVISOR SALI','2026-03-05 15:22:36'),
(459,1,'USUÁRIO','Cadastrou: thiago marcio','2026-03-05 15:23:04'),
(460,1,'LOGOUT','Saiu do sistema','2026-03-05 15:23:12'),
(461,42,'LOGIN','Acesso realizado','2026-03-05 15:23:23'),
(462,42,'VENDA','Venda Nova: 702759 - R$ 90.9','2026-03-05 15:23:46'),
(463,42,'VENDA','Upgrade: 129 - R$ 90.9 (anterior: R$ 89.9)','2026-03-05 15:24:06'),
(464,42,'VENDA','Venda Nova: 89,90 - R$ 90.9','2026-03-05 15:24:23'),
(465,42,'LOGOUT','Saiu do sistema','2026-03-05 15:24:44'),
(466,41,'LOGIN','Acesso realizado','2026-03-05 15:24:53'),
(467,41,'APROVAÇÃO','Venda 135 aprovada - R$ 90.9','2026-03-05 15:24:58'),
(468,41,'APROVAÇÃO','Venda 134 aprovada - R$ 90.9','2026-03-05 15:25:01'),
(469,41,'APROVAÇÃO','Venda 133 aprovada - R$ 90.9','2026-03-05 15:25:04'),
(470,41,'LOGOUT','Saiu do sistema','2026-03-05 15:26:43'),
(471,42,'LOGIN','Acesso realizado','2026-03-05 15:26:59'),
(472,42,'VENDA','Upgrade: 739468 - R$ 129.0 (anterior: R$ 80.0)','2026-03-05 15:27:26'),
(473,42,'VENDA','Upgrade: 4823u - R$ 129.0 (anterior: R$ 80.0)','2026-03-05 15:27:44'),
(474,42,'VENDA','Venda Nova: 4823866g - R$ 129.0','2026-03-05 15:27:54'),
(475,42,'LOGOUT','Saiu do sistema','2026-03-05 15:27:57'),
(476,41,'LOGIN','Acesso realizado','2026-03-05 15:28:15'),
(477,41,'LOGOUT','Saiu do sistema','2026-03-05 15:30:52'),
(478,42,'LOGIN','Acesso realizado','2026-03-05 15:31:07'),
(479,42,'VENDA','Downgrade: 7202830 - R$ 89.0 (anterior: R$ 129.9)','2026-03-05 15:31:40'),
(480,42,'LOGOUT','Saiu do sistema','2026-03-05 15:31:41'),
(481,41,'LOGIN','Acesso realizado','2026-03-05 15:31:50'),
(482,41,'REPROVAÇÃO','Venda 138 reprovada','2026-03-05 15:37:32'),
(483,41,'APROVAÇÃO','Venda 139 aprovada - R$ 89.0','2026-03-05 15:37:49'),
(484,1,'LOGIN','Acesso realizado','2026-03-05 15:38:08'),
(485,1,'LOGOUT','Saiu do sistema','2026-03-05 15:38:25'),
(486,20,'LOGIN','Acesso realizado','2026-03-05 15:38:51'),
(487,20,'LOGIN','Acesso realizado','2026-03-05 19:26:14'),
(488,26,'BACKUP_AUTOMATICO','Backup automático: C:\\Users\\Asus\\Desktop\\plataformaMell\\backup_auto_plataforma_mell_2026-03-05_16-26.sql','2026-03-05 19:26:14');
/*!40000 ALTER TABLE `logs_sistema` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `meta`
--

DROP TABLE IF EXISTS `meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `meta` (
  `id_meta` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `valor` decimal(10,0) NOT NULL,
  `ativo` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id_meta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meta`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `meta` WRITE;
/*!40000 ALTER TABLE `meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `meta` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `metas_regionais`
--

DROP TABLE IF EXISTS `metas_regionais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `metas_regionais` (
  `id_meta` int(11) NOT NULL AUTO_INCREMENT,
  `id_regional` int(11) NOT NULL,
  `mes_referencia` date NOT NULL,
  `meta_vendas_qtd` int(11) DEFAULT 0,
  `meta_migracao_qtd` int(11) DEFAULT 0,
  PRIMARY KEY (`id_meta`),
  UNIQUE KEY `id_regional` (`id_regional`,`mes_referencia`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metas_regionais`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `metas_regionais` WRITE;
/*!40000 ALTER TABLE `metas_regionais` DISABLE KEYS */;
INSERT INTO `metas_regionais` VALUES
(1,1,'2026-02-01',1,1),
(2,2,'2026-02-01',100000,1),
(6,5,'2026-02-01',10,10),
(15,1,'2026-03-01',40,1236),
(16,5,'2026-03-01',80,1232);
/*!40000 ALTER TABLE `metas_regionais` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `notificacoes`
--

DROP TABLE IF EXISTS `notificacoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificacoes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `mensagem` text NOT NULL,
  `destinatario` varchar(50) NOT NULL,
  `data_envio` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `notificacoes` WRITE;
/*!40000 ALTER TABLE `notificacoes` DISABLE KEYS */;
INSERT INTO `notificacoes` VALUES
(1,'Atualização ','na data do dia \'x\' havera atualização  as \'y\'','Todos','2026-02-24 17:51:56'),
(2,'implelementaçao ','🚨🚨impoimportante 🚨🚨\nimplementação sistemica nos proximos dias ','Supervisores','2026-02-25 15:20:46'),
(3,'🚨teste de notificação 🚨','corpo da notificaçao ','Todos','2026-02-26 17:11:49'),
(4,'novo teste','teste apos adiçao de funçao de backup  ','Todos','2026-02-26 20:28:26'),
(5,'🆕 Novo Treinamento: desempenho ','Um novo conteúdo de Sistema foi liberado. Confira na sua biblioteca!','Vendedor','2026-03-02 19:01:20'),
(6,'Novo Treinamento Disponível','Um novo conteúdo de Vendas foi publicado.','Vendedor','2026-03-02 19:11:32'),
(7,'teste ','teste  notificaçao apos atualizar ','Todos','2026-03-02 19:19:37'),
(8,'teste ','teste ','Todos','2026-03-02 19:25:08'),
(9,'Teste Manual','Verificando o sino agora','Todos','2026-03-02 19:39:56'),
(10,'teste ','teste oqnsk','Todos','2026-03-02 19:42:55'),
(11,'teste ','tetse ','Todos','2026-03-02 19:46:35'),
(12,'teste ','teste ','Todos','2026-03-02 19:49:56'),
(13,'🆕 Novo Treinamento: teste final ','Um novo conteúdo de Vendas foi liberado para você na biblioteca!','Todos','2026-03-02 19:58:18'),
(14,'🆕 Novo Treinamento: ultimo ','Um novo conteúdo de Vendas foi liberado. Confira na sua biblioteca!','Todos','2026-03-02 20:00:45'),
(15,'🆕 Novo Treinamento: teste ','Um novo conteúdo de Sistema foi liberado. Confira na sua biblioteca!','Admins','2026-03-02 20:04:04'),
(16,'Ação Corretiva: ultimo ','Prazo de 7 dias. Obs: teste','Todos','2026-03-03 17:40:34'),
(17,'🚀 Novo Conteúdo','Um novo treinamento de Vendas foi publicado: teste ','admin','2026-03-03 19:37:04'),
(18,'teste','teste','Todos','2026-03-03 19:38:06'),
(19,'um nvo test ','teste ','todos','2026-03-03 19:45:44'),
(20,'teste de notificaçao ','teste de notificaçao ','todos','2026-03-03 19:50:41'),
(21,'teste de notificaçao ','notificaçao ','todos','2026-03-03 20:10:17'),
(22,'teste ','jose maria joao ','todos','2026-03-03 20:10:42'),
(23,'teste ','teste ','todos','2026-03-03 20:15:28'),
(24,'teste ','teste odudmd,','todos','2026-03-03 20:21:08'),
(25,'🚀 Novo Conteúdo','Um novo treinamento de Vendas foi publicado: teste de notificaçao ','admin','2026-03-03 20:22:33'),
(26,'Teste de Sistema','Se você está lendo isso, o banco está ok!','todos','2026-03-03 20:27:16'),
(27,'Sistema Online','As notificações foram configuradas com sucesso!','todos','2026-03-03 20:27:31'),
(28,'TESTE URGENTE','Se aparecer, o sistema está OK','todos','2026-03-03 20:33:19'),
(29,'teste ','teste ','todos','2026-03-03 20:34:07'),
(30,'Teste de Conexão','Se você vê isso, o problema é o filtro de cargo.','todos','2026-03-03 20:34:31'),
(31,'teste ','teste ','todos','2026-03-03 20:42:26'),
(32,'teste ','yesgsm','todos','2026-03-03 20:48:21'),
(33,'teste ','teste ','todos','2026-03-03 20:50:33'),
(34,'teste ','teste','todos','2026-03-04 18:17:26');
/*!40000 ALTER TABLE `notificacoes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `notificacoes_lidas`
--

DROP TABLE IF EXISTS `notificacoes_lidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificacoes_lidas` (
  `id_usuario` int(11) NOT NULL,
  `id_notificacao` int(11) NOT NULL,
  `data_leitura` datetime DEFAULT NULL,
  PRIMARY KEY (`id_usuario`,`id_notificacao`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacoes_lidas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `notificacoes_lidas` WRITE;
/*!40000 ALTER TABLE `notificacoes_lidas` DISABLE KEYS */;
INSERT INTO `notificacoes_lidas` VALUES
(1,1,'2026-03-04 14:16:05'),
(1,3,'2026-03-04 14:16:05'),
(1,4,'2026-03-04 14:16:05'),
(1,7,'2026-03-04 14:16:05'),
(1,8,'2026-03-04 14:16:05'),
(1,9,'2026-03-04 14:16:05'),
(1,10,'2026-03-04 14:16:05'),
(1,11,'2026-03-04 14:16:05'),
(1,12,'2026-03-04 14:16:05'),
(1,13,'2026-03-04 14:16:05'),
(1,14,'2026-03-04 14:16:05'),
(1,16,'2026-03-04 14:16:05'),
(1,17,'2026-03-04 14:16:05'),
(1,18,'2026-03-04 14:16:05'),
(1,19,'2026-03-04 14:16:05'),
(1,20,'2026-03-04 14:16:05'),
(1,21,'2026-03-04 14:16:05'),
(1,22,'2026-03-04 14:16:05'),
(1,23,'2026-03-04 14:16:05'),
(1,24,'2026-03-04 14:16:05'),
(1,25,'2026-03-04 14:16:05'),
(1,26,'2026-03-04 14:16:05'),
(1,27,'2026-03-04 14:16:05'),
(1,28,'2026-03-04 14:16:05'),
(1,29,'2026-03-04 14:16:05'),
(1,30,'2026-03-04 14:16:05'),
(1,31,'2026-03-04 14:16:05'),
(1,32,'2026-03-04 14:16:05'),
(1,33,'2026-03-04 14:16:05'),
(1,34,'2026-03-04 15:33:34'),
(2,1,'2026-03-04 15:32:14'),
(2,3,'2026-03-04 15:32:14'),
(2,4,'2026-03-04 15:32:14'),
(2,7,'2026-03-04 15:32:14'),
(2,8,'2026-03-04 15:32:14'),
(2,9,'2026-03-04 15:32:14'),
(2,10,'2026-03-04 15:32:14'),
(2,11,'2026-03-04 15:32:14'),
(2,12,'2026-03-04 15:32:14'),
(2,13,'2026-03-04 15:32:14'),
(2,14,'2026-03-04 15:32:14'),
(2,16,'2026-03-04 15:32:14'),
(2,18,'2026-03-04 15:32:14'),
(2,19,'2026-03-04 15:32:14'),
(2,20,'2026-03-04 15:32:14'),
(2,21,'2026-03-04 15:32:14'),
(2,22,'2026-03-04 15:32:14'),
(2,23,'2026-03-04 15:32:14'),
(2,24,'2026-03-04 15:32:14'),
(2,26,'2026-03-04 15:32:14'),
(2,27,'2026-03-04 15:32:14'),
(2,28,'2026-03-04 15:32:14'),
(2,29,'2026-03-04 15:32:14'),
(2,30,'2026-03-04 15:32:14'),
(2,31,'2026-03-04 15:32:14'),
(2,32,'2026-03-04 15:32:14'),
(2,33,'2026-03-04 15:32:14'),
(2,34,'2026-03-04 15:32:14'),
(4,1,'2026-03-04 16:48:20'),
(4,3,'2026-03-04 16:48:20'),
(4,4,'2026-03-04 16:48:20'),
(4,5,'2026-03-04 16:48:20'),
(4,6,'2026-03-04 16:48:20'),
(4,7,'2026-03-04 16:48:20'),
(4,8,'2026-03-04 16:48:20'),
(4,9,'2026-03-04 16:48:20'),
(4,10,'2026-03-04 16:48:20'),
(4,11,'2026-03-04 16:48:20'),
(4,12,'2026-03-04 16:48:20'),
(4,13,'2026-03-04 16:48:20'),
(4,14,'2026-03-04 16:48:20'),
(4,16,'2026-03-04 16:48:20'),
(4,18,'2026-03-04 16:48:20'),
(4,19,'2026-03-04 16:48:20'),
(4,20,'2026-03-04 16:48:20'),
(4,21,'2026-03-04 16:48:20'),
(4,22,'2026-03-04 16:48:20'),
(4,23,'2026-03-04 16:48:20'),
(4,24,'2026-03-04 16:48:20'),
(4,26,'2026-03-04 16:48:20'),
(4,27,'2026-03-04 16:48:20'),
(4,28,'2026-03-04 16:48:20'),
(4,29,'2026-03-04 16:48:20'),
(4,30,'2026-03-04 16:48:20'),
(4,31,'2026-03-04 16:48:20'),
(4,32,'2026-03-04 16:48:20'),
(4,33,'2026-03-04 16:48:20'),
(4,34,'2026-03-04 16:48:20'),
(19,1,'2026-03-04 16:19:42'),
(19,3,'2026-03-04 16:19:42'),
(19,4,'2026-03-04 16:19:42'),
(19,7,'2026-03-04 16:19:42'),
(19,8,'2026-03-04 16:19:42'),
(19,9,'2026-03-04 16:19:42'),
(19,10,'2026-03-04 16:19:42'),
(19,11,'2026-03-04 16:19:42'),
(19,12,'2026-03-04 16:19:42'),
(19,13,'2026-03-04 16:19:42'),
(19,14,'2026-03-04 16:19:42'),
(19,16,'2026-03-04 16:19:42'),
(19,18,'2026-03-04 16:19:42'),
(19,19,'2026-03-04 16:19:42'),
(19,20,'2026-03-04 16:19:42'),
(19,21,'2026-03-04 16:19:42'),
(19,22,'2026-03-04 16:19:42'),
(19,23,'2026-03-04 16:19:42'),
(19,24,'2026-03-04 16:19:42'),
(19,26,'2026-03-04 16:19:42'),
(19,27,'2026-03-04 16:19:42'),
(19,28,'2026-03-04 16:19:42'),
(19,29,'2026-03-04 16:19:42'),
(19,30,'2026-03-04 16:19:42'),
(19,31,'2026-03-04 16:19:42'),
(19,32,'2026-03-04 16:19:42'),
(19,33,'2026-03-04 16:19:42'),
(19,34,'2026-03-04 16:19:42'),
(20,1,'2026-03-04 15:17:28'),
(20,3,'2026-03-04 15:17:28'),
(20,4,'2026-03-04 15:17:28'),
(20,7,'2026-03-04 15:17:28'),
(20,8,'2026-03-04 15:17:28'),
(20,9,'2026-03-04 15:17:28'),
(20,10,'2026-03-04 15:17:28'),
(20,11,'2026-03-04 15:17:28'),
(20,12,'2026-03-04 15:17:28'),
(20,13,'2026-03-04 15:17:28'),
(20,14,'2026-03-04 15:17:28'),
(20,16,'2026-03-04 15:17:28'),
(20,18,'2026-03-04 15:17:28'),
(20,19,'2026-03-04 15:17:28'),
(20,20,'2026-03-04 15:17:28'),
(20,21,'2026-03-04 15:17:28'),
(20,22,'2026-03-04 15:17:28'),
(20,23,'2026-03-04 15:17:28'),
(20,24,'2026-03-04 15:17:28'),
(20,26,'2026-03-04 15:17:28'),
(20,27,'2026-03-04 15:17:28'),
(20,28,'2026-03-04 15:17:28'),
(20,29,'2026-03-04 15:17:28'),
(20,30,'2026-03-04 15:17:28'),
(20,31,'2026-03-04 15:17:28'),
(20,32,'2026-03-04 15:17:28'),
(20,33,'2026-03-04 15:17:28'),
(20,34,'2026-03-04 15:17:28');
/*!40000 ALTER TABLE `notificacoes_lidas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `regional`
--

DROP TABLE IF EXISTS `regional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `regional` (
  `id_regional` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id_regional`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regional`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `regional` WRITE;
/*!40000 ALTER TABLE `regional` DISABLE KEYS */;
INSERT INTO `regional` VALUES
(1,'Moc',1),
(2,'Curvelo',1),
(3,'Salinas',1),
(4,'Serra Geral',1),
(5,'Geral',1);
/*!40000 ALTER TABLE `regional` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `status` (
  `id_status` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id_status`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
INSERT INTO `status` VALUES
(1,'EM ANÁLISE',1),
(2,'APROVADO',1),
(3,'REPROVADO',1),
(4,'CANCELADO',1);
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `status_financeiro`
--

DROP TABLE IF EXISTS `status_financeiro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_financeiro` (
  `id_status_financeiro` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `ativo` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_status_financeiro`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_financeiro`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `status_financeiro` WRITE;
/*!40000 ALTER TABLE `status_financeiro` DISABLE KEYS */;
INSERT INTO `status_financeiro` VALUES
(1,'PENDENTE DE AUDITORIA',1),
(2,'PROCESSADO',1);
/*!40000 ALTER TABLE `status_financeiro` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `supervisor_vendedor`
--

DROP TABLE IF EXISTS `supervisor_vendedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `supervisor_vendedor` (
  `id_supervisor` int(11) NOT NULL,
  `id_vendedor` int(11) NOT NULL,
  `data_inicio` datetime DEFAULT current_timestamp(),
  `ativo` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id_supervisor`,`id_vendedor`),
  KEY `id_vendedor` (`id_vendedor`),
  CONSTRAINT `supervisor_vendedor_ibfk_1` FOREIGN KEY (`id_supervisor`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `supervisor_vendedor_ibfk_2` FOREIGN KEY (`id_vendedor`) REFERENCES `users` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supervisor_vendedor`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `supervisor_vendedor` WRITE;
/*!40000 ALTER TABLE `supervisor_vendedor` DISABLE KEYS */;
INSERT INTO `supervisor_vendedor` VALUES
(2,4,'2026-03-05 09:15:45',1),
(2,14,'2026-03-05 09:15:45',1),
(2,16,'2026-03-05 09:15:45',1),
(3,5,'2026-03-05 09:15:51',1),
(3,6,'2026-03-05 09:15:51',1),
(3,15,'2026-03-05 09:15:51',1),
(3,17,'2026-03-05 09:15:51',1),
(39,21,'2026-03-05 09:15:38',1),
(39,22,'2026-03-05 09:15:38',1),
(39,25,'2026-03-05 09:15:38',1),
(39,26,'2026-03-05 09:15:38',1);
/*!40000 ALTER TABLE `supervisor_vendedor` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `tipo_operacao`
--

DROP TABLE IF EXISTS `tipo_operacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_operacao` (
  `id_tipo_operacao` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id_tipo_operacao`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_operacao`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `tipo_operacao` WRITE;
/*!40000 ALTER TABLE `tipo_operacao` DISABLE KEYS */;
INSERT INTO `tipo_operacao` VALUES
(1,'Venda Nova',1),
(2,'Migração (Upgrade)',1),
(3,'Telefonia Avulsa',1),
(4,'B2B',1);
/*!40000 ALTER TABLE `tipo_operacao` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `tipo_usuario`
--

DROP TABLE IF EXISTS `tipo_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_usuario` (
  `id_tipo_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) DEFAULT NULL,
  `ativo` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_tipo_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_usuario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `tipo_usuario` WRITE;
/*!40000 ALTER TABLE `tipo_usuario` DISABLE KEYS */;
INSERT INTO `tipo_usuario` VALUES
(1,'Admin',1),
(2,'Vendedor',1),
(3,'Supervisor',1),
(4,'Auditor Financeiro',1),
(26,'SUPORTE TECNICO',1);
/*!40000 ALTER TABLE `tipo_usuario` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `treinamento_progresso`
--

DROP TABLE IF EXISTS `treinamento_progresso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `treinamento_progresso` (
  `id_progresso` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `id_treinamento` int(11) DEFAULT NULL,
  `data_conclusao` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_progresso`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_treinamento` (`id_treinamento`),
  CONSTRAINT `treinamento_progresso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `treinamento_progresso_ibfk_2` FOREIGN KEY (`id_treinamento`) REFERENCES `treinamentos` (`id_treinamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treinamento_progresso`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `treinamento_progresso` WRITE;
/*!40000 ALTER TABLE `treinamento_progresso` DISABLE KEYS */;
/*!40000 ALTER TABLE `treinamento_progresso` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `treinamentos`
--

DROP TABLE IF EXISTS `treinamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `treinamentos` (
  `id_treinamento` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `descricao` text DEFAULT NULL,
  `url_video` varchar(255) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `data_cadastro` datetime DEFAULT current_timestamp(),
  `url_documento` varchar(500) DEFAULT NULL,
  `cargo_destino` int(11) DEFAULT NULL,
  `validade_meses` int(11) DEFAULT 12,
  `id_tipo_usuario_alvo` int(11) DEFAULT 0,
  PRIMARY KEY (`id_treinamento`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treinamentos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `treinamentos` WRITE;
/*!40000 ALTER TABLE `treinamentos` DISABLE KEYS */;
INSERT INTO `treinamentos` VALUES
(9,'teste01','teste 01','https://manus.im/app','Vendas','2026-03-02 11:14:16','https://manus.com.br',NULL,12,0),
(10,'um novo teste ','um novo teste ','https://chat.deepseek.com/a/c','Vendas','2026-03-02 11:47:29','https://chat.deepseek.com',2,3,0),
(11,'teste ','teste','https://drive.google.com','Vendas','2026-03-02 12:28:50','https://drive.google.com/drive/home',0,12,0),
(12,'teste apos alteraçoes ','teste apos alteraçoes mensgaem ','https://chat.deepseek.com/a/','Vendas','2026-03-02 15:50:38','https://chat.deepseek.com/a/chat/s/b89d0172-a1a1-4938-9c6c-3f5b4fb57820',NULL,12,2),
(13,'desempenho ','desempenho 02','https://chat.deepseek.com/a/chat/s/b89d0172-a1a','Sistema','2026-03-02 16:01:20','https://chat.deepseek.com',NULL,12,2),
(14,'teste final ','este e uma prova que foi corrigo o  problema ','https://drive.google.com/me','Vendas','2026-03-02 16:58:18','https://drive.goo.com',NULL,12,0),
(15,'ultimo ','teste de atusistemica ','https:// umnovotestedeatualizaçeos','Vendas','2026-03-02 17:00:45','https:// umnovotested.com',NULL,12,0),
(16,'teste ','teste sem bal~~ao ','https:// umnovotestedeatualizaçeos','Sistema','2026-03-02 17:04:04','https:// umnovotestedea.com',NULL,12,1),
(17,'analise ','novo teste ','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:13:14','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,2),
(18,'pc ','pc','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:18:19','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,1),
(19,'teste de notificaçao','teste de notificaçao','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:34:40','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,26),
(20,'teste ','https://www.youtube.com/watch?v=WH34Ea693Cs','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:37:04','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,1),
(21,'teste de notificaçao ','teste de notificaçao ','httpps/;linkteste.com.br ','Vendas','2026-03-03 17:22:33','httpps/;linkteste.com.br ',NULL,12,1);
/*!40000 ALTER TABLE `treinamentos` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `treinamentos_concluidos`
--

DROP TABLE IF EXISTS `treinamentos_concluidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `treinamentos_concluidos` (
  `id_conclusao` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `id_treinamento` int(11) DEFAULT NULL,
  `data_conclusao` datetime DEFAULT NULL,
  `data_vencimento` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_conclusao`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_treinamento` (`id_treinamento`),
  CONSTRAINT `treinamentos_concluidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `treinamentos_concluidos_ibfk_2` FOREIGN KEY (`id_treinamento`) REFERENCES `treinamentos` (`id_treinamento`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treinamentos_concluidos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `treinamentos_concluidos` WRITE;
/*!40000 ALTER TABLE `treinamentos_concluidos` DISABLE KEYS */;
INSERT INTO `treinamentos_concluidos` VALUES
(1,4,9,'2026-03-02 11:15:44','2027-03-02 11:15:44','Concluído'),
(2,4,10,'2026-02-15 10:00:00','2026-05-15 10:00:00','Concluído'),
(3,4,9,'2026-01-20 14:30:00','2027-01-20 14:30:00','Concluído'),
(4,2,10,'2026-02-10 09:15:00','2026-05-10 09:15:00','Concluído'),
(5,6,13,'2026-02-25 16:45:00','2027-02-25 16:45:00','Concluído'),
(6,19,15,'2026-03-01 11:20:00','2027-03-01 11:20:00','Concluído'),
(7,2,11,'2026-03-03 14:52:44','2027-03-03 14:52:44','Concluído'),
(8,4,11,'2026-03-03 15:48:46','2027-03-03 15:48:46','Concluído'),
(9,2,9,'2026-03-03 15:49:56','2027-03-03 15:49:56','Concluído'),
(10,1,9,'2026-03-03 16:18:44','2027-03-03 16:18:44','Concluído'),
(11,1,10,'2026-03-03 16:18:46','2026-06-03 16:18:46','Concluído'),
(12,1,11,'2026-03-03 16:18:48','2027-03-03 16:18:48','Concluído'),
(13,1,14,'2026-03-03 16:18:50','2027-03-03 16:18:50','Concluído'),
(14,1,15,'2026-03-03 16:18:52','2027-03-03 16:18:52','Concluído'),
(15,24,9,'2026-03-03 16:23:41','2027-03-03 16:23:41','Concluído'),
(16,4,14,'2026-03-03 17:22:54','2027-03-03 17:22:54','Concluído'),
(17,4,15,'2026-03-03 17:22:57','2027-03-03 17:22:57','Concluído'),
(18,6,9,'2026-03-03 17:24:57','2027-03-03 17:24:57','Concluído'),
(19,6,10,'2026-03-03 17:24:59','2026-06-03 17:24:59','Concluído'),
(20,6,11,'2026-03-03 17:25:01','2027-03-03 17:25:01','Concluído'),
(21,6,14,'2026-03-03 17:25:03','2027-03-03 17:25:03','Concluído'),
(22,6,15,'2026-03-03 17:25:04','2027-03-03 17:25:04','Concluído'),
(23,2,14,'2026-03-03 17:26:19','2027-03-03 17:26:19','Concluído'),
(24,2,15,'2026-03-03 17:26:21','2027-03-03 17:26:21','Concluído');
/*!40000 ALTER TABLE `treinamentos_concluidos` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nome_usuario` varchar(255) DEFAULT NULL,
  `cpf` varchar(11) DEFAULT NULL,
  `id_regional` int(11) DEFAULT NULL,
  `ativo` tinyint(4) NOT NULL DEFAULT 1,
  `id_tipo_usuario` int(11) DEFAULT NULL,
  `id_usuario_hubsoft` int(11) DEFAULT NULL,
  `senha` varchar(255) NOT NULL DEFAULT 'Mell@9004',
  `regional` varchar(100) DEFAULT 'Geral',
  `ultimo_acesso` datetime DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `id_regional` (`id_regional`),
  KEY `id_tipo_usuario` (`id_tipo_usuario`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_regional`) REFERENCES `regional` (`id_regional`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `tipo_usuario` (`id_tipo_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'ADMINISTRADOR','admin123',5,1,1,NULL,'Mell@9004','MOC','2026-03-04 16:06:30'),
(2,'SUPERVISOR MOC','123456',1,1,3,NULL,'Mell@9004','MOC','2026-03-04 10:52:10'),
(3,'SUPERVISOR CURVELO','123456',2,1,3,NULL,'Mell@9004','MOC','2026-03-04 09:43:37'),
(4,'ANA PAULA PEREIRA ROCHA','12038340633',1,1,2,NULL,'Mell@9004','MOC','2026-03-04 16:38:24'),
(5,'PAMELA LUIZA ALVES ROCHA','01981059679',2,1,2,NULL,'Mell@9004','MOC',NULL),
(6,'PEDRO HENRIQUE PEREIRA SILVA','01230487068',2,1,2,NULL,'Mell@9004','MOC','2026-03-04 09:39:33'),
(14,'ze maria da mel ',NULL,1,1,2,NULL,'Mell@2026','Geral','2026-03-02 15:06:01'),
(15,'ze maria da mel ',NULL,2,1,2,NULL,'Mell@9004','Geral',NULL),
(16,'samanta ',NULL,1,1,2,NULL,'Mell@9004','Geral','2026-03-02 15:06:10'),
(17,'jose aquino ',NULL,2,1,2,NULL,'Mell@9004','Geral','2026-03-02 15:08:43'),
(18,'jojo',NULL,2,1,1,NULL,'Mell@9004','Geral',NULL),
(19,'auditoria_mell',NULL,1,1,4,NULL,'Mell@9004','Geral','2026-03-04 10:52:50'),
(20,'SUPORTE TECNICO','00000000000',5,1,26,NULL,'Mell@9004','Geral','2026-03-03 17:48:14'),
(21,'jose luciano ','12309791341',4,1,2,NULL,'Mell@9004','Serra Geral',NULL),
(22,'claudia ','22212213212',4,1,2,NULL,'Mell@9004','Serra Geral',NULL),
(23,'mercia lopes','12318292710',4,1,1,NULL,'Mell@9004','Serra Geral',NULL),
(24,'GESTOR_TREINAMENTO',NULL,1,1,1,NULL,'Mell@2026','Geral','2026-03-03 17:22:16'),
(25,'otavio','2380883973',4,1,2,NULL,'Mell@9004','Geral',NULL),
(26,'tulio','6529753974',4,1,2,NULL,'Mell@9004','Geral',NULL),
(27,'natasha','79362082639',1,0,1,NULL,'Mell@2026','Geral',NULL),
(33,'joaquina','0937293787',1,1,1,NULL,'Mell@2026','Geral',NULL),
(34,'ludmila','08308725387',1,1,1,NULL,'Mell@2026','Geral',NULL),
(35,'tereza','03792735399',1,1,1,NULL,'Mell@2026','Geral',NULL),
(36,'joaquina','093729378',1,1,1,NULL,'Mell@2026','Geral',NULL),
(39,'SUPERVISOR SERRA GERAL','55566677788',4,1,3,NULL,'Mell@2026','Geral','2026-03-05 09:37:24'),
(40,'SUPERVISOR GERAL','55566677788',5,0,3,NULL,'Mell@2026','Geral',NULL),
(41,'SUPERVISOR SALI','74027258242',3,1,3,NULL,'Mell@9004','Geral',NULL),
(42,'THIAGO MARCIO','52937303793',3,1,2,NULL,'Mell@9004','Geral',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `venda`
--

DROP TABLE IF EXISTS `venda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `venda` (
  `id_venda` int(11) NOT NULL AUTO_INCREMENT,
  `id_tipo_operacao` int(11) NOT NULL,
  `id_usuario_vendedor` int(11) NOT NULL,
  `id_status` int(11) NOT NULL,
  `id_status_financeiro` int(11) DEFAULT 1,
  `valor_venda` decimal(10,2) NOT NULL,
  `valor_venda_antiga` decimal(10,2) DEFAULT 0.00,
  `codigo_cliente_servico` decimal(10,0) DEFAULT NULL,
  `ativo` tinyint(4) NOT NULL DEFAULT 1,
  `data_venda` date NOT NULL DEFAULT curdate(),
  `data_aprovacao` date DEFAULT NULL,
  `codigo_cliente` varchar(50) DEFAULT NULL,
  `valor_anterior` decimal(10,2) DEFAULT 0.00,
  PRIMARY KEY (`id_venda`),
  KEY `id_tipo_operacao` (`id_tipo_operacao`),
  KEY `id_usuario_vendedor` (`id_usuario_vendedor`),
  KEY `id_status` (`id_status`),
  KEY `id_status_financeiro` (`id_status_financeiro`),
  CONSTRAINT `venda_ibfk_1` FOREIGN KEY (`id_tipo_operacao`) REFERENCES `tipo_operacao` (`id_tipo_operacao`),
  CONSTRAINT `venda_ibfk_2` FOREIGN KEY (`id_usuario_vendedor`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `venda_ibfk_3` FOREIGN KEY (`id_status`) REFERENCES `status` (`id_status`),
  CONSTRAINT `venda_ibfk_4` FOREIGN KEY (`id_status_financeiro`) REFERENCES `status_financeiro` (`id_status_financeiro`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `venda` WRITE;
/*!40000 ALTER TABLE `venda` DISABLE KEYS */;
INSERT INTO `venda` VALUES
(6,2,4,2,2,110.00,0.00,10200,1,'2026-02-07',NULL,NULL,0.00),
(7,1,4,2,2,109.00,0.00,177890,1,'2026-02-07',NULL,NULL,0.00),
(8,2,4,2,1,110.00,89.90,1,1,'2026-02-07','2026-02-07',NULL,0.00),
(9,2,4,2,1,110.00,89.90,89321,1,'2026-02-07','2026-02-07',NULL,0.00),
(10,1,4,2,1,0.00,0.00,111111,1,'2026-02-07','2026-02-07',NULL,0.00),
(11,1,4,2,1,1000.00,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(12,1,4,2,1,100.00,0.00,13,1,'2026-02-08','2026-02-08',NULL,0.00),
(13,1,4,2,1,100.00,0.00,4,1,'2026-02-08','2026-02-08',NULL,0.00),
(14,1,4,2,1,100.00,0.00,5,1,'2026-02-08','2026-02-08',NULL,0.00),
(15,1,4,2,1,100.00,0.00,11,1,'2026-02-08','2026-02-08',NULL,0.00),
(16,1,4,2,1,98.00,0.00,99,1,'2026-02-08','2026-02-08',NULL,0.00),
(17,1,4,2,1,90.00,0.00,19,1,'2026-02-08','2026-02-08',NULL,0.00),
(18,1,4,2,1,50.00,0.00,22,1,'2026-02-08','2026-02-08',NULL,0.00),
(19,2,4,2,1,110.00,89.90,1234,1,'2026-02-08','2026-02-08',NULL,0.00),
(20,1,4,2,1,1000.00,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(21,1,4,2,1,0.00,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(22,4,4,2,1,90.00,109.90,101010,1,'2026-02-08','2026-02-08',NULL,0.00),
(23,1,4,2,1,19.00,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(24,1,4,2,1,19.00,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(25,1,4,2,1,19.00,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(26,1,4,2,1,90.00,0.00,909090909,1,'2026-02-10',NULL,NULL,0.00),
(27,1,4,2,1,100000.00,0.00,10101010,1,'2026-02-10',NULL,NULL,0.00),
(28,2,4,2,1,10.00,8.00,10,1,'2026-02-10',NULL,NULL,0.00),
(29,2,4,2,1,10.00,8.00,20,1,'2026-02-10',NULL,NULL,0.00),
(30,2,4,2,1,20.00,8.00,30,1,'2026-02-10',NULL,NULL,0.00),
(31,2,4,2,1,20.00,8.00,40,1,'2026-02-10',NULL,NULL,0.00),
(32,2,4,2,1,19.00,8.00,50,1,'2026-02-10',NULL,NULL,0.00),
(33,2,4,2,1,20.00,9.00,60,1,'2026-02-10',NULL,NULL,0.00),
(34,2,4,2,1,90.00,9.00,70,1,'2026-02-10',NULL,NULL,0.00),
(35,3,4,2,1,90.00,90.00,1999,1,'2026-02-10',NULL,NULL,0.00),
(36,1,16,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'9090909',0.00),
(37,2,16,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'9090909',90.00),
(38,1,17,2,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'22222',0.00),
(39,2,17,2,1,109.00,0.00,NULL,1,'2026-02-11',NULL,'22221',90.90),
(40,1,17,2,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'paulinho ',0.00),
(41,1,17,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'000000',0.00),
(42,1,17,2,1,2000.00,0.00,NULL,1,'2026-02-11',NULL,'11111',0.00),
(43,1,17,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'333333',0.00),
(44,1,17,2,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'12009',0.00),
(45,2,17,3,1,190.00,0.00,NULL,1,'2026-02-11',NULL,'12009',100.00),
(46,1,4,3,1,10.00,0.00,NULL,1,'2026-02-11',NULL,'22222222',0.00),
(47,1,4,4,1,50.00,0.00,NULL,1,'2026-02-11',NULL,'1122020',0.00),
(48,2,4,2,1,70.00,0.00,NULL,1,'2026-02-11',NULL,'4002',89.90),
(49,2,4,2,1,50.00,0.00,NULL,1,'2026-02-11',NULL,'090909',100.00),
(50,2,4,2,1,10.00,0.00,NULL,1,'2026-02-11',NULL,'202020',20.00),
(51,2,4,2,1,30.00,0.00,NULL,1,'2026-02-11',NULL,'000012',15.00),
(52,2,4,3,1,75.00,0.00,NULL,1,'2026-02-11',NULL,'11111111',85.00),
(53,2,4,4,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'88888',1000.00),
(54,2,4,3,1,20.00,30.00,12980,1,'2026-02-11',NULL,NULL,0.00),
(55,2,4,2,1,50.00,60.00,7,1,'2026-02-11',NULL,NULL,0.00),
(56,1,4,2,1,109.00,0.00,1,1,'2026-02-12',NULL,NULL,0.00),
(57,2,4,2,1,109.00,139.00,2,1,'2026-02-12',NULL,NULL,0.00),
(58,2,4,2,1,100.00,89.00,109090,1,'2026-02-12',NULL,NULL,0.00),
(59,1,4,2,1,120.00,0.00,9009,1,'2026-02-12',NULL,NULL,0.00),
(60,1,4,3,1,109.00,0.00,NULL,1,'2026-02-19',NULL,'marina ',0.00),
(61,1,4,2,1,109.00,0.00,NULL,1,'2026-02-19',NULL,'marina ',0.00),
(62,1,4,2,1,35.00,0.00,NULL,1,'2026-02-23',NULL,'223432',0.00),
(63,1,16,2,1,110.00,0.00,NULL,1,'2026-02-23',NULL,'1232',0.00),
(64,3,16,2,1,90.00,109.90,NULL,1,'2026-02-23',NULL,'1232',0.00),
(65,3,16,2,1,90.00,79.90,NULL,1,'2026-02-23',NULL,'1232',0.00),
(66,1,16,3,1,91.00,0.00,NULL,1,'2026-02-23',NULL,'2222',0.00),
(67,1,16,2,1,91.00,0.00,NULL,1,'2026-02-23',NULL,'2228',0.00),
(68,1,16,2,1,109.00,0.00,NULL,1,'2026-02-23',NULL,'90909',0.00),
(69,2,16,1,1,109.00,100.00,NULL,1,'2026-02-23',NULL,'0010101',0.00),
(70,3,16,1,1,109.00,89.90,NULL,1,'2026-02-27',NULL,'123478',0.00),
(71,1,4,2,1,90.00,0.00,NULL,1,'2026-03-02',NULL,'21211',0.00),
(72,2,4,2,1,90.00,109.90,NULL,1,'2026-03-02',NULL,'21210',0.00),
(73,1,4,2,1,91.00,0.00,NULL,1,'2026-03-02',NULL,'2222',0.00),
(74,1,4,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'222341',0.00),
(75,2,4,2,1,109.90,89.90,NULL,1,'2026-03-02',NULL,'222341',0.00),
(76,1,4,2,1,99.99,0.00,NULL,1,'2026-03-02',NULL,'222341',0.00),
(77,1,16,2,1,89.90,0.00,NULL,1,'2026-03-02',NULL,'21312',0.00),
(78,1,16,2,1,109.00,0.00,NULL,1,'2026-03-02',NULL,'21310',0.00),
(79,3,16,2,1,109.00,129.29,NULL,1,'2026-03-02',NULL,'21310',0.00),
(80,1,16,2,1,109.00,0.00,NULL,1,'2026-03-02',NULL,'212090',0.00),
(81,1,17,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'128253',0.00),
(82,1,17,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'828253',0.00),
(83,3,17,2,1,90.90,109.90,NULL,1,'2026-03-02',NULL,'79352',0.00),
(84,1,17,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'536298',0.00),
(85,1,17,2,1,79.90,0.00,NULL,1,'2026-03-02',NULL,'536298',0.00),
(86,1,17,2,1,79.90,0.00,NULL,1,'2026-03-02',NULL,'82747',0.00),
(87,1,6,2,1,89.90,0.00,NULL,1,'2026-03-02',NULL,'69297',0.00),
(88,1,6,2,1,109.90,0.00,NULL,1,'2026-03-02',NULL,'824396',0.00),
(89,1,6,2,1,79.90,0.00,NULL,1,'2026-03-02',NULL,'436297',0.00),
(90,3,6,2,1,89.90,109.90,NULL,1,'2026-03-02',NULL,'436297',0.00),
(91,2,6,2,1,120.90,89.90,NULL,1,'2026-03-02',NULL,'639398',0.00),
(92,4,6,2,1,89.90,79.90,NULL,1,'2026-03-02',NULL,'75339',0.00),
(93,1,4,2,1,109.90,0.00,NULL,1,'2026-03-03',NULL,'64997',0.00),
(94,1,4,2,1,89.90,0.00,NULL,1,'2026-03-03',NULL,'649',0.00),
(95,1,6,2,1,89.90,0.00,NULL,1,'2026-03-03','2026-03-04','0940749',0.00),
(96,3,6,2,1,89.90,79.90,NULL,1,'2026-03-03','2026-03-04','040749',0.00),
(97,1,6,3,1,109.90,0.00,NULL,1,'2026-03-04',NULL,'9753',0.00),
(98,1,4,2,1,89.90,0.00,NULL,1,'2026-03-04',NULL,'7043',0.00),
(99,2,4,3,1,89.90,0.00,NULL,1,'2026-03-04',NULL,'80835',0.00),
(100,2,15,2,1,109.00,89.00,NULL,1,'2026-03-04','2026-03-04','4306',89.00),
(101,1,15,2,1,89.90,0.00,NULL,1,'2026-03-04','2026-03-04','32t20',0.00),
(102,2,15,2,1,89.90,109.90,NULL,1,'2026-03-04','2026-03-04','65293',109.90),
(103,2,16,2,1,89.90,109.90,NULL,1,'2026-03-04','2026-03-04','33036',109.90),
(104,2,16,2,1,79.90,109.90,NULL,1,'2026-03-04','2026-03-04','2136',109.90),
(105,2,17,2,1,109.00,89.00,NULL,1,'2026-03-04','2026-03-04','4393',89.00),
(106,2,17,3,1,129.90,109.00,NULL,1,'2026-03-04',NULL,'2134',109.00),
(107,2,17,2,1,109.90,89.00,NULL,1,'2026-03-04','2026-03-04','00826',89.00),
(108,2,17,2,1,109.90,89.00,NULL,1,'2026-03-04','2026-03-04','00826',89.00),
(109,1,17,1,1,109.90,0.00,NULL,1,'2026-03-04',NULL,'02829',0.00),
(110,1,21,2,1,350.00,0.00,NULL,1,'2026-03-01','2026-03-05',NULL,0.00),
(111,1,21,2,1,450.00,0.00,NULL,1,'2026-03-05',NULL,NULL,0.00),
(112,1,22,2,1,280.00,0.00,NULL,1,'2026-03-02','2026-03-05',NULL,0.00),
(113,1,22,2,1,390.00,0.00,NULL,1,'2026-03-06',NULL,NULL,0.00),
(114,1,25,2,1,420.00,0.00,NULL,1,'2026-03-03','2026-03-05',NULL,0.00),
(115,1,25,2,1,520.00,0.00,NULL,1,'2026-03-07',NULL,NULL,0.00),
(116,1,26,2,1,310.00,0.00,NULL,1,'2026-03-04','2026-03-05',NULL,0.00),
(117,1,26,2,1,610.00,0.00,NULL,1,'2026-03-08',NULL,NULL,0.00),
(118,1,21,3,1,350.00,0.00,NULL,1,'2026-03-01',NULL,NULL,0.00),
(119,1,21,2,1,450.00,0.00,NULL,1,'2026-03-05',NULL,NULL,0.00),
(120,1,22,1,1,280.00,0.00,NULL,1,'2026-03-02',NULL,NULL,0.00),
(121,1,22,2,1,390.00,0.00,NULL,1,'2026-03-06',NULL,NULL,0.00),
(122,1,25,3,1,420.00,0.00,NULL,1,'2026-03-03',NULL,NULL,0.00),
(123,1,25,2,1,520.00,0.00,NULL,1,'2026-03-07',NULL,NULL,0.00),
(124,1,26,3,1,310.00,0.00,NULL,1,'2026-03-04',NULL,NULL,0.00),
(125,1,26,2,1,610.00,0.00,NULL,1,'2026-03-08',NULL,NULL,0.00),
(126,1,22,3,1,89.90,0.00,NULL,1,'2026-03-05',NULL,'549368',0.00),
(127,1,22,3,1,89.90,0.00,NULL,1,'2026-03-05',NULL,'549368',0.00),
(128,1,22,2,1,109.90,0.00,NULL,1,'2026-03-05','2026-03-05','549388',0.00),
(129,2,22,2,1,109.90,129.90,NULL,1,'2026-03-05','2026-03-05','549388',129.90),
(130,2,22,2,1,79.90,129.90,NULL,1,'2026-03-05','2026-03-05','t5382',129.90),
(131,2,4,2,1,89.00,79.90,NULL,1,'2026-03-05','2026-03-05','yo927',79.90),
(132,2,4,1,1,89.90,79.90,NULL,1,'2026-03-05',NULL,'y680',79.90),
(133,1,42,2,1,90.90,0.00,NULL,1,'2026-03-05','2026-03-05','702759',0.00),
(134,2,42,2,1,90.90,89.90,NULL,1,'2026-03-05','2026-03-05','129',89.90),
(135,1,42,2,1,90.90,0.00,NULL,1,'2026-03-05','2026-03-05','89,90',0.00),
(136,2,42,1,1,129.00,80.00,NULL,1,'2026-03-05',NULL,'739468',80.00),
(137,2,42,1,1,129.00,80.00,NULL,1,'2026-03-05',NULL,'4823u',80.00),
(138,1,42,3,1,129.00,0.00,NULL,1,'2026-03-05',NULL,'4823866g',0.00),
(139,2,42,2,1,89.00,129.90,NULL,1,'2026-03-05','2026-03-05','7202830',129.90);
/*!40000 ALTER TABLE `venda` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-05 16:26:21
