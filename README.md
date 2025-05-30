
# ✈️ 航空订票管理系统（Air Ticket Booking System）

本项目是一个基于 **Flask** 框架与 **SQLite** 数据库的网页端航空订票管理系统，支持航班信息管理、旅客订票、退票处理和信息可视化展示，适合作为信息系统开发的课程设计或中小型项目部署。

---

## 🔧 核心功能（Features）

- **航班信息管理（Flight Management）**：可对航班编号、机型、目的地、出发时间、余票等信息进行添加、修改与展示。
- **订票与退票系统（Booking & Cancellation）**：支持通过航班号和身份证进行订票，重复票自动检测；退票操作保留历史记录并标记为作废。
- **角色权限控制（Role-based Access）**：
  - 管理员（Admin）：维护航班与操作员信息。
  - 操作员（Operator）：负责订票、退票、查看数据。
- **信息总览与可视化（Information Overview）**：以表格形式展示航班与票务信息，已退票使用删除线标记。
- **数据持久化（Data Persistence）**：使用内置的 **SQLite** 本地数据库，无需服务器支持。
- **登录认证（User Login）**：基于 JSON 储存的用户凭证，支持权限区分。

---

## 🗂 项目结构（Project Structure）

```

air\_ticket\_system-cope/
├── app.py                 # 主程序入口，路由与逻辑
├── db\_utils.py            # 数据库操作封装
├── passwords.json         # 登录账户信息（已加密）
├── templates/             # 页面模板（Jinja2）
│   ├── index.html
│   ├── login.html
│   ├── admin.html
│   ├── operator.html
│   ├── book\_ticket.html
│   ├── cancel\_ticket.html
│   ├── edit\_flights.html
│   ├── edit\_operator.html
│   ├── all\_info.html
│   └── view\_flights.html
├── static/                # 静态资源（CSS、图片等）
└── database.db            # 自动生成的 SQLite 数据库文件

````

---

## 🚀 项目运行说明（How to Run）

> 请确保环境中已安装 **Python 3.8+** 与 **Flask**

### 1. 克隆项目（Clone the Repository）

```bash
git clone https://github.com/YuyangZhu7/air_ticket_system-cope.git
cd air_ticket_system-cope
````

### 2. 可选：创建虚拟环境（Recommended）

```bash
python -m venv venv
.\venv\Scripts\activate    # Windows
```

### 3. 安装依赖（Install Dependencies）

```bash
pip install flask
```

### 4. 运行项目（Run the App）

```bash
python app.py
```

浏览器访问地址：

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 👥 默认账户信息（Default Accounts）

> 账号信息存储在 `passwords.json` 中（可自行修改）

| 角色（Role）     | 用户名（Username） | 密码（Password） |
| ------------ | ------------- | ------------ |
| 管理员 Admin    | `admin`       | `admin`      |
| 操作员 Operator | `operator`    | `operator`   |

> ⚠️ 注意：正式部署前请修改默认密码以保障系统安全

---

## 📌 使用说明备注（Usage Notes）

* 首次运行时系统会自动生成数据库及默认账户。
* 所有订票记录默认按航班号排序，退票记录保留并使用删除线标记。
* 可视化页面使用 **Jinja2** 模板渲染，兼容现代浏览器。
* 所有信息编辑操作具备输入验证和基础错误提示。

---

## 📄 许可声明（License）

本项目仅用于学习和教学目的，不得用于商业用途。
This project is for academic and non-commercial use only.




