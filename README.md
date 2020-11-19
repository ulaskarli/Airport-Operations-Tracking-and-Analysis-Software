# Airport-Operations-Tracking-and-Analysis-Software
This repo is for Senior design project of Ulas Berk Karlı, Umay Bengisu Bozkurt and Berkay Hopalı.

## Dataset

We created our own dataset by using images from google and annotated them using CVAT and LabelImg. Then preprocessed using Roboflow.
- Format: YoloV5
- Image size: 416x416
- Classes
  - Catering Truck
  - baggagetruck
  - Boarding stairs
  - Borading Bridge
  
Examples:
  
![Total Dataset](https://github.com/ulaskarli/Airport-Operations-Tracking-and-Analysis-Software/blob/main/Dataset/dataset%20samples/dataset_total.png)

## Detection Model

We are using YoloV5 from ultralytics. Following is the repo that we use for the model and the link to the .ipynb used as a starting point
- [ultralytics Yolov5](https://github.com/ultralytics/yolov5.git)
- [Training YoloV5 Colab](https://colab.research.google.com/drive/1gDZ2xcTOgR39tGGs-EZ6i3RTs16wmzZQ)

Last update:
- Creation of repo: 03/11/2020
- Submission of annotated images: 05/11/2020
- Sumission of Custom Dataset-v1: 05/11/2020
- Submission of Detection model starter code: 05/11/2020
- Submision of Detection model training Python notebook: 19/11/2020
- Submission of Trained Weights: 19/11/2020
