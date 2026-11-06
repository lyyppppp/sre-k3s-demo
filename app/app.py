import os
import pymysql
from flask import Flask, jsonify, Response

DB_HOST = os.environ.get("DB_HOST", "mysql")
DB_USER = os.environ.get("DB_USER", "app")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "app123")

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>SRE Demo</title>
<style>body{font-family:sans-serif;max-width:600px;margin:60px auto;text-align:center}</style></head>
<body>
<h1>项目二：k3s 应用 v1</h1>
<p>数据库状态：<b id="db">加载中...</b></p>
<p>MySQL 版本：<b id="ver">-</b></p>
<p>你是第 <b id="cnt">-</b> 位访客</p>
<script>
fetch('/api/status').then(r=>r.json()).then(d=>{
  document.getElementById('db').textContent = d.db === 'connected' ? '已连接' : '错误: ' + d.error;
  document.getElementById('ver').textContent = d.mysql_version || '-';
  document.getElementById('cnt').textContent = d.visitors || '-';
});
</script>
</body></html>
"""

def get_conn():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                           database="sre_demo")

@app.route("/")
def index():
    return Response(INDEX_HTML, mimetype="text/html")

@app.route("/api/status")
def status():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()[0]
            cur.execute("""CREATE TABLE IF NOT EXISTS visitors(
                id INT AUTO_INCREMENT PRIMARY KEY,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            cur.execute("INSERT INTO visitors() VALUES()")
            cur.execute("SELECT COUNT(*) FROM visitors")
            count = cur.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify(db="connected", mysql_version=version, visitors=count)
    except Exception as e:
        return jsonify(db="error", error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
