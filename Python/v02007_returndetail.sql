DROP VIEW IF EXISTS v02007_returndetail;
CREATE VIEW v02007_returndetail
AS
    SELECT 
	a.Code,
	a.Status MStatus,
	a.Source,
	a.SourceType,
	a.Type,
	a.SalesCode,
	a.CustomerName,
	a.TotalReturnAmount,
	a.ReturnDate,
	a.ExcuterName,
	a.Theme,
	a.Remark,
	a.Uuid,
	a.CrtUuid,
	a.CrtName,
	a.CrtTime,
	a.Version,
	a.BcCode,
	a.TUuid,
	a.ReceiverContacterPhone,
	a.ReceiverName,
	a.CustomerUuid,
	a.ReceiverId,
	a.SettlementStatus,
	a.TotalTaxAmount,
	a.ProcessMethod,
    b.*
    FROM joinfsc_sales.return a
    JOIN joinfsc_sales.returndetail b 
    ON a.Id = b.Mid;