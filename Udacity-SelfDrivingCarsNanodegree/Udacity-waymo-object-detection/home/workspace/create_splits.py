import argparse
import glob
import os
import random

import numpy as np

from utils import get_module_logger
import shutil


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the 
    same directory. This folder should be named train, val and test.

    args:
        --data_dir the path to your /data/waymo folder
    """
        
    total_data_dir = os.path.join(data_dir, 'training_and_validation')
    train_dir =os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')
    
    
    train_and_val_data = os.listdir(total_data_dir)
    
    if len(train_and_val_data)==0:
        print("Cannot find the path specified")
    else:
        total_qty = len(train_and_val_data)##97 files
        print("Total train and val tfrecords: ", total_qty)
        
        #shuffle the data
        np.random.shuffle(train_and_val_data)
        
        #split quantities
        train_perc = 0.85
        val_perc = 0.15
        
        train_data, val_data = np.split(train_and_val_data, [int(train_perc*total_qty)])
        print("We split the total of {} tf records in {} train {} validation files".format(total_qty,
                                                                                               len(train_data),
                                                                                               len(val_data)))
                                                                                               
        #move
        for tfrecord in train_data:
            source_path = os.path.join(total_data_dir, tfrecord)
            destination_path = os.path.join(train_dir, tfrecord)
            shutil.move(source_path, destination_path)
           
        for tfrecord in val_data:
            source_path = os.path.join(total_data_dir, tfrecord)
            destination_path = os.path.join(val_dir, tfrecord)
            shutil.move(source_path, destination_path)
        

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Split data into training / validation')
    parser.add_argument('--data_dir', required=True,help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)
