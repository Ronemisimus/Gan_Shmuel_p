 
--
-- Database: `billdb`
--

CREATE DATABASE IF NOT EXISTS `billdb`;
USE `billdb`;

-- --------------------------------------------------------

--
-- Table structure
--

CREATE TABLE IF NOT EXISTS `Provider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL UNIQUE,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  AUTO_INCREMENT=10001 ;

CREATE TABLE IF NOT EXISTS `Rates` (
  `product_id` varchar(50) NOT NULL,
  `rate` int(11) DEFAULT 0,
  `scope` varchar(50) DEFAULT 'ALL',
  FOREIGN KEY (scope) REFERENCES `Provider`(`id`),
  CONSTRAINT PK_Product_Scope PRIMARY KEY (product_id, scope)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

CREATE TABLE IF NOT EXISTS `Trucks` (
  `id` varchar(10) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`provider_id`) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;
--
-- Dumping data
--


INSERT INTO Provider (`name`) VALUES ('Ron'), ('pro1'),
('pro2'),('ALL');

INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES ('first', 2, 'ALL'),
('second', 4, 'pro1'),('Oranges',5,'10001'),('Apples',7,'10001');

INSERT INTO Trucks (`id`, `provider_id`) VALUES ('134-33-443', 2),
('222-33-111', 1), ('Truck1', 10001);