USE [BankChurn]
GO

--Create Demographic Table
CREATE TABLE demographic (
	CustomerId INT PRIMARY KEY IDENTITY(1,1),
	Gender NVARCHAR(10),
	Age INT,
	Salary DECIMAL(10,2),
	LocationId INT,
	Churned BIT
);

--Create Account Table
CREATE TABLE account (
	CustomerId INT,
	Tenure INT,
	Balance DECIMAL(10,2),
	NumProducts INT,
	HasCreditCard BIT,
	IsActive BIT
);

--Create Location Table
CREATE TABLE [location] (
	LocationId INT PRIMARY KEY IDENTITY (1,1),
	[Geography] NVARCHAR(15)
);
