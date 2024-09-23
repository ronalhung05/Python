import json
import os
import random
from flask import Flask, request, redirect, url_for, session, render_template

app = Flask(__name__)
app.secret_key = 'secret_key'  # Để mã hóa session

# Bảng giá điện sau tháng 5/2023
electricity_rates = [
    (50, 1.728),
    (50, 1.786),
    (100, 2.074),
    (100, 2.612),
    (100, 2.919),
    (float('inf'), 3.015)  # Bậc 6 cho kWh trên 400
]

# Bảng giá điện trước tháng 5/2023
electricity_rates_before_052023 = [
    (50, 1.678),
    (50, 1.734),
    (100, 2.014),
    (100, 2.536),
    (100, 2.834),
    (float('inf'), 2.927)  # Giá bậc 6 trước tháng 5/2023
]

# Thông tin khách hàng mẫu
customers = {
    'user1': {'password': '1', 'name': 'Nguyen Van A', 'address': '123 ABC St', 'electricity_usage': 350},
    'user2': {'password': '2', 'name': 'Tran Thi B', 'address': '456 XYZ St', 'electricity_usage': 150}
}

# Hàm tính tiền điện
def calculate_electricity_bill(usage, rates):
    bill = 0
    remaining_usage = usage
    for limit, rate in rates:
        if remaining_usage > limit:
            bill += limit * rate
            remaining_usage -= limit
        else:
            bill += remaining_usage * rate
            break
    # Format kết quả với 3 chữ số thập phân
    return f"{bill:.3f}"

# File lưu dữ liệu tiền điện
data_file = 'electricity_data.json'

# Hàm lưu dữ liệu vào file JSON
def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Hàm đọc dữ liệu từ file JSON
def load_data_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

# Sinh ngẫu nhiên số điện tiêu thụ mỗi tháng từ 200 đến 500 kWh
def generate_random_electricity_usage():
    return random.randint(200, 500)

# Sinh dữ liệu tiền điện từ tháng 4/2023 đến tháng 8/2024
def generate_electricity_data():
    data = {}
    for year in range(2023, 2025):
        for month in range(1, 13):
            if year == 2023 and month < 4:
                continue
            if year == 2024 and month > 8:
                break

            # Chọn bảng giá dựa trên tháng
            if year == 2023 and month < 5:
                rates = electricity_rates_before_052023
            else:
                rates = electricity_rates

            # Sinh ngẫu nhiên số điện tiêu thụ
            usage_user1 = generate_random_electricity_usage()
            usage_user2 = generate_random_electricity_usage()

            # Tính tiền điện cho mỗi user
            bill_user1 = calculate_electricity_bill(usage_user1, rates)
            bill_user2 = calculate_electricity_bill(usage_user2, rates)

            # Lưu dữ liệu cho tháng đó
            data[f"{year}-{month:02d}"] = {
                'user1': {
                    'usage': usage_user1,
                    'bill': bill_user1
                },
                'user2': {
                    'usage': usage_user2,
                    'bill': bill_user2
                }
            }
    return data

# Khởi tạo hoặc đọc dữ liệu từ file
electricity_data = load_data_from_file(data_file)
if electricity_data is None:
    electricity_data = generate_electricity_data()
    save_data_to_file(electricity_data, data_file)

# Trang đăng nhập
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in customers and customers[username]['password'] == password:
            session['username'] = username  # Lưu username vào session
            return redirect(url_for('electricity'))
        else:
            return render_template('login.html', error='Invalid credentials!')
    return render_template('login.html')

# Trang tính tiền điện
@app.route('/electricity')
def electricity():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    customer_info = customers[username]
    usage = customer_info['electricity_usage']
    rates = electricity_rates if usage > 50 else electricity_rates_before_052023
    bill = calculate_electricity_bill(usage, rates)
    return render_template('electricity.html', name=customer_info['name'], usage=usage, bill=bill)

# Trang lịch sử tiền điện
@app.route('/history')
def electricity_history():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    history = {month: data[username] for month, data in electricity_data.items()}
    return render_template('history.html', history=history)

# Trang thông tin khách hàng
@app.route('/customer')
def customer():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    customer_info = customers[username]
    return render_template('customer.html', customer=customer_info)

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
