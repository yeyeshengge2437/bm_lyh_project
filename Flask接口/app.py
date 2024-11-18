from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {'pdf'}

# 确保你的上传文件夹存在
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 检查文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': '欢迎使用Flask PDF上传接口'}), 200


# 路由装饰器用于告诉Flask哪个URL应该触发我们的函数
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'message': '请求中没有文件部分'}), 400
    file = request.files['file']
    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分
    if file.filename == '':
        return jsonify({'message': '未选择要上传的文件'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # 将pdf转化为图片

        return jsonify({'message': '文件上传成功'}), 201
    else:
        return jsonify({'message': '不允许文件类型'}), 400


# 启动Flask应用程序
if __name__ == '__main__':
    app.run(debug=True)
