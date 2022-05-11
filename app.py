from flask import Flask, request, Response, render_template, jsonify, make_response, send_from_directory, copy_current_request_context,redirect,url_for
from werkzeug.utils import secure_filename
import uuid, datetime, threading
from strUtil import Pic_str
from face import detect_faces
from cheat_detect import cheat_detect_fuc
from opt import *
from deepface import DeepFace

app = Flask(__name__)  # 实例Flask应用
# 设置图片保存文件夹
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.after_request(after_request)

# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS

# 首页
@app.route('/')
def hello_world():
    return render_template('upload.html')

# 心跳检测
@app.route("/check", methods=["GET"])
def check():
    return 'Im live'

# 上传图片
@app.route("/upload_image", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        # 获取文件
        file = request.files['file']
        # 检测文件格式
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
            file_name_hz = secure_filename(file.filename).split('.')[-1]
            # 使用uuid生成唯一图片名
            first_name = str(uuid.uuid4())
            # 将 uuid和后缀拼接为 完整的文件名
            file_name = first_name + '.' + file_name_hz
            # 保存原图
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            # 返回原本和缩略图的 完整浏览链接
            return {"code": '200', "image_url": image_url + file_name, "message": "上传成功"}
        else:
            return "格式错误，仅支持jpg、png、jpeg格式文件"
    return {"code": '503', "data": "", "message": "仅支持post方法"}

# 网页上传图片
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        print(os.path.join(file_dir, new_filename))
        return jsonify({"success": 200, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})

# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

# 图片获取地址 用于存放静态文件
@app.route("/image/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    try:
        with open(r'./static/image/{}'.format(imageId), 'rb') as f:
            image = f.read()
            result = Response(image, mimetype="image/jpg")
            return result
    except BaseException as e:
        return {"code": '503', "data": str(e), "message": "图片不存在"}

@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
            return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        pass

# 人脸检测
@app.route("/face_detect", methods=['POST', "GET"])
def face_detect():

    # 使用uuid生成唯一图片名
    first_name = str(uuid.uuid4())

    @copy_current_request_context
    def save_file(closeAfterWrite):

        # 这段代码是将上传的文件写入到我们的文件存储，确保文件存在
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " i am doing")
        f = request.files['file']
        # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
        file_name_hz = secure_filename(f.filename).split('.')[-1]
        # 将 uuid和后缀拼接为 完整的文件名
        file_name = first_name + '.' + file_name_hz
        # 保存原图
        f.save(os.path.join(UPLOAD_FOLDER, file_name))
        closeAfterWrite()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " write done")

        detect_faces(file_name, first_name, file_name_hz)

    def passExit():
        pass

    if request.method == 'POST':

        f = request.files['file']

        if f and allowed_file(f.filename):
            # 创建一个新的线程，用于保存文件
            normalExit = f.stream.close
            f.stream.close = passExit
            t = threading.Thread(target=save_file, args=(normalExit,))
            t.start()

            file_name_hz = secure_filename(f.filename).split('.')[-1]
            return {"code": '200', "image_url_detect": image_url + first_name + '_detect.jpg',
                    "image_url": image_url + first_name + '.' + file_name_hz}

            # return redirect(url_for('face_detect'))
        else:
            return "格式错误，仅支持jpg、png、jpeg格式文件"
    else:
        return {}

# 人脸对比
@app.route("/face_compare_detect", methods=['POST', "GET"])
def face_compare_detect():

    # 使用uuid生成唯一图片名
    first_name = str(uuid.uuid4())

    @copy_current_request_context
    def save_file(closeAfterWrite):

        # 这段代码是将上传的文件写入到我们的文件存储，确保文件存在
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " i am doing")
        # f = request.files['file']
        img1 = request.files['img1_path']
        img2 = request.files['img2_path']
        # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
        file_name_hz1 = secure_filename(img1.filename).split('.')[-1]
        file_name_hz2 = secure_filename(img2.filename).split('.')[-1]
        # 将 uuid和后缀拼接为 完整的文件名
        img1_name = first_name + '.' + file_name_hz1
        img2_name = first_name + '.' + file_name_hz2
        # 保存原图
        img1.save(os.path.join(UPLOAD_FOLDER, img1_name))
        img2.save(os.path.join(UPLOAD_FOLDER, img2_name))
        closeAfterWrite()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " write done")

        result = DeepFace.verify(img1_path = os.path.join(UPLOAD_FOLDER, img1_name), img2_path = os.path.join(UPLOAD_FOLDER, img2_name), model_name="Facenet")
        print(result)

        # 保存结果
        with open(os.path.join(RESULT_FOLDER, first_name + '_result.txt'), 'w') as f:
            f.write(str(result))

    def passExit():
        pass

    if request.method == 'POST':

        img1 = request.files['img1_path']
        img2 = request.files['img2_path']

        if img1 and img2 and allowed_file(img1.filename):
            # 创建一个新的线程，用于保存文件
            normalExit = img1.stream.close
            img1.stream.close = passExit
            img2.stream.close = passExit
            t = threading.Thread(target=save_file, args=(normalExit,))
            t.start()

            return {"code": '200', "result": os.path.join(RESULT_FOLDER, first_name + '_result.txt')}

        else:
            return "格式错误，仅支持jpg、png、jpeg格式文件"
    else:
        return {}

# 作弊检测
@app.route("/cheat_detect", methods=['POST', "GET"])
def cheat_detect():

    # 使用uuid生成唯一图片名
    first_name = str(uuid.uuid4())

    @copy_current_request_context
    def save_file(closeAfterWrite):

        # 这段代码是将上传的文件写入到我们的文件存储，确保文件存在
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " i am doing")
        f = request.files['file']
        # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
        file_name_hz = secure_filename(f.filename).split('.')[-1]
        # 将 uuid和后缀拼接为 完整的文件名
        file_name = first_name + '.' + file_name_hz
        # 保存原图
        f.save(os.path.join(UPLOAD_FOLDER, file_name))
        closeAfterWrite()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " write done")

        result = cheat_detect_fuc(os.path.join(UPLOAD_FOLDER, file_name), first_name)
        print(result)
        with open(os.path.join(RESULT_FOLDER, first_name + '_result.txt'), 'w') as f:
            f.write(str(result))

    def passExit():
        pass

    if request.method == 'POST':

        f = request.files['file']

        if f and allowed_file(f.filename):
            # 创建一个新的线程，用于保存文件
            normalExit = f.stream.close
            f.stream.close = passExit
            t = threading.Thread(target=save_file, args=(normalExit,))
            t.start()
            return {"code": '200', "result": os.path.join(RESULT_FOLDER, first_name + '_result.txt'), 'image_url':"static/image/{}.jpg".format(first_name)}
        else:
            return "格式错误，仅支持jpg、png、jpeg格式文件"
    else:
        return {}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)  # 项目入口