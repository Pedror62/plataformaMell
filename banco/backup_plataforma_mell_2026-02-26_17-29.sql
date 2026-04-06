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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(4,'jose aquino ','Curvelo',2,2026,0.00,'RECUSADO','recusado','2026-02-23 17:29:34');
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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(53,20,'NOTIFICACAO_ENVIADA','Título: novo teste','2026-02-26 20:28:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metas_regionais`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `metas_regionais` WRITE;
/*!40000 ALTER TABLE `metas_regionais` DISABLE KEYS */;
INSERT INTO `metas_regionais` VALUES
(1,1,'2026-02-01',10,10),
(2,2,'2026-02-01',100000,1),
(6,5,'2026-02-01',10,10);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(4,'novo teste','teste apos adiçao de funçao de backup  ','Todos','2026-02-26 20:28:26');
/*!40000 ALTER TABLE `notificacoes` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'ADMINISTRADOR','admin123',5,1,1,NULL,'Mell@9004','MOC','2026-02-23 20:45:02'),
(2,'SUPERVISOR MOC','123456',1,1,3,NULL,'Mell@9004','MOC','2026-02-23 20:22:59'),
(3,'SUPERVISOR CURVELO','123456',2,1,3,NULL,'Mell@9004','MOC','2026-02-19 19:43:09'),
(4,'ANA PAULA PEREIRA ROCHA','12038340633',1,0,2,NULL,'Mell@9004','MOC','2026-02-24 12:21:17'),
(5,'PAMELA LUIZA ALVES ROCHA','01981059679',2,1,2,NULL,'Mell@9004','MOC',NULL),
(6,'PEDRO HENRIQUE PEREIRA SILVA','01230487068',2,0,2,NULL,'Mell@9004','MOC',NULL),
(14,'ze maria da mel ',NULL,1,1,2,NULL,'Mell@9004','Geral',NULL),
(15,'ze maria da mel ',NULL,2,1,2,NULL,'Mell@9004','Geral',NULL),
(16,'samanta ',NULL,1,1,2,NULL,'Mell@9004','Geral','2026-02-23 20:39:24'),
(17,'jose aquino ',NULL,2,1,2,NULL,'Mell@9004','Geral','2026-02-11 18:25:53'),
(18,'jojo',NULL,2,1,1,NULL,'Mell@9004','Geral',NULL),
(19,'auditoria_mell',NULL,1,1,4,NULL,'Mell@9004','Geral','2026-02-23 19:58:47'),
(20,'SUPORTE TECNICO','00000000000',5,1,26,NULL,'Mell@9004','Geral',NULL);
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
  `valor_venda` decimal(10,0) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `venda` WRITE;
/*!40000 ALTER TABLE `venda` DISABLE KEYS */;
INSERT INTO `venda` VALUES
(6,2,4,2,2,110,0.00,10200,1,'2026-02-07',NULL,NULL,0.00),
(7,1,4,2,2,109,0.00,177890,1,'2026-02-07',NULL,NULL,0.00),
(8,2,4,2,1,110,89.90,1,1,'2026-02-07','2026-02-07',NULL,0.00),
(9,2,4,2,1,110,89.90,89321,1,'2026-02-07','2026-02-07',NULL,0.00),
(10,1,4,2,1,0,0.00,111111,1,'2026-02-07','2026-02-07',NULL,0.00),
(11,1,4,2,1,1000,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(12,1,4,2,1,100,0.00,13,1,'2026-02-08','2026-02-08',NULL,0.00),
(13,1,4,2,1,100,0.00,4,1,'2026-02-08','2026-02-08',NULL,0.00),
(14,1,4,2,1,100,0.00,5,1,'2026-02-08','2026-02-08',NULL,0.00),
(15,1,4,2,1,100,0.00,11,1,'2026-02-08','2026-02-08',NULL,0.00),
(16,1,4,2,1,98,0.00,99,1,'2026-02-08','2026-02-08',NULL,0.00),
(17,1,4,2,1,90,0.00,19,1,'2026-02-08','2026-02-08',NULL,0.00),
(18,1,4,2,1,50,0.00,22,1,'2026-02-08','2026-02-08',NULL,0.00),
(19,2,4,2,1,110,89.90,1234,1,'2026-02-08','2026-02-08',NULL,0.00),
(20,1,4,2,1,1000,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(21,1,4,2,1,0,0.00,1,1,'2026-02-08','2026-02-08',NULL,0.00),
(22,4,4,2,1,90,109.90,101010,1,'2026-02-08','2026-02-08',NULL,0.00),
(23,1,4,2,1,19,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(24,1,4,2,1,19,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(25,1,4,2,1,19,0.00,NULL,1,'2026-02-10',NULL,NULL,0.00),
(26,1,4,2,1,90,0.00,909090909,1,'2026-02-10',NULL,NULL,0.00),
(27,1,4,2,1,100000,0.00,10101010,1,'2026-02-10',NULL,NULL,0.00),
(28,2,4,2,1,10,8.00,10,1,'2026-02-10',NULL,NULL,0.00),
(29,2,4,2,1,10,8.00,20,1,'2026-02-10',NULL,NULL,0.00),
(30,2,4,2,1,20,8.00,30,1,'2026-02-10',NULL,NULL,0.00),
(31,2,4,2,1,20,8.00,40,1,'2026-02-10',NULL,NULL,0.00),
(32,2,4,2,1,19,8.00,50,1,'2026-02-10',NULL,NULL,0.00),
(33,2,4,2,1,20,9.00,60,1,'2026-02-10',NULL,NULL,0.00),
(34,2,4,2,1,90,9.00,70,1,'2026-02-10',NULL,NULL,0.00),
(35,3,4,2,1,90,90.00,1999,1,'2026-02-10',NULL,NULL,0.00),
(36,1,16,2,1,120,0.00,NULL,1,'2026-02-11',NULL,'9090909',0.00),
(37,2,16,2,1,120,0.00,NULL,1,'2026-02-11',NULL,'9090909',90.00),
(38,1,17,2,1,90,0.00,NULL,1,'2026-02-11',NULL,'22222',0.00),
(39,2,17,2,1,109,0.00,NULL,1,'2026-02-11',NULL,'22221',90.90),
(40,1,17,2,1,90,0.00,NULL,1,'2026-02-11',NULL,'paulinho ',0.00),
(41,1,17,2,1,120,0.00,NULL,1,'2026-02-11',NULL,'000000',0.00),
(42,1,17,2,1,2000,0.00,NULL,1,'2026-02-11',NULL,'11111',0.00),
(43,1,17,2,1,120,0.00,NULL,1,'2026-02-11',NULL,'333333',0.00),
(44,1,17,2,1,90,0.00,NULL,1,'2026-02-11',NULL,'12009',0.00),
(45,2,17,3,1,190,0.00,NULL,1,'2026-02-11',NULL,'12009',100.00),
(46,1,4,3,1,10,0.00,NULL,1,'2026-02-11',NULL,'22222222',0.00),
(47,1,4,4,1,50,0.00,NULL,1,'2026-02-11',NULL,'1122020',0.00),
(48,2,4,2,1,70,0.00,NULL,1,'2026-02-11',NULL,'4002',89.90),
(49,2,4,2,1,50,0.00,NULL,1,'2026-02-11',NULL,'090909',100.00),
(50,2,4,2,1,10,0.00,NULL,1,'2026-02-11',NULL,'202020',20.00),
(51,2,4,2,1,30,0.00,NULL,1,'2026-02-11',NULL,'000012',15.00),
(52,2,4,3,1,75,0.00,NULL,1,'2026-02-11',NULL,'11111111',85.00),
(53,2,4,4,1,90,0.00,NULL,1,'2026-02-11',NULL,'88888',1000.00),
(54,2,4,3,1,20,30.00,12980,1,'2026-02-11',NULL,NULL,0.00),
(55,2,4,2,1,50,60.00,7,1,'2026-02-11',NULL,NULL,0.00),
(56,1,4,2,1,109,0.00,1,1,'2026-02-12',NULL,NULL,0.00),
(57,2,4,2,1,109,139.00,2,1,'2026-02-12',NULL,NULL,0.00),
(58,2,4,2,1,100,89.00,109090,1,'2026-02-12',NULL,NULL,0.00),
(59,1,4,2,1,120,0.00,9009,1,'2026-02-12',NULL,NULL,0.00),
(60,1,4,3,1,109,0.00,NULL,1,'2026-02-19',NULL,'marina ',0.00),
(61,1,4,2,1,109,0.00,NULL,1,'2026-02-19',NULL,'marina ',0.00),
(62,1,4,2,1,35,0.00,NULL,1,'2026-02-23',NULL,'223432',0.00),
(63,1,16,2,1,110,0.00,NULL,1,'2026-02-23',NULL,'1232',0.00),
(64,3,16,2,1,90,109.90,NULL,1,'2026-02-23',NULL,'1232',0.00),
(65,3,16,2,1,90,79.90,NULL,1,'2026-02-23',NULL,'1232',0.00),
(66,1,16,3,1,91,0.00,NULL,1,'2026-02-23',NULL,'2222',0.00),
(67,1,16,2,1,91,0.00,NULL,1,'2026-02-23',NULL,'2228',0.00),
(68,1,16,2,1,109,0.00,NULL,1,'2026-02-23',NULL,'90909',0.00),
(69,2,16,1,1,109,100.00,NULL,1,'2026-02-23',NULL,'0010101',0.00);
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

-- Dump completed on 2026-02-26 17:29:53
