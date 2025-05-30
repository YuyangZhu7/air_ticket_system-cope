from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from db_utils import get_flights, get_routes, update_flight, save_routes

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

PASSWORD_FILE = "passwords.json"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['password']
        with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
            passwords = json.load(f)
        if name in passwords[role] and passwords[role][name] == pwd:
            session['user'] = name
            session['role'] = role
            return redirect(url_for(f'{role}_dashboard'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html', role=role)

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/admin/edit_flights', methods=['GET', 'POST'])
def edit_flights():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            count = int(request.form.get('count', 0))
            for i in range(1, count + 1):
                fid = request.form.get(f'fid_{i}', '').strip()
                model = request.form.get(f'model_{i}', '').strip()
                departure = request.form.get(f'departure_{i}', '').strip()
                booked = request.form.get(f'booked_{i}', '0').strip()
                available = request.form.get(f'available_{i}', '0').strip()

                # 忽略空航班号的行
                if not fid:
                    continue

                # 尝试将数字字段转换为整数
                try:
                    booked = int(booked)
                    available = int(available)
                except ValueError:
                    flash(f"第{i}行座位数格式错误，跳过")
                    continue

                # 更新或新增航班
                update_flight(fid, {
                    'model': model,
                    'departure': departure,
                    'booked': booked,
                    'available': available
                })

            flash('航班信息已成功保存')

        except Exception as e:
            import traceback
            traceback.print_exc()
            flash(f"保存失败：{e}")

    # 加载最新航班数据
    flights = get_flights()
    return render_template('edit_flights.html', flights=flights)




@app.route('/edit_operators', methods=['GET', 'POST'])
def edit_operators():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
        passwords = json.load(f)

    if request.method == 'POST':
        try:
            new_ops = {}
            usernames = request.form.getlist('username')
            passwords_list = request.form.getlist('password')
            for uname, pwd in zip(usernames, passwords_list):
                if uname.strip():
                    new_ops[uname.strip()] = pwd.strip()
            passwords['operator'] = new_ops
            with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
                json.dump(passwords, f, ensure_ascii=False)
            flash('操作员信息已更新')
        except Exception as e:
            flash(f"保存失败: {e}")

    return render_template('edit_operators.html', operators=passwords.get('operator', {}))


@app.route('/operator')
def operator_dashboard():
    if session.get('role') != 'operator':
        return redirect(url_for('index'))
    return render_template('operator.html')

@app.route('/operator/view_flights')
def view_flights():
    flights = get_flights()
    return render_template('view_flights.html', flights=flights)

@app.route('/operator/book_ticket', methods=['GET', 'POST'])
def book_ticket():
    from db_utils import get_flights, get_routes, update_flight, save_routes
    if request.method == 'POST':
        name = request.form['name']
        pid = request.form['pid']
        fid = request.form['fid']

        flights = get_flights()
        routes = get_routes()

        if fid not in flights:
            flash('航班号不存在')
            return redirect(url_for('book_ticket'))

        flight = flights[fid]
        if flight['available'] <= 0:
            flash('该航班已满，无法订票')
            return redirect(url_for('book_ticket'))

        if fid not in routes:
            routes[fid] = []

        used_seats = set(int(r['seat']) for r in routes[fid] if r.get('status') != '退票')
        seat_num = 1
        while seat_num in used_seats:
            seat_num += 1

        routes[fid].append({"name": name, "id": pid, "seat": str(seat_num), "status": "预订"})
        flight['booked'] += 1
        flight['available'] -= 1

        update_flight(fid, flight)
        save_routes(routes)

        flash(f"订票成功，座位号为 {seat_num}")
        return redirect(url_for('operator_dashboard'))

    return render_template('book_ticket.html')

@app.route('/operator/cancel_ticket', methods=['GET', 'POST'])
def cancel_ticket():
    from db_utils import get_flights, get_routes, update_flight, save_routes
    if request.method == 'POST':
        name = request.form['name']
        fid = request.form['fid']

        flights = get_flights()
        routes = get_routes()

        if fid not in routes:
            flash('航班号不存在或无客户信息')
            return redirect(url_for('cancel_ticket'))

        found = False
        for r in routes[fid]:
            if r['name'] == name and r.get('status') != '退票':
                r['status'] = '退票'
                r['seat'] = r.get('seat', '')
                found = True
                break

        if not found:
            flash('未找到该客户或该客户已退票')
            return redirect(url_for('cancel_ticket'))

        flights[fid]['booked'] -= 1
        flights[fid]['available'] += 1

        update_flight(fid, flights[fid])
        save_routes(routes)

        flash('退票成功')
        return redirect(url_for('operator_dashboard'))

    return render_template('cancel_ticket.html')

@app.route('/operator/all_info')
def all_info():
    flights = get_flights()
    routes = get_routes()
    return render_template('all_info.html', flights=flights, routes=routes)

if __name__ == '__main__':
    app.run(debug=True)
