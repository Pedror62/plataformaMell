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
-- Table structure for table `cancelamentos`
--

DROP TABLE IF EXISTS `cancelamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cancelamentos` (
  `id_cancelamento` int(11) NOT NULL AUTO_INCREMENT,
  `id_venda_original` int(11) DEFAULT NULL,
  `id_usuario_vendedor` int(11) NOT NULL,
  `id_regional` int(11) NOT NULL,
  `id_supervisor_cancelamento` int(11) NOT NULL,
  `data_cancelamento` datetime DEFAULT current_timestamp(),
  `data_ocorrencia` date NOT NULL,
  `valor_original` decimal(10,2) NOT NULL,
  `id_motivo_cancelamento` int(11) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `status` enum('pendente','aprovado','revisado') DEFAULT 'pendente',
  `impactou_comissao` tinyint(4) DEFAULT 0,
  `data_estorno_comissao` datetime DEFAULT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  `observacao_rejeicao` text DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_cancelamento`),
  KEY `id_venda_original` (`id_venda_original`),
  KEY `id_usuario_vendedor` (`id_usuario_vendedor`),
  KEY `id_regional` (`id_regional`),
  KEY `id_supervisor_cancelamento` (`id_supervisor_cancelamento`),
  KEY `id_motivo_cancelamento` (`id_motivo_cancelamento`),
  CONSTRAINT `cancelamentos_ibfk_1` FOREIGN KEY (`id_venda_original`) REFERENCES `venda` (`id_venda`),
  CONSTRAINT `cancelamentos_ibfk_2` FOREIGN KEY (`id_usuario_vendedor`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `cancelamentos_ibfk_3` FOREIGN KEY (`id_regional`) REFERENCES `regional` (`id_regional`),
  CONSTRAINT `cancelamentos_ibfk_4` FOREIGN KEY (`id_supervisor_cancelamento`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `cancelamentos_ibfk_5` FOREIGN KEY (`id_motivo_cancelamento`) REFERENCES `motivos_cancelamento` (`id_motivo`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancelamentos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `cancelamentos` WRITE;
/*!40000 ALTER TABLE `cancelamentos` DISABLE KEYS */;
INSERT INTO `cancelamentos` VALUES
(1,94,4,1,2,'2026-03-09 10:47:34','2026-03-09',89.90,2,'demora no instalação ','aprovado',0,NULL,1,NULL,NULL),
(2,140,4,1,2,'2026-03-09 10:49:25','2026-03-09',89.00,2,'teste manual','revisado',0,NULL,1,'reprovado',NULL),
(3,93,4,1,2,'2026-03-09 10:50:07','2026-03-09',109.90,2,'demora no instalação ','revisado',0,NULL,1,'lançado errado',NULL),
(4,77,16,1,2,'2026-03-09 10:51:27','2026-03-09',89.90,6,'oferta cobre o plano atual','aprovado',0,NULL,1,NULL,NULL),
(5,79,16,1,2,'2026-03-09 10:53:55','2026-03-09',109.00,6,'oferta cobre o plano atual','revisado',0,NULL,1,'resolvido',NULL),
(6,75,4,1,2,'2026-03-09 10:54:46','2026-03-09',109.90,4,'apos contrataçao o mesmo se mudou ','revisado',0,NULL,1,'cliente desitiu, probelma resolvido',NULL),
(7,108,17,2,3,'2026-03-09 10:57:13','2026-03-09',109.90,7,'','revisado',0,NULL,1,'descurso do tempo',NULL),
(8,102,15,2,3,'2026-03-09 10:57:32','2026-03-09',89.90,4,'','aprovado',0,NULL,1,NULL,NULL),
(9,81,17,2,3,'2026-03-09 11:02:03','2026-03-09',90.90,3,'','aprovado',0,NULL,1,NULL,NULL),
(10,90,6,2,3,'2026-03-09 11:02:35','2026-03-09',89.90,9,'atendimento inificiente ','aprovado',0,NULL,1,NULL,NULL),
(11,91,6,2,3,'2026-03-09 12:13:18','2026-03-09',120.90,7,'','pendente',0,NULL,1,NULL,NULL),
(12,123,25,4,39,'2026-03-10 15:16:42','2026-03-10',520.00,7,'','aprovado',0,NULL,1,NULL,NULL),
(13,128,22,4,39,'2026-03-11 08:30:25','2026-03-11',109.90,6,'','revisado',0,NULL,1,'resolvido',NULL);
/*!40000 ALTER TABLE `cancelamentos` ENABLE KEYS */;
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
-- Table structure for table `funcionalidades`
--

DROP TABLE IF EXISTS `funcionalidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionalidades` (
  `id_funcionalidade` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `rota` varchar(100) DEFAULT NULL,
  `icone` varchar(50) DEFAULT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  `ordem` int(11) DEFAULT 0,
  PRIMARY KEY (`id_funcionalidade`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionalidades`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `funcionalidades` WRITE;
/*!40000 ALTER TABLE `funcionalidades` DISABLE KEYS */;
INSERT INTO `funcionalidades` VALUES
(1,'Dashboard Estratégico','Visão geral de indicadores','dashboard','📊',1,1),
(2,'Gestão de Usuários','CRUD de usuários do sistema','usuarios','👥',1,2),
(3,'Metas Regionais','Definição de metas por regional','metas','🎯',1,3),
(4,'Treinamentos','Gestão de treinamentos','treinamentos','📚',1,4),
(5,'Visão de Supervisor','Aprovações e acompanhamento','supervisor','🛡️',1,5),
(6,'Auditoria','Logs e auditoria do sistema','auditoria','📑',1,6),
(7,'Painel Suporte','Ferramentas de suporte técnico','suporte','🛠️',1,7),
(8,'Comissões','Cálculo de comissionamento','comissoes','💰',1,8);
/*!40000 ALTER TABLE `funcionalidades` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(7,'PEDRO HENRIQUE PEREIRA SILVA','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42'),
(14,'ANA PAULA PEREIRA ROCHA',NULL,3,2026,629.40,'PAGO','Comissão baseada em 6 vendas','2026-03-17 19:35:09'),
(15,'samanta ',NULL,3,2026,709.20,'PAGO','Comissão baseada em 8 vendas','2026-03-17 19:35:09'),
(16,'ANA PAULA PEREIRA ROCHA',NULL,3,2026,629.40,'PAGO','Comissão baseada em 6 vendas','2026-03-17 19:35:38'),
(17,'samanta ',NULL,3,2026,709.20,'PAGO','Comissão baseada em 8 vendas','2026-03-17 19:35:38');
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
) ENGINE=InnoDB AUTO_INCREMENT=1314 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(488,26,'BACKUP_AUTOMATICO','Backup automático: C:\\Users\\Asus\\Desktop\\plataformaMell\\backup_auto_plataforma_mell_2026-03-05_16-26.sql','2026-03-05 19:26:14'),
(489,20,'LOGOUT','Saiu do sistema','2026-03-05 19:57:44'),
(490,2,'LOGIN','Acesso realizado','2026-03-05 19:57:57'),
(491,1,'LOGIN','Acesso realizado','2026-03-05 20:01:21'),
(492,1,'LOGOUT','Saiu do sistema','2026-03-05 20:01:28'),
(493,2,'LOGIN','Acesso realizado','2026-03-05 20:01:45'),
(494,2,'LOGOUT','Saiu do sistema','2026-03-05 20:01:51'),
(495,2,'LOGIN','Acesso realizado','2026-03-05 20:42:46'),
(496,2,'LOGOUT','Saiu do sistema','2026-03-05 20:43:01'),
(497,4,'LOGIN','Acesso realizado','2026-03-05 20:43:07'),
(498,1,'LOGIN','Acesso realizado','2026-03-06 15:13:40'),
(499,1,'LOGOUT','Saiu do sistema','2026-03-06 15:29:25'),
(500,4,'LOGIN','Acesso realizado','2026-03-06 15:29:33'),
(501,4,'LOGOUT','Saiu do sistema','2026-03-06 15:32:49'),
(502,1,'LOGIN','Acesso realizado','2026-03-06 15:32:58'),
(503,1,'LOGOUT','Saiu do sistema','2026-03-06 15:36:24'),
(504,4,'LOGIN','Acesso realizado','2026-03-06 15:36:36'),
(505,1,'LOGIN','Acesso realizado','2026-03-06 17:03:09'),
(506,1,'LOGOUT','Saiu do sistema','2026-03-06 17:07:04'),
(507,4,'LOGIN','Acesso realizado','2026-03-06 17:07:14'),
(508,4,'VENDA','Downgrade: 83753 - R$ 89.0 (anterior: R$ 109.0)','2026-03-06 17:07:48'),
(509,4,'LOGOUT','Saiu do sistema','2026-03-06 17:08:02'),
(510,2,'LOGIN','Acesso realizado','2026-03-06 17:08:08'),
(511,2,'REPROVAÇÃO','Venda 132 reprovada','2026-03-06 17:08:17'),
(512,2,'LOGOUT','Saiu do sistema','2026-03-06 17:08:43'),
(513,6,'LOGIN','Acesso realizado','2026-03-06 17:08:53'),
(514,6,'VENDA','Venda Nova: 8047 - R$ 90.0','2026-03-06 17:09:13'),
(515,6,'LOGOUT','Saiu do sistema','2026-03-06 17:09:18'),
(516,1,'LOGIN','Acesso realizado','2026-03-06 17:18:36'),
(517,1,'LOGOUT','Saiu do sistema','2026-03-06 17:20:39'),
(518,20,'LOGIN','Acesso realizado','2026-03-06 17:23:29'),
(519,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-06_14-23.sql','2026-03-06 17:23:30'),
(520,20,'BACKUP_MANUAL','Backup gerado: backup_plataforma_mell_2026-03-06_14-23.sql','2026-03-06 17:23:40'),
(521,20,'LOGOUT','Saiu do sistema','2026-03-06 17:24:55'),
(522,4,'LOGIN','Acesso realizado','2026-03-06 17:25:28'),
(523,4,'LOGOUT','Saiu do sistema','2026-03-06 17:27:28'),
(524,1,'LOGIN','Acesso realizado','2026-03-06 17:27:45'),
(525,1,'LOGOUT','Saiu do sistema','2026-03-06 17:27:57'),
(526,2,'LOGIN','Acesso realizado','2026-03-06 17:28:02'),
(527,2,'LOGOUT','Saiu do sistema','2026-03-06 17:28:25'),
(528,3,'LOGIN','Acesso realizado','2026-03-06 17:28:32'),
(529,3,'LOGOUT','Saiu do sistema','2026-03-06 17:29:04'),
(530,39,'LOGIN','Acesso realizado','2026-03-06 17:29:26'),
(531,39,'LOGOUT','Saiu do sistema','2026-03-06 17:30:58'),
(532,1,'LOGIN','Acesso realizado','2026-03-06 17:31:16'),
(533,1,'LOGOUT','Saiu do sistema','2026-03-06 17:31:42'),
(534,26,'LOGIN','Acesso realizado','2026-03-06 17:31:54'),
(535,26,'VENDA','Telefonia Avulsa: 498948 - R$ 49.0','2026-03-06 17:33:41'),
(536,26,'VENDA','Telefonia Avulsa: 4989400 - R$ 49.0','2026-03-06 17:33:49'),
(537,26,'LOGOUT','Saiu do sistema','2026-03-06 17:34:26'),
(538,39,'LOGIN','Acesso realizado','2026-03-06 17:34:49'),
(539,39,'LOGOUT','Saiu do sistema','2026-03-06 17:35:35'),
(540,20,'LOGIN','Acesso realizado','2026-03-06 17:35:45'),
(541,20,'LOGOUT','Saiu do sistema','2026-03-06 17:40:49'),
(542,1,'LOGIN','Acesso realizado','2026-03-06 17:43:16'),
(543,1,'LOGOUT','Saiu do sistema','2026-03-06 17:43:30'),
(544,42,'LOGIN','Acesso realizado','2026-03-06 17:43:37'),
(545,42,'LOGOUT','Saiu do sistema','2026-03-06 17:43:41'),
(546,1,'LOGIN','Acesso realizado','2026-03-06 17:43:58'),
(547,1,'LOGOUT','Saiu do sistema','2026-03-06 17:44:14'),
(548,19,'LOGIN','Acesso realizado','2026-03-06 17:45:05'),
(549,19,'LOGOUT','Saiu do sistema','2026-03-06 17:55:21'),
(550,4,'LOGIN','Acesso realizado','2026-03-06 18:06:11'),
(551,4,'LOGOUT','Saiu do sistema','2026-03-06 18:06:18'),
(552,20,'LOGIN','Acesso realizado','2026-03-06 18:06:32'),
(553,20,'LOGOUT','Saiu do sistema','2026-03-06 18:10:51'),
(554,24,'LOGIN','Acesso realizado','2026-03-06 18:11:15'),
(555,24,'LOGOUT','Saiu do sistema','2026-03-06 18:11:39'),
(556,24,'LOGIN','Acesso realizado','2026-03-06 18:23:04'),
(557,24,'LOGOUT','Saiu do sistema','2026-03-06 18:23:51'),
(558,4,'LOGIN','Acesso realizado','2026-03-06 18:24:01'),
(559,4,'TREINAMENTO','Concluiu: teste apos alteraçoes ','2026-03-06 18:28:50'),
(560,4,'LOGOUT','Saiu do sistema','2026-03-06 18:28:54'),
(561,24,'LOGIN','Acesso realizado','2026-03-06 18:29:18'),
(562,24,'TREINAMENTO','Publicou: apos novas atualiaçao para Vendedor','2026-03-06 18:38:15'),
(563,6,'LOGIN','Acesso realizado','2026-03-06 18:38:42'),
(564,24,'LOGOUT','Saiu do sistema','2026-03-06 19:07:51'),
(565,1,'LOGIN','Acesso realizado','2026-03-06 19:08:00'),
(566,6,'VENDA','Downgrade: 7428 - R$ 79.0 (anterior: R$ 129.0)','2026-03-06 19:24:59'),
(567,1,'LOGOUT','Saiu do sistema','2026-03-06 19:35:04'),
(568,24,'LOGIN','Acesso realizado','2026-03-06 19:35:24'),
(569,24,'LOGOUT','Saiu do sistema','2026-03-06 19:40:17'),
(570,24,'LOGIN','Acesso realizado','2026-03-06 19:40:41'),
(571,1,'LOGIN','Acesso realizado','2026-03-06 19:57:46'),
(572,1,'LOGOUT','Saiu do sistema','2026-03-06 19:58:13'),
(573,20,'LOGIN','Acesso realizado','2026-03-06 19:58:24'),
(574,20,'PERMISSOES','Atualizou permissões do usuário PEDRO HENRIQUE PEREIRA SILVA (Vendedor)','2026-03-06 20:00:34'),
(575,6,'LOGIN','Acesso realizado','2026-03-06 20:00:57'),
(576,20,'LOGOUT','Saiu do sistema','2026-03-06 20:06:12'),
(577,1,'LOGIN','Acesso realizado','2026-03-06 20:06:28'),
(578,1,'LOGIN','Acesso realizado','2026-03-06 20:06:54'),
(579,1,'LOGOUT','Saiu do sistema','2026-03-06 20:07:15'),
(580,20,'LOGIN','Acesso realizado','2026-03-06 20:07:29'),
(581,20,'LOGOUT','Saiu do sistema','2026-03-06 20:09:15'),
(582,20,'LOGIN','Acesso realizado','2026-03-06 20:09:30'),
(583,20,'LOGIN','Acesso realizado','2026-03-07 18:14:08'),
(584,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-07_15-14.sql','2026-03-07 18:14:10'),
(585,1,'LOGIN','Acesso realizado','2026-03-07 18:18:12'),
(586,1,'LOGOUT','Saiu do sistema','2026-03-07 18:19:27'),
(587,4,'LOGIN','Acesso realizado','2026-03-07 18:19:46'),
(588,20,'PERMISSOES','Atualizou permissões do usuário ANA PAULA PEREIRA ROCHA (Vendedor)','2026-03-07 18:27:17'),
(589,4,'LOGOUT','Saiu do sistema','2026-03-07 18:27:34'),
(590,4,'LOGIN','Acesso realizado','2026-03-07 18:27:56'),
(591,20,'LOGOUT','Saiu do sistema','2026-03-07 18:29:34'),
(592,1,'LOGIN','Acesso realizado','2026-03-07 18:30:03'),
(593,4,'VENDA','Upgrade: 9765 - R$ 129.0 (anterior: R$ 90.0)','2026-03-07 18:33:18'),
(594,4,'VENDA','Telefonia Avulsa: 9765 - R$ 49.0','2026-03-07 18:34:23'),
(595,4,'LOGIN','Acesso realizado','2026-03-09 11:14:15'),
(596,4,'VENDA','Downgrade: 8027 - R$ 90.9 (anterior: R$ 129.0)','2026-03-09 11:14:38'),
(597,4,'LOGOUT','Saiu do sistema','2026-03-09 11:15:02'),
(598,1,'LOGIN','Acesso realizado','2026-03-09 11:15:07'),
(599,1,'LOGOUT','Saiu do sistema','2026-03-09 11:15:22'),
(600,19,'LOGIN','Acesso realizado','2026-03-09 11:15:34'),
(601,19,'LOGOUT','Saiu do sistema','2026-03-09 11:17:08'),
(602,24,'LOGIN','Acesso realizado','2026-03-09 11:17:25'),
(603,1,'LOGIN','Acesso realizado','2026-03-09 12:48:39'),
(604,2,'LOGIN','Acesso realizado','2026-03-09 13:24:34'),
(605,1,'LOGIN','Acesso realizado','2026-03-09 13:27:50'),
(606,1,'LOGOUT','Saiu do sistema','2026-03-09 13:29:41'),
(607,2,'LOGIN','Acesso realizado','2026-03-09 13:29:53'),
(608,2,'APROVAÇÃO','Venda 140 aprovada - R$ 89.0','2026-03-09 13:35:06'),
(609,2,'LOGOUT','Saiu do sistema','2026-03-09 13:56:47'),
(610,3,'LOGIN','Acesso realizado','2026-03-09 13:57:03'),
(611,3,'TREINAMENTO','Concluiu: teste01','2026-03-09 14:13:25'),
(612,3,'LOGOUT','Saiu do sistema','2026-03-09 14:14:17'),
(613,1,'LOGIN','Acesso realizado','2026-03-09 14:14:29'),
(614,2,'LOGIN','Acesso realizado','2026-03-09 14:16:11'),
(615,2,'LOGOUT','Saiu do sistema','2026-03-09 14:27:59'),
(616,19,'LOGIN','Acesso realizado','2026-03-09 14:28:05'),
(617,19,'TREINAMENTO','Concluiu: teste','2026-03-09 14:33:20'),
(618,1,'META','Metas salvas para Curvelo','2026-03-09 14:43:40'),
(619,19,'LOGOUT','Saiu do sistema','2026-03-09 14:54:01'),
(620,3,'LOGIN','Acesso realizado','2026-03-09 14:54:07'),
(621,1,'LOGOUT','Saiu do sistema','2026-03-09 15:13:38'),
(622,19,'LOGIN','Acesso realizado','2026-03-09 15:13:52'),
(623,3,'LOGOUT','Saiu do sistema','2026-03-09 15:21:22'),
(624,20,'LOGIN','Acesso realizado','2026-03-09 15:21:35'),
(625,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-09_12-21.sql','2026-03-09 15:21:36'),
(626,20,'LOGOUT','Saiu do sistema','2026-03-09 15:36:10'),
(627,4,'LOGIN','Acesso realizado','2026-03-09 15:36:27'),
(628,4,'LOGOUT','Saiu do sistema','2026-03-09 15:37:52'),
(629,6,'LOGIN','Acesso realizado','2026-03-09 15:38:04'),
(630,6,'LOGOUT','Saiu do sistema','2026-03-09 15:47:43'),
(631,39,'LOGIN','Acesso realizado','2026-03-09 15:48:02'),
(632,19,'LOGIN','Acesso realizado','2026-03-09 17:36:04'),
(633,19,'LOGIN','Acesso realizado','2026-03-09 17:37:33'),
(634,1,'LOGIN','Acesso realizado','2026-03-09 17:40:18'),
(635,1,'META','Metas salvas para Serra Geral','2026-03-09 17:40:30'),
(636,1,'META','Metas salvas para Serra Geral','2026-03-09 17:41:18'),
(637,1,'META','Metas salvas para Serra Geral','2026-03-09 17:41:21'),
(638,1,'LOGOUT','Saiu do sistema','2026-03-09 17:44:46'),
(639,2,'LOGIN','Acesso realizado','2026-03-09 17:44:52'),
(640,2,'APROVAÇÃO','Venda 146 aprovada - R$ 49.0','2026-03-09 17:44:55'),
(641,2,'APROVAÇÃO','Venda 145 aprovada - R$ 129.0','2026-03-09 17:44:59'),
(642,19,'LOGOUT','Saiu do sistema','2026-03-09 17:45:35'),
(643,4,'LOGIN','Acesso realizado','2026-03-09 17:45:45'),
(644,4,'VENDA','Venda Nova: 00387 - R$ 129.0','2026-03-09 17:46:02'),
(645,4,'VENDA','Venda Nova: 223387 - R$ 129.0','2026-03-09 17:46:12'),
(646,4,'VENDA','Venda Nova: 754836 - R$ 109.0','2026-03-09 17:46:23'),
(647,2,'APROVAÇÃO','Venda 148 aprovada - R$ 129.0','2026-03-09 17:46:37'),
(648,2,'APROVAÇÃO','Venda 149 aprovada - R$ 129.0','2026-03-09 17:46:39'),
(649,2,'APROVAÇÃO','Venda 150 aprovada - R$ 109.0','2026-03-09 17:46:40'),
(650,2,'APROVAÇÃO','Venda 147 aprovada - R$ 90.9','2026-03-09 17:46:45'),
(651,4,'LOGOUT','Saiu do sistema','2026-03-09 17:47:06'),
(652,1,'LOGIN','Acesso realizado','2026-03-09 17:47:12'),
(653,1,'LOGOUT','Saiu do sistema','2026-03-09 17:47:33'),
(654,5,'LOGIN','Acesso realizado','2026-03-09 17:47:38'),
(655,5,'VENDA','B2B: 38999 - R$ 250.0','2026-03-09 17:47:58'),
(656,5,'VENDA','Upgrade: 38999 - R$ 250.0 (anterior: R$ 190.0)','2026-03-09 17:48:12'),
(657,5,'VENDA','Venda Nova: 0843 - R$ 89.0','2026-03-09 17:48:33'),
(658,5,'VENDA','Venda Nova: 2965 - R$ 129.0','2026-03-09 17:48:56'),
(659,2,'LOGOUT','Saiu do sistema','2026-03-09 17:49:07'),
(660,3,'LOGIN','Acesso realizado','2026-03-09 17:49:23'),
(661,3,'APROVAÇÃO','Venda 151 aprovada - R$ 250.0','2026-03-09 17:49:26'),
(662,3,'APROVAÇÃO','Venda 152 aprovada - R$ 250.0','2026-03-09 17:49:28'),
(663,3,'APROVAÇÃO','Venda 154 aprovada - R$ 129.0','2026-03-09 17:49:31'),
(664,3,'APROVAÇÃO','Venda 153 aprovada - R$ 89.0','2026-03-09 17:49:33'),
(665,3,'APROVAÇÃO','Venda 144 aprovada - R$ 79.0','2026-03-09 17:49:35'),
(666,3,'APROVAÇÃO','Venda 109 aprovada - R$ 109.9','2026-03-09 17:49:39'),
(667,3,'APROVAÇÃO','Venda 141 aprovada - R$ 90.0','2026-03-09 17:49:41'),
(668,5,'LOGOUT','Saiu do sistema','2026-03-09 17:51:31'),
(669,19,'LOGIN','Acesso realizado','2026-03-09 17:51:42'),
(670,3,'LOGOUT','Saiu do sistema','2026-03-09 18:50:05'),
(671,1,'LOGIN','Acesso realizado','2026-03-09 18:50:11'),
(672,19,'LOGOUT','Saiu do sistema','2026-03-09 20:04:43'),
(673,19,'LOGIN','Acesso realizado','2026-03-09 20:04:55'),
(674,1,'META','Metas salvas para Moc','2026-03-09 20:22:48'),
(675,1,'META','Metas salvas para Moc','2026-03-09 20:22:53'),
(676,1,'META','Metas salvas para Moc','2026-03-09 20:23:43'),
(677,19,'LOGOUT','Saiu do sistema','2026-03-09 20:35:03'),
(678,1,'LOGIN','Acesso realizado','2026-03-09 20:35:09'),
(679,1,'LOGOUT','Saiu do sistema','2026-03-09 20:35:35'),
(680,4,'LOGIN','Acesso realizado','2026-03-09 20:35:44'),
(681,4,'LOGOUT','Saiu do sistema','2026-03-09 20:36:49'),
(682,6,'LOGIN','Acesso realizado','2026-03-09 20:37:01'),
(683,1,'LOGIN','Acesso realizado','2026-03-10 13:14:36'),
(684,1,'USUÁRIO','Cadastrou: Paulo cesar','2026-03-10 13:42:22'),
(685,1,'LOGOUT','Saiu do sistema','2026-03-10 13:44:14'),
(686,2,'LOGIN','Acesso realizado','2026-03-10 13:44:30'),
(687,2,'LOGOUT','Saiu do sistema','2026-03-10 13:44:48'),
(688,4,'LOGIN','Acesso realizado','2026-03-10 13:44:53'),
(689,4,'VENDA','Upgrade: 79475 - R$ 129.0 (anterior: R$ 89.0)','2026-03-10 13:45:12'),
(690,4,'VENDA','Upgrade: 00086 - R$ 129.0 (anterior: R$ 89.0)','2026-03-10 13:45:23'),
(691,4,'VENDA','Venda Nova: 34357 - R$ 89.0','2026-03-10 13:45:36'),
(692,4,'LOGOUT','Saiu do sistema','2026-03-10 13:45:39'),
(693,16,'LOGIN','Acesso realizado','2026-03-10 13:46:00'),
(694,16,'VENDA','Upgrade: 89279 - R$ 129.0 (anterior: R$ 79.0)','2026-03-10 13:46:32'),
(695,16,'VENDA','Venda Nova: 169364 - R$ 79.0','2026-03-10 13:46:57'),
(696,16,'VENDA','Telefonia Avulsa: 49740 - R$ 49.0','2026-03-10 13:47:22'),
(697,16,'LOGOUT','Saiu do sistema','2026-03-10 13:47:32'),
(698,2,'LOGIN','Acesso realizado','2026-03-10 13:47:47'),
(699,2,'APROVAÇÃO','Venda 157 aprovada - R$ 89.0','2026-03-10 13:47:52'),
(700,2,'APROVAÇÃO','Venda 159 aprovada - R$ 79.0','2026-03-10 13:47:54'),
(701,2,'APROVAÇÃO','Venda 155 aprovada - R$ 129.0','2026-03-10 13:47:55'),
(702,2,'APROVAÇÃO','Venda 160 aprovada - R$ 49.0','2026-03-10 13:47:59'),
(703,2,'APROVAÇÃO','Venda 156 aprovada - R$ 129.0','2026-03-10 13:48:07'),
(704,2,'APROVAÇÃO','Venda 158 aprovada - R$ 129.0','2026-03-10 13:48:09'),
(705,2,'LOGOUT','Saiu do sistema','2026-03-10 13:48:26'),
(706,1,'LOGIN','Acesso realizado','2026-03-10 13:51:02'),
(707,1,'LOGOUT','Saiu do sistema','2026-03-10 13:52:40'),
(708,20,'LOGIN','Acesso realizado','2026-03-10 13:52:55'),
(709,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-10_10-52.sql','2026-03-10 13:52:56'),
(710,1,'LOGIN','Acesso realizado','2026-03-10 14:26:33'),
(711,1,'META','Metas salvas para Moc','2026-03-10 14:27:18'),
(712,1,'META','Metas salvas para Moc','2026-03-10 14:27:45'),
(713,1,'META','Metas salvas para Moc','2026-03-10 14:27:57'),
(714,1,'META','Metas salvas para Curvelo','2026-03-10 14:28:16'),
(715,1,'META','Metas salvas para Curvelo','2026-03-10 14:28:20'),
(716,1,'META','Metas salvas para Serra Geral','2026-03-10 14:28:38'),
(717,1,'META','Metas salvas para Salinas','2026-03-10 14:28:59'),
(718,42,'LOGIN','Acesso realizado','2026-03-10 14:45:14'),
(719,42,'VENDA','Upgrade: 898 - R$ 89.0 (anterior: R$ 79.0)','2026-03-10 14:45:38'),
(720,1,'CANCELAMENTO','Aprovou cancelamento ID: 9','2026-03-10 14:55:45'),
(721,2,'LOGIN','Acesso realizado','2026-03-10 15:23:47'),
(722,1,'CANCELAMENTO','Aprovou cancelamento ID: 4','2026-03-10 15:27:28'),
(723,1,'LOGIN','Acesso realizado','2026-03-10 17:07:16'),
(724,1,'LOGIN','Acesso realizado','2026-03-10 17:08:14'),
(725,1,'CANCELAMENTO','Rejeitou ID: 5 - Motivo: resolvido...','2026-03-10 17:11:32'),
(726,1,'CANCELAMENTO','Revisou ID: 5 - resolvido','2026-03-10 17:52:11'),
(727,1,'CANCELAMENTO','REVISADO ID: 1 - resolvido','2026-03-10 18:06:04'),
(728,1,'LOGIN','Acesso realizado','2026-03-10 18:06:18'),
(729,1,'CANCELAMENTO','APROVADO ID: 1','2026-03-10 18:06:43'),
(730,1,'CANCELAMENTO','REVISADO ID: 2 - nao autorizado','2026-03-10 18:07:04'),
(731,1,'CANCELAMENTO','Revisou ID: 2 - resolvido','2026-03-10 18:09:35'),
(732,1,'CANCELAMENTO','Revisou ID: 2 - resolvido','2026-03-10 18:09:41'),
(733,1,'CANCELAMENTO','Revisou ID: 2 - resolvido','2026-03-10 18:10:03'),
(734,1,'CANCELAMENTO','Revisou ID: 2 - resolvido','2026-03-10 18:14:31'),
(735,1,'CANCELAMENTO','Revisou ID: 2 - teste','2026-03-10 18:14:54'),
(736,39,'LOGIN','Acesso realizado','2026-03-10 18:16:30'),
(737,1,'CANCELAMENTO','Revisou ID: 12 - errado ','2026-03-10 18:17:05'),
(738,1,'CANCELAMENTO','Revisou ID: 12','2026-03-10 18:18:41'),
(739,1,'LOGIN','Acesso realizado','2026-03-10 18:19:39'),
(740,1,'CANCELAMENTO','Revisou ID: 12','2026-03-10 18:19:51'),
(741,1,'CANCELAMENTO','Revisou ID: 12','2026-03-10 18:24:10'),
(742,1,'CANCELAMENTO','Aprovou ID: 12','2026-03-10 18:24:25'),
(743,1,'CANCELAMENTO','Revisou ID: 2','2026-03-10 18:27:35'),
(744,1,'CANCELAMENTO','Revisou ID: 3','2026-03-10 18:27:59'),
(745,1,'CANCELAMENTO','Revisou ID: 6','2026-03-10 18:28:38'),
(746,39,'LOGOUT','Saiu do sistema','2026-03-10 18:31:32'),
(747,2,'LOGIN','Acesso realizado','2026-03-10 18:31:38'),
(748,2,'LOGOUT','Saiu do sistema','2026-03-10 18:42:54'),
(749,3,'LOGIN','Acesso realizado','2026-03-10 18:43:00'),
(750,1,'LOGIN','Acesso realizado','2026-03-10 19:09:07'),
(751,1,'LOGIN','Acesso realizado','2026-03-10 19:12:15'),
(752,1,'META','Metas salvas para Curvelo','2026-03-10 19:13:59'),
(753,1,'META','Metas salvas para Moc','2026-03-10 19:14:25'),
(754,1,'META','Metas salvas para Curvelo','2026-03-10 19:14:30'),
(755,1,'META','Metas salvas para Curvelo','2026-03-10 19:14:36'),
(756,1,'META','Metas salvas para Curvelo','2026-03-10 19:15:04'),
(757,1,'META','Metas salvas para Curvelo','2026-03-10 19:15:39'),
(758,1,'LOGOUT','Saiu do sistema','2026-03-10 20:30:15'),
(759,2,'LOGIN','Acesso realizado','2026-03-10 20:39:13'),
(760,1,'LOGIN','Acesso realizado','2026-03-11 11:11:45'),
(761,1,'LOGOUT','Saiu do sistema','2026-03-11 11:20:39'),
(762,4,'LOGIN','Acesso realizado','2026-03-11 11:20:47'),
(763,4,'LOGOUT','Saiu do sistema','2026-03-11 11:22:32'),
(764,2,'LOGIN','Acesso realizado','2026-03-11 11:22:43'),
(765,2,'LOGOUT','Saiu do sistema','2026-03-11 11:22:48'),
(766,3,'LOGIN','Acesso realizado','2026-03-11 11:23:01'),
(767,3,'LOGOUT','Saiu do sistema','2026-03-11 11:23:05'),
(768,39,'LOGIN','Acesso realizado','2026-03-11 11:23:36'),
(769,39,'REPROVAÇÃO','Venda 142 reprovada','2026-03-11 11:23:44'),
(770,39,'LOGOUT','Saiu do sistema','2026-03-11 11:30:26'),
(771,1,'LOGIN','Acesso realizado','2026-03-11 11:30:37'),
(772,1,'CANCELAMENTO','Revisou ID: 13','2026-03-11 11:30:50'),
(773,1,'LOGOUT','Saiu do sistema','2026-03-11 11:30:53'),
(774,39,'LOGIN','Acesso realizado','2026-03-11 11:31:15'),
(775,1,'LOGIN','Acesso realizado','2026-03-11 12:24:04'),
(776,1,'META','Metas salvas para Moc','2026-03-11 12:32:37'),
(777,1,'LOGOUT','Saiu do sistema','2026-03-11 12:46:13'),
(778,4,'LOGIN','Acesso realizado','2026-03-11 12:46:24'),
(779,4,'LOGOUT','Saiu do sistema','2026-03-11 12:53:08'),
(780,39,'LOGIN','Acesso realizado','2026-03-11 12:54:02'),
(781,39,'LOGOUT','Saiu do sistema','2026-03-11 12:54:58'),
(782,19,'LOGIN','Acesso realizado','2026-03-11 12:55:12'),
(783,19,'LOGOUT','Saiu do sistema','2026-03-11 13:11:25'),
(784,6,'LOGIN','Acesso realizado','2026-03-11 13:11:38'),
(785,6,'VENDA','Venda Nova: 15336 - R$ 89.0','2026-03-11 13:12:47'),
(786,6,'LOGOUT','Saiu do sistema','2026-03-11 13:12:54'),
(787,3,'LOGIN','Acesso realizado','2026-03-11 13:13:16'),
(788,3,'LOGOUT','Saiu do sistema','2026-03-11 13:14:51'),
(789,6,'LOGIN','Acesso realizado','2026-03-11 13:15:06'),
(790,6,'LOGOUT','Saiu do sistema','2026-03-11 13:16:40'),
(791,1,'LOGIN','Acesso realizado','2026-03-11 13:16:52'),
(792,1,'LOGOUT','Saiu do sistema','2026-03-11 13:26:57'),
(793,2,'LOGIN','Acesso realizado','2026-03-11 13:27:10'),
(794,2,'LOGOUT','Saiu do sistema','2026-03-11 13:31:55'),
(795,16,'LOGIN','Acesso realizado','2026-03-11 13:32:03'),
(796,16,'VENDA','Telefonia Avulsa: 8498 - R$ 49.0','2026-03-11 13:34:34'),
(797,16,'LOGOUT','Saiu do sistema','2026-03-11 13:46:02'),
(798,19,'LOGIN','Acesso realizado','2026-03-11 13:46:26'),
(799,19,'LOGOUT','Saiu do sistema','2026-03-11 13:58:52'),
(800,4,'LOGIN','Acesso realizado','2026-03-11 13:58:58'),
(801,4,'LOGOUT','Saiu do sistema','2026-03-11 13:59:17'),
(802,19,'LOGIN','Acesso realizado','2026-03-11 13:59:42'),
(803,19,'LOGOUT','Saiu do sistema','2026-03-11 14:05:54'),
(804,2,'LOGIN','Acesso realizado','2026-03-11 14:06:02'),
(805,2,'LOGOUT','Saiu do sistema','2026-03-11 14:06:43'),
(806,3,'LOGIN','Acesso realizado','2026-03-11 14:06:50'),
(807,3,'LOGOUT','Saiu do sistema','2026-03-11 14:06:53'),
(808,39,'LOGIN','Acesso realizado','2026-03-11 14:07:19'),
(809,39,'APROVAÇÃO','Venda 143 aprovada - R$ 49.0','2026-03-11 14:07:38'),
(810,39,'REPROVAÇÃO','Venda 120 reprovada','2026-03-11 14:07:42'),
(811,39,'LOGOUT','Saiu do sistema','2026-03-11 14:08:36'),
(812,1,'LOGIN','Acesso realizado','2026-03-11 14:08:42'),
(813,1,'LOGOUT','Saiu do sistema','2026-03-11 14:10:32'),
(814,20,'LOGIN','Acesso realizado','2026-03-11 14:10:58'),
(815,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-11_11-10.sql','2026-03-11 14:11:01'),
(816,20,'LOGOUT','Saiu do sistema','2026-03-11 14:12:17'),
(817,2,'LOGIN','Acesso realizado','2026-03-11 14:12:32'),
(818,2,'APROVAÇÃO','Venda 163 aprovada - R$ 49.0','2026-03-11 14:13:36'),
(819,2,'LOGOUT','Saiu do sistema','2026-03-11 14:20:51'),
(820,24,'LOGIN','Acesso realizado','2026-03-11 14:21:11'),
(821,1,'LOGIN','Acesso realizado','2026-03-11 17:45:51'),
(822,1,'LOGIN','Entrou no sistema','2026-03-12 12:25:22'),
(823,19,'LOGIN','Acesso realizado','2026-03-13 12:03:52'),
(824,19,'LOGOUT','Saiu do sistema','2026-03-13 12:08:33'),
(825,1,'LOGIN','Acesso realizado','2026-03-13 12:21:18'),
(826,19,'LOGIN','Acesso realizado','2026-03-13 16:47:38'),
(827,19,'LOGOUT','Saiu do sistema','2026-03-13 16:53:12'),
(828,1,'LOGIN','Acesso realizado','2026-03-13 16:53:18'),
(829,1,'META','Metas salvas para Curvelo','2026-03-13 16:54:06'),
(830,1,'LOGOUT','Saiu do sistema','2026-03-13 16:56:26'),
(831,19,'LOGIN','Acesso realizado','2026-03-13 16:56:39'),
(832,19,'LOGIN','Acesso realizado','2026-03-13 17:05:10'),
(833,19,'LOGIN','Acesso realizado','2026-03-13 17:46:06'),
(834,19,'LOGIN','Acesso realizado','2026-03-13 18:29:55'),
(835,19,'LOGOUT','Saiu do sistema','2026-03-13 19:06:43'),
(836,6,'LOGIN','Acesso realizado','2026-03-13 19:06:52'),
(837,6,'VENDA','Venda Nova: 259564 - R$ 120.0','2026-03-13 19:07:05'),
(838,6,'LOGOUT','Saiu do sistema','2026-03-13 19:07:09'),
(839,3,'LOGIN','Acesso realizado','2026-03-13 19:07:27'),
(840,3,'APROVAÇÃO','Venda 164 aprovada - R$ 120.0','2026-03-13 19:07:35'),
(841,3,'LOGOUT','Saiu do sistema','2026-03-13 19:07:40'),
(842,19,'LOGIN','Acesso realizado','2026-03-13 19:07:53'),
(843,19,'LOGIN','Acesso realizado','2026-03-13 19:16:35'),
(844,19,'LOGOUT','Saiu do sistema','2026-03-13 19:17:55'),
(845,1,'LOGIN','Acesso realizado','2026-03-13 19:18:01'),
(846,1,'META','Metas salvas para Curvelo','2026-03-13 19:18:09'),
(847,1,'META','Metas salvas para Curvelo','2026-03-13 19:18:09'),
(848,1,'LOGOUT','Saiu do sistema','2026-03-13 19:18:18'),
(849,19,'LOGIN','Acesso realizado','2026-03-13 19:18:35'),
(850,19,'LOGIN','Acesso realizado','2026-03-13 19:36:37'),
(851,19,'LOGIN','Acesso realizado','2026-03-16 12:02:41'),
(852,19,'LOGIN','Acesso realizado','2026-03-16 12:04:26'),
(853,19,'LOGIN','Acesso realizado','2026-03-16 13:49:00'),
(854,19,'LOGOUT','Saiu do sistema','2026-03-16 13:56:33'),
(855,6,'LOGIN','Acesso realizado','2026-03-16 13:56:41'),
(856,6,'VENDA','Venda Nova: 262416 - R$ 79.9','2026-03-16 13:57:05'),
(857,6,'LOGOUT','Saiu do sistema','2026-03-16 13:57:09'),
(858,3,'LOGIN','Acesso realizado','2026-03-16 13:57:51'),
(859,3,'APROVAÇÃO','Venda 165 aprovada - R$ 79.9','2026-03-16 13:57:54'),
(860,3,'LOGOUT','Saiu do sistema','2026-03-16 13:58:05'),
(861,19,'LOGIN','Acesso realizado','2026-03-16 13:58:30'),
(862,6,'LOGIN','Acesso realizado','2026-03-16 14:01:54'),
(863,6,'VENDA','Venda Nova: 262407 - R$ 79.9','2026-03-16 14:02:23'),
(864,6,'LOGOUT','Saiu do sistema','2026-03-16 14:02:45'),
(865,3,'LOGIN','Acesso realizado','2026-03-16 14:03:02'),
(866,3,'APROVAÇÃO','Venda 166 aprovada - R$ 79.9','2026-03-16 14:03:06'),
(867,3,'REPROVAÇÃO','Venda 162 reprovada','2026-03-16 14:03:20'),
(868,3,'LOGOUT','Saiu do sistema','2026-03-16 14:03:23'),
(869,19,'LOGIN','Acesso realizado','2026-03-16 14:03:37'),
(870,19,'LOGOUT','Saiu do sistema','2026-03-16 14:25:49'),
(871,6,'LOGIN','Acesso realizado','2026-03-16 14:25:54'),
(872,19,'LOGIN','Acesso realizado','2026-03-16 14:32:06'),
(873,19,'LOGIN','Acesso realizado','2026-03-16 14:35:49'),
(874,19,'LOGIN','Acesso realizado','2026-03-16 15:36:30'),
(875,19,'LOGOUT','Saiu do sistema','2026-03-16 15:43:29'),
(876,16,'LOGIN','Acesso realizado','2026-03-16 15:43:46'),
(877,16,'VENDA','Venda Nova: 262423 - R$ 59.9','2026-03-16 15:44:38'),
(878,16,'LOGOUT','Saiu do sistema','2026-03-16 15:44:44'),
(879,2,'LOGIN','Acesso realizado','2026-03-16 15:44:50'),
(880,2,'APROVAÇÃO','Venda 167 aprovada - R$ 59.9','2026-03-16 15:44:53'),
(881,2,'LOGOUT','Saiu do sistema','2026-03-16 15:45:08'),
(882,19,'LOGIN','Acesso realizado','2026-03-16 15:45:22'),
(883,16,'LOGIN','Acesso realizado','2026-03-16 17:47:54'),
(884,16,'VENDA','Venda Nova: 249876 - R$ 99.9','2026-03-16 17:48:31'),
(885,16,'LOGOUT','Saiu do sistema','2026-03-16 17:48:41'),
(886,2,'LOGIN','Acesso realizado','2026-03-16 17:48:46'),
(887,2,'APROVAÇÃO','Venda 168 aprovada - R$ 99.9','2026-03-16 17:48:48'),
(888,2,'LOGOUT','Saiu do sistema','2026-03-16 17:49:52'),
(889,1,'LOGIN','Acesso realizado','2026-03-16 17:49:58'),
(890,1,'META','Metas salvas para Moc','2026-03-16 17:50:09'),
(891,1,'LOGOUT','Saiu do sistema','2026-03-16 17:50:23'),
(892,1,'LOGIN','Acesso realizado','2026-03-16 17:54:43'),
(893,1,'META','Metas salvas para Serra Geral','2026-03-16 17:58:17'),
(894,19,'LOGIN','Acesso realizado','2026-03-16 18:07:00'),
(895,19,'LOGOUT','Saiu do sistema','2026-03-16 18:59:55'),
(896,1,'LOGIN','Acesso realizado','2026-03-16 19:00:24'),
(897,19,'LOGOUT','Saiu do sistema','2026-03-16 19:11:13'),
(898,4,'LOGIN','Acesso realizado','2026-03-16 19:11:28'),
(899,4,'LOGOUT','Saiu do sistema','2026-03-16 19:14:12'),
(900,19,'LOGIN','Acesso realizado','2026-03-16 19:14:27'),
(901,19,'LOGIN','Acesso realizado','2026-03-17 13:48:02'),
(902,19,'LOGIN','Acesso realizado','2026-03-17 14:42:55'),
(903,19,'LOGOUT','Saiu do sistema','2026-03-17 14:47:12'),
(904,1,'LOGIN','Acesso realizado','2026-03-17 14:47:18'),
(905,1,'META','Metas salvas para Moc','2026-03-17 14:47:44'),
(906,1,'LOGOUT','Saiu do sistema','2026-03-17 14:48:39'),
(907,19,'LOGIN','Acesso realizado','2026-03-17 14:48:48'),
(908,19,'LOGOUT','Saiu do sistema','2026-03-17 15:11:00'),
(909,6,'LOGIN','Acesso realizado','2026-03-17 15:11:19'),
(910,6,'VENDA','Venda Nova: 260512 - R$ 69.9','2026-03-17 15:12:27'),
(911,6,'LOGOUT','Saiu do sistema','2026-03-17 15:12:30'),
(912,3,'LOGIN','Acesso realizado','2026-03-17 15:12:50'),
(913,3,'APROVAÇÃO','Venda 169 aprovada - R$ 69.9','2026-03-17 15:12:52'),
(914,3,'LOGOUT','Saiu do sistema','2026-03-17 15:12:59'),
(915,19,'LOGIN','Acesso realizado','2026-03-17 15:13:21'),
(916,19,'LOGIN','Acesso realizado','2026-03-17 17:02:55'),
(917,19,'LOGIN','Acesso realizado','2026-03-17 17:59:07'),
(918,19,'LOGIN','Acesso realizado','2026-03-17 18:19:54'),
(919,19,'LOGIN','Acesso realizado','2026-03-17 18:30:32'),
(920,19,'LOGOUT','Saiu do sistema','2026-03-17 18:49:07'),
(921,19,'LOGIN','Acesso realizado','2026-03-17 18:49:17'),
(922,19,'LOGOUT','Saiu do sistema','2026-03-17 18:55:52'),
(923,19,'LOGIN','Acesso realizado','2026-03-17 18:56:16'),
(924,19,'LOGIN','Acesso realizado','2026-03-17 19:00:51'),
(925,19,'LOGIN','Acesso realizado','2026-03-17 19:06:05'),
(926,19,'LOGIN','Acesso realizado','2026-03-17 19:30:45'),
(927,19,'LOGOUT','Saiu do sistema','2026-03-17 19:32:19'),
(928,4,'LOGIN','Acesso realizado','2026-03-17 19:32:25'),
(929,4,'VENDA','Venda Nova: 220735 - R$ 99.9','2026-03-17 19:32:50'),
(930,4,'LOGOUT','Saiu do sistema','2026-03-17 19:32:53'),
(931,2,'LOGIN','Acesso realizado','2026-03-17 19:32:58'),
(932,2,'APROVAÇÃO','Venda 170 aprovada - R$ 99.9','2026-03-17 19:33:00'),
(933,2,'LOGOUT','Saiu do sistema','2026-03-17 19:33:02'),
(934,19,'LOGIN','Acesso realizado','2026-03-17 19:33:12'),
(935,19,'LOGIN','Acesso realizado','2026-03-17 20:29:43'),
(936,19,'LOGIN','Acesso realizado','2026-03-18 11:57:56'),
(937,1,'LOGIN','Acesso realizado','2026-03-18 12:07:39'),
(938,1,'LOGOUT','Saiu do sistema','2026-03-18 12:56:01'),
(939,1,'LOGIN','Acesso realizado','2026-03-18 12:57:10'),
(940,1,'LOGIN','Acesso realizado','2026-03-18 13:00:25'),
(941,1,'LOGOUT','Saiu do sistema','2026-03-18 13:06:00'),
(942,2,'LOGIN','Acesso realizado','2026-03-18 13:06:13'),
(943,2,'LOGOUT','Saiu do sistema','2026-03-18 13:06:46'),
(944,1,'LOGIN','Acesso realizado','2026-03-18 13:09:48'),
(945,1,'LOGIN','Acesso realizado','2026-03-18 13:23:08'),
(946,41,'LOGIN','Acesso realizado','2026-03-18 13:25:46'),
(947,41,'REPROVAÇÃO','Venda 161 reprovada','2026-03-18 13:25:51'),
(948,41,'APROVAÇÃO','Venda 136 aprovada - R$ 129.0','2026-03-18 13:25:55'),
(949,41,'APROVAÇÃO','Venda 137 aprovada - R$ 129.0','2026-03-18 13:26:00'),
(950,41,'LOGOUT','Saiu do sistema','2026-03-18 13:26:06'),
(951,42,'LOGIN','Acesso realizado','2026-03-18 13:26:14'),
(952,42,'VENDA','Venda Nova: 260853 - R$ 79.9','2026-03-18 13:27:06'),
(953,42,'VENDA','Venda Nova: 260749 - R$ 79.9','2026-03-18 13:28:16'),
(954,42,'LOGOUT','Saiu do sistema','2026-03-18 13:28:20'),
(955,41,'LOGIN','Acesso realizado','2026-03-18 13:28:35'),
(956,41,'APROVAÇÃO','Venda 172 aprovada - R$ 79.9','2026-03-18 13:28:38'),
(957,41,'APROVAÇÃO','Venda 171 aprovada - R$ 79.9','2026-03-18 13:28:41'),
(958,1,'CANCELAMENTO','Revisou ID: 5','2026-03-18 13:33:12'),
(959,1,'CANCELAMENTO','Revisou ID: 7','2026-03-18 13:33:28'),
(960,1,'LOGIN','Acesso realizado','2026-03-18 14:32:45'),
(961,1,'CANCELAMENTO','Aprovou ID: 8','2026-03-18 14:55:24'),
(962,1,'LOGOUT','Saiu do sistema','2026-03-18 15:10:20'),
(963,20,'LOGIN','Acesso realizado','2026-03-18 15:10:31'),
(964,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-18_12-10.sql','2026-03-18 15:10:33'),
(965,20,'PERMISSOES','Atualizou permissões do usuário ADMINISTRADOR (Admin)','2026-03-18 15:11:13'),
(966,20,'LOGOUT','Saiu do sistema','2026-03-18 15:11:18'),
(967,1,'LOGIN','Acesso realizado','2026-03-18 15:11:27'),
(968,1,'LOGOUT','Saiu do sistema','2026-03-18 15:11:38'),
(969,20,'LOGIN','Acesso realizado','2026-03-18 15:11:59'),
(970,20,'LOGIN','Acesso realizado','2026-03-18 16:41:51'),
(971,20,'LOGIN','Acesso realizado','2026-03-18 17:01:56'),
(972,20,'LOGIN','Acesso realizado','2026-03-18 17:24:10'),
(973,20,'TREINAMENTO','Concluiu: teste de notificaçao','2026-03-18 17:29:11'),
(974,20,'LOGOUT','Saiu do sistema','2026-03-18 17:33:19'),
(975,20,'LOGIN','Acesso realizado','2026-03-18 17:33:33'),
(976,20,'LOGIN','Acesso realizado','2026-03-18 17:36:54'),
(977,20,'LOGIN','Acesso realizado','2026-03-18 17:40:57'),
(978,20,'LOGIN','Acesso realizado','2026-03-18 17:45:32'),
(979,20,'LOGIN','Acesso realizado','2026-03-18 17:48:04'),
(980,20,'LOGOUT','Saiu do sistema','2026-03-18 17:51:19'),
(981,16,'LOGIN','Acesso realizado','2026-03-18 17:51:40'),
(982,16,'VENDA','Venda Nova: 260870 - R$ 79.9','2026-03-18 17:52:31'),
(983,16,'LOGOUT','Saiu do sistema','2026-03-18 17:52:35'),
(984,2,'LOGIN','Acesso realizado','2026-03-18 17:52:43'),
(985,2,'APROVAÇÃO','Venda 173 aprovada - R$ 79.9','2026-03-18 17:52:48'),
(986,2,'LOGOUT','Saiu do sistema','2026-03-18 17:52:56'),
(987,19,'LOGIN','Acesso realizado','2026-03-18 17:53:09'),
(988,19,'LOGOUT','Saiu do sistema','2026-03-18 17:54:27'),
(989,20,'LOGIN','Acesso realizado','2026-03-18 17:54:43'),
(990,20,'LOGIN','Acesso realizado','2026-03-18 19:28:26'),
(991,1,'LOGIN','Acesso realizado','2026-03-18 19:33:21'),
(992,1,'LOGOUT','Saiu do sistema','2026-03-18 19:55:46'),
(993,2,'LOGIN','Acesso realizado','2026-03-18 19:55:56'),
(994,2,'LOGOUT','Saiu do sistema','2026-03-18 19:57:21'),
(995,1,'LOGIN','Acesso realizado','2026-03-18 20:11:07'),
(996,1,'META','Metas salvas para Curvelo','2026-03-18 20:17:59'),
(997,1,'META','Metas salvas para Salinas','2026-03-18 20:18:10'),
(998,1,'META','Metas salvas para Serra Geral','2026-03-18 20:18:35'),
(999,1,'META','Metas salvas para Geral','2026-03-18 20:19:13'),
(1000,1,'LOGIN','Acesso realizado','2026-03-18 20:38:29'),
(1001,1,'LOGOUT','Saiu do sistema','2026-03-18 20:38:41'),
(1002,1,'LOGIN','Acesso realizado','2026-03-18 20:38:58'),
(1003,1,'LOGOUT','Saiu do sistema','2026-03-18 20:40:10'),
(1004,24,'LOGIN','Acesso realizado','2026-03-18 20:40:34'),
(1005,24,'TREINAMENTO','Publicou: treinamento teste para Todos','2026-03-18 20:42:13'),
(1006,24,'LOGOUT','Saiu do sistema','2026-03-18 20:42:25'),
(1007,4,'LOGIN','Acesso realizado','2026-03-18 20:42:34'),
(1008,4,'LOGOUT','Saiu do sistema','2026-03-18 20:43:20'),
(1009,24,'LOGIN','Acesso realizado','2026-03-18 20:44:56'),
(1010,19,'LOGIN','Acesso realizado','2026-03-19 11:32:19'),
(1011,1,'LOGIN','Acesso realizado','2026-03-19 12:10:38'),
(1012,1,'LOGOUT','Saiu do sistema','2026-03-19 12:14:30'),
(1013,4,'LOGIN','Acesso realizado','2026-03-19 12:14:37'),
(1014,4,'VENDA','Venda Nova: 260870 - R$ 79.9','2026-03-19 12:25:14'),
(1015,4,'LOGOUT','Saiu do sistema','2026-03-19 12:28:12'),
(1016,2,'LOGIN','Acesso realizado','2026-03-19 12:28:23'),
(1017,2,'APROVAÇÃO','Venda 174 aprovada - R$ 79.9','2026-03-19 12:32:02'),
(1018,2,'LOGOUT','Saiu do sistema','2026-03-19 12:47:31'),
(1019,20,'LOGIN','Acesso realizado','2026-03-19 12:47:43'),
(1020,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-19_09-47.sql','2026-03-19 12:47:45'),
(1021,20,'USUÁRIO','Desativou: joaquina','2026-03-19 13:13:07'),
(1022,20,'USUÁRIO','Ativou: joaquina','2026-03-19 13:13:11'),
(1023,20,'LOGOUT','Saiu do sistema','2026-03-19 13:16:31'),
(1024,24,'LOGIN','Acesso realizado','2026-03-19 13:16:51'),
(1025,1,'LOGIN','Acesso realizado','2026-03-19 14:34:43'),
(1026,1,'LOGIN','Acesso realizado','2026-03-19 14:35:55'),
(1027,1,'USUÁRIO','Cadastrou: lucas','2026-03-19 14:49:51'),
(1028,44,'LOGIN','Acesso realizado','2026-03-19 14:51:35'),
(1029,1,'LOGIN','Acesso realizado','2026-03-19 15:13:03'),
(1030,1,'LOGIN','Acesso realizado','2026-03-19 15:13:56'),
(1031,44,'LOGIN','Acesso realizado','2026-03-19 15:15:46'),
(1032,1,'LOGIN','Acesso realizado','2026-03-19 15:22:24'),
(1033,44,'VENDA_TELEVENDAS','Venda: 262836 - R$ 79.90','2026-03-19 15:35:49'),
(1034,44,'LOGOUT','Saiu do sistema','2026-03-19 15:43:32'),
(1035,45,'LOGIN','Acesso realizado','2026-03-19 15:43:48'),
(1036,45,'LOGOUT','Saiu do sistema','2026-03-19 15:43:59'),
(1037,1,'LOGIN','Acesso realizado','2026-03-19 15:44:04'),
(1038,1,'LOGOUT','Saiu do sistema','2026-03-19 15:45:00'),
(1039,45,'LOGIN','Acesso realizado','2026-03-19 15:45:05'),
(1040,45,'LOGIN','Acesso realizado','2026-03-19 15:50:33'),
(1041,45,'LOGIN','Acesso realizado','2026-03-19 15:52:04'),
(1042,45,'LOGOUT','Saiu do sistema','2026-03-19 15:53:10'),
(1043,44,'LOGIN','Acesso realizado','2026-03-19 15:53:21'),
(1044,44,'LOGOUT','Saiu do sistema','2026-03-19 15:55:39'),
(1045,45,'LOGIN','Acesso realizado','2026-03-19 15:55:51'),
(1046,1,'LOGIN','Acesso realizado','2026-03-19 15:59:59'),
(1047,45,'LOGIN','Acesso realizado','2026-03-19 16:04:03'),
(1048,45,'LOGOUT','Saiu do sistema','2026-03-19 16:04:07'),
(1049,44,'LOGIN','Acesso realizado','2026-03-19 16:04:19'),
(1050,44,'VENDA_TELEVENDAS','Venda: 262777 - R$ 79.90','2026-03-19 16:04:41'),
(1051,44,'LOGOUT','Saiu do sistema','2026-03-19 16:04:43'),
(1052,45,'LOGIN','Acesso realizado','2026-03-19 16:04:51'),
(1053,1,'LOGOUT','Saiu do sistema','2026-03-19 17:32:41'),
(1054,44,'LOGIN','Acesso realizado','2026-03-19 17:32:56'),
(1055,44,'VENDA_TELEVENDAS','Venda: 262789 - R$ 79.90 (aguardando aprovação)','2026-03-19 17:33:25'),
(1056,45,'LOGIN','Acesso realizado','2026-03-19 17:33:45'),
(1057,1,'LOGIN','Acesso realizado','2026-03-19 17:42:46'),
(1058,1,'LOGOUT','Saiu do sistema','2026-03-19 17:42:55'),
(1059,44,'LOGIN','Acesso realizado','2026-03-19 17:43:16'),
(1060,44,'VENDA_TELEVENDAS','Venda: 262733 - R$ 79.90 (aguardando aprovação)','2026-03-19 17:51:51'),
(1061,44,'VENDA_TELEVENDAS','Venda: 262639 - R$ 100.00 (aguardando aprovação)','2026-03-19 17:52:32'),
(1062,45,'LOGIN','Acesso realizado','2026-03-19 17:52:53'),
(1063,44,'LOGOUT','Saiu do sistema','2026-03-19 17:54:43'),
(1064,19,'LOGIN','Acesso realizado','2026-03-19 17:54:59'),
(1065,19,'LOGOUT','Saiu do sistema','2026-03-19 17:57:07'),
(1066,44,'LOGIN','Acesso realizado','2026-03-19 17:57:20'),
(1067,44,'LOGOUT','Saiu do sistema','2026-03-19 18:11:02'),
(1068,19,'LOGIN','Acesso realizado','2026-03-19 18:11:12'),
(1069,19,'LOGOUT','Saiu do sistema','2026-03-19 18:34:47'),
(1070,44,'LOGIN','Acesso realizado','2026-03-19 18:34:59'),
(1071,44,'LOGOUT','Saiu do sistema','2026-03-19 18:35:13'),
(1072,6,'LOGIN','Acesso realizado','2026-03-19 18:35:25'),
(1073,6,'LOGOUT','Saiu do sistema','2026-03-19 18:40:48'),
(1074,1,'LOGIN','Acesso realizado','2026-03-19 18:50:41'),
(1075,1,'LOGIN','Acesso realizado','2026-03-19 19:09:03'),
(1076,1,'LOGOUT','Saiu do sistema','2026-03-19 19:12:38'),
(1077,2,'LOGIN','Acesso realizado','2026-03-19 19:12:43'),
(1078,2,'LOGOUT','Saiu do sistema','2026-03-19 19:12:51'),
(1079,19,'LOGIN','Acesso realizado','2026-03-19 19:13:05'),
(1080,19,'LOGOUT','Saiu do sistema','2026-03-19 19:19:07'),
(1081,1,'LOGIN','Acesso realizado','2026-03-19 19:19:12'),
(1082,1,'USUÁRIO','Cadastrou: maria','2026-03-19 19:19:48'),
(1083,1,'LOGOUT','Saiu do sistema','2026-03-19 19:19:55'),
(1084,46,'LOGIN','Acesso realizado','2026-03-19 19:20:04'),
(1085,46,'META_TELEVENDAS','Meta Março/2026: 50 vendas, R$ 2,000.00','2026-03-19 19:27:17'),
(1086,46,'LOGIN','Acesso realizado','2026-03-19 19:36:22'),
(1087,46,'LOGIN','Acesso realizado','2026-03-19 19:48:20'),
(1088,45,'APROVACAO_TV','Venda 178 aprovada - R$ 79.90','2026-03-19 19:50:06'),
(1089,45,'LOGOUT','Saiu do sistema','2026-03-19 19:51:10'),
(1090,19,'LOGIN','Acesso realizado','2026-03-19 19:51:15'),
(1091,46,'LOGOUT','Saiu do sistema','2026-03-19 19:52:44'),
(1092,4,'LOGIN','Acesso realizado','2026-03-19 19:52:57'),
(1093,4,'LOGOUT','Saiu do sistema','2026-03-19 20:01:11'),
(1094,20,'LOGIN','Acesso realizado','2026-03-19 20:01:24'),
(1095,1,'LOGIN','Acesso realizado','2026-03-20 11:32:13'),
(1096,1,'LOGOUT','Saiu do sistema','2026-03-20 11:44:36'),
(1097,1,'LOGIN','Acesso realizado','2026-03-20 12:10:31'),
(1098,1,'LOGOUT','Saiu do sistema','2026-03-20 12:10:56'),
(1099,1,'LOGIN','Acesso realizado','2026-03-20 12:13:24'),
(1100,1,'LOGIN','Acesso realizado','2026-03-20 12:17:50'),
(1101,1,'LOGOUT','Saiu do sistema','2026-03-20 12:21:14'),
(1102,1,'LOGIN','Acesso realizado','2026-03-20 12:28:30'),
(1103,1,'LOGOUT','Saiu do sistema','2026-03-20 12:32:06'),
(1104,1,'LOGIN','Acesso realizado','2026-03-20 12:33:00'),
(1105,1,'LOGOUT','Saiu do sistema','2026-03-20 12:33:27'),
(1106,1,'LOGIN','Acesso realizado','2026-03-20 12:53:50'),
(1107,1,'LOGOUT','Saiu do sistema','2026-03-20 13:32:38'),
(1108,4,'LOGIN','Acesso realizado','2026-03-20 13:32:48'),
(1109,4,'VENDA','B2B: 262918 - R$ 79.9','2026-03-20 13:33:21'),
(1110,4,'LOGOUT','Saiu do sistema','2026-03-20 13:33:24'),
(1111,2,'LOGIN','Acesso realizado','2026-03-20 13:33:31'),
(1112,2,'APROVAÇÃO','Venda 180 aprovada - R$ 79.9','2026-03-20 13:33:34'),
(1113,2,'LOGOUT','Saiu do sistema','2026-03-20 13:33:36'),
(1114,19,'LOGIN','Acesso realizado','2026-03-20 13:34:23'),
(1115,19,'LOGOUT','Saiu do sistema','2026-03-20 13:42:13'),
(1116,6,'LOGIN','Acesso realizado','2026-03-20 13:43:59'),
(1117,6,'LOGIN','Acesso realizado','2026-03-20 14:25:59'),
(1118,6,'VENDA','Venda Nova: 262914 - R$ 79.9','2026-03-20 14:30:10'),
(1119,6,'VENDA','Downgrade: 26291 - R$ 79.9 (anterior: R$ 120.9)','2026-03-20 14:32:49'),
(1120,6,'LOGOUT','Saiu do sistema','2026-03-20 14:35:46'),
(1121,3,'LOGIN','Acesso realizado','2026-03-20 14:36:19'),
(1122,3,'LOGOUT','Saiu do sistema','2026-03-20 14:38:39'),
(1123,6,'LOGIN','Acesso realizado','2026-03-20 14:39:07'),
(1124,6,'LOGOUT','Saiu do sistema','2026-03-20 14:42:57'),
(1125,3,'LOGIN','Acesso realizado','2026-03-20 14:43:12'),
(1126,3,'APROVAÇÃO','Venda 181 aprovada - R$ 79.9','2026-03-20 14:49:35'),
(1127,3,'META','Metas salvas para Curvelo','2026-03-20 15:01:21'),
(1128,3,'LOGOUT','Saiu do sistema','2026-03-20 15:02:41'),
(1129,1,'LOGIN','Acesso realizado','2026-03-20 15:03:21'),
(1130,1,'LOGIN','Acesso realizado','2026-03-23 20:43:06'),
(1131,1,'META','Metas salvas para Salinas','2026-03-23 20:43:28'),
(1132,1,'META','Metas salvas para Moc','2026-03-23 20:43:46'),
(1133,1,'META','Metas salvas para Moc','2026-03-23 20:44:01'),
(1134,1,'META','Metas salvas para Salinas','2026-03-23 20:44:18'),
(1135,1,'META','Metas salvas para Moc','2026-03-23 20:44:23'),
(1136,1,'LOGIN','Entrou no sistema','2026-03-24 11:31:46'),
(1137,1,'LOGIN','Acesso realizado','2026-03-24 13:04:47'),
(1138,1,'LOGIN','Acesso realizado','2026-03-24 13:13:12'),
(1139,1,'LOGOUT','Saiu do sistema','2026-03-24 13:19:40'),
(1140,6,'LOGIN','Acesso realizado','2026-03-24 13:19:53'),
(1141,6,'VENDA','Downgrade: 262880 - R$ 89.9 (anterior: R$ 129.9)','2026-03-24 13:21:12'),
(1142,6,'VENDA','Upgrade: 262918 - R$ 129.9 (anterior: R$ 89.9)','2026-03-24 13:21:55'),
(1143,6,'LOGOUT','Saiu do sistema','2026-03-24 13:22:10'),
(1144,3,'LOGIN','Acesso realizado','2026-03-24 13:22:27'),
(1145,20,'LOGIN','Acesso realizado','2026-03-24 13:42:24'),
(1146,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-24_10-42.sql','2026-03-24 13:42:27'),
(1147,20,'LOGOUT','Saiu do sistema','2026-03-24 13:44:25'),
(1148,3,'LOGIN','Acesso realizado','2026-03-24 13:44:47'),
(1149,3,'META','Metas salvas para Moc','2026-03-24 13:57:25'),
(1150,3,'LOGOUT','Saiu do sistema','2026-03-24 14:00:30'),
(1151,1,'LOGIN','Acesso realizado','2026-03-24 14:00:40'),
(1152,1,'META','Metas salvas para Curvelo','2026-03-24 14:00:55'),
(1153,1,'LOGOUT','Saiu do sistema','2026-03-24 14:00:57'),
(1154,3,'LOGIN','Acesso realizado','2026-03-24 14:01:15'),
(1155,3,'LOGOUT','Saiu do sistema','2026-03-24 14:01:47'),
(1156,1,'LOGIN','Acesso realizado','2026-03-24 14:02:11'),
(1157,1,'META','Metas salvas para Curvelo','2026-03-24 14:02:29'),
(1158,1,'LOGOUT','Saiu do sistema','2026-03-24 14:02:35'),
(1159,1,'LOGIN','Acesso realizado','2026-03-24 17:15:30'),
(1160,1,'LOGIN','Acesso realizado','2026-03-24 18:17:50'),
(1161,1,'LOGIN','Acesso realizado','2026-03-25 13:57:24'),
(1162,1,'LOGOUT','Saiu do sistema','2026-03-25 14:06:43'),
(1163,19,'LOGIN','Acesso realizado','2026-03-25 14:06:54'),
(1164,19,'LOGIN','Acesso realizado','2026-03-25 14:36:31'),
(1165,19,'LOGIN','Acesso realizado','2026-03-25 15:24:34'),
(1166,19,'LOGOUT','Saiu do sistema','2026-03-25 15:37:04'),
(1167,2,'LOGIN','Acesso realizado','2026-03-25 15:37:14'),
(1168,2,'LOGOUT','Saiu do sistema','2026-03-25 15:37:32'),
(1169,1,'LOGIN','Acesso realizado','2026-03-25 15:37:40'),
(1170,1,'LOGOUT','Saiu do sistema','2026-03-25 15:38:16'),
(1171,19,'LOGIN','Acesso realizado','2026-03-25 15:39:28'),
(1172,19,'LOGIN','Acesso realizado','2026-03-25 17:09:38'),
(1173,19,'LOGIN','Acesso realizado','2026-03-25 17:47:06'),
(1174,19,'LOGIN','Acesso realizado','2026-03-25 18:42:36'),
(1175,19,'LOGIN','Acesso realizado','2026-03-25 18:46:26'),
(1176,19,'LOGOUT','Saiu do sistema','2026-03-25 18:51:37'),
(1177,6,'LOGIN','Acesso realizado','2026-03-25 18:51:45'),
(1178,6,'VENDA','Venda Nova: 263463 - R$ 79.9','2026-03-25 18:52:14'),
(1179,6,'LOGOUT','Saiu do sistema','2026-03-25 18:52:20'),
(1180,3,'LOGIN','Acesso realizado','2026-03-25 18:52:33'),
(1181,3,'APROVAÇÃO','Venda 185 aprovada - Venda Nova - R$ 79.9','2026-03-25 18:52:48'),
(1182,3,'LOGOUT','Saiu do sistema','2026-03-25 18:52:54'),
(1183,19,'LOGIN','Acesso realizado','2026-03-25 18:53:05'),
(1184,19,'LOGOUT','Saiu do sistema','2026-03-25 18:54:29'),
(1185,6,'LOGIN','Acesso realizado','2026-03-25 18:54:34'),
(1186,6,'VENDA','Venda Nova: 263347 - R$ 69.9','2026-03-25 18:55:02'),
(1187,6,'LOGOUT','Saiu do sistema','2026-03-25 18:55:04'),
(1188,3,'LOGIN','Acesso realizado','2026-03-25 18:55:21'),
(1189,3,'APROVAÇÃO','Venda 186 aprovada - Venda Nova - R$ 69.9','2026-03-25 18:55:30'),
(1190,3,'LOGOUT','Saiu do sistema','2026-03-25 18:55:35'),
(1191,19,'LOGIN','Acesso realizado','2026-03-25 18:55:48'),
(1192,1,'LOGIN','Acesso realizado','2026-03-25 20:17:59'),
(1193,1,'LOGIN','Acesso realizado','2026-03-25 20:45:02'),
(1194,1,'LOGIN','Acesso realizado','2026-03-25 20:50:38'),
(1195,1,'LOGIN','Acesso realizado','2026-03-26 12:03:59'),
(1196,1,'LOGOUT','Saiu do sistema','2026-03-26 12:04:06'),
(1197,1,'LOGIN','Acesso realizado','2026-03-26 12:41:08'),
(1198,1,'LOGOUT','Saiu do sistema','2026-03-26 12:44:03'),
(1199,1,'LOGIN','Acesso realizado','2026-03-26 13:15:01'),
(1200,1,'LOGOUT','Saiu do sistema','2026-03-26 13:15:04'),
(1201,1,'LOGIN','Acesso realizado','2026-03-26 13:41:27'),
(1202,1,'LOGOUT','Saiu do sistema','2026-03-26 13:41:38'),
(1203,6,'LOGIN','Acesso realizado','2026-03-26 14:46:37'),
(1204,6,'LOGOUT','Saiu do sistema','2026-03-26 14:48:16'),
(1205,1,'LOGIN','Acesso realizado','2026-03-26 14:52:17'),
(1206,1,'LOGIN','Acesso realizado','2026-03-26 14:53:45'),
(1207,1,'LOGOUT','Saiu do sistema','2026-03-26 14:57:22'),
(1208,20,'LOGIN','Acesso realizado','2026-03-26 15:12:01'),
(1209,26,'BACKUP_AUTOMATICO','Backup automático: backup_plataforma_mell_2026-03-26_12-12.sql','2026-03-26 15:12:05'),
(1210,20,'NOTIFICACAO_ENVIADA','Título: teste de caminho  | Para: Todos','2026-03-26 15:21:50'),
(1211,20,'LOGOUT','Saiu do sistema','2026-03-26 15:23:04'),
(1212,19,'LOGIN','Acesso realizado','2026-03-26 15:23:18'),
(1213,19,'LOGOUT','Saiu do sistema','2026-03-26 15:27:39'),
(1214,20,'LOGIN','Acesso realizado','2026-03-26 15:28:04'),
(1215,20,'LOGOUT','Saiu do sistema','2026-03-26 15:31:15'),
(1216,1,'LOGIN','Acesso realizado','2026-03-26 15:31:26'),
(1217,1,'LOGIN','Acesso realizado','2026-03-26 15:37:40'),
(1218,1,'LOGOUT','Saiu do sistema','2026-03-26 15:43:45'),
(1219,24,'LOGIN','Acesso realizado','2026-03-26 15:44:11'),
(1220,24,'LOGIN','Acesso realizado','2026-03-26 17:24:31'),
(1221,24,'LOGIN','Acesso realizado','2026-03-26 17:50:59'),
(1222,24,'LOGIN','Acesso realizado','2026-03-26 17:53:01'),
(1223,24,'LOGIN','Acesso realizado','2026-03-26 17:56:10'),
(1224,24,'LOGIN','Acesso realizado','2026-03-26 18:03:16'),
(1225,24,'TREINAMENTO','Publicou: teste de compliance para Admin','2026-03-26 18:07:32'),
(1226,24,'LOGOUT','Saiu do sistema','2026-03-26 18:09:46'),
(1227,1,'LOGIN','Acesso realizado','2026-03-26 18:10:02'),
(1228,1,'LOGOUT','Saiu do sistema','2026-03-26 18:10:19'),
(1229,1,'LOGIN','Acesso realizado','2026-03-26 18:10:32'),
(1230,1,'TREINAMENTO','Publicou: teste para Admin','2026-03-26 18:10:47'),
(1231,1,'TREINAMENTO','Publicou: fdffg para Admin','2026-03-26 18:11:50'),
(1232,1,'TREINAMENTO','Publicou: eretr para Vendedor','2026-03-26 18:12:03'),
(1233,1,'LOGOUT','Saiu do sistema','2026-03-26 18:12:07'),
(1234,6,'LOGIN','Acesso realizado','2026-03-26 18:12:21'),
(1235,6,'TREINAMENTO','Concluiu: eretr','2026-03-26 18:12:38'),
(1236,6,'LOGOUT','Saiu do sistema','2026-03-26 18:12:54'),
(1237,1,'LOGIN','Acesso realizado','2026-03-26 18:13:01'),
(1238,1,'TREINAMENTO','Publicou: teste novo para Vendedor','2026-03-26 18:17:59'),
(1239,1,'LOGOUT','Saiu do sistema','2026-03-26 18:18:04'),
(1240,6,'LOGIN','Acesso realizado','2026-03-26 18:18:27'),
(1241,6,'TREINAMENTO','Concluiu: teste novo','2026-03-26 18:19:34'),
(1242,6,'LOGOUT','Saiu do sistema','2026-03-26 18:19:40'),
(1243,24,'LOGIN','Acesso realizado','2026-03-26 18:20:09'),
(1244,24,'LOGOUT','Saiu do sistema','2026-03-26 18:23:07'),
(1245,4,'LOGIN','Acesso realizado','2026-03-26 18:23:27'),
(1246,4,'TREINAMENTO','Concluiu: desempenho','2026-03-26 18:25:05'),
(1247,4,'TREINAMENTO','Concluiu: analise','2026-03-26 18:25:08'),
(1248,4,'TREINAMENTO','Concluiu: apos novas atualiaçao','2026-03-26 18:25:21'),
(1249,4,'TREINAMENTO','Concluiu: teste novo','2026-03-26 18:25:41'),
(1250,24,'LOGIN','Acesso realizado','2026-03-26 19:12:47'),
(1251,24,'LOGOUT','Saiu do sistema','2026-03-26 19:20:49'),
(1252,4,'LOGIN','Acesso realizado','2026-03-26 19:21:01'),
(1253,4,'LOGOUT','Saiu do sistema','2026-03-26 19:21:33'),
(1254,1,'LOGIN','Acesso realizado','2026-03-26 19:21:40'),
(1255,1,'TREINAMENTO','Publicou: teste para Todos','2026-03-26 19:22:36'),
(1256,1,'TREINAMENTO','Publicou: teste de titulo para Todos','2026-03-26 19:28:41'),
(1257,4,'TREINAMENTO','Concluiu: teste de titulo','2026-03-26 19:29:26'),
(1258,4,'LOGIN','Acesso realizado','2026-03-26 19:35:25'),
(1259,4,'LOGIN','Acesso realizado','2026-03-26 19:43:44'),
(1260,1,'TREINAMENTO','Publicou: teste apos correção de espaço para Todos','2026-03-26 19:47:23'),
(1261,1,'TREINAMENTO','Publicou: teste de correçao espaçamento para Todos','2026-03-26 19:51:24'),
(1262,1,'TREINAMENTO','Publicou: indentaçao para Vendedor','2026-03-26 20:10:05'),
(1263,1,'TREINAMENTO','Publicou: testet para Todos','2026-03-26 20:11:17'),
(1264,4,'TREINAMENTO','Concluiu: treinamento teste','2026-03-26 20:17:31'),
(1265,19,'LOGIN','Acesso realizado','2026-03-27 14:02:15'),
(1266,19,'LOGOUT','Saiu do sistema','2026-03-27 14:21:44'),
(1267,1,'LOGIN','Acesso realizado','2026-03-27 15:35:28'),
(1268,1,'LOGIN','Acesso realizado','2026-03-27 15:36:59'),
(1269,1,'LOGOUT','Saiu do sistema','2026-03-27 15:37:05'),
(1270,1,'LOGIN','Acesso realizado','2026-03-27 16:57:47'),
(1271,1,'LOGOUT','Saiu do sistema','2026-03-27 16:58:58'),
(1272,1,'LOGIN','Acesso realizado','2026-03-27 17:04:58'),
(1273,1,'LOGOUT','Saiu do sistema','2026-03-27 17:07:35'),
(1274,6,'LOGIN','Acesso realizado','2026-03-27 17:07:59'),
(1275,6,'LOGOUT','Saiu do sistema','2026-03-27 17:41:53'),
(1276,24,'LOGIN','Acesso realizado','2026-03-27 17:42:31'),
(1277,24,'LOGOUT','Saiu do sistema','2026-03-27 17:45:29'),
(1278,6,'LOGIN','Acesso realizado','2026-03-27 17:45:42'),
(1279,6,'LOGOUT','Saiu do sistema','2026-03-27 17:45:51'),
(1280,4,'LOGIN','Acesso realizado','2026-03-27 17:46:02'),
(1281,4,'LOGOUT','Saiu do sistema','2026-03-27 17:46:13'),
(1282,24,'LOGIN','Acesso realizado','2026-03-27 17:46:37'),
(1283,24,'LOGOUT','Saiu do sistema','2026-03-27 17:47:09'),
(1284,6,'LOGIN','Acesso realizado','2026-03-27 17:47:26'),
(1285,6,'TREINAMENTO','Concluiu: apos novas atualiaçao','2026-03-27 17:49:18'),
(1286,6,'TREINAMENTO','Concluiu: analise','2026-03-27 17:49:24'),
(1287,6,'TREINAMENTO','Concluiu: teste apos alteraçoes','2026-03-27 17:49:29'),
(1288,6,'LOGOUT','Saiu do sistema','2026-03-27 17:57:36'),
(1289,24,'LOGIN','Acesso realizado','2026-03-27 17:57:57'),
(1290,24,'LOGOUT','Saiu do sistema','2026-03-27 17:59:05'),
(1291,6,'LOGIN','Acesso realizado','2026-03-27 17:59:22'),
(1292,6,'LOGOUT','Saiu do sistema','2026-03-27 18:03:18'),
(1293,24,'LOGIN','Acesso realizado','2026-03-27 18:03:46'),
(1294,24,'LOGOUT','Saiu do sistema','2026-03-27 18:04:19'),
(1295,6,'LOGIN','Acesso realizado','2026-03-27 18:04:25'),
(1296,6,'LOGOUT','Saiu do sistema','2026-03-27 19:34:42'),
(1297,24,'LOGIN','Acesso realizado','2026-03-27 19:35:02'),
(1298,24,'LOGOUT','Saiu do sistema','2026-03-27 19:35:40'),
(1299,6,'LOGIN','Acesso realizado','2026-03-27 19:35:59'),
(1300,6,'LOGOUT','Saiu do sistema','2026-03-27 19:36:10'),
(1301,24,'LOGIN','Acesso realizado','2026-03-27 19:36:39'),
(1302,24,'TREINAMENTO','Publicou: teste para Todos','2026-03-27 19:38:22'),
(1303,24,'LOGOUT','Saiu do sistema','2026-03-27 19:40:14'),
(1304,6,'LOGIN','Acesso realizado','2026-03-27 19:40:24'),
(1305,6,'LOGOUT','Saiu do sistema','2026-03-27 19:49:29'),
(1306,24,'LOGIN','Acesso realizado','2026-03-27 19:49:52'),
(1307,24,'TREINAMENTO','Publicou: intrutor para Todos','2026-03-27 19:50:47'),
(1308,24,'LOGOUT','Saiu do sistema','2026-03-27 19:51:04'),
(1309,6,'LOGIN','Acesso realizado','2026-03-27 19:51:23'),
(1310,6,'TREINAMENTO','Concluiu: intrutor','2026-03-27 19:53:36'),
(1311,6,'TREINAMENTO','Concluiu: teste','2026-03-27 19:53:55'),
(1312,6,'TREINAMENTO','Concluiu: testet','2026-03-27 19:54:05'),
(1313,6,'TREINAMENTO','Concluiu: treinamento teste','2026-03-27 20:01:32');
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(15,1,'2026-03-01',4,6),
(16,5,'2026-03-01',300,1232),
(29,2,'2026-03-01',5,5),
(30,4,'2026-03-01',25,90),
(42,3,'2026-03-01',10,5);
/*!40000 ALTER TABLE `metas_regionais` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `metas_televendas`
--

DROP TABLE IF EXISTS `metas_televendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `metas_televendas` (
  `id_meta` int(11) NOT NULL AUTO_INCREMENT,
  `mes_referencia` date NOT NULL,
  `meta_vendas_qtd` int(11) DEFAULT 0,
  `meta_migracao_qtd` int(11) DEFAULT 0,
  `meta_faturamento` decimal(10,2) DEFAULT 0.00,
  `data_criacao` timestamp NULL DEFAULT current_timestamp(),
  `data_atualizacao` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_meta`),
  UNIQUE KEY `unique_mes` (`mes_referencia`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metas_televendas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `metas_televendas` WRITE;
/*!40000 ALTER TABLE `metas_televendas` DISABLE KEYS */;
INSERT INTO `metas_televendas` VALUES
(1,'2026-03-01',50,10,2000.00,'2026-03-19 13:57:39','2026-03-19 19:27:17');
/*!40000 ALTER TABLE `metas_televendas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `motivos_cancelamento`
--

DROP TABLE IF EXISTS `motivos_cancelamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `motivos_cancelamento` (
  `id_motivo` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(255) NOT NULL,
  `categoria` enum('financeiro','insatisfacao','tecnico','outros') DEFAULT 'outros',
  `ativo` tinyint(4) DEFAULT 1,
  PRIMARY KEY (`id_motivo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivos_cancelamento`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `motivos_cancelamento` WRITE;
/*!40000 ALTER TABLE `motivos_cancelamento` DISABLE KEYS */;
INSERT INTO `motivos_cancelamento` VALUES
(1,'Inadimplência','financeiro',1),
(2,'Cliente insatisfeito','insatisfacao',1),
(3,'Problemas técnicos','tecnico',1),
(4,'Mudou de cidade','outros',1),
(5,'Valor muito alto','financeiro',1),
(6,'Concorrência','insatisfacao',1),
(7,'Cancelamento a pedido','outros',1),
(8,'Sem necessidade do serviço','outros',1),
(9,'Problemas com atendimento','insatisfacao',1),
(10,'Questões contratuais','financeiro',1);
/*!40000 ALTER TABLE `motivos_cancelamento` ENABLE KEYS */;
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
  `id_usuario_destino` int(11) DEFAULT NULL COMMENT 'ID do usuário destino (para notificações individuais)',
  `data_envio` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_notificacoes_usuario_destino` (`id_usuario_destino`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `notificacoes` WRITE;
/*!40000 ALTER TABLE `notificacoes` DISABLE KEYS */;
INSERT INTO `notificacoes` VALUES
(1,'Atualização ','na data do dia \'x\' havera atualização  as \'y\'','Todos',NULL,'2026-02-24 17:51:56'),
(2,'implelementaçao ','🚨🚨impoimportante 🚨🚨\nimplementação sistemica nos proximos dias ','Supervisores',NULL,'2026-02-25 15:20:46'),
(3,'🚨teste de notificação 🚨','corpo da notificaçao ','Todos',NULL,'2026-02-26 17:11:49'),
(4,'novo teste','teste apos adiçao de funçao de backup  ','Todos',NULL,'2026-02-26 20:28:26'),
(5,'🆕 Novo Treinamento: desempenho ','Um novo conteúdo de Sistema foi liberado. Confira na sua biblioteca!','Vendedor',NULL,'2026-03-02 19:01:20'),
(6,'Novo Treinamento Disponível','Um novo conteúdo de Vendas foi publicado.','Vendedor',NULL,'2026-03-02 19:11:32'),
(7,'teste ','teste  notificaçao apos atualizar ','Todos',NULL,'2026-03-02 19:19:37'),
(8,'teste ','teste ','Todos',NULL,'2026-03-02 19:25:08'),
(9,'Teste Manual','Verificando o sino agora','Todos',NULL,'2026-03-02 19:39:56'),
(10,'teste ','teste oqnsk','Todos',NULL,'2026-03-02 19:42:55'),
(11,'teste ','tetse ','Todos',NULL,'2026-03-02 19:46:35'),
(12,'teste ','teste ','Todos',NULL,'2026-03-02 19:49:56'),
(13,'🆕 Novo Treinamento: teste final ','Um novo conteúdo de Vendas foi liberado para você na biblioteca!','Todos',NULL,'2026-03-02 19:58:18'),
(14,'🆕 Novo Treinamento: ultimo ','Um novo conteúdo de Vendas foi liberado. Confira na sua biblioteca!','Todos',NULL,'2026-03-02 20:00:45'),
(15,'🆕 Novo Treinamento: teste ','Um novo conteúdo de Sistema foi liberado. Confira na sua biblioteca!','Admins',NULL,'2026-03-02 20:04:04'),
(16,'Ação Corretiva: ultimo ','Prazo de 7 dias. Obs: teste','Todos',NULL,'2026-03-03 17:40:34'),
(17,'🚀 Novo Conteúdo','Um novo treinamento de Vendas foi publicado: teste ','admin',NULL,'2026-03-03 19:37:04'),
(18,'teste','teste','Todos',NULL,'2026-03-03 19:38:06'),
(19,'um nvo test ','teste ','todos',NULL,'2026-03-03 19:45:44'),
(20,'teste de notificaçao ','teste de notificaçao ','todos',NULL,'2026-03-03 19:50:41'),
(21,'teste de notificaçao ','notificaçao ','todos',NULL,'2026-03-03 20:10:17'),
(22,'teste ','jose maria joao ','todos',NULL,'2026-03-03 20:10:42'),
(23,'teste ','teste ','todos',NULL,'2026-03-03 20:15:28'),
(24,'teste ','teste odudmd,','todos',NULL,'2026-03-03 20:21:08'),
(25,'🚀 Novo Conteúdo','Um novo treinamento de Vendas foi publicado: teste de notificaçao ','admin',NULL,'2026-03-03 20:22:33'),
(26,'Teste de Sistema','Se você está lendo isso, o banco está ok!','todos',NULL,'2026-03-03 20:27:16'),
(27,'Sistema Online','As notificações foram configuradas com sucesso!','todos',NULL,'2026-03-03 20:27:31'),
(28,'TESTE URGENTE','Se aparecer, o sistema está OK','todos',NULL,'2026-03-03 20:33:19'),
(29,'teste ','teste ','todos',NULL,'2026-03-03 20:34:07'),
(30,'Teste de Conexão','Se você vê isso, o problema é o filtro de cargo.','todos',NULL,'2026-03-03 20:34:31'),
(31,'teste ','teste ','todos',NULL,'2026-03-03 20:42:26'),
(32,'teste ','yesgsm','todos',NULL,'2026-03-03 20:48:21'),
(33,'teste ','teste ','todos',NULL,'2026-03-03 20:50:33'),
(34,'teste ','teste','todos',NULL,'2026-03-04 18:17:26'),
(35,'📚 Novo Treinamento: apos novas atualiaçao','Um novo treinamento \'apos novas atualiaçao\' foi publicado e está disponível para você!','vendedores',NULL,'2026-03-06 18:38:15'),
(36,'📚 Novo Treinamento: treinamento teste','Um novo treinamento \'treinamento teste\' foi publicado e está disponível para você!','todos',NULL,'2026-03-18 20:42:13'),
(37,'teste de caminho ','teste de caminho (26/03/2026)','todos',NULL,'2026-03-26 15:21:50'),
(38,'📚 Novo Treinamento: teste de compliance','Um novo treinamento \'teste de compliance\' foi publicado e está disponível para você!','admins',NULL,'2026-03-26 18:07:32'),
(39,'📚 Novo Treinamento: teste','Um novo treinamento \'teste\' foi publicado e está disponível para você!','admins',NULL,'2026-03-26 18:10:47'),
(40,'📚 Novo Treinamento: fdffg','Um novo treinamento \'fdffg\' foi publicado e está disponível para você!','admins',NULL,'2026-03-26 18:11:50'),
(41,'📚 Novo Treinamento: eretr','Um novo treinamento \'eretr\' foi publicado e está disponível para você!','vendedores',NULL,'2026-03-26 18:12:02'),
(42,'📚 Novo Treinamento: teste novo','Um novo treinamento \'teste novo\' foi publicado e está disponível para você!','vendedores',NULL,'2026-03-26 18:17:59'),
(43,'📚 Novo Treinamento Disponível: teste','\n        🎓 **teste** foi publicado e está disponível para você!\n        \n        📝 Acesse o Centro de Treinamentos para iniciar o curso.\n        ⏱️ Carga horária: [carga] horas\n        🎓 Modalidade: [modalidade]\n        ✅ Conclua e receba seu certificado!\n        ','todos',NULL,'2026-03-26 19:22:36'),
(44,'📚 Novo Treinamento Disponível: teste','\n        🎓 **teste** foi publicado e está disponível para você!\n        \n        📝 Acesse o Centro de Treinamentos para iniciar o curso.\n        ⏱️ Carga horária: [carga] horas\n        🎓 Modalidade: [modalidade]\n        ✅ Conclua e receba seu certificado!\n        ','todos',NULL,'2026-03-26 19:22:36'),
(45,'📚 Novo Treinamento Disponível: teste de titulo','\n🎓 **teste de titulo** foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 1 horas\n🎓 **Modalidade:** EAD\n\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 19:28:40'),
(46,'📚 Novo Treinamento Disponível: teste de titulo','\n🎓 **teste de titulo** foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 19:28:40'),
(47,'📚 Novo Treinamento Disponível:teste apos correção de espaço','🎓teste apos correção de espaço foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** Presencial\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 19:47:23'),
(48,'📚 Novo Treinamento Disponível:teste apos correção de espaço','🎓teste apos correção de espaço foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 19:47:23'),
(49,'📚 Novo Treinamento Disponível:teste de correçao espaçamento','🎓teste de correçao espaçamento foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** Presencial\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 19:51:24'),
(50,'📚 Novo Treinamento Disponível:teste de correçao espaçamento','🎓teste de correçao espaçamento foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 19:51:24'),
(51,'📚 Novo Treinamento :indentaçao','🎓indentaçao foi publicado e está disponível para você!\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** Presencial\n✅ Conclua e receba seu certificado!\n','vendedores',NULL,'2026-03-26 20:10:05'),
(52,'📚 Novo Treinamento :indentaçao','🎓indentaçao foi publicado e está disponível para você!\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','vendedores',NULL,'2026-03-26 20:10:05'),
(53,'📚 Novo Treinamento :testet','🎓testet foi publicado e está disponível para você!\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 20:11:17'),
(54,'📚 Novo Treinamento :testet','🎓testet foi publicado e está disponível para você!\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-26 20:11:17'),
(55,'📚 Novo Treinamento :**teste**','🎓teste foi publicado e está disponível para você!\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-27 19:38:22'),
(56,'📚 Novo Treinamento :**teste**','🎓teste foi publicado e está disponível para você!\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n✅ Conclua e receba seu certificado!\n','todos',NULL,'2026-03-27 19:38:22'),
(57,'📚 Novo Treinamento: intrutor','🎓 **intrutor** foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** Híbrido\n\n✅ Conclua e receba seu certificado!','todos',NULL,'2026-03-27 19:50:47'),
(58,'📚 Novo Treinamento: intrutor','🎓 **intrutor** foi publicado e está disponível para você!\n\n📝 Acesse o Centro de Treinamentos para iniciar o curso.\n\n⏱️ **Carga horária:** 4 horas\n🎓 **Modalidade:** EAD\n\n✅ Conclua e receba seu certificado!','todos',NULL,'2026-03-27 19:50:47'),
(59,'🎉 Parabéns!','Você concluiu o treinamento **intrutor** com sucesso!\n\n📜 Seu certificado já está disponível para download.','individual',6,'2026-03-27 19:53:36'),
(60,'🎉 Parabéns!','Você concluiu o treinamento **teste** com sucesso!\n\n📜 Seu certificado já está disponível para download.','individual',6,'2026-03-27 19:53:55'),
(61,'🎉 Parabéns!','Você concluiu o treinamento **testet** com sucesso!\n\n📜 Seu certificado já está disponível para download.','individual',6,'2026-03-27 19:54:05'),
(62,'🎉 Parabéns!','Você concluiu o treinamento **treinamento teste** com sucesso!\n\n📜 Seu certificado já está disponível para download.','individual',6,'2026-03-27 20:01:32');
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
(1,36,'2026-03-26 16:21:46'),
(1,37,'2026-03-26 16:21:46'),
(1,43,'2026-03-26 16:46:05'),
(1,44,'2026-03-26 16:46:06'),
(1,45,'2026-03-26 16:46:05'),
(1,46,'2026-03-26 16:46:05'),
(1,47,'2026-03-26 17:09:12'),
(1,48,'2026-03-26 17:09:12'),
(1,49,'2026-03-26 17:09:12'),
(1,50,'2026-03-26 17:09:12'),
(1,53,'2026-03-27 14:07:05'),
(1,54,'2026-03-27 14:07:05'),
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
(4,36,'2026-03-18 17:43:16'),
(4,37,'2026-03-26 15:24:40'),
(4,43,'2026-03-26 16:45:52'),
(4,44,'2026-03-26 16:45:52'),
(4,45,'2026-03-26 16:45:52'),
(4,46,'2026-03-26 16:45:52'),
(4,47,'2026-03-26 16:50:18'),
(4,48,'2026-03-26 16:50:18'),
(4,49,'2026-03-26 17:09:01'),
(4,50,'2026-03-26 17:09:01'),
(4,53,'2026-03-27 14:46:09'),
(4,54,'2026-03-27 14:46:10'),
(6,1,'2026-03-27 14:45:47'),
(6,3,'2026-03-27 14:45:47'),
(6,4,'2026-03-27 14:45:47'),
(6,5,'2026-03-27 14:45:47'),
(6,6,'2026-03-27 14:45:47'),
(6,7,'2026-03-27 14:45:47'),
(6,8,'2026-03-27 14:45:47'),
(6,9,'2026-03-27 14:45:47'),
(6,10,'2026-03-27 14:45:47'),
(6,11,'2026-03-27 14:45:47'),
(6,12,'2026-03-27 14:45:47'),
(6,13,'2026-03-27 14:45:47'),
(6,14,'2026-03-27 14:45:47'),
(6,16,'2026-03-27 14:45:47'),
(6,18,'2026-03-27 14:45:47'),
(6,19,'2026-03-27 14:45:47'),
(6,20,'2026-03-27 14:45:47'),
(6,21,'2026-03-27 14:45:47'),
(6,22,'2026-03-27 14:45:47'),
(6,23,'2026-03-27 14:45:47'),
(6,24,'2026-03-27 14:45:47'),
(6,26,'2026-03-27 14:45:47'),
(6,27,'2026-03-27 14:45:47'),
(6,28,'2026-03-27 14:45:47'),
(6,29,'2026-03-27 14:45:47'),
(6,30,'2026-03-27 14:45:47'),
(6,31,'2026-03-27 14:45:47'),
(6,32,'2026-03-27 14:45:47'),
(6,33,'2026-03-27 14:45:47'),
(6,34,'2026-03-27 14:45:47'),
(6,36,'2026-03-27 14:45:47'),
(6,37,'2026-03-27 14:45:47'),
(6,43,'2026-03-27 14:45:47'),
(6,44,'2026-03-27 14:45:47'),
(6,45,'2026-03-27 14:45:46'),
(6,46,'2026-03-27 14:45:46'),
(6,47,'2026-03-27 14:45:46'),
(6,48,'2026-03-27 14:45:46'),
(6,49,'2026-03-27 14:45:46'),
(6,50,'2026-03-27 14:45:46'),
(6,53,'2026-03-27 14:45:46'),
(6,54,'2026-03-27 14:45:46'),
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
(19,36,'2026-03-27 11:21:40'),
(19,37,'2026-03-27 11:21:40'),
(19,43,'2026-03-27 11:21:40'),
(19,44,'2026-03-27 11:21:40'),
(19,45,'2026-03-27 11:21:40'),
(19,46,'2026-03-27 11:21:40'),
(19,47,'2026-03-27 11:21:40'),
(19,48,'2026-03-27 11:21:40'),
(19,49,'2026-03-27 11:21:40'),
(19,50,'2026-03-27 11:21:40'),
(19,53,'2026-03-27 11:21:40'),
(19,54,'2026-03-27 11:21:40'),
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
(20,34,'2026-03-04 15:17:28'),
(24,1,'2026-03-27 14:42:49'),
(24,3,'2026-03-27 14:42:49'),
(24,4,'2026-03-27 14:42:49'),
(24,7,'2026-03-27 14:42:49'),
(24,8,'2026-03-27 14:42:49'),
(24,9,'2026-03-27 14:42:49'),
(24,10,'2026-03-27 14:42:49'),
(24,11,'2026-03-27 14:42:49'),
(24,12,'2026-03-27 14:42:49'),
(24,13,'2026-03-27 14:42:49'),
(24,14,'2026-03-27 14:42:49'),
(24,16,'2026-03-27 14:42:49'),
(24,17,'2026-03-27 14:42:49'),
(24,18,'2026-03-27 14:42:49'),
(24,19,'2026-03-27 14:42:49'),
(24,20,'2026-03-27 14:42:49'),
(24,21,'2026-03-27 14:42:49'),
(24,22,'2026-03-27 14:42:49'),
(24,23,'2026-03-27 14:42:49'),
(24,24,'2026-03-27 14:42:49'),
(24,25,'2026-03-27 14:42:49'),
(24,26,'2026-03-27 14:42:49'),
(24,27,'2026-03-27 14:42:49'),
(24,28,'2026-03-27 14:42:49'),
(24,29,'2026-03-27 14:42:49'),
(24,30,'2026-03-27 14:42:49'),
(24,31,'2026-03-27 14:42:49'),
(24,32,'2026-03-27 14:42:49'),
(24,33,'2026-03-27 14:42:49'),
(24,34,'2026-03-27 14:42:49'),
(24,36,'2026-03-27 14:42:49'),
(24,37,'2026-03-27 14:42:49'),
(24,43,'2026-03-27 14:42:49'),
(24,44,'2026-03-27 14:42:49'),
(24,45,'2026-03-27 14:42:49'),
(24,46,'2026-03-27 14:42:49'),
(24,47,'2026-03-27 14:42:49'),
(24,48,'2026-03-27 14:42:49'),
(24,49,'2026-03-27 14:42:49'),
(24,50,'2026-03-27 14:42:49'),
(24,53,'2026-03-27 14:42:49'),
(24,54,'2026-03-27 14:42:49');
/*!40000 ALTER TABLE `notificacoes_lidas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `permissoes_cargo`
--

DROP TABLE IF EXISTS `permissoes_cargo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissoes_cargo` (
  `id_permissao` int(11) NOT NULL AUTO_INCREMENT,
  `id_tipo_usuario` int(11) NOT NULL,
  `id_funcionalidade` int(11) NOT NULL,
  `pode_visualizar` tinyint(4) DEFAULT 1,
  `pode_criar` tinyint(4) DEFAULT 0,
  `pode_editar` tinyint(4) DEFAULT 0,
  `pode_excluir` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`id_permissao`),
  UNIQUE KEY `unique_permissao` (`id_tipo_usuario`,`id_funcionalidade`),
  KEY `id_funcionalidade` (`id_funcionalidade`),
  CONSTRAINT `permissoes_cargo_ibfk_1` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `tipo_usuario` (`id_tipo_usuario`),
  CONSTRAINT `permissoes_cargo_ibfk_2` FOREIGN KEY (`id_funcionalidade`) REFERENCES `funcionalidades` (`id_funcionalidade`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissoes_cargo`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `permissoes_cargo` WRITE;
/*!40000 ALTER TABLE `permissoes_cargo` DISABLE KEYS */;
INSERT INTO `permissoes_cargo` VALUES
(1,4,1,1,0,0,0),
(2,4,2,0,0,0,0),
(3,4,3,0,0,0,0),
(4,4,4,0,0,0,0),
(5,4,5,0,0,0,0),
(6,4,6,1,0,0,0),
(7,4,7,0,0,0,0),
(8,4,8,0,0,0,0);
/*!40000 ALTER TABLE `permissoes_cargo` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `permissoes_usuario`
--

DROP TABLE IF EXISTS `permissoes_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `permissoes_usuario` (
  `id_permissao_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) NOT NULL,
  `id_funcionalidade` int(11) NOT NULL,
  `pode_visualizar` tinyint(4) DEFAULT 1,
  `pode_criar` tinyint(4) DEFAULT 0,
  `pode_editar` tinyint(4) DEFAULT 0,
  `pode_excluir` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`id_permissao_usuario`),
  UNIQUE KEY `unique_permissao_usuario` (`id_usuario`,`id_funcionalidade`),
  KEY `id_funcionalidade` (`id_funcionalidade`),
  CONSTRAINT `permissoes_usuario_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `permissoes_usuario_ibfk_2` FOREIGN KEY (`id_funcionalidade`) REFERENCES `funcionalidades` (`id_funcionalidade`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissoes_usuario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `permissoes_usuario` WRITE;
/*!40000 ALTER TABLE `permissoes_usuario` DISABLE KEYS */;
INSERT INTO `permissoes_usuario` VALUES
(1,6,1,0,0,0,0),
(2,6,2,1,0,0,0),
(3,6,3,0,0,0,0),
(4,6,4,0,0,0,0),
(5,6,5,0,0,0,0),
(6,6,6,0,0,0,0),
(7,6,7,0,0,0,0),
(8,6,8,0,0,0,0),
(9,4,1,0,0,0,0),
(10,4,2,1,0,0,0),
(11,4,3,0,0,0,0),
(12,4,4,0,0,0,0),
(13,4,5,0,0,0,0),
(14,4,6,0,0,0,0),
(15,4,7,0,0,0,0),
(16,4,8,0,0,0,0),
(17,1,1,0,0,0,0),
(18,1,2,0,0,0,0),
(19,1,3,0,0,0,0),
(20,1,4,0,0,0,0),
(21,1,5,0,0,0,0),
(22,1,6,0,0,0,0),
(23,1,7,1,0,0,0),
(24,1,8,0,0,0,0);
/*!40000 ALTER TABLE `permissoes_usuario` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(26,'SUPORTE TECNICO',1),
(27,'COORDENADOR_TELEVENDAS',1);
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
  `obrigatorio` tinyint(4) DEFAULT 0 COMMENT 'Treinamento obrigatório por lei/norma',
  `carga_horaria` int(11) DEFAULT 0 COMMENT 'Carga horária em horas',
  `modalidade` varchar(20) DEFAULT 'EAD' COMMENT 'Modalidade do treinamento',
  `area_responsavel` varchar(50) DEFAULT NULL COMMENT 'Área responsável',
  `periodicidade` varchar(20) DEFAULT 'Anual' COMMENT 'Periodicidade de reciclagem',
  `instrutor` varchar(100) DEFAULT NULL COMMENT 'Nome do instrutor',
  `publico_alvo` text DEFAULT NULL COMMENT 'Descrição do público-alvo',
  `id_tipo_usuario_alvo` int(11) DEFAULT 0,
  PRIMARY KEY (`id_treinamento`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treinamentos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `treinamentos` WRITE;
/*!40000 ALTER TABLE `treinamentos` DISABLE KEYS */;
INSERT INTO `treinamentos` VALUES
(9,'teste01','teste 01','https://manus.im/app','Vendas','2026-03-02 11:14:16','https://manus.com.br',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,0),
(10,'um novo teste ','um novo teste ','https://chat.deepseek.com/a/c','Vendas','2026-03-02 11:47:29','https://chat.deepseek.com',2,3,0,0,'EAD',NULL,'Anual',NULL,NULL,0),
(11,'teste ','teste','https://drive.google.com','Vendas','2026-03-02 12:28:50','https://drive.google.com/drive/home',0,12,0,0,'EAD',NULL,'Anual',NULL,NULL,0),
(12,'teste apos alteraçoes ','teste apos alteraçoes mensgaem ','https://chat.deepseek.com/a/','Vendas','2026-03-02 15:50:38','https://chat.deepseek.com/a/chat/s/b89d0172-a1a1-4938-9c6c-3f5b4fb57820',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,2),
(13,'desempenho ','desempenho 02','https://chat.deepseek.com/a/chat/s/b89d0172-a1a','Sistema','2026-03-02 16:01:20','https://chat.deepseek.com',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,2),
(14,'teste final ','este e uma prova que foi corrigo o  problema ','https://drive.google.com/me','Vendas','2026-03-02 16:58:18','https://drive.goo.com',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,0),
(15,'ultimo ','teste de atusistemica ','https:// umnovotestedeatualizaçeos','Vendas','2026-03-02 17:00:45','https:// umnovotested.com',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,0),
(16,'teste ','teste sem bal~~ao ','https:// umnovotestedeatualizaçeos','Sistema','2026-03-02 17:04:04','https:// umnovotestedea.com',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,1),
(17,'analise ','novo teste ','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:13:14','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,2),
(18,'pc ','pc','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:18:19','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,1),
(19,'teste de notificaçao','teste de notificaçao','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:34:40','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,26),
(20,'teste ','https://www.youtube.com/watch?v=WH34Ea693Cs','https://www.youtube.com/watch?v=WH34Ea693Cs','Vendas','2026-03-03 16:37:04','https://www.youtube.com/watch?v=WH34Ea693Cs',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,1),
(21,'teste de notificaçao ','teste de notificaçao ','httpps/;linkteste.com.br ','Vendas','2026-03-03 17:22:33','httpps/;linkteste.com.br ',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,1),
(22,'apos novas atualiaçao','este e uma publicaçao teste apos novas atualiaçao','https://www.youtube.com/watch?v=CvqE6vATDwA','Atendimento','2026-03-06 15:38:15','https://www.youtube.com',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,2),
(23,'treinamento teste','treinamento teste inicio da nova implantação ','https://www.youtube.com/watch?v=COc7xniZPJk','Produtos','2026-03-18 17:42:13','https://www.google.com/maps',NULL,12,0,0,'EAD',NULL,'Anual',NULL,NULL,0),
(24,'teste de compliance','teste de compliance','','Obrigatórios (Leis e Normas)','2026-03-26 15:07:31','',NULL,12,1,4,'EAD','RH','Mensal','','',1),
(25,'teste','teste 029','','Obrigatórios (Leis e Normas)','2026-03-26 15:10:47','',NULL,12,1,4,'EAD','RH','Mensal','','',1),
(26,'fdffg','sfsf ghh09','','Obrigatórios (Leis e Normas)','2026-03-26 15:11:50','',NULL,12,0,4,'EAD','RH','Mensal','','',1),
(27,'eretr','vwg ','','Obrigatórios (Leis e Normas)','2026-03-26 15:12:02','',NULL,12,0,4,'EAD','RH','Mensal','','',2),
(28,'teste novo','teste com novas funcionalidades','https://www.youtube.com/watch?v=mJaPVDMzH2U','Comercial e Vendas','2026-03-26 15:17:59','https://mellinternet.com.br/',NULL,12,1,4,'EAD','TI','Anual','Pedro','Este e voltado para os vendedorees para um bom atendimento. ',2),
(29,'teste','teste com novas atualizações','','Obrigatórios (Leis e Normas)','2026-03-26 16:22:36','',NULL,12,1,4,'EAD','Operações','Mensal','','',0),
(30,'teste de titulo','teste de titulo ','','Obrigatórios (Leis e Normas)','2026-03-26 16:28:40','',NULL,12,1,1,'EAD','RH','Mensal','','',0),
(31,'teste apos correção de espaço','teste apos correção de espaço ','','Segurança e Compliance','2026-03-26 16:47:23','',NULL,3,1,4,'Presencial','TI','Mensal','Pedro','funcionários',0),
(32,'teste de correçao espaçamento','teste de correçao espaçamento','','Obrigatórios (Leis e Normas)','2026-03-26 16:51:24','',NULL,1,1,4,'Presencial','RH','Mensal','Pedro','interntos ',0),
(33,'indentaçao','indentaçao ','','Ferramentas e Sistemas','2026-03-26 17:10:05','',NULL,12,1,4,'Presencial','RH','Trimestral','pedro','teste',2),
(34,'testet','tetse de espaçamento ','','Gestão e Liderança','2026-03-26 17:11:17','',NULL,12,1,4,'EAD','RH','Mensal','pedro','interno',0),
(35,'teste','testando notificações indiidual ','','Ferramentas e Sistemas','2026-03-27 16:38:22','',NULL,12,1,4,'EAD','TI','Mensal','Pedro','interno ',0),
(36,'intrutor','demonstração de intrutor ativa ','','Obrigatórios (Leis e Normas)','2026-03-27 16:50:47','',NULL,12,1,4,'Híbrido','TI','Mensal','Pedro','interno',0);
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
  KEY `idx_vencimento` (`data_vencimento`),
  KEY `idx_treinamentos_vencimento` (`data_vencimento`),
  CONSTRAINT `treinamentos_concluidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `treinamentos_concluidos_ibfk_2` FOREIGN KEY (`id_treinamento`) REFERENCES `treinamentos` (`id_treinamento`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(24,2,15,'2026-03-03 17:26:21','2027-03-03 17:26:21','Concluído'),
(25,4,12,'2026-03-06 15:28:50','2027-03-01 15:28:51','concluido'),
(26,3,9,'2026-03-09 11:13:25','2027-03-04 11:13:24','concluido'),
(27,19,11,'2026-03-09 11:33:19','2027-03-04 11:33:19','concluido'),
(28,20,19,'2026-03-18 14:29:11','2027-03-13 14:29:11','concluido'),
(29,6,27,'2026-03-26 15:12:38','2027-03-21 15:12:38','concluido'),
(30,6,28,'2026-03-26 15:19:34','2027-03-21 15:19:34','concluido'),
(31,4,13,'2026-03-26 15:25:03','2027-03-21 15:25:03','concluido'),
(32,4,17,'2026-03-26 15:25:08','2027-03-21 15:25:08','concluido'),
(33,4,22,'2026-03-26 15:25:21','2027-03-21 15:25:21','concluido'),
(34,4,28,'2026-03-26 15:25:41','2027-03-21 15:25:41','concluido'),
(35,4,30,'2026-03-26 16:29:26','2027-03-21 16:29:25','concluido'),
(36,4,23,'2026-03-26 17:17:31','2027-03-21 17:17:30','concluido'),
(37,6,22,'2026-03-27 14:49:18','2027-03-22 14:49:19','concluido'),
(38,6,17,'2026-03-27 14:49:24','2027-03-22 14:49:24','concluido'),
(39,6,12,'2026-03-27 14:49:29','2027-03-22 14:49:30','concluido'),
(40,6,36,'2026-03-27 16:53:35','2027-03-22 16:53:35','concluido'),
(41,6,35,'2026-03-27 16:53:55','2027-03-22 16:53:55','concluido'),
(42,6,34,'2026-03-27 16:54:05','2027-03-22 16:54:05','concluido'),
(43,6,23,'2026-03-27 17:01:32','2027-03-22 17:01:32','concluido');
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
  `setor` enum('comercial','televendas') DEFAULT 'comercial',
  `id_usuario_hubsoft` int(11) DEFAULT NULL,
  `senha` varchar(255) NOT NULL DEFAULT 'Mell@9004',
  `regional` varchar(100) DEFAULT 'Geral',
  `ultimo_acesso` datetime DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `id_regional` (`id_regional`),
  KEY `id_tipo_usuario` (`id_tipo_usuario`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_regional`) REFERENCES `regional` (`id_regional`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `tipo_usuario` (`id_tipo_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'ADMINISTRADOR','admin123',5,1,1,'comercial',NULL,'Mell@9004','MOC','2026-03-24 08:31:46'),
(2,'SUPERVISOR MOC','123456',1,1,3,'comercial',NULL,'Mell@9004','MOC','2026-03-04 10:52:10'),
(3,'SUPERVISOR CURVELO','123456',2,1,3,'comercial',NULL,'Mell@9004','MOC','2026-03-04 09:43:37'),
(4,'ANA PAULA PEREIRA ROCHA','12038340633',1,1,2,'comercial',NULL,'Mell@9004','MOC','2026-03-04 16:38:24'),
(5,'PAMELA LUIZA ALVES ROCHA','01981059679',2,1,2,'comercial',NULL,'Mell@9004','MOC',NULL),
(6,'PEDRO HENRIQUE PEREIRA SILVA','01230487068',2,1,2,'comercial',NULL,'Mell@9004','MOC','2026-03-04 09:39:33'),
(14,'ze maria da mel ',NULL,1,1,2,'comercial',NULL,'Mell@2026','Geral','2026-03-02 15:06:01'),
(15,'ze maria da mel ',NULL,2,1,2,'comercial',NULL,'Mell@9004','Geral',NULL),
(16,'samanta ',NULL,1,1,2,'comercial',NULL,'Mell@9004','Geral','2026-03-02 15:06:10'),
(17,'jose aquino ',NULL,2,1,2,'comercial',NULL,'Mell@9004','Geral','2026-03-02 15:08:43'),
(18,'jojo',NULL,2,1,1,'comercial',NULL,'Mell@9004','Geral',NULL),
(19,'auditoria_mell',NULL,1,1,4,'comercial',NULL,'Mell@9004','Geral','2026-03-04 10:52:50'),
(20,'SUPORTE TECNICO','00000000000',5,1,26,'comercial',NULL,'Mell@9004','Geral','2026-03-03 17:48:14'),
(21,'jose luciano ','12309791341',4,1,2,'comercial',NULL,'Mell@9004','Serra Geral',NULL),
(22,'claudia ','22212213212',4,1,2,'comercial',NULL,'Mell@9004','Serra Geral',NULL),
(23,'mercia lopes','12318292710',4,1,1,'comercial',NULL,'Mell@9004','Serra Geral',NULL),
(24,'GESTOR_TREINAMENTO',NULL,1,1,1,'comercial',NULL,'Mell@2026','Geral','2026-03-03 17:22:16'),
(25,'otavio','2380883973',4,1,2,'comercial',NULL,'Mell@9004','Geral',NULL),
(26,'tulio','6529753974',4,1,2,'comercial',NULL,'Mell@9004','Geral',NULL),
(27,'natasha','79362082639',1,0,1,'comercial',NULL,'Mell@2026','Geral',NULL),
(33,'joaquina','0937293787',1,1,1,'comercial',NULL,'Mell@2026','Geral',NULL),
(34,'ludmila','08308725387',1,1,1,'comercial',NULL,'Mell@2026','Geral',NULL),
(35,'tereza','03792735399',1,1,1,'comercial',NULL,'Mell@2026','Geral',NULL),
(36,'joaquina','093729378',1,1,1,'comercial',NULL,'Mell@2026','Geral',NULL),
(39,'SUPERVISOR SERRA GERAL','55566677788',4,1,3,'comercial',NULL,'Mell@2026','Geral','2026-03-05 09:37:24'),
(40,'SUPERVISOR GERAL','55566677788',5,0,3,'comercial',NULL,'Mell@2026','Geral',NULL),
(41,'SUPERVISOR SALI','74027258242',3,1,3,'comercial',NULL,'Mell@9004','Geral',NULL),
(42,'THIAGO MARCIO','52937303793',3,1,2,'comercial',NULL,'Mell@9004','Geral',NULL),
(43,'PAULO CESAR','77167379748',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(44,'Marcelina','12345678901',NULL,0,2,'televendas',NULL,'Mell@2026','Geral',NULL),
(45,'LUCAS','42344509543',1,0,3,'televendas',NULL,'Mell@9004','Geral',NULL),
(46,'MARIA','00908087776',1,0,27,'televendas',NULL,'Mell@2026','Geral',NULL);
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
  `setor` enum('comercial','televendas') DEFAULT 'comercial',
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
  KEY `id_status_financeiro` (`id_status_financeiro`),
  KEY `idx_venda_data` (`data_venda`),
  KEY `idx_venda_vendedor` (`id_usuario_vendedor`),
  KEY `idx_venda_status` (`id_status`),
  CONSTRAINT `venda_ibfk_1` FOREIGN KEY (`id_tipo_operacao`) REFERENCES `tipo_operacao` (`id_tipo_operacao`),
  CONSTRAINT `venda_ibfk_2` FOREIGN KEY (`id_usuario_vendedor`) REFERENCES `users` (`id_usuario`),
  CONSTRAINT `venda_ibfk_3` FOREIGN KEY (`id_status`) REFERENCES `status` (`id_status`),
  CONSTRAINT `venda_ibfk_4` FOREIGN KEY (`id_status_financeiro`) REFERENCES `status_financeiro` (`id_status_financeiro`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `venda` WRITE;
/*!40000 ALTER TABLE `venda` DISABLE KEYS */;
INSERT INTO `venda` VALUES
(6,2,'comercial',4,2,2,110.00,0.00,10200,1,'2026-02-07',NULL,NULL,0.00),
(7,1,'comercial',4,2,2,109.00,0.00,177890,1,'2026-02-07',NULL,NULL,0.00),
(8,2,'comercial',4,2,1,110.00,89.90,1,1,'2026-02-07','2026-02-07',NULL,0.00),
(9,2,'comercial',4,2,1,110.00,89.90,89321,1,'2026-02-07','2026-02-07',NULL,0.00),
(10,1,'comercial',4,2,1,0.00,0.00,111111,1,'2026-02-07','2026-02-07',NULL,0.00),
(11,1,'comercial',4,2,1,1000.00,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(12,1,'comercial',4,2,1,100.00,0.00,13,1,'2026-02-08','2026-02-08',NULL,0.00),
(13,1,'comercial',4,2,1,100.00,0.00,4,1,'2026-02-08','2026-02-08',NULL,0.00),
(14,1,'comercial',4,2,1,100.00,0.00,5,1,'2026-02-08','2026-02-08',NULL,0.00),
(15,1,'comercial',4,2,1,100.00,0.00,11,1,'2026-02-08','2026-02-08',NULL,0.00),
(16,1,'comercial',4,2,1,98.00,0.00,99,1,'2026-02-08','2026-02-08',NULL,0.00),
(17,1,'comercial',4,2,1,90.00,0.00,19,1,'2026-02-08','2026-02-08',NULL,0.00),
(18,1,'comercial',4,2,1,50.00,0.00,22,1,'2026-02-08','2026-02-08',NULL,0.00),
(19,2,'comercial',4,2,1,110.00,89.90,1234,1,'2026-02-08','2026-02-08',NULL,0.00),
(20,1,'comercial',4,2,1,1000.00,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(21,1,'comercial',4,2,1,0.00,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(22,4,'comercial',4,2,1,90.00,109.90,101010,1,'2026-02-08','2026-02-08',NULL,0.00),
(23,1,'comercial',4,2,1,19.00,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(24,1,'comercial',4,2,1,19.00,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(25,1,'comercial',4,2,1,19.00,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(26,1,'comercial',4,2,1,90.00,0.00,909090909,1,'2026-02-10',NULL,NULL,0.00),
(27,1,'comercial',4,2,1,100000.00,0.00,10101010,1,'2026-02-10',NULL,NULL,0.00),
(28,2,'comercial',4,2,1,10.00,8.00,10,1,'2026-02-10',NULL,NULL,0.00),
(29,2,'comercial',4,2,1,10.00,8.00,20,1,'2026-02-10',NULL,NULL,0.00),
(30,2,'comercial',4,2,1,20.00,8.00,30,1,'2026-02-10',NULL,NULL,0.00),
(31,2,'comercial',4,2,1,20.00,8.00,40,1,'2026-02-10',NULL,NULL,0.00),
(32,2,'comercial',4,2,1,19.00,8.00,50,1,'2026-02-10',NULL,NULL,0.00),
(33,2,'comercial',4,2,1,20.00,9.00,60,1,'2026-02-10',NULL,NULL,0.00),
(34,2,'comercial',4,2,1,90.00,9.00,70,1,'2026-02-10',NULL,NULL,0.00),
(35,3,'comercial',4,2,1,90.00,90.00,1999,1,'2026-02-10',NULL,NULL,0.00),
(36,1,'comercial',16,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'9090909',0.00),
(37,2,'comercial',16,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'9090909',90.00),
(38,1,'comercial',17,2,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'22222',0.00),
(39,2,'comercial',17,2,1,109.00,0.00,NULL,1,'2026-02-11',NULL,'22221',90.90),
(40,1,'comercial',17,2,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'paulinho ',0.00),
(41,1,'comercial',17,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'000000',0.00),
(42,1,'comercial',17,2,1,2000.00,0.00,NULL,1,'2026-02-11',NULL,'11111',0.00),
(43,1,'comercial',17,2,1,120.00,0.00,NULL,1,'2026-02-11',NULL,'333333',0.00),
(44,1,'comercial',17,2,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'12009',0.00),
(45,2,'comercial',17,3,1,190.00,0.00,NULL,1,'2026-02-11',NULL,'12009',100.00),
(46,1,'comercial',4,3,1,10.00,0.00,NULL,1,'2026-02-11',NULL,'22222222',0.00),
(47,1,'comercial',4,4,1,50.00,0.00,NULL,1,'2026-02-11',NULL,'1122020',0.00),
(48,2,'comercial',4,2,1,70.00,0.00,NULL,1,'2026-02-11',NULL,'4002',89.90),
(49,2,'comercial',4,2,1,50.00,0.00,NULL,1,'2026-02-11',NULL,'090909',100.00),
(50,2,'comercial',4,2,1,10.00,0.00,NULL,1,'2026-02-11',NULL,'202020',20.00),
(51,2,'comercial',4,2,1,30.00,0.00,NULL,1,'2026-02-11',NULL,'000012',15.00),
(52,2,'comercial',4,3,1,75.00,0.00,NULL,1,'2026-02-11',NULL,'11111111',85.00),
(53,2,'comercial',4,4,1,90.00,0.00,NULL,1,'2026-02-11',NULL,'88888',1000.00),
(54,2,'comercial',4,3,1,20.00,30.00,12980,1,'2026-02-11',NULL,NULL,0.00),
(55,2,'comercial',4,2,1,50.00,60.00,7,1,'2026-02-11',NULL,NULL,0.00),
(56,1,'comercial',4,2,1,109.00,0.00,1,1,'2026-02-12',NULL,NULL,0.00),
(57,2,'comercial',4,2,1,109.00,139.00,2,1,'2026-02-12',NULL,NULL,0.00),
(58,2,'comercial',4,2,1,100.00,89.00,109090,1,'2026-02-12',NULL,NULL,0.00),
(59,1,'comercial',4,2,1,120.00,0.00,9009,1,'2026-02-12',NULL,NULL,0.00),
(60,1,'comercial',4,3,1,109.00,0.00,NULL,1,'2026-02-19',NULL,'marina ',0.00),
(61,1,'comercial',4,2,1,109.00,0.00,NULL,1,'2026-02-19',NULL,'marina ',0.00),
(62,1,'comercial',4,2,1,35.00,0.00,NULL,1,'2026-02-23',NULL,'223432',0.00),
(63,1,'comercial',16,2,1,110.00,0.00,NULL,1,'2026-02-23',NULL,'1232',0.00),
(64,3,'comercial',16,2,1,90.00,109.90,NULL,1,'2026-02-23',NULL,'1232',0.00),
(65,3,'comercial',16,2,1,90.00,79.90,NULL,1,'2026-02-23',NULL,'1232',0.00),
(66,1,'comercial',16,3,1,91.00,0.00,NULL,1,'2026-02-23',NULL,'2222',0.00),
(67,1,'comercial',16,2,1,91.00,0.00,NULL,1,'2026-02-23',NULL,'2228',0.00),
(68,1,'comercial',16,2,1,109.00,0.00,NULL,1,'2026-02-23',NULL,'90909',0.00),
(69,2,'comercial',16,1,1,109.00,100.00,NULL,1,'2026-02-23',NULL,'0010101',0.00),
(70,3,'comercial',16,1,1,109.00,89.90,NULL,1,'2026-02-27',NULL,'123478',0.00),
(71,1,'comercial',4,2,1,90.00,0.00,NULL,1,'2026-03-02',NULL,'21211',0.00),
(72,2,'comercial',4,2,1,90.00,109.90,NULL,1,'2026-03-02',NULL,'21210',0.00),
(73,1,'comercial',4,2,1,91.00,0.00,NULL,1,'2026-03-02',NULL,'2222',0.00),
(74,1,'comercial',4,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'222341',0.00),
(75,2,'comercial',4,4,1,109.90,89.90,NULL,1,'2026-03-02',NULL,'222341',0.00),
(76,1,'comercial',4,2,1,99.99,0.00,NULL,1,'2026-03-02',NULL,'222341',0.00),
(77,1,'comercial',16,4,1,89.90,0.00,NULL,1,'2026-03-02',NULL,'21312',0.00),
(78,1,'comercial',16,2,1,109.00,0.00,NULL,1,'2026-03-02',NULL,'21310',0.00),
(79,3,'comercial',16,4,1,109.00,129.29,NULL,1,'2026-03-02',NULL,'21310',0.00),
(80,1,'comercial',16,4,1,109.00,0.00,NULL,1,'2026-03-02',NULL,'212090',0.00),
(81,1,'comercial',17,4,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'128253',0.00),
(82,1,'comercial',17,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'828253',0.00),
(83,3,'comercial',17,2,1,90.90,109.90,NULL,1,'2026-03-02',NULL,'79352',0.00),
(84,1,'comercial',17,2,1,90.90,0.00,NULL,1,'2026-03-02',NULL,'536298',0.00),
(85,1,'comercial',17,2,1,79.90,0.00,NULL,1,'2026-03-02',NULL,'536298',0.00),
(86,1,'comercial',17,2,1,79.90,0.00,NULL,1,'2026-03-02',NULL,'82747',0.00),
(87,1,'comercial',6,2,1,89.90,0.00,NULL,1,'2026-03-02',NULL,'69297',0.00),
(88,1,'comercial',6,2,1,109.90,0.00,NULL,1,'2026-03-02',NULL,'824396',0.00),
(89,1,'comercial',6,2,1,79.90,0.00,NULL,1,'2026-03-02',NULL,'436297',0.00),
(90,3,'comercial',6,4,1,89.90,109.90,NULL,1,'2026-03-02',NULL,'436297',0.00),
(91,2,'comercial',6,4,1,120.90,89.90,NULL,1,'2026-03-02',NULL,'639398',0.00),
(92,4,'comercial',6,2,1,89.90,79.90,NULL,1,'2026-03-02',NULL,'75339',0.00),
(93,1,'comercial',4,4,1,109.90,0.00,NULL,1,'2026-03-03',NULL,'64997',0.00),
(94,1,'comercial',4,4,1,89.90,0.00,NULL,1,'2026-03-03',NULL,'649',0.00),
(95,1,'comercial',6,2,1,89.90,0.00,NULL,1,'2026-03-03','2026-03-04','0940749',0.00),
(96,3,'comercial',6,2,1,89.90,79.90,NULL,1,'2026-03-03','2026-03-04','040749',0.00),
(97,1,'comercial',6,3,1,109.90,0.00,NULL,1,'2026-03-04',NULL,'9753',0.00),
(98,1,'comercial',4,4,1,89.90,0.00,NULL,1,'2026-03-04',NULL,'7043',0.00),
(99,2,'comercial',4,3,1,89.90,0.00,NULL,1,'2026-03-04',NULL,'80835',0.00),
(100,2,'comercial',15,2,1,109.00,89.00,NULL,1,'2026-03-04','2026-03-04','4306',89.00),
(101,1,'comercial',15,2,1,89.90,0.00,NULL,1,'2026-03-04','2026-03-04','32t20',0.00),
(102,2,'comercial',15,4,1,89.90,109.90,NULL,1,'2026-03-04','2026-03-04','65293',109.90),
(103,2,'comercial',16,4,1,89.90,109.90,NULL,1,'2026-03-04','2026-03-04','33036',109.90),
(104,2,'comercial',16,4,1,79.90,109.90,NULL,1,'2026-03-04','2026-03-04','2136',109.90),
(105,2,'comercial',17,2,1,109.00,89.00,NULL,1,'2026-03-04','2026-03-04','4393',89.00),
(106,2,'comercial',17,3,1,129.90,109.00,NULL,1,'2026-03-04',NULL,'2134',109.00),
(107,2,'comercial',17,2,1,109.90,89.00,NULL,1,'2026-03-04','2026-03-04','00826',89.00),
(108,2,'comercial',17,4,1,109.90,89.00,NULL,1,'2026-03-04','2026-03-04','00826',89.00),
(109,1,'comercial',17,2,1,109.90,0.00,NULL,1,'2026-03-04','2026-03-09','02829',0.00),
(110,1,'comercial',21,2,1,350.00,0.00,NULL,1,'2026-03-01','2026-03-05',NULL,0.00),
(111,1,'comercial',21,2,1,450.00,0.00,NULL,1,'2026-03-05',NULL,NULL,0.00),
(112,1,'comercial',22,2,1,280.00,0.00,NULL,1,'2026-03-02','2026-03-05',NULL,0.00),
(113,1,'comercial',22,2,1,390.00,0.00,NULL,1,'2026-03-06',NULL,NULL,0.00),
(114,1,'comercial',25,2,1,420.00,0.00,NULL,1,'2026-03-03','2026-03-05',NULL,0.00),
(115,1,'comercial',25,2,1,520.00,0.00,NULL,1,'2026-03-07',NULL,NULL,0.00),
(116,1,'comercial',26,2,1,310.00,0.00,NULL,1,'2026-03-04','2026-03-05',NULL,0.00),
(117,1,'comercial',26,2,1,610.00,0.00,NULL,1,'2026-03-08',NULL,NULL,0.00),
(118,1,'comercial',21,3,1,350.00,0.00,NULL,1,'2026-03-01',NULL,NULL,0.00),
(119,1,'comercial',21,2,1,450.00,0.00,NULL,1,'2026-03-05',NULL,NULL,0.00),
(120,1,'comercial',22,3,1,280.00,0.00,NULL,1,'2026-03-02',NULL,NULL,0.00),
(121,1,'comercial',22,2,1,390.00,0.00,NULL,1,'2026-03-06',NULL,NULL,0.00),
(122,1,'comercial',25,3,1,420.00,0.00,NULL,1,'2026-03-03',NULL,NULL,0.00),
(123,1,'comercial',25,4,1,520.00,0.00,NULL,1,'2026-03-07',NULL,NULL,0.00),
(124,1,'comercial',26,3,1,310.00,0.00,NULL,1,'2026-03-04',NULL,NULL,0.00),
(125,1,'comercial',26,2,1,610.00,0.00,NULL,1,'2026-03-08',NULL,NULL,0.00),
(126,1,'comercial',22,3,1,89.90,0.00,NULL,1,'2026-03-05',NULL,'549368',0.00),
(127,1,'comercial',22,3,1,89.90,0.00,NULL,1,'2026-03-05',NULL,'549368',0.00),
(128,1,'comercial',22,4,1,109.90,0.00,NULL,1,'2026-03-05','2026-03-05','549388',0.00),
(129,2,'comercial',22,2,1,109.90,129.90,NULL,1,'2026-03-05','2026-03-05','549388',129.90),
(130,2,'comercial',22,2,1,79.90,129.90,NULL,1,'2026-03-05','2026-03-05','t5382',129.90),
(131,2,'comercial',4,4,1,89.00,79.90,NULL,1,'2026-03-05','2026-03-05','yo927',79.90),
(132,2,'comercial',4,3,1,89.90,79.90,NULL,1,'2026-03-05',NULL,'y680',79.90),
(133,1,'comercial',42,2,1,90.90,0.00,NULL,1,'2026-03-05','2026-03-05','702759',0.00),
(134,2,'comercial',42,2,1,90.90,89.90,NULL,1,'2026-03-05','2026-03-05','129',89.90),
(135,1,'comercial',42,2,1,90.90,0.00,NULL,1,'2026-03-05','2026-03-05','89,90',0.00),
(136,2,'comercial',42,2,1,129.00,80.00,NULL,1,'2026-03-05','2026-03-18','739468',80.00),
(137,2,'comercial',42,2,1,129.00,80.00,NULL,1,'2026-03-05','2026-03-18','4823u',80.00),
(138,1,'comercial',42,3,1,129.00,0.00,NULL,1,'2026-03-05',NULL,'4823866g',0.00),
(139,2,'comercial',42,2,1,89.00,129.90,NULL,1,'2026-03-05','2026-03-05','7202830',129.90),
(140,2,'comercial',4,4,1,89.00,109.00,NULL,1,'2026-03-06','2026-03-09','83753',109.00),
(141,1,'comercial',6,2,1,90.00,0.00,NULL,1,'2026-03-06','2026-03-09','8047',0.00),
(142,3,'comercial',26,3,1,49.00,0.00,NULL,1,'2026-03-06',NULL,'498948',0.00),
(143,3,'comercial',26,2,1,49.00,0.00,NULL,1,'2026-03-06','2026-03-11','4989400',0.00),
(144,2,'comercial',6,2,1,79.00,129.00,NULL,1,'2026-03-06','2026-03-09','7428',129.00),
(145,2,'comercial',4,2,1,129.00,90.00,NULL,1,'2026-03-07','2026-03-09','9765',90.00),
(146,3,'comercial',4,2,1,49.00,0.00,NULL,1,'2026-03-07','2026-03-09','9765',0.00),
(147,2,'comercial',4,2,1,90.90,129.00,NULL,1,'2026-03-09','2026-03-09','8027',129.00),
(148,1,'comercial',4,2,1,129.00,0.00,NULL,1,'2026-03-09','2026-03-09','00387',0.00),
(149,1,'comercial',4,2,1,129.00,0.00,NULL,1,'2026-03-09','2026-03-09','223387',0.00),
(150,1,'comercial',4,2,1,109.00,0.00,NULL,1,'2026-03-09','2026-03-09','754836',0.00),
(151,4,'comercial',5,2,1,250.00,0.00,NULL,1,'2026-03-09','2026-03-09','38999',0.00),
(152,2,'comercial',5,2,1,250.00,190.00,NULL,1,'2026-03-09','2026-03-09','38999',190.00),
(153,1,'comercial',5,2,1,89.00,0.00,NULL,1,'2026-03-09','2026-03-09','0843',0.00),
(154,1,'comercial',5,2,1,129.00,0.00,NULL,1,'2026-03-09','2026-03-09','2965',0.00),
(155,2,'comercial',4,2,1,129.00,89.00,NULL,1,'2026-03-10','2026-03-10','79475',89.00),
(156,2,'comercial',4,2,1,129.00,89.00,NULL,1,'2026-03-10','2026-03-10','00086',89.00),
(157,1,'comercial',4,2,1,89.00,0.00,NULL,1,'2026-03-10','2026-03-10','34357',0.00),
(158,2,'comercial',16,2,1,129.00,79.00,NULL,1,'2026-03-10','2026-03-10','89279',79.00),
(159,1,'comercial',16,2,1,79.00,0.00,NULL,1,'2026-03-10','2026-03-10','169364',0.00),
(160,3,'comercial',16,2,1,49.00,0.00,NULL,1,'2026-03-10','2026-03-10','49740',0.00),
(161,2,'comercial',42,3,1,89.00,79.00,NULL,1,'2026-03-10',NULL,'898',79.00),
(162,1,'comercial',6,3,1,89.00,0.00,NULL,1,'2026-03-11',NULL,'15336',0.00),
(163,3,'comercial',16,2,1,49.00,0.00,NULL,1,'2026-03-11','2026-03-11','8498',0.00),
(164,1,'comercial',6,2,1,120.00,0.00,NULL,1,'2026-03-13','2026-03-13','259564',0.00),
(165,1,'comercial',6,2,1,79.90,0.00,NULL,1,'2026-03-16','2026-03-16','262416',0.00),
(166,1,'comercial',6,2,1,79.90,0.00,NULL,1,'2026-03-16','2026-03-16','262407',0.00),
(167,1,'comercial',16,2,1,59.90,0.00,NULL,1,'2026-03-16','2026-03-16','262423',0.00),
(168,1,'comercial',16,2,1,99.90,0.00,NULL,1,'2026-03-16','2026-03-16','249876',0.00),
(169,1,'comercial',6,2,1,69.90,0.00,NULL,1,'2026-03-17','2026-03-17','260512',0.00),
(170,1,'comercial',4,2,1,99.90,0.00,NULL,1,'2026-03-17','2026-03-17','220735',0.00),
(171,1,'comercial',42,2,1,79.90,0.00,NULL,1,'2026-03-18','2026-03-18','260853',0.00),
(172,1,'comercial',42,2,1,79.90,0.00,NULL,1,'2026-03-18','2026-03-18','260749',0.00),
(173,1,'comercial',16,2,1,79.90,0.00,NULL,1,'2026-03-18','2026-03-18','260870',0.00),
(174,1,'comercial',4,2,1,79.90,0.00,NULL,1,'2026-03-19','2026-03-19','260870',0.00),
(175,1,'televendas',44,2,1,79.90,0.00,NULL,1,'2026-03-19',NULL,'262836',0.00),
(176,1,'televendas',44,2,1,79.90,0.00,NULL,1,'2026-03-19',NULL,'262777',0.00),
(177,1,'televendas',44,2,1,79.90,0.00,NULL,1,'2026-03-19','2026-03-19','262789',0.00),
(178,1,'televendas',44,2,1,79.90,0.00,NULL,1,'2026-03-19','2026-03-19','262733',0.00),
(179,1,'televendas',44,1,1,100.00,0.00,NULL,1,'2026-03-19',NULL,'262639',0.00),
(180,4,'comercial',4,2,1,79.90,0.00,NULL,1,'2026-03-20','2026-03-20','262918',0.00),
(181,1,'comercial',6,2,1,79.90,0.00,NULL,1,'2026-03-20','2026-03-20','262914',0.00),
(182,2,'comercial',6,1,1,79.90,120.90,NULL,1,'2026-03-20',NULL,'26291',120.90),
(183,2,'comercial',6,1,1,89.90,129.90,NULL,1,'2026-03-24',NULL,'262880',129.90),
(184,2,'comercial',6,1,1,129.90,89.90,NULL,1,'2026-03-24',NULL,'262918',89.90),
(185,1,'comercial',6,2,1,79.90,0.00,NULL,1,'2026-03-25','2026-03-25','263463',0.00),
(186,1,'comercial',6,2,1,69.90,0.00,NULL,1,'2026-03-25','2026-03-25','263347',0.00);
/*!40000 ALTER TABLE `venda` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Temporary table structure for view `vendas_consolidadas`
--

DROP TABLE IF EXISTS `vendas_consolidadas`;
/*!50001 DROP VIEW IF EXISTS `vendas_consolidadas`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `vendas_consolidadas` AS SELECT
 1 AS `id_venda`,
  1 AS `id_tipo_operacao`,
  1 AS `setor`,
  1 AS `id_usuario_vendedor`,
  1 AS `id_status`,
  1 AS `id_status_financeiro`,
  1 AS `valor_venda`,
  1 AS `valor_venda_antiga`,
  1 AS `codigo_cliente_servico`,
  1 AS `ativo`,
  1 AS `data_venda`,
  1 AS `data_aprovacao`,
  1 AS `codigo_cliente`,
  1 AS `valor_anterior`,
  1 AS `vendedor_nome`,
  1 AS `vendedor_setor`,
  1 AS `regional_nome` */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vendas_consolidadas`
--

/*!50001 DROP VIEW IF EXISTS `vendas_consolidadas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`intramell`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vendas_consolidadas` AS select `v`.`id_venda` AS `id_venda`,`v`.`id_tipo_operacao` AS `id_tipo_operacao`,`v`.`setor` AS `setor`,`v`.`id_usuario_vendedor` AS `id_usuario_vendedor`,`v`.`id_status` AS `id_status`,`v`.`id_status_financeiro` AS `id_status_financeiro`,`v`.`valor_venda` AS `valor_venda`,`v`.`valor_venda_antiga` AS `valor_venda_antiga`,`v`.`codigo_cliente_servico` AS `codigo_cliente_servico`,`v`.`ativo` AS `ativo`,`v`.`data_venda` AS `data_venda`,`v`.`data_aprovacao` AS `data_aprovacao`,`v`.`codigo_cliente` AS `codigo_cliente`,`v`.`valor_anterior` AS `valor_anterior`,`u`.`nome_usuario` AS `vendedor_nome`,`u`.`setor` AS `vendedor_setor`,`r`.`descricao` AS `regional_nome` from ((`venda` `v` join `users` `u` on(`v`.`id_usuario_vendedor` = `u`.`id_usuario`)) left join `regional` `r` on(`u`.`id_regional` = `r`.`id_regional`)) */;
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
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-30  8:28:21
