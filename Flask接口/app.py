from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import os
from quark_text import quark_text

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Hello, World!"


@app.route('/inner-api/paper-deal/quark/table-start', methods=['POST'])
def quark_table_start():
    pass


@app.route('/inner-api/paper-deal/tell-queue/next', methods=['POST'])
def tell_queue_next():
    # 获取post请求的json数据
    data = request.get_json()
    # 判断传入的工具列表
    id = data.get('id')
    name = data.get('name')
    paper_id = data.get('paper_id')
    tell_type = data.get('tell_type')
    tell_tool = data.get('tell_tool')
    files = data.get('files')
    input_text = data.get('input_text')
    input_key = data.get('input_key')
    pass



if __name__ == '__main__':
    # 开启调试调试模式（开发阶段）
    # app.run(debug=True)
    # 更改端口信息，让所有主机都可访问
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
