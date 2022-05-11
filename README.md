# 智能监考系统接口说明文档

## 1. 安装（Install）
    
    mkdir require
    cd require
    wget https://github.com/ultralytics/yolov5/blob/master/requirements.txt
    pip install -r requirements.txt
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
    cd smart_exam   # 项目目录
    pip install -r requirements.txt

## 2. 使用（Usage）

### 2.1 启动：
    conda activate py38
    cd /root/python/project/smart_exam/
    nohup python app.py &
### 2.2 关闭 
    查看端口5000的信息
    netstat -tunlp |grep 5000
    kill -9 123 #123 是进程 PID，此命令可杀掉 PID 为 123 的端口进程

## 3. 接口详情：
### 3.1 BaseUrl = http://124.70.177.168:5000/            
### 3.2 接口人脸检测：BaseUrl/face_detect  form-data {"file": file}  (POST方式)
    返回： 
    {
    "code": "200",
    "image_url": "http://124.70.177.168:5000/image/229dd23f-9662-46f3-a999-12d49a710ede.jpg",     # 原图
    "image_url_detect": "http://124.70.177.168:5000/image/229dd23f-9662-46f3-a999-12d49a710ede_detect.jpg" # 检测结果
    }
### 3.3 接口人脸对比：BaseUrl/face_compare_detect  form-data {"img1_path": file1_path, "img2_path": file2_path}  (POST方式)
    返回：
    {
    'verified': True,  # 是否为同一人
    'distance': 0.0,    # 置信度，越小越好
    'threshold': 0.4,   # 阈值，小于这个值被认为是同一人
    'model': 'Facenet', # 模型，Facenet（谷歌出品）
    'detector_backend': 'opencv', 
    'similarity_metric': 'cosine'
    }
### 3.4 接口作弊检测：BaseUrl/cheat_detect  form-data {"file": file}  (POST方式)
    返回:
    {
    "code": "200",
    "image_url": "static/image/d092340b-154f-4887-9a95-54346679ea26.jpg",  # 作弊证据：需要拼接 BaseUrl + image_url
    "result": "static/d092340b-154f-4887-9a95-54346679ea26_result.txt"     # 检测结果：需要拼接 BaseUrl + result 
    }
    
    result格式：
    {
    'count_person': 1,  # 该图像检测到的人数
    'has_phone': 0,      # 该图像检测到的手机数
    'result_path': 'static/image/d092340b-154f-4887-9a95-54346679ea26.jpg' # BaseUrl + image_url
    }
### 3.5 接口获取jpg图片：BaseUrl/image/<string:filename>
### 3.6 接口获取png图片：BaseUrl/show/<string:filename>
### 3.7 接口下载图片：BaseUrl/download/<string:filename>  

## 4. 其他说明： 
    部分功能不在服务器上实现： 
    如：检测学生是否离开摄像头10秒，此功能不在服务器上实现
    如需此功能，请在客户端循环获取学生脸部图像后，调用face_detect接口来实现
