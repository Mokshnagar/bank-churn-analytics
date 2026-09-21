-- How does churn behavior change when we dynamically slice customers by business parameters?
DECLARE @MinTenure INT = 9;
DECLARE @MaxBalance DECIMAL = 120000;
DECLARE @MaxProduct INT = 6

SELECT
	A.[CustomerId],
	A.[Tenure],
	A.[Balance],
	A.[NumProducts],
	D.[Churned]
FROM [dbo].[account] A
JOIN [dbo].[demographic] D ON D.[CustomerId] = A.[CustomerId]
WHERE
	[Tenure] > @MinTenure
	AND [Balance] < @MaxBalance
	AND [NumProducts] < @MaxProduct
