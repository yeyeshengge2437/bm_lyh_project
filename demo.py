from datetime import datetime, timedelta

# 获取当前时间
now = datetime.now()

# 设置起始年份和月份
start_year = now.year - 2
start_month = now.month
current_date = datetime(start_year, start_month, 1)

# 当前日期
formatted_date = current_date.strftime('%Y-%m/%d')

# 打印起始日期
print("起始日期:", formatted_date)

# 遍历近两年的日期
while current_date <= now:
    # 计算下一天的日期
    current_date += timedelta(days=1)
    # 更新格式化的日期
    formatted_date = current_date.strftime('%Y-%m/%d')
    print(formatted_date)