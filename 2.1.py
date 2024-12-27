import requests
import re
import json
import pandas as pd
import matplotlib.pyplot as plt

# 定义请求头，模拟浏览器访问
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "qgqp_b_id=7a4905023cbf4aa0231b7e81058ce6c4; st_si=81258989878087; st_asi=delete; st_pvi=76995703392395; st_sp=2024-12-25%2011%3A37%3A01; st_inirUrl=; st_sn=4; st_psi=20241225114542696-113200301321-6514246244",
    "Host": "5.push2.eastmoney.com",
    "Referer": "https://quote.eastmoney.com/center/gridlist.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

# 定义爬取数据的 URL
url = "https://5.push2.eastmoney.com/api/qt/clist/get"
params = {
    "cb": "jQuery1124020671735158521964_1735098352235",
    "pn": 1,
    "pz": 20,
    "po": 1,
    "np": 1,
    "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    "fltt": 2,
    "invt": 2,
    "dect": 1,
    "wbp2u": "|0|0|0|web",
    "fid": "f3",
    "fs": "m:1+t:2,m:1+t:23",
    "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
    "_": "1735098352236"
}

# 发送 GET 请求获取数据
response = requests.get(url, headers=headers, params=params)

# 打印响应的原始内容
print(response.text)

# 处理 JSONP 数据，去掉回调函数部分
jsonp_data = response.text
match = re.search(r'^\w+\((.*)\);$', jsonp_data)  # 匹配回调函数并提取其中的 JSON 数据
if match:
    json_data = match.group(1)  # 提取 JSON 部分
    data = json.loads(json_data)  # 解析 JSON 数据
    stocks = data['data']['diff']
else:
    print("没有找到有效的 JSON 数据")

# 将数据存入 DataFrame
df = pd.DataFrame(stocks, columns=[
    "股票代码", "当前价格", "涨幅", "振幅", "成交量", "成交额", "买入", "卖出", "最高", "最低",
    "昨收", "股票名称", "市盈率", "市净率", "总市值", "流通市值", "成交额(亿)", "涨停", "跌停", "换手率"
])

# 处理数值列：去除非数值字符并转换为数值类型
df['涨幅'] = pd.to_numeric(df['涨幅'], errors='coerce')
df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
df['当前价格'] = pd.to_numeric(df['当前价格'], errors='coerce')

# 过滤出有效数据（移除存在NaN的行）
df = df.dropna(subset=['涨幅', '成交量', '当前价格'])

# 按涨幅排序，选择前10名
df_top10 = df.sort_values(by='涨幅', ascending=False).head(10)

# 将结果保存为 JSON 文件
output_file = "top_10_stocks.json"
df_top10_json = df_top10.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries

try:
    with open('top_10_stocks.json', 'w') as f:
        json.dump(data, f)
except Exception as e:
    print(f"Error occurred: {e}")


print(f"前10名数据已保存为 {output_file}")

