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
-- Table structure for table `assinaturas_certificados`
--

DROP TABLE IF EXISTS `assinaturas_certificados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `assinaturas_certificados` (
  `id_assinatura` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL COMMENT 'coordenacao, gerencia, diretor, rh',
  `nome` varchar(100) NOT NULL COMMENT 'Nome do responsÃ¡vel',
  `cargo` varchar(100) NOT NULL COMMENT 'Cargo do responsÃ¡vel',
  `imagem_assinatura` longblob DEFAULT NULL COMMENT 'Imagem da assinatura digitalizada',
  `ativo` tinyint(4) DEFAULT 1,
  `ordem` int(11) DEFAULT 0,
  `data_cadastro` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_assinatura`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assinaturas_certificados`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `assinaturas_certificados` WRITE;
/*!40000 ALTER TABLE `assinaturas_certificados` DISABLE KEYS */;
INSERT INTO `assinaturas_certificados` VALUES
(1,'diretor','Wamberto','Diretor Geral','‰PNG\r\n\Z\n\0\0\0\rIHDR\0\03\0\0Ì\0\0\0áğöS\0\0\0sRGB\0®Îé\0\0\0gAMA\0\0±üa\0\0\0	pHYs\0\0Ã\0\0ÃÇo¨d\0\0…IDATx^íİïkUw‚Çñıƒ|æìŸtdÂH@Rè¤,eJ·¿²T„ê°®B×Ê¥¥ˆ0D*\"B è“¸ˆb‘@E(· Z*Å¢\"*Âwïsî=÷æê´‰Óæã¼^p`z<797Î{¾?Î¿\0\0€@b\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ´9bææB™Ş9Y¶¾»PV«S\0\0\0Ï²)bfu~¦lyi²}ì+sßW\'\0\0a}1sïF™?½P®İ«ş{ƒ®}:]ÅÌ‘rşAurS»_–½V¶ì<TÎıX\0\0~SëŠ™¥cğhï](·«s±ôaõóvÍ–kÕ¹MíÛ3e¢_“eÿWÕ¹M§\n®ö=î½ô¸:\0\0/uÅÌõS½‡ä-/½VNÜ¨N®Û­2÷—*fSı£\rF’¦ËÑ•êäfsõdÙÖ½ÇÉòú—wª“\0\0ğâXß4³¯>©æ\'ËîÏoU\'×ëJÙ_ı¬‰S­êÜfÖ*\'^îİïf7®7Ë‰o«“\0\0ğY_Ì<X,{«\0Ùrp±<¬N¯qo¥k¦ìıòÁsóLÙ]ı¬ıKÕ¹!ËêòÙ²ÿ­é²µsİÎ}eş÷Üòlõl™ª¿ûºG’ÚßéÒlyıÕ©ŞÏÙs¨Ì}s¿ú·ça¥İUİã_ÎÚ!\0€Òúb¦üPæŞ¨–w|RÆ6Hû}ñpuÍKÊüSÊ?¼x¤Í¹Ÿª“µ\'·Ê¹÷ë†ÆñÆÙÒzR]óÜïd™š_Ç¨Ô“ÊùÃc¾Óó\\/ÔÄgŞãÏ­rîä²ûOUTí|³ì_)w§¿-\0\0ü\ZëŒ™æ4¦™2{³:ÙôãB™®¨;ÇÄéñSÈú‹ÿGGÚ!3÷nõİ>v»\\V¿«GEfÊÜz†İ/·º¿v$éÉ²tr¦lÛ1Y¶x¥Ü­NÓüŞ¿ş—¥cÕçw¼Y_j•ësõ¶ÔO‹Â1ıP?îİï–]ÊÜÈßÿö—ªŸù´5MKkáPÙŞù|÷ºáãïı\r\0\0`3XwÌ4G(ö^\\»[ÖõÓo= oÙu²,¯ùüÓ¡F×Ë´>¯ò£ËõZÊâ¸ÑƒG­2÷{Ê¿ı©}M;fkEn/,»wö~ŞöO«öG¢éÙQÑ‘zù³r½:Û‰ƒÛWÊş7z?gÛ{ãGVfËöê÷Ô‹òû§WÎ4~Ş@ë‹}eëKSeú‹êoĞ¹ßúê£÷Ë¹÷«óõhO7âî”ÖÕËåüülyçÏƒïûÇ÷ÊõÎºŸGwÊò©}Õùérôjçƒ\0\0°y­;f†Öûº:Yyp¥ì¯\"eêğ‘jã1Èí‡ûŞ[#‹Ôo|ÖßúxÛƒQ‚å«Qqë@ê‡üíî]Ó•¸ûÕ\'ıˆèı©q÷ËÒ‡#S¾†\"eØİ¯ş»üáÕuõw¾w£ÌıµŞİmp¬‰jL»«ÂîáwgÊTwtdºìÿjÜš™¯Ëázô¤û#;ı£úìêBy½^\'ó­ÿyqxæÉ`3†uM¡\0€ßĞúc¦¹È|$\0úoôßq¤,>¸Sæß­®;|yhŠWÊÖPœÜ)çŞ«®oş|ıbÎ{‹eïĞƒ}Ã£V™íVL—™ÿ}§wM½ÓØÍvtUŸÛº³‘èMkÍW#“ÓƒØiÇÓX÷Úú»\'Ëªëº£Q?¶ïi²úÜ×ÊÛ§Ëñú»ŞccÓ„mŸ®”Û?êOózz8âbËeµñ~›©S#k[Ú13]<=vN—‰—ß+{êûİÕº5;±‰\0\0rl fJYü z0n.ŞoŒÊÔ£ÍEşı\0bhz¡ñ”±ïG¹ßş]‰æbù{7Ê‰jÚUç¼RÀzÒ*\'^©>ÓÙ4`©¦v¤œûæLodiÇ¾2·Tıïö1ö!¾õ™x§ük÷º™2{éBy»ƒWgËÒÏá6ºË[s´©OİkÚ´ÿâÕ•v4Ş3U/wşcÛ>½ÒÙyæš–æˆÙ—‡×5bhèo^ëÿí7ñûs\0\0 ²¡˜,4Ÿ¬¾‡Geú£*.÷GUús©\nœîèM÷TW*Ùd;Xª‘‡»uÕ#3ii7—‡ß.ôƒbêóV÷¡½ÿûÛ1ÑªïoG;¶:Õ?ÎL™ê¾¨³¢5€µ1SOEk_{êXõùé²­\n±íï_¬éKçç6Öuìÿ×¿WŸí[ß=S®u¨¡?ÂTE_cÚ×ë§>ëm¨Ğü»³ôQÿwŒ¾,sğ²Ó1ïÇéŒ<ÕqòòR\0\0ş¹m(fšĞ}yfc*Øè‚ş~¤t×‹F0¶}ÜX»!Àİo>ëMëŒ Ü\\)ÇëîúİX:Ö;?ñ·3ıŸÕ¨o¼ì³sôG8\Zßcø¾ï—åO{ô;×Ş¨C©>†¶ˆn,ÌïL	ëœzp«,<ĞŸNÖ}ONû˜8¹²vGµŸ¿.G_íı{?¨š‘õFïw?mW¸Ú XFw™kl^02îáêbÙ¿§ú·ÉOÊÒ³b	\0\06‰ÅLómøï-”óõ\Z˜q£)N{ÕòGßN?¼fãîòlÙİ\r™×ÊázüÍåíÎƒ÷©²ûà™²´:¼“Z½ÕóÄËÕC}óÁ½3‘ŸæÈ–Évl=ê<à_)Ç«]ÎºÑÓ¾¶?êÓ½nø¡¿¿şfÇL9qéJ™ûp¦/[vÎ”£ÿw¹üOWÏ.şÔ»ï‡?·ÊÒéz›ä©2=ßaêjÄLwTjdk­æz£Ñ]Ù—óë;RÎıÜşİ÷ZC±5˜.\0\0›ßc¦ñ˜Æ1:*ÓÓXOR#tã¨^ãR;÷•¿âíøÃ÷3²ö£3#ÓÀÆîÖ9ÚÁtr¥¿>¥3{/îiÍniõÑ®©/—Õvu¬~Qo}<æØs¨Ì­Œ¬ciÆLûÅ\Z§±ûÙ˜©b—ŸrŸïùñ•r»?Ê\0\0›ß†c¦¿ö¥>Æî’Õó°ıĞ_/îï†Æ¸w™Ü¼Pö¾Ú™*Ï–k¿rÊÓPÌ\\^(ïJ9úÊTÙún5\r¬éQ«Ì|³7šÒõÙ7[GF}ú1ÓxgÎİ•j\Z\\ı;«ÏO}¸°vML;šV/Í–×»ß¯wİö·”Zãßº?3¿`Qş÷ƒëG·Ë®tŞ·3]¿ñ×keº}ŸËÕ(\0\0$ÙpÌ4w/ëÍ‹µî—k§;/œ,Ûÿº¸6(ƒÁúŸKQ¿´óà…rû»+åÄèûevÎ”ıóWJë™SÁ~…¡if£ÓÆÆè¿·gÜF\0\0ğbÙxÌ´u§Yíh,¨ÿ=uŞ²ß¹—cÿ€{yr«ÌvwA9ö*\'–o•‡Ï{šVãİ4k¶z§­ö1ñ·ê¡\0\0ğ‚z.1óÏäáòÉ2Q½œrÛ«ÊñK?üıÈØ€ës3eÛ®™rüê/X7ôÓby»?åm_™û¾:\0\0/ 1ó‚i}QOãk¼ÿ\0\0^@b\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€@¥ü? PÃ‹Î‡`\0\0\0\0IEND®B`‚',1,3,'2026-03-30 13:49:55'),
(2,'rh','_________________________','Recursos Humanos',NULL,0,4,'2026-03-30 13:49:55'),
(3,'tecnico','_________________________','Coordenador TÃ©cnico',NULL,0,5,'2026-03-30 13:49:55'),
(4,'coordenacao','Marian','Coordenador de Treinamentos','‰PNG\r\n\Z\n\0\0\0\rIHDR\0\03\0\0Ì\0\0\0áğöS\0\0\0sRGB\0®Îé\0\0\0gAMA\0\0±üa\0\0\0	pHYs\0\0Ã\0\0ÃÇo¨d\0\0óIDATx^íİïkU÷ÇñıA>ëƒ‘=2A˜È$c%–Š©£\"T¥……²Q)\"ƒJ…JXç¡Ø\')HÃ$>(E„‰02(Z*EIB±øîşø{Ob³nõîS_/8¨ç“{ã£ûæûãü¬\0\0\03\0\0@$1\0\0D3\0\0@$1\0\0D3\0\0@$1\0\0D3\0\0@¤à˜Y)s§\'ËgËÜr=\0\0<3bcfiîí2¶sÙÑ=Şü¬<¬çGfõn¹üÚ‹½ÏóÜËWÊb=\r\0\0ü8F3÷ËåW\'z0vø|™ı¦~’åÙr|W\r™ÎqüÓ•úÂèÜ~ÿÈàóìØu¶ÌÕó\0\0Àc´1óÏ‹eO\0İãå+å^}iS«wË…Ã­{v*—¿­¯ĞíO”±İÏ³k¢úèn=\0\0üXF\Z3‹hEI÷8Q.|U_ÜÄÂÌº{~óA¹]_\0\0#™¹Ó­(©ÇÉ­ægİš.ãë®ßñÒ%ëS\0\0à4Â˜Y(ç~Sƒäğ‰2Qãdìİ[õõu–çËÉıõú]§ÊÑWêß·3çË…Óu\ZØÎ‰2ù·ÿ“i`«÷ËíO¦Ë¡ƒıuC;œ/sßÕ×\0\0€-.f/\ræĞÇóÃ°Ù;]nÖK†VÊÕ×ëë;\'ËÉëÃu3¯|²å:›…ßx|4g×‰ráËzÁzÍ®d»^,gn<ª\'Ë·Ê™ƒë>Wç?=_–ê%ùf¶íÙî7ÊÕÿƒuB\0\00J#‹™{Ÿª_à_,çî”rû½ş¶ÆİX9óE½¨j¯“ïÜtB`oÿß;:_ş7³ğÑ‰ò\\½oÇÁ³ev±A/õÿ=1³ñèÌğsuwIÆÌÃ/?+:ql¸ÈÿÃ…ávĞßÌ—3/LtÎ¿±½Í–çË›êçêü¾Ggn•¥¹³õß›ï„6\\ct¬\\0·\0€gÜÈbfö­æËüÛevµs¢½³Yû¹1w>?|©,t¯ıö“r¨Û÷á&SÆ¾¼8ùÜW>/oÖ-7^›ó¨Ì¾r O³KÚ÷e¦>?fíÑDÇır¹™ò¶sª\\}â4±•Îï>Y¯ï2õ·•„ÊËBïÌ:æËïÙ¼Oı?ëY)7g¦Ê^dm3¦\0\0à\'`D1Ó\ZY9Ü<`ò~™y¹ù²~ªÌô9Ó\n…îÔ°f4¢8‡>¾_O¶¬.”sÏ×ûöv¾ø/×ó_œ¯ÚÜxdcÍNi{§ËÜ¿®”£Í:İÇÊ™kwËÃÕşçë³:½m¾œlîÙÆÎjKŸN\rŞcbb­ß}£‘¦f½ĞzÍ`ĞJ™;İ„Q÷ØNL\0ÀOÃhb¦#{ŞC<¼~vğTÿ±Î—ú{­§ü¯y0fçºæüÉëõ\\ËÚ©bÍ}íu7ëcæQYø°2¿øm½fïd¯£8ã¯^)ß×K×ûêÊpèõÙáˆÒFü¥ì¯×>ß	Ÿft¥=ú´>fÔÙõ‡rìwıkú›$¬™îáa\0\0<;F3‹3Ç_À×N÷jOÙê5&ÆŞZ»(~x½Í\Z«­QŸÖæ\0K­0ê­Ëlš¶Rn¾WGd_*j®é[.Èïjmd°ÕúîâıWšÏÕ~ÿÕ»eº®ãéí\r\r:÷ïu§£ı}0E®»–g8Â3Yöl¢FÌ\0\0ğìAÌ´ƒeƒ‡d¶G)ºÇşÎôfšXuóİæËûÓÅSÉZÁ°Ü‰‚\ZM uG„~·Pf^­?ëğÅŞèËšgßÖÚla1³tcºìkŞ¿{´‚åö{GúçŸoª\\]~Tî]oîé„ÌÜıÖ:¡ceúZç=›×®¯´â®®ó\0€gÀÓ™ÕùrrğÅ~ã‘„ŞvÊİkvo¼…ò08™Aè4ëW–ï”suçîf7Ï¯ŸšÕ]ÿ2[îÕhÙêgo¨3ë§™}ÿu™ıc•Îñóúg³KÚ½O§úÛFwƒíËÙrtğÿRÎïîušÜ­éA¤×u<ƒÙZÓî_[¿ôJ¹qşX™Üd÷6\0\0HõôcfÍÈËÓ¢¾[)K›¬SÙ*8¯½t©,<ø|ğ,—ñ?ÖébÍsd:çÆN•s7¾^ ÃŸ½Í)[İ8ë]ß9z£*sß¯”…kçË¾ŞC:ûÇÄ;.¿®?yıQY¸RŸÓ\n¶¥/¦û÷ì,“ïÌ–Ûúç»Úë€ºÇšéoß}6yÚ?U./öƒæá··Ê…:òôxä\0\0@¶§3­Q„ºÆco\0pûıáHHÿ˜(“ïßÙzİKËğg··?ŞÊ£2ûfûıÖ“åè•î”¶Vp4Ç·ËÕŞ®mOÖ^g´Ñô·á3h?¸î\0\0=ı˜¹ÑŠ™]?,f†ØÜ_öt¾¨7SÄzº#/¯)cpxîù©r¡™¦µMÃ(øÖŸ¬_çÓíibİ‘—É_u®9Q&ŞY÷¹Ÿàá­ê¨Í‰2³Éô·{sÓåĞÁÎÏ¯ï?vğTùÓµµ#O\0\0ğS1‚53wÊt÷iùİ“~à:Áú‘ş±ÑöÌ?Øâ•2Ù‰†Á´´mZºq±z¾†ÄŞ#åøûóeq³íœ\0€ÿÚÓ™ÿ‰•2÷Î‘ò\\\'Æ_ûäÉ;\0\0?9¡1\0\0<ëÄ\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0¨”-‡Šº$ÊÃÌ\0\0\0\0IEND®B`‚',1,1,'2026-03-30 14:02:13'),
(5,'gerencia','Fabiana','Gerente de RH','‰PNG\r\n\Z\n\0\0\0\rIHDR\0\03\0\0Ì\0\0\0áğöS\0\0\0sRGB\0®Îé\0\0\0gAMA\0\0±üa\0\0\0	pHYs\0\0Ã\0\0ÃÇo¨d\0\0IDATx^íİÿkUwÇñıƒÜa™ş0–®²—B%‹›îH„J‹ˆ([ª…22®ÊJËHW„Á‚(Œ(N!P–D¡˜J‘,íúËÄÀ”J±D‘4ï½÷æÜä$&~ëÜ®/y<à`rî¹ç&ñ—óäs>Ÿó7\0\0HÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0IÌ\0\0\0‘Ä\0\0éåŒ™[“5şÚhmØzª®>hö\0\0/•ÿ‡˜Y¨¹¿Ü¨«ÿ}¡>:|°¶¼¹£F6uÃãÕÑÚøş¥ê<l{n5uhñ|^İ[çf›İÏâŞL}ôÖØâÏô‡¯j¾Ù\r\0\0¼8†3s_¨½Xy}GmŞºëoãul¦yãsëÔÉ7ç;RŸyd¦Cİmçd=O\0\0Ã5ä˜¹[{Zağ„mãûS??LÕ¾Á9ß:ßM›gu·¦şc×âhÑk»êØ—÷›ı\0\0À‹dè#3ß~²c9X¶¬g&kêòLu~¸[w~\\hú+ºq¶6>ïÃ¯š\0\0ÀËæŒ™uòF³sˆæ¿8²Oï|~·Ù\0\0¼l†3uñƒf”äÕã5õ³\'÷?Ù/Oó³×êÜÑı5Ò[EíÕ±\Zÿóíæ\0\0`†3·ëô[MÌ<çDúG\"áÓÇEB+6¨«ÍŞúq¦&î]œ³i¬ÆNUç§æµ¿‚Îç¿«ı€jm›ö×¹[Ík,Œ0öØßçY-ÔÜ÷kşa÷ß{C¸…\0\0^ C™ku`pqôZ³ïiİ¯ëgö×+í@èmíHyDk%³¦úK*Ï}s~ñ™3«Ï³V\\İ›©c¿İZ¿ŞÜ}}ôt]ov?NçÓÖÏ¸ıDMÍvêÜÛ‹ßM¬*İŸs[óÖßeşæTØ¹¸âÛ+ÛNÔÅï›h¡f/Ÿª±×›sö·ñ:`ñ\0\0^bÃ™Ù5Ö\\\\¯¸°¸P¯\'ëäƒ—ÑÚ}iåü–ÎÄş¥ó-^©Î_.ÕîæûÕÇÌ]>P¿¼çO·——…î^Øï˜©;?uYšS3^Ç¾nŞØ5s²v.¾·¿½y¶¾m^[×­óK¿ß†šgä|U‡úŸ9ZÖ¬®îïşÇ·ëo›÷|Ü¬E}«û·jŞ·´ºòägÜÜ»Q\'÷ŒÕÈ»gëêÍ»5÷ u«İh7ü<4\0€—ÔpcfúÄÒ…ùæÃgëdï!™ë<kfÅdıÖŠd#‡¯Õ\\oßÃåQ_öZéáL{c´~58fb«F(~¸Tï4ÇëÎÇ›è­¿k^Œì¬ëaktåõã5u¯Ùÿõ©\ZéŸcív¶#­·õƒ§}®ÛæıïÖ«ÿĞ;î`M´Fq¦ÿ0ştï\0€`C™ÙOW^¸¯µ½òÆşÚwæZİYºèn=´rÓ‘º8ˆ„¥À9XŸıĞìkéüio÷µß.wC\'ÌIiÅÌ;“7êâáÁ‚c5şï¿o¾îÆ×\'BÍs;—İ÷Å –î·<X3İŸqñïñ÷Ûÿµ9fñw¹şq›ö×é›­Y;ˆúnıWıS?dFë7G¯-‡×½©Ú7áy÷Rİiv\0ÀËf¨1³t‘>Ø^ßQãœª““Wjº¹%êßOÖxsüæ3ËA±¼JÙ\Zsfš[´~³s×ògu·İ‹üş¨NËÜ¥ß5¯ÕÈ`Ék{ë£é»U_.$­?ß¥{ÿ9±<áÿß–ƒaîêñfT¦·×±æ²şüŸOš°Ûy¡Îÿ¾9æÍ³u}éVµÖR÷<‹ç­CÓ‹»Úæo^¨ñlÎ±ês¦·şæÏ<O	\0\0r5f¦.¸wÕG3O·ºÖ·gAÒºuêÁµ:°4¹}UÌÜë¾Ö›ë²éH=ÓiëÍŒêÓİ^Ùs¾®ÿØ¼şÄ˜Y¨Îd{å²VH´GDš{£;ó:5ñ^;ÏWç§ÛKl8|¾Îí\\üzExugKïõî¶úY9sÓ§kKÿüÿ¼xÖÜÕ·°‰\0\0^fCŒ™ÖEûZ£)kj½§u‹Ô·Ÿ´G\\ÔÅÁˆÎO:İÅQ«GÇ´oıj<ì»	‡ş¶iGí¸±rä¦3ÜföãLDÉêèMÂoÎİ‹ ë§VHu·‡§š[é–W\\mkÏ¹éyĞ\r£Á{ßîP÷}ó?t?ÿıÁèÔ¶zã_š×›`Ysyè\'Íû\0€`CŒ™åU½6¼Õ½ oö>Vë\"~02Ò_‘¬·¯{á¿x±Ş\r—«÷k~öJÚ¾òØå˜iOÏ÷×–ío[×g³kŒµFD6lë†J/>|WÓİPü.İÏß¾·ùúíÕùñ«:Öœ{ã‡ƒÅ\nn×gMxŒl?R\'§¿kEEëïÒœïÑ%”Û!¸zë=kç›úì½æûM»êw‘Óû~ücs+İë§jz0©s{zóü®Ù\0\0Ù†3­ÕÇzıOõÀÌÖRÎû./ÔüÍó‹+’õ@ù]MìiÎ·´×îÏ—o›ÜfÖŒ=¼[×W„H{„d-ë­*Ölİp86}·u+Ü`ëFÂ™U£<ëúnÅÑzssî|~°uşfÛ´£|ÑÄÈ½™ú¨y&MûõC½0jÍ;ÚøŞùš˜8UïlëÛû;>Õ\0\0¼ø†3­0yê˜ypeyŞÉ`ëÄ×ÍÈÅ­Kµ¯wQŞİ?²óTM­]™ìÇÏ+{&k¶÷\0ÌöhL÷<‡®>yTbù94«¶­Ç—bÙyù`Wô>kÛ‘:÷Íê‘•Ç„Ê–g@÷kúÔŞşgôbióşÓ5µÎC4çïujúòLuZ£QÌŸym|ÆŸ\0\0^dÃ‹™ÖÈO3]sß\\h‚åñğ·z~Ì³\\È/TçÒñ¥§é÷–>v©Ssëæ<Ÿù{O· ÂÏqgf²N~xºÎ]¾Ñ`(\0\0¼L†8g¦ªóéÁşÈÂÆ¿ú…\'¢ß®‰w[#8ÏD\0\0À‹l¨1\0\00,b\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€Hb\0\0ˆ$f\0\0€@Uÿß®Óíhï×i\0\0\0\0IEND®B`‚',1,2,'2026-03-30 14:02:13');
/*!40000 ALTER TABLE `assinaturas_certificados` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `backup_historico_final`
--

DROP TABLE IF EXISTS `backup_historico_final`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_historico_final` (
  `id_historico` int(11) NOT NULL DEFAULT 0,
  `vendedor_nome` varchar(255) DEFAULT NULL,
  `regional` varchar(100) DEFAULT NULL,
  `mes_referencia` int(11) DEFAULT NULL,
  `ano_referencia` int(11) DEFAULT NULL,
  `valor_pago` decimal(10,2) DEFAULT NULL,
  `status_pagamento` varchar(50) DEFAULT NULL,
  `observacao` text DEFAULT NULL,
  `data_fechamento` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_historico_final`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `backup_historico_final` WRITE;
/*!40000 ALTER TABLE `backup_historico_final` DISABLE KEYS */;
INSERT INTO `backup_historico_final` VALUES
(1,'samanta ','Moc',2,2026,0.00,'RECUSADO','','2026-02-23 17:28:58'),
(2,'ANA PAULA PEREIRA ROCHA','Moc',2,2026,52065.80,'PAGO','','2026-02-23 17:28:58'),
(3,'jose aquino ','Curvelo',2,2026,0.00,'RECUSADO','','2026-02-23 17:29:31'),
(4,'jose aquino ','Curvelo',2,2026,0.00,'RECUSADO','recusado','2026-02-23 17:29:34'),
(5,'ANA PAULA PEREIRA ROCHA','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42'),
(6,'samanta ','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42'),
(7,'PEDRO HENRIQUE PEREIRA SILVA','Moc',3,2026,0.00,'PAGO','','2026-03-03 12:18:42'),
(14,'ANA PAULA PEREIRA ROCHA',NULL,3,2026,629.40,'PAGO','ComissÃ£o baseada em 6 vendas','2026-03-17 19:35:09'),
(15,'samanta ',NULL,3,2026,709.20,'PAGO','ComissÃ£o baseada em 8 vendas','2026-03-17 19:35:09'),
(16,'ANA PAULA PEREIRA ROCHA',NULL,3,2026,629.40,'PAGO','ComissÃ£o baseada em 6 vendas','2026-03-17 19:35:38'),
(17,'samanta ',NULL,3,2026,709.20,'PAGO','ComissÃ£o baseada em 8 vendas','2026-03-17 19:35:38'),
(18,'PEDRO HENRIQUE PEREIRA SILVA','Moc',3,2026,0.00,'RECUSADO','','2026-03-31 18:45:01'),
(19,'ANA PAULA PEREIRA ROCHA','Moc',3,2026,614.74,'PAGO','','2026-03-31 18:45:01'),
(20,'samanta ','Moc',3,2026,0.00,'RECUSADO','','2026-03-31 18:45:01'),
(21,'PAMELA LUIZA ALVES ROCHA','Moc',3,2026,0.00,'RECUSADO','','2026-03-31 18:45:01'),
(22,'ANA PAULA PEREIRA ROCHA','Salinas',3,2026,279.70,'PAGO','Pagamento de 3 serviÃ§os','2026-03-31 18:56:32'),
(23,'samanta ','Salinas',3,2026,139.80,'PAGO','Pagamento de 2 serviÃ§os','2026-03-31 18:56:32'),
(29,'PEDRO HENRIQUE PEREIRA SILVA','Curvelo',4,2026,0.00,'PAGO','NÃ£o elegÃ­vel: Vendas 66.7% | MigraÃ§Ãµes 100.0% (mÃ­nimo 80% em ambas)','2026-04-01 12:05:04'),
(30,'PEDRO HENRIQUE PEREIRA SILVA','Curvelo',4,2026,0.00,'PAGO','NÃ£o elegÃ­vel: Vendas 66.7% | MigraÃ§Ãµes 100.0% (mÃ­nimo 80% em ambas)','2026-04-01 12:55:01'),
(31,'PEDRO HENRIQUE PEREIRA SILVA','Curvelo',4,2026,0.00,'PAGO','NÃ£o elegÃ­vel: Vendas 66.7% | MigraÃ§Ãµes 100.0% (mÃ­nimo 80% em ambas)','2026-04-01 12:55:06');
/*!40000 ALTER TABLE `backup_historico_final` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancelamentos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `cancelamentos` WRITE;
/*!40000 ALTER TABLE `cancelamentos` DISABLE KEYS */;
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
-- Table structure for table `comissoes`
--

DROP TABLE IF EXISTS `comissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `comissoes` (
  `id_comissao` int(11) NOT NULL AUTO_INCREMENT,
  `vendedor_id` int(11) NOT NULL,
  `vendedor_nome` varchar(100) NOT NULL,
  `setor` varchar(20) NOT NULL,
  `mes_referencia` int(11) NOT NULL,
  `ano_referencia` int(11) NOT NULL,
  `valor_total_vendas` decimal(10,2) DEFAULT 0.00,
  `valor_total_migracoes` decimal(10,2) DEFAULT 0.00,
  `qtd_vendas` int(11) DEFAULT 0,
  `qtd_migracoes` int(11) DEFAULT 0,
  `comissao_base` decimal(10,2) DEFAULT 0.00,
  `bonus_aplicado` decimal(10,2) DEFAULT 0.00,
  `valor_estornos` decimal(10,2) DEFAULT 0.00,
  `valor_final` decimal(10,2) DEFAULT 0.00,
  `status` varchar(20) DEFAULT 'calculado',
  `data_calculo` datetime DEFAULT current_timestamp(),
  `data_pagamento` datetime DEFAULT NULL,
  `observacao` text DEFAULT NULL,
  PRIMARY KEY (`id_comissao`),
  UNIQUE KEY `unique_comissao_periodo` (`vendedor_id`,`mes_referencia`,`ano_referencia`),
  KEY `idx_vendedor` (`vendedor_id`),
  KEY `idx_periodo` (`mes_referencia`,`ano_referencia`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `comissoes` WRITE;
/*!40000 ALTER TABLE `comissoes` DISABLE KEYS */;
INSERT INTO `comissoes` VALUES
(1,4,'ANA PAULA PEREIRA ROCHA','comercial',3,2026,1207.49,776.70,12,8,83.68,0.00,0.00,83.68,'calculado','2026-03-31 17:43:16',NULL,NULL),
(2,16,'samanta ','comercial',3,2026,427.70,227.00,5,3,28.20,0.00,0.00,28.20,'calculado','2026-03-31 17:43:16',NULL,NULL),
(3,17,'jose aquino ','comercial',3,2026,451.50,309.80,5,3,31.87,0.00,0.00,31.87,'calculado','2026-03-31 17:43:16',NULL,NULL),
(4,6,'PEDRO HENRIQUE PEREIRA SILVA','comercial',3,2026,1138.90,358.70,13,4,67.71,0.00,0.00,67.71,'calculado','2026-03-31 17:43:16',NULL,NULL),
(5,15,'ze maria da mel ','comercial',3,2026,89.90,109.00,1,1,7.77,0.00,0.00,7.77,'calculado','2026-03-31 17:43:16',NULL,NULL),
(6,21,'jose luciano ','comercial',3,2026,1250.00,0.00,3,0,62.50,0.00,0.00,62.50,'calculado','2026-03-31 17:43:16',NULL,NULL),
(7,22,'claudia ','comercial',3,2026,1060.00,189.80,3,2,58.69,0.00,0.00,58.69,'calculado','2026-03-31 17:43:16',NULL,NULL),
(8,25,'otavio','comercial',3,2026,940.00,0.00,2,0,47.00,0.00,0.00,47.00,'calculado','2026-03-31 17:43:16',NULL,NULL),
(9,26,'tulio','comercial',3,2026,1530.00,49.00,3,1,77.97,0.00,0.00,77.97,'calculado','2026-03-31 17:43:16',NULL,NULL),
(10,42,'THIAGO MARCIO','comercial',3,2026,511.40,517.80,6,5,41.10,0.00,0.00,41.10,'calculado','2026-03-31 17:43:16',NULL,NULL),
(11,5,'PAMELA LUIZA ALVES ROCHA','comercial',3,2026,218.00,500.00,2,2,25.90,0.00,0.00,25.90,'calculado','2026-03-31 17:43:16',NULL,NULL),
(12,44,'Marcelina','televendas',3,2026,319.60,0.00,4,0,15.98,0.00,0.00,15.98,'calculado','2026-03-31 17:43:16',NULL,NULL);
/*!40000 ALTER TABLE `comissoes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `comissoes_aprovadas`
--

DROP TABLE IF EXISTS `comissoes_aprovadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `comissoes_aprovadas` (
  `id_comissao` int(11) NOT NULL AUTO_INCREMENT,
  `id_vendedor` int(11) NOT NULL,
  `vendedor_nome` varchar(100) NOT NULL,
  `mes_referencia` int(11) NOT NULL,
  `ano_referencia` int(11) NOT NULL,
  `total_vendas` int(11) NOT NULL,
  `meta` int(11) NOT NULL,
  `vendas_acima_meta` int(11) NOT NULL,
  `migracoes` int(11) NOT NULL,
  `comissao_base` decimal(10,2) NOT NULL,
  `comissao_migracoes` decimal(10,2) NOT NULL,
  `comissao_total` decimal(10,2) NOT NULL,
  `faturamento` decimal(10,2) NOT NULL,
  `ids_vendas` text DEFAULT NULL,
  `status_pagamento` varchar(20) DEFAULT 'PENDENTE',
  `data_aprovacao` datetime DEFAULT current_timestamp(),
  `id_auditor_aprovador` int(11) DEFAULT NULL,
  `observacao` text DEFAULT NULL,
  PRIMARY KEY (`id_comissao`),
  KEY `idx_vendedor` (`id_vendedor`),
  KEY `idx_data` (`mes_referencia`,`ano_referencia`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissoes_aprovadas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `comissoes_aprovadas` WRITE;
/*!40000 ALTER TABLE `comissoes_aprovadas` DISABLE KEYS */;
INSERT INTO `comissoes_aprovadas` VALUES
(1,42,'THIAGO MARCIO',3,2026,11,8,3,5,150.00,50.00,200.00,1029.20,'133,134,135,136,137,139,171,172,194,195,196','PENDENTE','2026-03-31 12:39:25',19,NULL),
(2,6,'PEDRO HENRIQUE PEREIRA SILVA',3,2026,17,5,12,2,600.00,20.00,620.00,1497.60,'87,88,89,92,95,96,141,144,164,165,166,169,181,185,186,190,191','PENDENTE','2026-03-31 12:40:53',19,NULL),
(3,17,'jose aquino ',3,2026,8,5,3,3,150.00,30.00,180.00,761.30,'82,83,84,85,86,105,107,109','PENDENTE','2026-03-31 12:40:53',19,NULL),
(4,6,'PEDRO HENRIQUE PEREIRA SILVA',3,2026,17,5,12,2,600.00,20.00,620.00,1497.60,'87,88,89,92,95,96,141,144,164,165,166,169,181,185,186,190,191','PENDENTE','2026-03-31 13:57:58',19,NULL),
(5,17,'jose aquino ',3,2026,8,5,3,3,150.00,30.00,180.00,761.30,'82,83,84,85,86,105,107,109','PENDENTE','2026-03-31 13:57:58',19,NULL),
(6,4,'ANA PAULA PEREIRA ROCHA',3,2026,18,10,8,7,400.00,70.00,470.00,1784.39,NULL,'PENDENTE','2026-03-31 14:16:41',19,NULL),
(7,6,'PEDRO HENRIQUE PEREIRA SILVA',3,2026,17,5,12,2,600.00,20.00,620.00,1497.60,NULL,'PENDENTE','2026-03-31 14:16:41',19,NULL),
(8,17,'jose aquino ',3,2026,8,5,3,3,150.00,30.00,180.00,761.30,NULL,'PENDENTE','2026-03-31 14:16:41',19,NULL),
(9,42,'THIAGO MARCIO',3,2026,11,8,3,5,150.00,50.00,200.00,1029.20,NULL,'PENDENTE','2026-03-31 14:16:41',19,NULL),
(10,4,'ANA PAULA PEREIRA ROCHA',3,2026,18,10,8,7,400.00,70.00,470.00,1784.39,NULL,'PENDENTE','2026-03-31 14:18:59',19,NULL),
(11,6,'PEDRO HENRIQUE PEREIRA SILVA',3,2026,17,5,12,2,600.00,20.00,620.00,1497.60,NULL,'PENDENTE','2026-03-31 14:18:59',19,NULL),
(12,17,'jose aquino ',3,2026,8,5,3,3,150.00,30.00,180.00,761.30,NULL,'PENDENTE','2026-03-31 14:18:59',19,NULL),
(13,42,'THIAGO MARCIO',3,2026,11,8,3,5,150.00,50.00,200.00,1029.20,NULL,'PENDENTE','2026-03-31 14:18:59',19,NULL);
/*!40000 ALTER TABLE `comissoes_aprovadas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `comissoes_detalhes`
--

DROP TABLE IF EXISTS `comissoes_detalhes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `comissoes_detalhes` (
  `id_detalhe` int(11) NOT NULL AUTO_INCREMENT,
  `id_comissao` int(11) NOT NULL,
  `id_venda` int(11) NOT NULL,
  `id_servico` varchar(50) DEFAULT NULL,
  `tipo_operacao` varchar(20) DEFAULT NULL,
  `valor_venda` decimal(10,2) NOT NULL,
  `comissao_calculada` decimal(10,2) NOT NULL,
  `instalado_no_periodo` tinyint(1) DEFAULT 0,
  `data_instalacao` datetime DEFAULT NULL,
  `status_pagamento` varchar(20) DEFAULT 'pendente',
  PRIMARY KEY (`id_detalhe`),
  KEY `id_comissao` (`id_comissao`),
  KEY `idx_venda` (`id_venda`),
  KEY `idx_servico` (`id_servico`),
  CONSTRAINT `comissoes_detalhes_ibfk_1` FOREIGN KEY (`id_comissao`) REFERENCES `comissoes` (`id_comissao`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comissoes_detalhes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `comissoes_detalhes` WRITE;
/*!40000 ALTER TABLE `comissoes_detalhes` DISABLE KEYS */;
INSERT INTO `comissoes_detalhes` VALUES
(1,1,71,NULL,'VENDA',90.00,4.50,0,NULL,'pendente'),
(2,1,72,NULL,'MIGRAÃ‡ÃƒO',90.00,2.70,0,NULL,'pendente'),
(3,1,73,NULL,'VENDA',91.00,4.55,0,NULL,'pendente'),
(4,1,74,NULL,'VENDA',90.90,4.55,0,NULL,'pendente'),
(5,1,76,NULL,'VENDA',99.99,5.00,0,NULL,'pendente'),
(6,1,145,NULL,'MIGRAÃ‡ÃƒO',129.00,3.87,0,NULL,'pendente'),
(7,1,146,NULL,'MIGRAÃ‡ÃƒO',49.00,1.47,0,NULL,'pendente'),
(8,1,147,NULL,'MIGRAÃ‡ÃƒO',90.90,2.73,0,NULL,'pendente'),
(9,1,148,NULL,'VENDA',129.00,6.45,0,NULL,'pendente'),
(10,1,149,NULL,'VENDA',129.00,6.45,0,NULL,'pendente'),
(11,1,150,NULL,'VENDA',109.00,5.45,0,NULL,'pendente'),
(12,1,155,NULL,'MIGRAÃ‡ÃƒO',129.00,3.87,0,NULL,'pendente'),
(13,1,156,NULL,'MIGRAÃ‡ÃƒO',129.00,3.87,0,NULL,'pendente'),
(14,1,157,NULL,'VENDA',89.00,4.45,0,NULL,'pendente'),
(15,1,170,NULL,'VENDA',99.90,5.00,0,NULL,'pendente'),
(16,1,174,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(17,1,180,NULL,'MIGRAÃ‡ÃƒO',79.90,2.40,0,NULL,'pendente'),
(18,1,187,NULL,'VENDA',99.90,5.00,0,NULL,'pendente'),
(19,1,188,NULL,'VENDA',99.90,5.00,0,NULL,'pendente'),
(20,1,189,NULL,'MIGRAÃ‡ÃƒO',79.90,2.40,0,NULL,'pendente'),
(21,2,78,NULL,'VENDA',109.00,5.45,0,NULL,'pendente'),
(22,2,158,NULL,'MIGRAÃ‡ÃƒO',129.00,3.87,0,NULL,'pendente'),
(23,2,159,NULL,'VENDA',79.00,3.95,0,NULL,'pendente'),
(24,2,160,NULL,'MIGRAÃ‡ÃƒO',49.00,1.47,0,NULL,'pendente'),
(25,2,163,NULL,'MIGRAÃ‡ÃƒO',49.00,1.47,0,NULL,'pendente'),
(26,2,167,NULL,'VENDA',59.90,3.00,0,NULL,'pendente'),
(27,2,168,NULL,'VENDA',99.90,5.00,0,NULL,'pendente'),
(28,2,173,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(29,3,82,NULL,'VENDA',90.90,4.55,0,NULL,'pendente'),
(30,3,83,NULL,'MIGRAÃ‡ÃƒO',90.90,2.73,0,NULL,'pendente'),
(31,3,84,NULL,'VENDA',90.90,4.55,0,NULL,'pendente'),
(32,3,85,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(33,3,86,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(34,3,105,NULL,'MIGRAÃ‡ÃƒO',109.00,3.27,0,NULL,'pendente'),
(35,3,107,NULL,'MIGRAÃ‡ÃƒO',109.90,3.30,0,NULL,'pendente'),
(36,3,109,NULL,'VENDA',109.90,5.50,0,NULL,'pendente'),
(37,4,87,NULL,'VENDA',89.90,4.50,0,NULL,'pendente'),
(38,4,88,NULL,'VENDA',109.90,5.50,0,NULL,'pendente'),
(39,4,89,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(40,4,92,NULL,'MIGRAÃ‡ÃƒO',89.90,2.70,0,NULL,'pendente'),
(41,4,95,NULL,'VENDA',89.90,4.50,0,NULL,'pendente'),
(42,4,96,NULL,'MIGRAÃ‡ÃƒO',89.90,2.70,0,NULL,'pendente'),
(43,4,141,NULL,'VENDA',90.00,4.50,0,NULL,'pendente'),
(44,4,144,NULL,'MIGRAÃ‡ÃƒO',79.00,2.37,0,NULL,'pendente'),
(45,4,164,NULL,'VENDA',120.00,6.00,0,NULL,'pendente'),
(46,4,165,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(47,4,166,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(48,4,169,NULL,'VENDA',69.90,3.50,0,NULL,'pendente'),
(49,4,181,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(50,4,185,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(51,4,186,NULL,'VENDA',69.90,3.50,0,NULL,'pendente'),
(52,4,190,NULL,'VENDA',99.90,5.00,0,NULL,'pendente'),
(53,4,191,NULL,'MIGRAÃ‡ÃƒO',99.90,3.00,0,NULL,'pendente'),
(54,5,100,NULL,'MIGRAÃ‡ÃƒO',109.00,3.27,0,NULL,'pendente'),
(55,5,101,NULL,'VENDA',89.90,4.50,0,NULL,'pendente'),
(56,6,110,NULL,'VENDA',350.00,17.50,0,NULL,'pendente'),
(57,6,111,NULL,'VENDA',450.00,22.50,0,NULL,'pendente'),
(58,6,119,NULL,'VENDA',450.00,22.50,0,NULL,'pendente'),
(59,7,112,NULL,'VENDA',280.00,14.00,0,NULL,'pendente'),
(60,7,113,NULL,'VENDA',390.00,19.50,0,NULL,'pendente'),
(61,7,121,NULL,'VENDA',390.00,19.50,0,NULL,'pendente'),
(62,7,129,NULL,'MIGRAÃ‡ÃƒO',109.90,3.30,0,NULL,'pendente'),
(63,7,130,NULL,'MIGRAÃ‡ÃƒO',79.90,2.40,0,NULL,'pendente'),
(64,8,114,NULL,'VENDA',420.00,21.00,0,NULL,'pendente'),
(65,8,115,NULL,'VENDA',520.00,26.00,0,NULL,'pendente'),
(66,9,116,NULL,'VENDA',310.00,15.50,0,NULL,'pendente'),
(67,9,117,NULL,'VENDA',610.00,30.50,0,NULL,'pendente'),
(68,9,125,NULL,'VENDA',610.00,30.50,0,NULL,'pendente'),
(69,9,143,NULL,'MIGRAÃ‡ÃƒO',49.00,1.47,0,NULL,'pendente'),
(70,10,133,NULL,'VENDA',90.90,4.55,0,NULL,'pendente'),
(71,10,134,NULL,'MIGRAÃ‡ÃƒO',90.90,2.73,0,NULL,'pendente'),
(72,10,135,NULL,'VENDA',90.90,4.55,0,NULL,'pendente'),
(73,10,136,NULL,'MIGRAÃ‡ÃƒO',129.00,3.87,0,NULL,'pendente'),
(74,10,137,NULL,'MIGRAÃ‡ÃƒO',129.00,3.87,0,NULL,'pendente'),
(75,10,139,NULL,'MIGRAÃ‡ÃƒO',89.00,2.67,0,NULL,'pendente'),
(76,10,171,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(77,10,172,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(78,10,194,NULL,'VENDA',69.90,3.50,0,NULL,'pendente'),
(79,10,195,NULL,'VENDA',99.90,5.00,0,NULL,'pendente'),
(80,10,196,NULL,'MIGRAÃ‡ÃƒO',79.90,2.40,0,NULL,'pendente'),
(81,11,151,NULL,'MIGRAÃ‡ÃƒO',250.00,7.50,0,NULL,'pendente'),
(82,11,152,NULL,'MIGRAÃ‡ÃƒO',250.00,7.50,0,NULL,'pendente'),
(83,11,153,NULL,'VENDA',89.00,4.45,0,NULL,'pendente'),
(84,11,154,NULL,'VENDA',129.00,6.45,0,NULL,'pendente'),
(85,12,175,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(86,12,176,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(87,12,177,NULL,'VENDA',79.90,4.00,0,NULL,'pendente'),
(88,12,178,NULL,'VENDA',79.90,4.00,0,NULL,'pendente');
/*!40000 ALTER TABLE `comissoes_detalhes` ENABLE KEYS */;
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
(1,'Dashboard EstratÃ©gico','VisÃ£o geral de indicadores','dashboard','ğŸ“Š',1,1),
(2,'GestÃ£o de UsuÃ¡rios','CRUD de usuÃ¡rios do sistema','usuarios','ğŸ‘¥',1,2),
(3,'Metas Regionais','DefiniÃ§Ã£o de metas por regional','metas','ğŸ¯',1,3),
(4,'Treinamentos','GestÃ£o de treinamentos','treinamentos','ğŸ“š',1,4),
(5,'VisÃ£o de Supervisor','AprovaÃ§Ãµes e acompanhamento','supervisor','ğŸ›¡ï¸',1,5),
(6,'Auditoria','Logs e auditoria do sistema','auditoria','ğŸ“‘',1,6),
(7,'Painel Suporte','Ferramentas de suporte tÃ©cnico','suporte','ğŸ› ï¸',1,7),
(8,'ComissÃµes','CÃ¡lculo de comissionamento','comissoes','ğŸ’°',1,8);
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(14,'ANA PAULA PEREIRA ROCHA',NULL,3,2026,629.40,'PAGO','ComissÃ£o baseada em 6 vendas','2026-03-17 19:35:09'),
(15,'samanta ',NULL,3,2026,709.20,'PAGO','ComissÃ£o baseada em 8 vendas','2026-03-17 19:35:09'),
(16,'ANA PAULA PEREIRA ROCHA',NULL,3,2026,629.40,'PAGO','ComissÃ£o baseada em 6 vendas','2026-03-17 19:35:38'),
(17,'samanta ',NULL,3,2026,709.20,'PAGO','ComissÃ£o baseada em 8 vendas','2026-03-17 19:35:38'),
(18,'PEDRO HENRIQUE PEREIRA SILVA','Moc',3,2026,0.00,'RECUSADO','','2026-03-31 18:45:01'),
(19,'ANA PAULA PEREIRA ROCHA','Moc',3,2026,614.74,'PAGO','','2026-03-31 18:45:01'),
(20,'samanta ','Moc',3,2026,0.00,'RECUSADO','','2026-03-31 18:45:01'),
(21,'PAMELA LUIZA ALVES ROCHA','Moc',3,2026,0.00,'RECUSADO','','2026-03-31 18:45:01'),
(22,'ANA PAULA PEREIRA ROCHA','Salinas',3,2026,279.70,'PAGO','Pagamento de 3 serviÃ§os','2026-03-31 18:56:32'),
(23,'samanta ','Salinas',3,2026,139.80,'PAGO','Pagamento de 2 serviÃ§os','2026-03-31 18:56:32'),
(29,'PEDRO HENRIQUE PEREIRA SILVA','Curvelo',4,2026,0.00,'PAGO','NÃ£o elegÃ­vel: Vendas 66.7% | MigraÃ§Ãµes 100.0% (mÃ­nimo 80% em ambas)','2026-04-01 12:05:04'),
(30,'PEDRO HENRIQUE PEREIRA SILVA','Curvelo',4,2026,0.00,'PAGO','NÃ£o elegÃ­vel: Vendas 66.7% | MigraÃ§Ãµes 100.0% (mÃ­nimo 80% em ambas)','2026-04-01 12:55:01'),
(31,'PEDRO HENRIQUE PEREIRA SILVA','Curvelo',4,2026,0.00,'PAGO','NÃ£o elegÃ­vel: Vendas 66.7% | MigraÃ§Ãµes 100.0% (mÃ­nimo 80% em ambas)','2026-04-01 12:55:06');
/*!40000 ALTER TABLE `historico_comissoes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `historico_comissoes_detalhes`
--

DROP TABLE IF EXISTS `historico_comissoes_detalhes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `historico_comissoes_detalhes` (
  `id_detalhe` int(11) NOT NULL AUTO_INCREMENT,
  `id_historico` int(11) DEFAULT NULL,
  `id_venda` int(11) NOT NULL,
  `id_servico` varchar(50) NOT NULL,
  `vendedor_nome` varchar(100) NOT NULL,
  `valor` decimal(10,2) DEFAULT NULL,
  `mes_referencia` int(11) NOT NULL,
  `ano_referencia` int(11) NOT NULL,
  `setor` varchar(50) DEFAULT 'comercial',
  `data_pagamento` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_detalhe`),
  UNIQUE KEY `unique_venda_mes` (`id_venda`,`mes_referencia`,`ano_referencia`),
  KEY `idx_servico` (`id_servico`),
  KEY `idx_venda` (`id_venda`),
  KEY `idx_data` (`mes_referencia`,`ano_referencia`),
  KEY `id_historico` (`id_historico`),
  CONSTRAINT `historico_comissoes_detalhes_ibfk_1` FOREIGN KEY (`id_historico`) REFERENCES `historico_comissoes` (`id_historico`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico_comissoes_detalhes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `historico_comissoes_detalhes` WRITE;
/*!40000 ALTER TABLE `historico_comissoes_detalhes` DISABLE KEYS */;
/*!40000 ALTER TABLE `historico_comissoes_detalhes` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_sistema`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `logs_sistema` WRITE;
/*!40000 ALTER TABLE `logs_sistema` DISABLE KEYS */;
INSERT INTO `logs_sistema` VALUES
(1,1,'LOGIN','Acesso realizado','2026-04-01 13:51:47'),
(2,1,'USUÃRIO','Cadastrou: M.Pedro.Henrique','2026-04-01 13:54:12'),
(3,1,'USUÃRIO','Cadastrou: supervisor moc','2026-04-01 13:57:03'),
(4,1,'TREINAMENTO','Publicou: Teste para SUPORTE TECNICO','2026-04-01 14:01:51'),
(5,1,'LOGOUT','Saiu do sistema','2026-04-01 14:01:56'),
(6,49,'LOGIN','Acesso realizado','2026-04-01 14:03:05'),
(7,49,'TREINAMENTO','Concluiu: Teste','2026-04-01 14:03:56'),
(8,49,'LOGOUT','Saiu do sistema','2026-04-01 14:05:20'),
(9,24,'LOGIN','Acesso realizado','2026-04-01 14:05:31'),
(10,24,'LOGOUT','Saiu do sistema','2026-04-01 14:09:34'),
(11,49,'LOGIN','Acesso realizado','2026-04-01 14:09:56'),
(12,49,'LOGIN','Acesso realizado','2026-04-01 14:17:00'),
(13,1,'LOGIN','Entrou no sistema','2026-04-01 14:24:19'),
(14,49,'LOGIN','Acesso realizado','2026-04-01 15:46:37'),
(15,49,'USUÃRIO','Cadastrou: Nayara Freitas','2026-04-01 15:48:09'),
(16,49,'LOGOUT','Saiu do sistema','2026-04-01 15:48:24'),
(17,51,'LOGIN','Acesso realizado','2026-04-01 15:48:30'),
(18,51,'LOGOUT','Saiu do sistema','2026-04-01 15:49:22'),
(19,49,'LOGIN','Acesso realizado','2026-04-01 15:50:49'),
(20,49,'USUÃRIO','Cadastro em massa: 10 ok, 0 erros','2026-04-01 15:51:56'),
(21,49,'USUÃRIO','Cadastrou: Auditor Financeiro','2026-04-01 16:03:32'),
(22,1,'LOGIN','Acesso realizado','2026-04-01 17:20:13'),
(23,1,'LOGOUT','Saiu do sistema','2026-04-01 17:20:34'),
(24,62,'LOGIN','Acesso realizado','2026-04-01 17:20:42'),
(25,62,'LOGOUT','Saiu do sistema','2026-04-01 17:20:51'),
(26,1,'LOGIN','Acesso realizado','2026-04-01 18:01:16'),
(27,1,'LOGIN','Acesso realizado','2026-04-01 18:01:46'),
(28,1,'LOGIN','Acesso realizado','2026-04-01 18:11:29'),
(29,1,'LOGOUT','Saiu do sistema','2026-04-01 18:19:48'),
(30,49,'LOGIN','Acesso realizado','2026-04-01 18:20:29'),
(31,49,'USUÃRIO','Cadastrou: M.leo','2026-04-01 18:27:56'),
(32,49,'LOGOUT','Saiu do sistema','2026-04-01 18:28:50'),
(33,63,'LOGIN','Acesso realizado','2026-04-01 18:28:56'),
(34,63,'LOGIN','Acesso realizado','2026-04-01 18:29:18'),
(35,63,'SENHA','Senha alterada','2026-04-01 18:29:47'),
(36,1,'LOGIN','Acesso realizado','2026-04-01 18:34:21'),
(37,1,'LOGOUT','Saiu do sistema','2026-04-01 18:36:20'),
(38,62,'LOGIN','Acesso realizado','2026-04-01 18:36:44'),
(39,1,'LOGIN','Acesso realizado','2026-04-01 18:45:09'),
(40,1,'LOGIN','Acesso realizado','2026-04-01 18:46:04'),
(41,1,'LOGIN','Acesso realizado','2026-04-01 18:49:12'),
(42,1,'LOGIN','Acesso realizado','2026-04-01 18:51:55'),
(43,1,'LOGIN','Acesso realizado','2026-04-01 18:53:15'),
(44,1,'LOGIN','Acesso realizado','2026-04-01 18:53:39'),
(45,1,'LOGOUT','Saiu do sistema','2026-04-01 18:54:02'),
(46,49,'LOGIN','Acesso realizado','2026-04-01 18:59:23');
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
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(15,1,'2026-03-01',10,8),
(16,5,'2026-03-01',300,1232),
(29,2,'2026-03-01',5,5),
(30,4,'2026-03-01',25,90),
(42,3,'2026-03-01',8,5),
(73,2,'2026-04-01',25,90);
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
(1,'InadimplÃªncia','financeiro',1),
(2,'Cliente insatisfeito','insatisfacao',1),
(3,'Problemas tÃ©cnicos','tecnico',1),
(4,'Mudou de cidade','outros',1),
(5,'Valor muito alto','financeiro',1),
(6,'ConcorrÃªncia','insatisfacao',1),
(7,'Cancelamento a pedido','outros',1),
(8,'Sem necessidade do serviÃ§o','outros',1),
(9,'Problemas com atendimento','insatisfacao',1),
(10,'QuestÃµes contratuais','financeiro',1);
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
  `id_usuario_destino` int(11) DEFAULT NULL COMMENT 'ID do usuÃ¡rio destino (para notificaÃ§Ãµes individuais)',
  `data_envio` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_notificacoes_usuario_destino` (`id_usuario_destino`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificacoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `notificacoes` WRITE;
/*!40000 ALTER TABLE `notificacoes` DISABLE KEYS */;
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
/*!40000 ALTER TABLE `notificacoes_lidas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `pagamentos_comissoes`
--

DROP TABLE IF EXISTS `pagamentos_comissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagamentos_comissoes` (
  `id_pagamento` int(11) NOT NULL AUTO_INCREMENT,
  `id_comissao` int(11) NOT NULL,
  `vendedor_id` int(11) NOT NULL,
  `vendedor_nome` varchar(100) NOT NULL,
  `valor_pago` decimal(10,2) NOT NULL,
  `data_pagamento` datetime DEFAULT current_timestamp(),
  `forma_pagamento` varchar(50) DEFAULT 'transferencia',
  `comprovante` varchar(255) DEFAULT NULL,
  `observacao` text DEFAULT NULL,
  `usuario_responsavel` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_pagamento`),
  KEY `id_comissao` (`id_comissao`),
  KEY `idx_vendedor` (`vendedor_id`),
  KEY `idx_data` (`data_pagamento`),
  CONSTRAINT `pagamentos_comissoes_ibfk_1` FOREIGN KEY (`id_comissao`) REFERENCES `comissoes` (`id_comissao`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagamentos_comissoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pagamentos_comissoes` WRITE;
/*!40000 ALTER TABLE `pagamentos_comissoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagamentos_comissoes` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permissoes_usuario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `permissoes_usuario` WRITE;
/*!40000 ALTER TABLE `permissoes_usuario` DISABLE KEYS */;
INSERT INTO `permissoes_usuario` VALUES
(1,6,1,1,0,0,0),
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
-- Table structure for table `processamento_comissoes`
--

DROP TABLE IF EXISTS `processamento_comissoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `processamento_comissoes` (
  `id_processamento` int(11) NOT NULL AUTO_INCREMENT,
  `mes_referencia` int(11) NOT NULL,
  `ano_referencia` int(11) NOT NULL,
  `setor` varchar(20) DEFAULT NULL,
  `data_processamento` datetime DEFAULT current_timestamp(),
  `total_vendas` int(11) DEFAULT NULL,
  `total_comissoes` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'processado',
  `observacao` text DEFAULT NULL,
  PRIMARY KEY (`id_processamento`),
  UNIQUE KEY `unique_processamento` (`mes_referencia`,`ano_referencia`,`setor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processamento_comissoes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `processamento_comissoes` WRITE;
/*!40000 ALTER TABLE `processamento_comissoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `processamento_comissoes` ENABLE KEYS */;
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
-- Table structure for table `selo_certificado`
--

DROP TABLE IF EXISTS `selo_certificado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `selo_certificado` (
  `id_selo` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `imagem` longblob NOT NULL,
  `ativo` tinyint(4) DEFAULT 1,
  `data_cadastro` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_selo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selo_certificado`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `selo_certificado` WRITE;
/*!40000 ALTER TABLE `selo_certificado` DISABLE KEYS */;
/*!40000 ALTER TABLE `selo_certificado` ENABLE KEYS */;
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
(1,'EM ANÃLISE',1),
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
(2,'MigraÃ§Ã£o (Upgrade)',1),
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
  `obrigatorio` tinyint(4) DEFAULT 0 COMMENT 'Treinamento obrigatÃ³rio por lei/norma',
  `carga_horaria` int(11) DEFAULT 0 COMMENT 'Carga horÃ¡ria em horas',
  `modalidade` varchar(20) DEFAULT 'EAD' COMMENT 'Modalidade do treinamento',
  `area_responsavel` varchar(50) DEFAULT NULL COMMENT 'Ãrea responsÃ¡vel',
  `periodicidade` varchar(20) DEFAULT 'Anual' COMMENT 'Periodicidade de reciclagem',
  `instrutor` varchar(100) DEFAULT NULL COMMENT 'Nome do instrutor',
  `publico_alvo` text DEFAULT NULL COMMENT 'DescriÃ§Ã£o do pÃºblico-alvo',
  `id_tipo_usuario_alvo` int(11) DEFAULT 0,
  PRIMARY KEY (`id_treinamento`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treinamentos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `treinamentos` WRITE;
/*!40000 ALTER TABLE `treinamentos` DISABLE KEYS */;
INSERT INTO `treinamentos` VALUES
(1,'Teste','ultmo teste de informaÃ§Ã£o ','https://www.youtube.com/watch?v=zwmEAWaclgU','ObrigatÃ³rios (Leis e Normas)','2026-04-01 11:01:51','https://trello.com/b/1n3WBsgL/meu-quadro-do-trello',NULL,12,1,1,'EAD','TI','Mensal','Pedro','internos',26);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treinamentos_concluidos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `treinamentos_concluidos` WRITE;
/*!40000 ALTER TABLE `treinamentos_concluidos` DISABLE KEYS */;
INSERT INTO `treinamentos_concluidos` VALUES
(1,49,1,'2026-04-01 11:03:56','2027-03-27 11:03:56','concluido');
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
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'ADMINISTRADOR','admin123',5,1,1,'comercial',NULL,'Mell@9004','MOC','2026-04-01 11:24:19'),
(24,'GESTOR_TREINAMENTO',NULL,1,1,1,'comercial',NULL,'Mell@2026','Geral','2026-03-03 17:22:16'),
(49,'M.PEDRO.HENRIQUE','02304870686',5,1,26,'comercial',NULL,'suporte@Mell','Geral',NULL),
(51,'NAYARA FREITAS','09844997682',1,1,3,'comercial',NULL,'Mell@2026','Geral',NULL),
(52,'KELLY RODRIGUES','07803609660',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(53,'MARIA EDUARDA','17059128697',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(54,'LUDMYLLA FREITAS','36561335813',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(55,'VANDERLUCIA PEREIRA','13298361623',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(56,'ANA CAROLINE','70101844611',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(57,'KELLY RIBEIRO','16076570660',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(58,'SHEILA SANTIAGO','01990211631',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(59,'THAIS DIAS','05316789628',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(60,'NUBIA PRISCILA','12900985650',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(61,'WELEN KATIANE','06886431676',1,1,2,'comercial',NULL,'Mell@2026','Geral',NULL),
(62,'AUDITOR FINANCEIRO','10000101010',5,1,4,'comercial',NULL,'Mell@2026','Geral',NULL),
(63,'M.LEO','41548432814',5,1,26,'comercial',NULL,'L120832$','Geral',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=200 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
(59,1,'comercial',4,2,1,120.00,0.00,9009,1,'2026-02-12',NULL,'229808',0.00),
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
(186,1,'comercial',6,2,1,69.90,0.00,NULL,1,'2026-03-25','2026-03-25','263347',0.00),
(187,1,'comercial',4,2,2,99.90,0.00,NULL,1,'2026-03-30','2026-03-31','263391',0.00),
(188,1,'comercial',4,2,2,99.90,0.00,NULL,1,'2026-03-30','2026-03-31','263391',0.00),
(189,2,'comercial',4,2,1,79.90,129.90,NULL,1,'2026-03-30','2026-03-30','263497',129.90),
(190,1,'comercial',6,2,1,99.90,0.00,NULL,1,'2026-03-30','2026-03-30','263103',0.00),
(191,4,'comercial',6,2,1,99.90,0.00,NULL,1,'2026-03-30','2026-03-30','263103',0.00),
(192,1,'comercial',6,1,1,69.90,0.00,NULL,1,'2026-03-30',NULL,'263452',0.00),
(193,2,'comercial',6,1,1,69.90,59.90,NULL,1,'2026-03-30',NULL,'263452',59.90),
(194,1,'comercial',42,2,1,69.90,0.00,NULL,1,'2026-03-31','2026-03-31','263367',0.00),
(195,1,'comercial',42,2,1,99.90,0.00,NULL,1,'2026-03-31','2026-03-31','263391',0.00),
(196,2,'comercial',42,2,1,79.90,79.90,NULL,1,'2026-03-31','2026-03-31','262961',79.90),
(197,1,'comercial',6,2,2,79.90,0.00,NULL,1,'2026-04-01','2026-04-01','264183',0.00),
(198,1,'comercial',6,2,2,79.90,0.00,NULL,1,'2026-04-01','2026-04-01','264084',0.00),
(199,2,'comercial',6,2,2,109.90,79.90,NULL,1,'2026-04-01','2026-04-01','263931',79.90);
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
-- Table structure for table `vendas_pagamentos`
--

DROP TABLE IF EXISTS `vendas_pagamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendas_pagamentos` (
  `id_pagamento` int(11) NOT NULL AUTO_INCREMENT,
  `id_venda` int(11) NOT NULL,
  `mes` int(11) NOT NULL,
  `ano` int(11) NOT NULL,
  `status_pagamento` varchar(20) DEFAULT 'confirmado',
  `data_confirmacao` datetime DEFAULT current_timestamp(),
  `tentativas` int(11) DEFAULT 1,
  PRIMARY KEY (`id_pagamento`),
  UNIQUE KEY `unique_venda_mes` (`id_venda`,`mes`,`ano`),
  KEY `idx_venda` (`id_venda`),
  KEY `idx_periodo` (`mes`,`ano`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas_pagamentos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `vendas_pagamentos` WRITE;
/*!40000 ALTER TABLE `vendas_pagamentos` DISABLE KEYS */;
INSERT INTO `vendas_pagamentos` VALUES
(1,1,3,2025,'confirmado','2026-03-31 17:29:04',1),
(2,1,4,2026,'confirmado','2026-04-01 08:39:06',1);
/*!40000 ALTER TABLE `vendas_pagamentos` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

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

-- Dump completed on 2026-04-01 15:59:27
