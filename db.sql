CREATE TABLE stock_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(20),
    stock_name VARCHAR(100),
    latest_price FLOAT,
    price_change FLOAT,
    price_change_percent FLOAT,
    volume INT,
    turnover FLOAT,
    amplitude FLOAT,
    high FLOAT,
    low FLOAT,
    open_price FLOAT,
    close_price FLOAT,
    volume_ratio FLOAT,
    turnover_rate FLOAT,
    dynamic_pe_ratio FLOAT,
    pb_ratio FLOAT
);
