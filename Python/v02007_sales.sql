DROP VIEW IF EXISTS v02007_sales;
CREATE VIEW v02007_sales
AS
    SELECT 
	a.*
    FROM joinfsc_sales.sales a;