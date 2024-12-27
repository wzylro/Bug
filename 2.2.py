import json
import os

import matplotlib.pyplot as plt
print("matplotlib 导入成功")
from matplotlib import rcParams

# 设置matplotlib使用SimHei字体，避免中文乱码
rcParams['font.family'] = ['SimHei']  # 'SimHei'是黑体字体
rcParams['axes.unicode_minus'] = False  # 防止负号显示为乱码
# 加载 JSON 文件
with open('top_10_stocks.json', 'r', encoding='utf-8') as file:
    raw_data = json.load(file)





# 访问数据示例
total = raw_data["data"]["total"]
stocks = raw_data["data"]["diff"]

# 打印总数
print(f"总股票数: {total}")
print("股票详情:")

# 创建可视化所需的数据
stock_names = []
price_changes = []  # 涨跌幅
volumes = []  # 成交量(手)
turnovers = []  # 成交额

for stock in stocks:
    # 提取并映射字段
    stock_code = stock['f12']  # 股票代码
    stock_name = stock['f14']  # 股票名称
    latest_price = stock['f2']  # 最新价
    price_change_percent = stock['f8']  # 涨跌幅
    price_change = stock['f7']  # 涨跌额
    volume = stock['f5']  # 成交量(手)
    turnover = stock['f6']  # 成交额
    amplitude = stock['f9']  # 振幅
    high = stock['f16']  # 最高
    low = stock['f17']  # 最低
    open_price = stock['f18']  # 今开
    close_price = stock['f15']  # 昨收
    volume_ratio = stock['f10']  # 量比
    turnover_rate = stock['f23']  # 换手率
    dynamic_pe_ratio = stock['f24']  # 市盈率(动态)
    pb_ratio = stock['f25']  # 市净率

    # 输出格式化的股票信息
    print(f"股票代码: {stock_code}")
    print(f"名称: {stock_name}")
    print(f"最新价: {latest_price}")
    print(f"涨跌额: {price_change} ({price_change_percent}%)")
    print(f"成交量: {volume} 手")
    print(f"成交额: {turnover}")
    print(f"振幅: {amplitude}")
    print(f"最高: {high}")
    print(f"最低: {low}")
    print(f"今开: {open_price}")
    print(f"昨收: {close_price}")
    print(f"量比: {volume_ratio}")
    print(f"换手率: {turnover_rate}")
    print(f"市盈率(动态): {dynamic_pe_ratio}")
    print(f"市净率: {pb_ratio}")
    print("-" * 40)  # 分隔符

    # 提取数据用于可视化
    stock_names.append(stock_name)
    price_changes.append(price_change_percent)
    volumes.append(volume)
    turnovers.append(turnover)

# 确定保存路径
save_dir = 'static'
os.makedirs(save_dir, exist_ok=True)  # 确保路径存在

涨跌幅图路径 = os.path.join(save_dir, '涨跌幅柱状图.png')
成交量图路径 = os.path.join(save_dir, '成交量柱状图.png')

# 1. 涨跌幅柱状图
plt.figure(figsize=(15, 18))

# 创建柱状图：涨跌幅
plt.subplot(2, 1, 1)
bars1 = plt.bar(stock_names, price_changes, color='orange')
plt.xlabel('股票名称')
plt.ylabel('涨跌幅 (%)')
plt.title('股票涨跌幅')

# 在柱子上添加数据注释
for bar in bars1:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}%', ha='center', va='bottom')

# 保存涨跌幅图表
plt.tight_layout()
plt.savefig(涨跌幅图路径)  # 保存为PNG文件
plt.close()  # 关闭当前图表，释放资源

# 2. 成交量柱状图
plt.figure(figsize=(10, 6))
bars2 = plt.bar(stock_names, volumes, color='green')
plt.xlabel('股票名称')
plt.ylabel('成交量 (手)')
plt.title('股票成交量')

# 在柱子上添加数据注释
for bar in bars2:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.0f}', ha='center', va='bottom')

# 自动旋转x轴标签
plt.xticks(rotation=45, ha='right')

# 保存成交量图表
plt.tight_layout()
plt.savefig(成交量图路径)  # 保存为PNG文件
plt.close()  # 关闭当前图表，释放资源

# 打印保存路径
print(f"涨跌幅柱状图保存到: {涨跌幅图路径}")
print(f"成交量柱状图保存到: {成交量图路径}")
# 调整图表布局
plt.tight_layout()

# 显示图表
plt.show()
