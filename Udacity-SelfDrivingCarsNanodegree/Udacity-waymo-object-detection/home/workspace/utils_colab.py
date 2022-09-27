import argparse
import glob
import os
import random

import numpy as np
import sys
sys.path.append('/content/gdrive/MyDrive/GoogleColab/UDACITY/SDC/1-waymo-object-detection/Udacity-waymo-object-detection/home/workspace/')
from utils import get_module_logger
import shutil


def test_colab():
    """
    Imports libraries in order to test if all the needed dependencies are loaded in google colab
    """
    
    print("current dir", os.getcwd())
    
    print("###########################")
    print("CONGRATS!")
    print("If you see this it means that all the dependencies have been correctly installed. Let's move on!")
    print("###########################")

        

if __name__ == "__main__":
    logger = get_module_logger(__name__)
    logger.info('Testing colab dependencies...')
    test_colab()
