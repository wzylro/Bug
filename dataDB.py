import pymysql
import json

# 加载 JSON 文件
with open('top_10_stocks.json', 'r', encoding='utf-8') as file:
    raw_data = json.load(file)

# 获取股票数据
stocks = raw_data["data"]["diff"]

# 数据库连接

try:
    # 尝试连接数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stats_db",
        charset="utf8mb4"
    )
    print("数据库连接成功！")
except Exception as e:
    print(f"连接数据库失败: {e}")

if connection.open:
    print("Connection is open.")
else:
    print("Connection failed.")

# 插入数据
cursor = connection.cursor()

# SQL 插入语句
sql = """
INSERT INTO stock_data (
    stock_code, stock_name, latest_price, price_change, price_change_percent, 
    volume, turnover, amplitude, high, low, open_price, close_price, 
    volume_ratio, turnover_rate, dynamic_pe_ratio, pb_ratio
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# 遍历股票数据并插入数据库
for stock in stocks:
    cursor.execute(sql, (
        stock['f12'],  # 股票代码
        stock['f14'],  # 股票名称
        stock['f2'],   # 最新价
        stock['f7'],   # 涨跌额
        stock['f8'],   # 涨跌幅
        stock['f5'],   # 成交量(手)
        stock['f6'],   # 成交额
        stock['f9'],   # 振幅
        stock['f16'],  # 最高
        stock['f17'],  # 最低
        stock['f18'],  # 今开
        stock['f15'],  # 昨收
        stock['f10'],  # 量比
        stock['f23'],  # 换手率
        stock['f24'],  # 市盈率(动态)
        stock['f25']   # 市净率
    ))

# 提交更改
connection.commit()

# 关闭连接
cursor.close()
connection.close()

print("数据已成功插入数据库！")
