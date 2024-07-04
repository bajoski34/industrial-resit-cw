
-- Create Author Table
CREATE TABLE `authors` (
    `A_ID` int(11) NOT NULL AUTO_INCREMENT,
    `A_FNAME` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `A_LNAME` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    PRIMARY KEY (`A_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

-- Create Books Table
CREATE TABLE `books` (
    `B_ID` int(11) NOT NULL AUTO_INCREMENT,
    `B_TITLE` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `B_A_ID` int(11) NOT NULL,
    `B_PUBLISHER` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `B_PUB_DATE` date NOT NULL,
    `B_SUBJECT` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `B_UNIT_PRIZE` decimal(10, 2) NOT NULL,
    `B_STOCK` int(11) NOT NULL,
    PRIMARY KEY (`B_ID`),
    FOREIGN KEY (`B_A_ID`) REFERENCES `authors`(`A_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

-- Create Customers Table
CREATE TABLE `customers` (
    `C_ID` int(11) NOT NULL AUTO_INCREMENT,
    `C_NAME` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `C_ADD` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    PRIMARY KEY (`C_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

-- Create Reservation Table
CREATE TABLE `reservation` (
    `R_ID` int(11) NOT NULL AUTO_INCREMENT,
    `R_C_ID` int(11) NOT NULL,
    `R_C_NAME` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `R_B_ID` int(11) NOT NULL,
    `R_B_TITLE` varchar(255) COLLATE utf8mb4_bin NOT NULL,
    `R_B_QUANTITY` int(11) NOT NULL,
    PRIMARY KEY (`R_ID`),
    FOREIGN KEY (`R_C_ID`) REFERENCES `customers`(`C_ID`),
    FOREIGN KEY (`R_B_ID`) REFERENCES `books`(`B_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;
