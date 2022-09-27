# Object Detection in an Urban Environment


## Project overview

In this project we use Tensorflow Object Detection APIs to perform 2D object detection on Waymo dataset, for 3 classes: Vehicles, Pedestrians, Cyclists.
We will walk through the complete pipeline of model training, including dataset analysis, data split, model training, model improvement, and model export. At the end, we will create a short video of our model predictions to showcase the result.

The project have been performed on Google Colab, and the notebooks will guide you in all the steps proposed above

![](https://drive.google.com/uc?id=1xPhKSj9TmeCf2X4MI00_i99TlixSHOTj)
(sample image from: https://medium.com/@lattandreas/2d-detection-on-waymo-open-dataset-f111e760d15b)

## Data

All the training and validation data will be from the [Waymo Open dataset](https://waymo.com/open/).
Data can be download as individual tf records from the [Google Cloud Bucket](https://console.cloud.google.com/storage/browser/waymo_open_dataset_v_1_2_0_individual_files/).

the structure I used is the following:

![Project structure on colab](https://drive.google.com/uc?id=1HkyE0qcMeNo1HH5yio9C5nPdDdTZe5ym)

- the **Udacity-waymo-object-detection** is this forked github folder. Name the fork as you want, and then you'll find the steps to clone it in the '0-Requirements' notebook. You should **not** put heavy files in it. 

- all the heavy files like datasets and train/eval results are in a google drive folder named **data**

the **data** folder has the structure below:

![Data folder structure](https://drive.google.com/uc?id=1Zh_kuCv9W-9GZn0MnJMZ4Zb2RAoNg6S9)


If you want to download the pre-splitted dataset, find it at this link to my **/data/waymo/ folder.

https://drive.google.com/drive/folders/1RjN9ZLoHiXVvTDO0PmVnZUlHt3vg09hJ?usp=sharing

(you'll have to send me the request to see it)
The splits were created using the **create_splits.py**. If you want a different train/val/test split, you should download the folder, then move all the tfrecords to the **train_and_validation_data** folder and split them again

- the results from the train/eval pipelines are stored in the folder **data/experiments** in my google drive, I suggest you to create a similar folder in order to store yours.

###Data structure

the tfrecords contain 2D RGB images from the Waymo dataset. The labels are the following:

```sh
item {
    id: 1
    name: 'vehicle'
}

item {
    id: 2
    name: 'pedestrian'
}

item {
    id: 4
    name: 'cyclist'
}

```

So our project will cover a 2D object detection with 3 classes


## Set up

In the Home folder you'll find the colabNotebooks folder
Please download it and upload it in your drive, outside the forked and then cloned github repo. You should run the notebooks from this location in order to set all the paths correctly.


## 0. Install requirements

In order to run the tensorflow object detection api, you'll need to install a bunch of libraries. You'll also want them to be already installed everytime you connect a new colab runtime.

I created the **0_Requirements.ipynb** notebook that covers these steps

https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/notebooks/0-requirements.ipynb

It also installs the libraries of the /build/requirements.txt file.

As you can see from the image above, I placed the lib folder in the UDACITY folder, so I can use it for my next projects.


## 1. Download and save the pretrained models in the **/data/experiments/pretrained_model** folder

The project starts with transfer learning from the ssdResnet50_v1 Retinanet checkpoints, on our own dataset
In order to do so, you should download the pretrained model from the tensorflow model zoo

https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md

extract it from the tar.gz folder and upload it in the **/data/experiments/pretrained_model** folder on your drive

Here the link to my folder  https://drive.google.com/drive/folders/19tuCfXGtFThPQffByOE6bdyVoz2OtLrr?usp=sharing


## 2. train/eval the desired model/pipeline via the colab notebooks

For each model or experiment I tried, I created a google notebook.
Each notebook follows some intial steps like mounting the drive, updating the paths and installing the object detection dependencies.
Have a look at the notebooks in the notebook folder

https://github.com/foiegreis/Udacity-waymo-object-detection/tree/main/notebooks

for further information.
Each train_* notebook will cover:

```sh
- mounting the drive
- installing dependencies
- creating pipeline.config file 
- train
- validation
- tensorboard visualization
- saving the model
- creating a animation.mp4 file over the test tfrecords
```

the train/val pipelines were run under **GPU - HIGH RAM** colab runtime.
In order to do so, I updated my Colab profile to ColabPro 

![smi](https://drive.google.com/uc?id=1hg_MvCom298qCKzuu4WEoAv2VkuYTxGc)

## Data analysis and models

you'll find all the notebooks in the /notebooks folder
Also, see https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/home/workspace/README.md

## Exploratory data analysis
see the notebook:  https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/home/workspace/Exploratory_Data_Analysis.ipynb

## Explore augmentation
see the notebook: https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/home/workspace/Explore_augmentations.ipynb

## Training

see the readme: https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/home/workspace/README.md 
and the notebooks in : https://github.com/foiegreis/Udacity-waymo-object-detection/tree/main/notebooks

