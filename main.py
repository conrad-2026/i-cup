from flask import Flask, render_template_string, request, jsonify
import json
import os
import subprocess
from datetime import datetime

app = Flask(__name__, static_folder=os.getcwd(), static_url_path='/static')
app.secret_key = 'icup'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>i-cup - Windows远程系统安装</title>
    <style>
        body {
            font-family: "Microsoft YaHei", Arial, sans-serif;
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
            font-size: 16px;
            line-height: 1.6;
        }
        h1 {
            font-size: 28px;
            text-align: center;
        }
        .menu {
            background-color: #0078d7;
            color: white;
            padding: 20px;
            font-size: 20px;
            cursor: pointer;
            margin-bottom: 30px;
            border-radius: 5px;
            text-align: center;
        }
        .verify-area {
            text-align: center;
            margin: 30px 0;
        }
        .qrcode-img {
            max-width: 350px;
            border: 1px solid #eee;
            padding: 10px;
            margin: 10px 0;
        }
        .verify-form {
            margin: 30px 0;
            font-size: 18px;
        }
        .verify-form input {
            padding: 12px;
            width: 250px;
            font-size: 16px;
        }
        .verify-form button {
            padding: 12px 20px;
            background-color: #0078d7;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }
        .install-guide {
            border: 2px solid #4CAF50;
            padding: 25px;
            margin-top: 30px;
            font-size: 18px;
            border-radius: 5px;
            background-color: #f0f8f0;
            text-align: left;
            display: none; /* 默认隐藏，验证成功后显示 */
        }
        .install-guide.show {
            display: block !important; /* 强制显示 */
        }
        .install-guide ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .install-guide li {
            margin: 12px 0;
            line-height: 1.8;
        }
        .error {
            color: #dc3545;
            margin: 15px 0;
            font-size: 18px;
            font-weight: bold;
        }
        .msg {
            text-align: center;
            font-size: 18px;
            margin: 20px 0;
            color: #28a745;
            font-weight: bold;
        }
        .run-btn {
            padding: 15px 30px;
            font-size: 18px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 10px;
        }
        .hidden {
            display: none;
        }
        #main-section {
            display: none;
        }
    </style>
</head>
<body>
    <h1>i-cup 远程系统安装服务</h1>
    <div class="menu" onclick="document.getElementById('main-section').style.display='block'">
        windows远程系统安装
    </div>

    <div id="main-section">
        <!-- 验证码+二维码区域 -->
        <div id="verify-area" class="verify-area">
            <h3>支付宝收款码（40元）</h3>
            <img src="/static/alipay.png" alt="支付宝收款码" class="qrcode-img">
            <p>缴费成功后，请联系客服：17713654484 索要验证码</p>

            <div class="verify-form">
                <input type="text" id="code-input" placeholder="输入验证码" required>
                <button onclick="verifyCode()" type="button">验证</button>
                <div id="error-msg" class="error"></div>
            </div>
        </div>

        <!-- 安装说明区域（核心：始终保留） -->
        <div id="install-guide" class="install-guide">
            <h3>安装操作说明</h3>
            <ul>
                <li><strong>给本机安装系统：</strong>拔掉本机所有U盘，点击下方「开始安装」按钮后，关闭弹出的小窗口，稍等片刻选择「重装系统」模式；</li>
                <li><strong>给其他电脑安装：</strong>给本机插入准备好的U盘，点击下方「开始安装」按钮后，在弹出的小窗口点击 [浏览]，选择U盘后点击 [选择文件夹]、然后点击 [确定]，在工具中选择「U盘启动」模式，点击 [制作启动U盘], 点击 [确定]，勾选系统版本后，选择 [只制作启动U盘]，完成后，将该U盘拔出、插入要安装系统的电脑，选择U盘启动安装系统；</li>
            </ul>
            <div style="margin-top: 20px; text-align:center;">
                <button class="run-btn" onclick="runInstall()" type="button">开始安装</button>
                <div id="run-msg" class="msg"></div>
            </div>
        </div>
    </div>

    <script>
        // 验证验证码
        function verifyCode() {
            const code = document.getElementById('code-input').value.trim();
            fetch('/verify', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: code})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // 验证成功：隐藏验证码区域，显示安装说明
                    document.getElementById('verify-area').style.display = 'none';
                    document.getElementById('install-guide').classList.add('show');
                    document.getElementById('error-msg').textContent = '';
                } else {
                    // 验证失败：显示错误提示
                    document.getElementById('error-msg').textContent = data.msg;
                }
            });
        }

        // 运行安装程序（无页面跳转）
        function runInstall() {
            fetch('/run', {method: 'POST'})
            .then(res => res.json())
            .then(data => {
                // 仅更新提示信息，安装说明保留
                document.getElementById('run-msg').textContent = data.msg;
            });
        }
    </script>
</body>
</html>
'''

def get_today_key():
    """获取当天对应的code.json键（1-7）"""
    return str(datetime.now().weekday() + 1)

def get_client_id():
    """生成用户电脑唯一标识（日期+IP）"""
    ip = request.remote_addr
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{today}_{ip}"

def init_code_json():
    """初始化验证码配置文件"""
    code_file = "code.json"
    default_data = {
        "1": "mon8888", "2": "tue9999", "3": "wed7777",
        "4": "thu6666", "5": "fri5555", "6": "sat4444",
        "7": "sun3333", "8": 0
    }
    if not os.path.exists(code_file):
        with open(code_file, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
    # 读取并确保键8为数字
    with open(code_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "8" not in data or not isinstance(data["8"], int):
        data["8"] = 0
        with open(code_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return data

def init_count_record():
    """初始化计数记录文件"""
    record_file = "count_record.json"
    if not os.path.exists(record_file):
        with open(record_file, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def update_count():
    """更新计数（同一电脑当天仅+1）"""
    client_id = get_client_id()
    # 加载计数记录
    init_count_record()
    with open("count_record.json", "r", encoding="utf-8") as f:
        record = json.load(f)
    
    if client_id not in record:
        # 计数+1
        code_data = init_code_json()
        code_data["8"] += 1
        with open("code.json", "w", encoding="utf-8") as f:
            json.dump(code_data, f, ensure_ascii=False, indent=2)
        # 标记已计数
        record[client_id] = True
        with open("count_record.json", "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print(f"✅ 计数更新成功，当前键8值：{code_data['8']}")

@app.route("/", methods=["GET"])
def index():
    """首页：仅渲染页面，无状态跳转"""
    init_code_json()
    init_count_record()
    return render_template_string(HTML_TEMPLATE)

@app.route("/verify", methods=["POST"])
def verify_code():
    """验证验证码接口（AJAX）"""
    data = request.get_json()
    user_code = data.get("code", "").strip()
    
    # 获取当天正确验证码
    key = get_today_key()
    code_data = init_code_json()
    right_code = str(code_data.get(key, "")).strip()

    if user_code == right_code:
        update_count()
        return jsonify({"success": True, "msg": "验证成功"})
    else:
        return jsonify({"success": False, "msg": "验证码错误！请联系客服确认正确验证码后重新输入"})

@app.route("/run", methods=["POST"])
def run_install():
    """运行安装程序接口（AJAX）"""
    try:
        # 运行安装程序
        software_path = os.path.join(os.getcwd(), "xbonekey.exe")
        subprocess.Popen(software_path)
        return jsonify({"success": True, "msg": "✅ 安装程序已成功启动，请按照上方说明操作！"})
    except Exception as e:
        return jsonify({"success": False, "msg": f"❌ 安装程序启动失败：{str(e)}（请确认xbonekey.exe在当前文件夹内）"})

if __name__ == "__main__":
    # 检查必要文件
    required_files = ["code.json", "alipay.png"]
    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print(f"❌ 缺少必要文件：{', '.join(missing)}")
    else:
        print("✅ 服务启动成功！访问地址：http://localhost:5000")
        app.run(host="0.0.0.0", port=5000, debug=False)
