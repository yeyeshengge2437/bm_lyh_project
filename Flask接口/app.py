from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import os
from quark_text import quark_text

app = Flask(__name__)

# 允许的图片MIME类型
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif'}

# 允许的图片扩展名
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return "Hello, World!"


@app.route('/img_to_text', methods=['POST'])
def upload():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'error': '请求中没有文件部分'}), 400

    file = request.files['file']
    file_name = secure_filename(file.filename)

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，不进行处理
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    # 检查MIME类型
    if file.content_type not in ALLOWED_MIME_TYPES:
        return jsonify({'error': '不允许文件类型'}), 400

    # 检查文件扩展名
    if not allowed_file(file.filename):
        return jsonify({'error': '不允许使用文件扩展名'}), 400
    # 保存文件到本地uploads文件夹
    file.save(file_name)
    try:
        identify_results = quark_text(file_name)
    except:
        return jsonify({'error': '识别失败'}), 400
    os.remove(file_name)  # 删除临时文件
    return jsonify({'message': identify_results}), 200


if __name__ == '__main__':
    # 开启调试调试模式（开发阶段）
    # app.run(debug=True)
    # 更改端口信息，让所有主机都可访问
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
