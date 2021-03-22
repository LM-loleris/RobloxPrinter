-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 22, 2021 at 11:18 AM
-- Server version: 10.3.25-MariaDB-log
-- PHP Version: 7.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `RobloxPrinter`
--

-- --------------------------------------------------------

--
-- Table structure for table `AdminRequests`
--

CREATE TABLE `AdminRequests` (
  `Id` int(11) NOT NULL,
  `AdminId` int(11) NOT NULL,
  `UserId` bigint(20) NOT NULL,
  `Username` varchar(40) NOT NULL,
  `Type` varchar(40) NOT NULL,
  `Param` text NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `IsPrinted` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Admins`
--

CREATE TABLE `Admins` (
  `Id` int(11) NOT NULL,
  `UserId` bigint(11) NOT NULL,
  `PermissionLevel` int(11) NOT NULL DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `BannedImages`
--

CREATE TABLE `BannedImages` (
  `Id` int(11) NOT NULL,
  `ImageId` bigint(20) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `BannedUsers`
--

CREATE TABLE `BannedUsers` (
  `Id` int(11) NOT NULL,
  `UserId` bigint(20) NOT NULL,
  `BannedForImageId` bigint(20) NOT NULL,
  `AdminId` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ImageRequests`
--

CREATE TABLE `ImageRequests` (
  `Id` int(11) NOT NULL,
  `UserId` bigint(20) NOT NULL,
  `Username` varchar(40) NOT NULL,
  `ImageId` bigint(20) NOT NULL,
  `RobuxPaid` int(11) NOT NULL DEFAULT 0,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `IsPrinted` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `PrinterConfig`
--

CREATE TABLE `PrinterConfig` (
  `Id` int(11) NOT NULL,
  `IsPrintingActive` tinyint(1) NOT NULL,
  `IsStreamActive` tinyint(1) NOT NULL,
  `IsScheduled` tinyint(1) NOT NULL,
  `ScheduledStartTime` int(11) NOT NULL,
  `ScheduledStopTime` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `PrinterSignal`
--

CREATE TABLE `PrinterSignal` (
  `Id` int(11) NOT NULL,
  `RestartApp` tinyint(1) NOT NULL,
  `ShutdownApp` tinyint(1) NOT NULL,
  `ShutdownDevice` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `PrinterStatus`
--

CREATE TABLE `PrinterStatus` (
  `Id` int(11) NOT NULL,
  `LastActive` bigint(20) NOT NULL DEFAULT 0,
  `IsMaintenance` tinyint(1) NOT NULL DEFAULT 0,
  `IsPaperLow` tinyint(1) NOT NULL,
  `IsOn` tinyint(1) NOT NULL DEFAULT 0,
  `IpLocal` text NOT NULL DEFAULT '0.0.0.0',
  `IpPublic` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SpecialRequests`
--

CREATE TABLE `SpecialRequests` (
  `Id` int(11) NOT NULL,
  `UserId` bigint(20) NOT NULL,
  `Username` varchar(40) NOT NULL,
  `Type` varchar(40) NOT NULL,
  `Param` text NOT NULL,
  `RobuxPaid` int(11) NOT NULL DEFAULT 0,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `IsPrinted` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `AdminRequests`
--
ALTER TABLE `AdminRequests`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Admins`
--
ALTER TABLE `Admins`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `BannedImages`
--
ALTER TABLE `BannedImages`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `BannedUsers`
--
ALTER TABLE `BannedUsers`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `ImageRequests`
--
ALTER TABLE `ImageRequests`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `PrinterConfig`
--
ALTER TABLE `PrinterConfig`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `PrinterSignal`
--
ALTER TABLE `PrinterSignal`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `PrinterStatus`
--
ALTER TABLE `PrinterStatus`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `SpecialRequests`
--
ALTER TABLE `SpecialRequests`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `AdminRequests`
--
ALTER TABLE `AdminRequests`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Admins`
--
ALTER TABLE `Admins`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `BannedImages`
--
ALTER TABLE `BannedImages`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `BannedUsers`
--
ALTER TABLE `BannedUsers`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ImageRequests`
--
ALTER TABLE `ImageRequests`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `PrinterConfig`
--
ALTER TABLE `PrinterConfig`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `PrinterSignal`
--
ALTER TABLE `PrinterSignal`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `PrinterStatus`
--
ALTER TABLE `PrinterStatus`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `SpecialRequests`
--
ALTER TABLE `SpecialRequests`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
