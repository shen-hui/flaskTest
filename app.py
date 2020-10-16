# coding:utf-8
from flask import *
from face_age_demo import *
from face_detect_demo import *

from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
app.send_file_max_age_default = timedelta(seconds=1)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        return upload_path

@app.route('/age', methods=['POST', 'GET'])
def age():
    if request.method == 'POST':
        upload_path = upload()
        return render_template('ageResult.html', userinput=testAge(upload_path), val1=time.time())
    return render_template('age.html')

@app.route('/face', methods=['POST', 'GET'])
def face():
    if request.method == 'POST':
        upload_path = upload()
        testFace(upload_path)
        return render_template('faceResult.html', userinput=testFace(upload_path), val1=time.time())
    return render_template('face.html')

@app.route('/')
def home():
    scores_list = [21, 34, 32, 67, 89, 43, 22, 13]

    content_h2 = testAge("asserts/test_07.png")
    content_h3 = '   <h3>今天你们真帅</h3>   '

    return render_template('home.html',
                           scores=scores_list,
                           content_h2=content_h2,
                           content_h3=content_h3)
    # testAge("asserts/test_08.png")
    # print(testAge("asserts/test_08.png"))
    # return render_template('home.html')


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5000)