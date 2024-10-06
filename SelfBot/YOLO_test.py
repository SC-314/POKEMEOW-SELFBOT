import discum
from discum.utils.button import Buttoner
import time
import random
import requests
from PIL import Image
from io import BytesIO
from PIL import Image
from ultralytics import YOLO

def captcha_solver(image):
    all_predictions = []
    for j in range(1):
        results = model.predict(image, conf=0.6) # 0.43 # i think bets is 0.6
        predictions = results[0].boxes.xyxy
        confidences = results[0].boxes.conf
        classes = results[0].boxes.cls

        prediction_list = []
        for i in range(len(predictions)):
            x_min, y_min, x_max, y_max = predictions[i].tolist()  # Get bounding box coordinates
            prediction_list.append({
                'class_id': int(classes[i]),
                'confidence': confidences[i].item(),
                'x_min': x_min,
                'y_min': y_min,
                'x_max': x_max,
                'y_max': y_max
            })
        all_predictions.append(prediction_list)

    predicts = []
    for j in all_predictions:
        numbers = []
        solution = []
        for i in j:
            numbers.append([i['x_max'], i['class_id']])
        for i in sorted(numbers):
            solution.append(i[1])
        predicts.append(solution)
    captcha_solution = ""
    for i in predicts[0]:
        captcha_solution += str(i)
    return captcha_solution

model = YOLO(r'C:\Users\Sam\Desktop\YOLO\runs\detect\train26\weights\best.pt')

image = Image.open(r'C:\Users\Sam\Desktop\YOLO\captcha_dataset\images\discord\7.png')
print(captcha_solver(image))