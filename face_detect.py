import cv2
import numpy as np

class FaceDetect():
    def __init__(self):
        config_path = "model/yolov4-tiny.cfg"
        weights_path = "model/yolov4-tiny.weights"
        label_path = "model/face.names"

        self.confThreshold = 0.85
        self.nmsThreshold = 0.4
        self.inpWidth, self.inpHeight = 416, 416

        with open(label_path, 'rt') as f:
            self.label = f.read().rstrip('\n').split('\n')
        self.colors = [np.random.randint(0, 255, size=3).tolist() for _ in range(len(self.label))]

        net = cv2.dnn.readNet(config_path, weights_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(self.inpWidth, self.inpHeight), scale=1 / 255, swapRB=True)

    def convert(self, image_size, bndbox):
        dw = 1. / image_size[0]
        dh = 1. / image_size[1]

        x = (bndbox[0] + bndbox[1]) / 2.0
        y = (bndbox[2] + bndbox[3]) / 2.0
        w = bndbox[1] - bndbox[0]
        h = bndbox[3] - bndbox[2]

        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)

    def detect(self, img):
        image_size = [img.shape[1], img.shape[0]]

        classes, scores, boxes = self.model.detect(img, self.confThreshold, self.nmsThreshold)

        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.colors[int(classid) % len(self.colors)]
            label = str(self.label[classid[0]])

            xmin = int(box[0])
            xmax = int(box[0]) + int(box[2])
            ymin = int(box[1])
            ymax = int(box[1]) + int(box[3])

            bndbox = [xmin, xmax, ymin, ymax]
            x, y, w, h = self.convert(image_size, bndbox)

            cv2.rectangle(img, box, color, 2)
            text = label + ":" + str(score[0])
            cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        return img

if __name__ == "__main__":
    face_detect = FaceDetect()

    img = cv2.imread("test.jpg")
    img = face_detect.detect(img)

    winName = "Face Detection"
    cv2.namedWindow(winName, 0)
    cv2.imshow(winName, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()