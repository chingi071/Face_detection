# Face_detection
本篇的人臉偵測使用 Darknet 進行訓練，model 為 YOLOv4-tiny

訓練集、驗證集使用 WIDER FACE

## Data preprocessing
執行 data_preprocessing.ipynb，其中 WIDER_FACE_covert_to_yolo.py 用於轉換資料集格式，記得修改檔案路徑

## 訓練模型
訓練步驟都寫在 yolov4-tiny.ipynb
可在 Colab 上進行訓練

## 防止 Colab 自動斷線
在 Colab 頁面按 F12，在 Console 貼上以下 Code 後按 Enter
    
    function ConnectButton(){
    console.log("Connect pushed"); 
    document.querySelector("#connect").click() 
    }
    setInterval(ConnectButton,60000);

## OpenCV inference
使用 opencv 進行 inference

    $ python face_detect.py

## 檔案放置路徑如下
<img width="400" height="550" src="https://github.com/chingi071/Face_detection/blob/main/README_pix/image1.jpg"/></div>

## YOLO 訓練流程
詳細流程可以參考我的 Medium: https://medium.com/@chingi071/yolo-c49f70241aa7
