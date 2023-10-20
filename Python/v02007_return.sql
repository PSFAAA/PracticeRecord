DROP VIEW IF EXISTS v02007_return;
CREATE VIEW v02007_return
AS
    SELECT 
	a.*
    FROM joinfsc_sales.return a;