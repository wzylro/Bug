import json
import subprocess

from flask import Flask, render_template, jsonify
import pymysql
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
# Database connection configuration
def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stats_db",
        charset="utf8mb4"
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to return rows as dictionaries

    # Query to fetch data from the stock_data table
    cursor.execute("""
        SELECT 
            stock_code AS code, 
            stock_name AS name, 
            latest_price AS latestPrice, 
            price_change AS priceChange, 
            price_change_percent AS changePercent, 
            volume, 
            turnover, 
            amplitude, 
            high, 
            low, 
            open_price AS openPrice, 
            close_price AS closePrice, 
            volume_ratio AS volumeRatio, 
            turnover_rate AS turnoverRate, 
            dynamic_pe_ratio AS peRatio, 
            pb_ratio AS pbRatio 
        FROM stock_data
    """)
    stocks = cursor.fetchall()

    # Close database connection
    cursor.close()
    connection.close()

    # Return the result as JSON
    return jsonify(stocks)


@app.route('/api/crawl', methods=['POST'])
def crawl():
    try:
        # 运行 2.1.py, 2.2.py, 和 dataDB.py 脚本
        subprocess.run(['python', '2.1.py'], check=True)
        subprocess.run(['python', '2.2.py'], check=True)
        subprocess.run(['python', 'dataDB.py'], check=True)

        # 读取最终的结果并返回响应
        with open('top_10_stocks.json', 'r', encoding='utf-8') as file:
            result_data = json.load(file)

        return jsonify({
            "status": "success",
            "message": "Crawling and data processing completed successfully.",
            "data": result_data
        })

    except subprocess.CalledProcessError as e:
        # 处理子进程错误
        return jsonify({
            "status": "error",
            "message": f"An error occurred while running the scripts: {e}",
        })

    except Exception as e:
        # 处理其他错误
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {e}",
        })
    return jsonify({"status": "success", "message": "Crawling executed."})

if __name__ == "__main__":
    app.run(debug=True)
