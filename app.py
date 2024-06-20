from flask import Flask, render_template, Response, request, jsonify
import cv2
import base64
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('./best.pt')  # Load the YOLO model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json['image']
    # Convert base64 image to numpy array
    img = base64.b64decode(data.split(',')[1])
    npimg = np.frombuffer(img, dtype=np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Process the frame with YOLO
    results = model(frame)
    for result in results:
        boxes = result.boxes.xyxy
        scores = result.boxes.conf
        labels = result.boxes.cls

        for box, score, label in zip(boxes, scores, labels):
            if score >= 0.4:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{model.names[int(label)]}: {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    _, jpeg = cv2.imencode('.jpg', frame)
    return jsonify({'image': base64.b64encode(jpeg).decode('utf-8')})

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=5000, ssl_context='adhoc'))
