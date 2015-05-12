-- phpMyAdmin SQL Dump
-- version 4.2.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 27, 2015 at 01:32 PM
-- Server version: 5.5.40-0ubuntu1
-- PHP Version: 5.5.12-2ubuntu4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `product_pendrives`
--

-- --------------------------------------------------------

--
-- Table structure for table `productlink`
--

CREATE TABLE IF NOT EXISTS `productlink` (
  `pid` varchar(30) NOT NULL,
  `link` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `product_details`
--

CREATE TABLE IF NOT EXISTS `product_details` (
  `pid` varchar(30) NOT NULL,
  `pname` varchar(50) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `avgrating` int(11) NOT NULL,
  `nofive` int(11) NOT NULL,
  `nofour` int(11) NOT NULL,
  `nothree` int(11) NOT NULL,
  `notwo` int(11) NOT NULL,
  `noone` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `product_review`
--

CREATE TABLE IF NOT EXISTS `product_review` (
  `pid` varchar(50) NOT NULL,
  `uid` varchar(50) NOT NULL,
  `rid` varchar(50) NOT NULL,
  `review` mediumtext NOT NULL,
  `pfeedback` int(11) NOT NULL,
  `nfeedback` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `date` varchar(20) NOT NULL,
  `flagdup` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `productlink`
--
ALTER TABLE `productlink`
 ADD PRIMARY KEY (`pid`);

--
-- Indexes for table `product_details`
--
ALTER TABLE `product_details`
 ADD PRIMARY KEY (`pid`), ADD FULLTEXT KEY `pname` (`pname`), ADD FULLTEXT KEY `pname_2` (`pname`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
