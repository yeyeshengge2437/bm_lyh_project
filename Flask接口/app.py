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
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/img_to_text', methods=['POST'])
def upload():
    # 检查是否有文件被上传
    if 'file' not in request.files:
        return jsonify({'error': '请求中没有文件部分'}), 400

    file = request.files['file']
    print(file)

    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分，不进行处理
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    # 检查MIME类型
    if file.content_type not in ALLOWED_MIME_TYPES:
        return jsonify({'error': '不允许文件类型'}), 400

    # 检查文件扩展名
    if not allowed_file(file.filename):
        return jsonify({'error': '不允许使用文件扩展名'}), 400

    # 进一步验证文件是否为图片
    filename = secure_filename(file.filename)
    # 如果没有uploads文件夹，则创建
    if not os.path.exists('/uploads'):
        os.makedirs('/uploads')
    file_path = os.path.join('/uploads', filename)

    try:
        # 尝试打开图片
        with Image.open(file.stream) as img:
            img.verify()
    except (IOError, SyntaxError):
        return jsonify({'error': '文件不是图像'}), 400

    identify_results = quark_text(file_path)
    return jsonify({'message': identify_results}), 200


if __name__ == '__main__':
    app.run(debug=True)
