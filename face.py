import mediapipe as mp
import cv2
import numpy as np
from opt import *

def detect_faces(file_name, first_name, file_name_hz):

    img_path = os.path.join(UPLOAD_FOLDER, file_name)
    # 构建脸部特征提取对象
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,  # Flase ：处理视频  True:处理单张图片
                                      max_num_faces=1,  # 最大脸的个数
                                      refine_landmarks=True,
                                      min_detection_confidence=0.5,  # 检测置信度
                                      min_tracking_confidence=0.5)  # 跟踪置信度
    # 构建绘图对象
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    img = cv2.imread(img_path)
    print(img.shape)

    # 获取宽度和高低
    img = cv2.flip(img, 1)
    image_height, image_width, _ = np.shape(img)
    # BGR 转 RGB
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 进行特征点提取
    results = face_mesh.process(img_RGB)

    # 存储嘴眼状态信息
    mouth_state = ''
    eye_state = ''
    has_faces = '0'
    if results.multi_face_landmarks:  # 检测到了人脸
        for face_landmarks in results.multi_face_landmarks:  # 绘制每张脸
            # 利用 内置的mp_drawing 进行绘图
            ## 人脸网格
            mp_drawing.draw_landmarks(image=img,
                                      landmark_list=face_landmarks,
                                      connections=mp_face_mesh.FACEMESH_TESSELATION,
                                      landmark_drawing_spec=None,
                                      connection_drawing_spec=mp_drawing_styles
                                      .get_default_face_mesh_tesselation_style())
            ## 人脸轮廓
            mp_drawing.draw_landmarks(image=img,
                                      landmark_list=face_landmarks,
                                      connections=mp_face_mesh.FACEMESH_CONTOURS,
                                      landmark_drawing_spec=None,
                                      connection_drawing_spec=mp_drawing_styles
                                      .get_default_face_mesh_contours_style())
            ## 瞳孔的轮廓
            mp_drawing.draw_landmarks(
                image=img,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())

            # 自行计算478个关键点的坐标 并绘制
            if face_landmarks:
                # print(face_landmarks)  所有点的 x y z 坐标
                # print(face_landmarks.landmark[0]) 第0个点的坐标
                # 计算关键点坐标
                for i in range(478):
                    pos_x = int(face_landmarks.landmark[i].x * image_width)
                    pos_y = int(face_landmarks.landmark[i].y * image_height)
                    if i in (13, 14, 145, 159, 374, 386):
                        cv2.circle(img, (pos_x, pos_y), 3, (0, 0, 255), -1)
                    else:
                        cv2.circle(img, (pos_x, pos_y), 3, (0, 255, 0), -1)

            # 判断上下嘴唇距离
            distance_mouth = (face_landmarks.landmark[14].y - face_landmarks.landmark[13].y) * image_height
            print("distance_mouth: ", distance_mouth)
            if distance_mouth > 20:
                mouth_state = "open mouth"
                print("是否张开嘴： 张嘴了")
            else:
                mouth_state = "not  mouth"
                print("是否张开嘴： 没有张嘴")

            # 判断上下眼睛距离
            distance_eye1 = (face_landmarks.landmark[145].y - face_landmarks.landmark[159].y) * image_height
            distance_eye2 = (face_landmarks.landmark[374].y - face_landmarks.landmark[386].y) * image_height
            print("distance_eye1: ", distance_eye1, "     distance_eye2: ", distance_eye2)
            if distance_eye1 > 7 and distance_eye2 > 7:
                eye_state = "open eye"
                print("是否睁开眼：   睁眼了")
            else:
                eye_state = "not  eye"
                print("是否睁开眼：   没有睁眼")

            cv2.putText(img, f'mouth -->{mouth_state}', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
            cv2.putText(img, f'  eye  -->{eye_state}', (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

    else:
        # 如果没有检测到人脸
        cv2.putText(img, f'mouth --> NULL', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
        cv2.putText(img, f'  eye  --> NULL', (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
    # opencv 保存图片
    cv2.imencode('.jpg', img)[1].tofile("./static/image/{}_detect.jpg".format(first_name))
    # return {"code": '200', "has_faces": has_faces, "mouth_state": mouth_state, "eye_state": eye_state, "image_url_detect": image_url + first_name + '_detect.jpg', "image_url": image_url + first_name + '.' + file_name_hz}

