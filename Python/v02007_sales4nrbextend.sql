DROP VIEW IF EXISTS v02007_sales4nrbextend;
CREATE VIEW v02007_sales4nrbextend
AS
    SELECT 
	a.*,
	b.Id TemplateId,
    b.TemplateUuid,
    b.TemplateName,
    b.CargoApproval,
    b.FinanceApproval
    FROM joinfsc_sales.sales a
    JOIN joinfsc_sales.sales4nrbextend b 
    ON a.Id = b.Mid;