CREATE DATABASE `furniture`;
USE `furniture`;

CREATE TABLE `stock` (
  `Stock_ID` INT NOT NULL AUTO_INCREMENT,
  `Stock_Capacity` INT NOT NULL,
  `Stock_Avail` INT DEFAULT NULL,
  PRIMARY KEY (`Stock_ID`)
);

CREATE TABLE `product` (
  `Prod_ID` INT NOT NULL AUTO_INCREMENT,
  `Prod_Name` VARCHAR(20) NOT NULL,
  `Prod_Descp` VARCHAR(30) DEFAULT NULL,
  `Prod_Price` INT DEFAULT NULL,
  `StockID` INT DEFAULT NULL,
  PRIMARY KEY (`Prod_ID`),
  FOREIGN KEY (`StockID`) REFERENCES `stock` (`Stock_ID`)
);

CREATE TABLE `customer` (
  `Customer_ID` INT NOT NULL AUTO_INCREMENT,
  `Customer_Name` VARCHAR(30) DEFAULT NULL,
  `Customer_Email` VARCHAR(30) DEFAULT NULL,
  `Customer_PhNo` VARCHAR(15) DEFAULT NULL,
  `Customer_Address` VARCHAR(60) DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`)
);

CREATE TABLE `purchase` (
  `purchase_id` INT NOT NULL AUTO_INCREMENT,
  `Customer_ID` INT NOT NULL,
  `Product_ID` INT NOT NULL,
  `Quantity` INT DEFAULT NULL,
  `Total` DECIMAL(10,2) DEFAULT NULL,
  `Payment_Method` VARCHAR(50) DEFAULT NULL,
  `Order_Date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`purchase_id`),
  FOREIGN KEY (`Customer_ID`) REFERENCES `customer`(`Customer_ID`),
  FOREIGN KEY (`Product_ID`) REFERENCES `product`(`Prod_ID`)
);

CREATE TABLE `supplier` (
  `Supplier_ID` INT NOT NULL AUTO_INCREMENT,
  `Supplier_Name` VARCHAR(30) DEFAULT NULL,
  `Supplier_PhNo` VARCHAR(15) DEFAULT NULL,
  `Supplier_Address` VARCHAR(60) DEFAULT NULL,
  `Emp_incharge` INT DEFAULT NULL,
  PRIMARY KEY (`Supplier_ID`)
);

CREATE TABLE `employee` (
  `Emp_ID` INT NOT NULL AUTO_INCREMENT,
  `Emp_Name` VARCHAR(30) DEFAULT NULL,
  `Emp_PhNo` VARCHAR(15) DEFAULT NULL,
  `Emp_Position` VARCHAR(20) DEFAULT NULL,
  `Emp_Email` VARCHAR(30) DEFAULT NULL,
  `Emp_Sal` INT DEFAULT NULL,
  PRIMARY KEY (`Emp_ID`)
);

CREATE TABLE `offer` (
  `Offer_ID` INT NOT NULL AUTO_INCREMENT,
  `Offer_Type` VARCHAR(100) NOT NULL,
  `Discount_Percentage` DECIMAL(5,2) NOT NULL,
  `Product_Included` VARCHAR(100) NOT NULL,
  `Offer_Start_Date` DATE,
  `Offer_End_Date` DATE,
  PRIMARY KEY (`Offer_ID`)
);

CREATE TABLE `storedetails` (
  `Branch_ID` INT NOT NULL AUTO_INCREMENT,
  `Store_Branch` VARCHAR(30) DEFAULT NULL,
  `Address` VARCHAR(50) DEFAULT NULL,
  `Contact` VARCHAR(15) DEFAULT NULL,
  `Manager_ID` INT DEFAULT NULL,
  PRIMARY KEY (`Branch_ID`)
);

CREATE TABLE `feedback` (
  `Feedback_ID` INT NOT NULL AUTO_INCREMENT,
  `Order_ID` INT DEFAULT NULL,
  `Rating` INT DEFAULT NULL,
  `Date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Feedback_ID`)
);

CREATE TABLE `warranty` (
  `Warranty_ID` INT NOT NULL AUTO_INCREMENT,
  `Purchase_ID` INT NOT NULL,
  `Product_ID` INT NOT NULL,
  `Warranty_Start_Date` DATE NOT NULL,
  `Warranty_End_Date` DATE NOT NULL,
  `Warranty_Terms` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`Warranty_ID`),
  FOREIGN KEY (`Purchase_ID`) REFERENCES `purchase`(`purchase_id`),
  FOREIGN KEY (`Product_ID`) REFERENCES `product`(`Prod_ID`)
);