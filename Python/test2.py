from datetime import datetime, timedelta

date_obj = datetime.strptime('2022-12-30', '%Y-%m-%d')

week_start_date = date_obj - timedelta(days=date_obj.weekday())

week_end_date = week_start_date + timedelta(days=6)

month_start_date = datetime(week_end_date.year, week_end_date.month, 1)

quarter_start_month = ((week_end_date.month - 1) // 3) * 3 + 1
quarter_start_date = datetime(week_end_date.year, quarter_start_month, 1)

year_start_date = datetime(week_end_date.year, 1, 1)

print("本周第一天：", week_start_date.date())
print("本周最后一天：", week_end_date.date())
print("该月的第一天：", month_start_date.date())
print("该季度的第一天：", quarter_start_date.date())
print("该年的第一天：", year_start_date.date())