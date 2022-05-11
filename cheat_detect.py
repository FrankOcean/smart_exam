# -*- coding: UTF-8 -*-
import torch
import cv2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
save_path = './img/tmp.jpg'

model_dec = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

# Images # or file, Path, PIL, OpenCV, numpy, list
def cheat_detect_fuc(image, uuidstr):
    result = ' '
    count_person = 0
    img = cv2.imread(image)
    # Inference
    results = model_dec(img)
    # Results
    pandas = results.pandas()  # or .show(), .save(), .crop(), .pandas(), etc. print()
    # print(pandas.xywhn[-1])
    names = pandas.xywhn[0].name
    name_list = []

    for name in names:
        name_list.append(name)

    has_phone = 0
    for name in names:
        if name == "person":
            count_person += 1
        if name == "cell phone":
            has_phone = 1
            result = "Phone cheating"
            print(result)
    if count_person > 1:
        result = "Number of people cheating"
        print(result)

    boxes = pandas.xyxy[0]

    for i in range(len(boxes)):
        box = boxes.loc[i]
        x = int(box.xmin)
        y = int(box.ymin)
        w = int(box.xmax) - x
        h = int(box.ymax) - y
        # print(x, y, w, h)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        save_cv2img_tofile(img, uuidstr + '.jpg')
    return {'count_person': count_person, 'has_phone': has_phone, 'result_path': "static/image/{}.jpg".format(uuidstr)}

def save_cv2img_tofile(img, save_path="face-mesh.jpg"):
    if isinstance(img, str):
        image = cv2.imread(img)
        cv2.imencode('.jpg', image)[1].tofile("./static/image/{}".format(save_path))
    else:
        # opencv 保存图片
        cv2.imencode('.jpg', img)[1].tofile("./static/image/{}".format(save_path))

