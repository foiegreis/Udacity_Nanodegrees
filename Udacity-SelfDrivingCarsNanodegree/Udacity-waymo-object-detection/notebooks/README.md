# Notebooks created for the project


## 1. Exploratory data analysis

In the 'Exploratory Data Analysis.ipynb' notebook you'll find the EDA performed on the dataset.
As a recall, these were some of the statistics covered:

## Classes distribution

![](https://drive.google.com/uc?id=1FuNF-gCKP7E4a9dvThZXG9DVGkW71fBE)

## Brightness analysis

![](https://drive.google.com/uc?id=1OXGlRqdP-mQPe005w4IJE9g0fdykIt_2)

## BBoxes areas and centers-wise analysis

![](https://drive.google.com/uc?id=1LZikM_lWkDOI7hxAv_UVxiwDYOy9wydn)


![](https://drive.google.com/uc?id=1yruuU7_CoZcetcMq-aqfurokhrmLcHvD)

**Please see the notebook for further information**
https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/home/workspace/Exploratory_Data_Analysis.ipynb

## 2. Data augmentation

In the 'Data Augmentation.ipynb' notebook you'll find the EDA performed on the dataset.
As a recall, these were some of the techniques covered:


![](https://drive.google.com/uc?id=1_IwYOwrjrPc7ZIMRdaTBs13WioxSyx9r)

![](https://drive.google.com/uc?id=1RZsGNZu9uSlLVvttAacXsZYTGhOLVhXJ)

**Please see the notebook for further information**
https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/home/workspace/Explore_augmentations.ipynb

## 3. Training

## Reference experiment

The Reference experiment refers to the training and evaluation of a ssdResnet50_v1 model, using transfer learning over the checkpoints downloaded from the modelzoo, on our custom dataset

In the 'train_reference.ipynb' notebook you'll find all the steps and settings used to train the model.
https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/notebooks/1-train_reference.ipynb

Here a snippet of the results

![](https://drive.google.com/uc?id=1X8CvEeQkazFfWxucWQiqmQ1jOQ7c0Mhe)

![](https://drive.google.com/uc?id=1W6sNtM-YIn1jOXyaYzx8pnfn3uN_V61b)

![](https://drive.google.com/uc?id=18cNSbDgUh6cAaxuAOgrZVd2yXH1QUDvy)


## Analysis 
In previous tries we noticed that the model couldn't converge even on the Train set. 
In order to fix it, we lowered the optimizer momentum to 0.6.

The results were clearly overfitting on the trainset. But this was a good baseline to check our model for further improvements (e.g. data augmentation, more training steps, learning rate tuning)

## 4. Improve on the reference

## Experiment1 - **our best output**

Above all the experiments we made, this was our best output.
Train and evaluate reference network with data Augmentation: ssd resnet50, batch 4, momentum 0.8, data augmentation, 25000 runs, lr 0.004

Let's add data augmentation and train a bit longer. 
Also, momentum 0.8 to prevent overfitting and data augmentation in the pipeline_new.config.

see the notebook:
https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/notebooks/2-train_experiment1.ipynb

## Analysis:

Training longer and working on the data augmentation and learning rate improved a lot the process.

(The loss visualization in tensorboard is not that accurate because many checkpoints were deleted based on the keep_max_num parameter in the trainer.py module of the od api. 
We've also modified the model_lib_v2.py file in order to being able to visualize both the train and val data in tensorboard. Please have a look at the files for further information.)

We can infer that the training loss is converging and the test loss is moving in the direction of the train, meaning the model isn't overfitting. Training for more epochs will lead to even better results.

The mAp and recall were increasing, denoting the model was improving during the training. Of course, we could have reached better results training longer.

![](https://drive.google.com/uc?id=1ZWEX6C8-9NtmEvsco7kkgYJNrqwHnWI1)

![](https://drive.google.com/uc?id=1LNdlcaU1zm902kKU3otfkuzYu-cdHe29)

![](https://drive.google.com/uc?id=1lE_tT8PZdLt888tKX3xDkeALwRfqQ5L1)


As you would see in the animation.mp4 file at this link, this was our best result

https://drive.google.com/file/d/1oAYSkN6cecO78yMi_5IbhWXeYVhj7v2z/view?usp=sharing

![](https://drive.google.com/uc?id=1z-Sr4fPIFah-Ze9xC1s0pv3UMLuCBKzi)

Here the link to the exported model

https://drive.google.com/drive/folders/1njrHlclFGYtLa-mRV2otzZoy6KqV81sS?usp=sharing


## Experiment 2 - great training curves but bad performances for box anchors

Train and evaluate reference network with data Augmentation: ssd resnet50, batch 4, momentum 0.9, data augmentation, 30000 runs, lr 0.079 with decay,
changes from the original model in:
- batch non max suppression
- convolutional box predictor
- dropout

Here a snippet of the results

![](https://drive.google.com/uc?id=1hqkG-tDxHuqLZ3GP8SeetRb09OVKrPQI)
![](https://drive.google.com/uc?id=10GruBcPZoX2TWDpfGkiKx_4lubJJMkQK)

see the notebook:
https://github.com/foiegreis/Udacity-waymo-object-detection/blob/main/notebooks/3-train_experiment2.ipynb

##Analysis:

Our chances on batch_non_max_suppression and convolutional_box_predictor performed poorly on our dataset, even if we tried to tailor the hyperparameters in order to take under consideration the infos we got from the eda process.
However, given the loss curves for train and eval, the dropout stage was performing well and we should keep it in future models.

Here's the animation - look how the boxes do not cover the entire vehicle area!
https://drive.google.com/file/d/1eBdaPGyxyVahNsSDSSpNjYq7TN7Ltd8f/view?usp=sharing

![](https://drive.google.com/uc?id=12eqjGcVPHpJiTtlRQ1Gh1FOADevEuoHN)

link to the saved model

https://drive.google.com/drive/folders/1d8hCchhA7cnEkycW1Oy4QnhIu-j8Dg_6?usp=sharing





