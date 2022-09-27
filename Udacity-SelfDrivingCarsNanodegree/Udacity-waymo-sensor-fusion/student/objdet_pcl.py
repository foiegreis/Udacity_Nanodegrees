# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Process the point-cloud and prepare it for object detection
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# general package imports
import cv2
import numpy as np
import torch
import zlib
import open3d as o3d

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils
from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2

# object detection tools and helper functions
import misc.objdet_tools as tools


# visualize lidar point-cloud
def show_pcl(pcl):
    """
    Visualize lidar point cloud
    
    :param:      pcl     lidar point cloud extracted from waymo dataset
    :type:       pcl     numpy.ndarray
    """
    print("\n")
    print("@student task ID_S1_EX2")
    print("## Point cloud visualization ##")
    print("## press the 'right arrow' to update the scene to the next frame ##")
    print("\n")
    
    # step 1 : initialize open3d with key callback and create window
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name = 'lidar pcd', width=1920, height=1080, visible=True)
    
    #define callback functions
    global update_flag
    update_flag = True
    def update(vis):
        global update_flag
        update_flag = False
        return
        
    vis.register_key_callback(262, update)

    
    # step 2 : create instance of open3d point-cloud class
    pcd = o3d.geometry.PointCloud()
    
    # step 3 : set points in pcd instance by converting the point-cloud into 3d vectors (using open3d function Vector3dVector)
    pcd.points = o3d.utility.Vector3dVector(pcl[:,0:3])
    
    # step 4 : for the first frame, add the pcd instance to visualization using add_geometry; for all other frames, use update_geometry instead
    vis.add_geometry(pcd)
    
    # step 5 : visualize point cloud and keep window open until right-arrow is pressed (key-code 262)
    while update_flag:
        vis.poll_events()
        vis.update_renderer()
    
        
           
# visualize range image
def show_range_image(frame, lidar_name):
    """
    Visualize lidar range image
    
    :param:     frame       range image extracted via waymo dataset reader
    :type:      frame       <class 'simple_waymo_open_dataset_reader.dataset_pb2.Frame'>
    
    :param:     lidar_name  name of the frame (ex. 1)
    :type:      lidar_name  int
    """
    print("\n")
    print("@student task ID_S1_EX1")

    # step 1 : extract lidar data and range image for the roof-mounted lidar
    lidar_data = [x for x in frame.lasers if x.name == lidar_name][0]
    
    
    # step 2 : extract two of the data channels within the range image, which are "range" and "intensity",
    ri = dataset_pb2.MatrixFloat()
    ri.ParseFromString(zlib.decompress(lidar_data.ri_return1.range_image_compressed))
    ri = np.array(ri.data).reshape(ri.shape.dims)
    
    # step 3 : set values <0 to zero
    ri[ri<0]=0.0

    
    # step 4 : map the range channel onto an 8-bit scale and make sure that the full range of values is appropriately considered
    ri_range = ri[:,:,0] #channel 0 is range channel
    ri_range = (ri_range * 255/ (np.amax(ri_range) - np.amin(ri_range))).astype(np.uint8)  #we expand the values from 0 to 255
    
    # step 5 : map the intensity channel onto an 8-bit scale and normalize with the difference between the 1- and 99-percentile to mitigate the influence of outliers
    ri_intensity = ri[:,:,1]
    percentile_1 = np.lib.function_base.percentile(ri_intensity, 1)
    percentile_99 = np.lib.function_base.percentile(ri_intensity, 99)
    
    #to scale the values between 1-99 percentile, we can use np.clip
    ri_intensity = 255 * np.clip(ri_intensity, percentile_1, percentile_99) / percentile_99
    ri_intensity = ri_intensity.astype(np.uint8)
    
    # step 6 : stack the range and intensity image vertically using np.vstack and convert the result to an unsigned 8-bit integer
    img_range_intensity = np.vstack((ri_range, ri_intensity))
    img_range_intensity = img_range_intensity.astype(np.uint8)
    
    #FRONT IMAGE
    deg45 = int(img_range_intensity.shape[1] / 8)
    ri_center = int(img_range_intensity.shape[1]/2)
    img_range_intensityFRONT = np.copy(img_range_intensity)
    img_range_intensityFRONT = img_range_intensityFRONT[:,ri_center-deg45:ri_center+deg45]
    
    #LEFT SIDE IMAGE
    img_range_intensityLEFT = np.copy(img_range_intensity)
    img_range_intensityLEFT = img_range_intensity[:,ri_center-3*deg45:ri_center-deg45]
    
    return img_range_intensity, img_range_intensityFRONT, img_range_intensityLEFT


# create birds-eye view of lidar data
def bev_from_pcl(lidar_pcl, configs):
    """
    Visualize birds-eye view from Lidar pcl
    
    :param:     lidar_pcl   lidar point cloud
    :type:      lidar_pcl   numpy.ndarray
    
    :param:     configs     bev image configs
    :type:      configs     <class 'easydict.EasyDict'>
    """
    ################################################################################
    print("\n@student task ID_S2_EX1")
    
    
    # remove lidar points outside detection area and with too low reflectivity
    mask = np.where((lidar_pcl[:, 0] >= configs.lim_x[0]) & (lidar_pcl[:, 0] <= configs.lim_x[1]) &
                    (lidar_pcl[:, 1] >= configs.lim_y[0]) & (lidar_pcl[:, 1] <= configs.lim_y[1]) &
                    (lidar_pcl[:, 2] >= configs.lim_z[0]) & (lidar_pcl[:, 2] <= configs.lim_z[1]))
    lidar_pcl = lidar_pcl[mask]
    
    # shift level of ground plane to avoid flipping from 0 to 255 for neighboring pixels
    lidar_pcl[:, 2] = lidar_pcl[:, 2] - configs.lim_z[0]  


    ## step 1 :  compute bev-map discretization by dividing x-range by the bev-image height (see configs)
    bev_discr = (configs.lim_x[1] - configs.lim_x[0]) / configs.bev_height
    
    ## step 2 : create a copy of the lidar pcl and transform all metrix x-coordinates into bev-image coordinates    
    lidar_pcl_copy = np.copy(lidar_pcl)
    lidar_pcl_copy[:, 0] = np.int_(np.floor(lidar_pcl_copy[:, 0] / bev_discr))
    
    # step 3 : perform the same operation as in step 2 for the y-coordinates but make sure that no negative bev-coordinates occur
    lidar_pcl_copy[:, 1] = np.int_(np.floor(lidar_pcl_copy[:, 1] / bev_discr) + (configs.bev_width + 1) / 2)
    lidar_pcl_copy[:, 1] = np.abs(lidar_pcl_copy[:,1])

    # step 4 : visualize point-cloud using the function show_pcl from a previous task
    show_pcl(lidar_pcl_copy)
    
    
    ########################################################################################
    print("\n@student task ID_S2_EX2")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    intensity_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))  #+1 so negative bev-coordinates cannot occur

    # step 2 : re-arrange elements in lidar_pcl_cpy by sorting first by x, then y, then -z (use numpy.lexsort)
    lidar_pcl_copy[lidar_pcl_copy[:, 3] > 1.0, 3] = 1.0
    idx_intensity = np.lexsort((-lidar_pcl_copy[:, 3], lidar_pcl_copy[:, 1], lidar_pcl_copy[:, 0]))
    lidar_pcl_top = lidar_pcl_copy[idx_intensity]
    
    ## step 3 : extract all points with identical x and y such that only the top-most z-coordinate is kept (use numpy.unique)
    ##          also, store the number of points per x,y-cell in a variable named "counts" for use in the next task
    lidar_pcl_int, indices_top, counts = np.unique(lidar_pcl_copy[:, 0:2], axis=0, return_index=True, return_counts=True)
    lidar_pcl_top = lidar_pcl_top[indices_top]
    
    ## step 4 : assign the intensity value of each unique entry in lidar_top_pcl to the intensity map / + intensity scaling + normalization
    lidar_pcl_top[lidar_pcl_top[:,3]>1.0, 3] = 1.0
    lidar_pcl_top[lidar_pcl_top[:,3]<0.0, 3] = 0.0
    
    intensity_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:, 1])] = lidar_pcl_top[:, 3] /(np.amax(lidar_pcl_top[:, 3])-np.amin(lidar_pcl_top[:, 3]))
    
    
    ## step 5 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    img_intensity = (intensity_map * 256).astype(np.uint8)
    cv2.imshow('Img intensity', img_intensity)
    cv2.waitKey(0)

    ########################################################################################
    print("\n@student task ID_S2_EX3")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    height_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))
    
    ## step 2 : assign the height value of each unique entry in lidar_top_pcl to the height map / + normalization
    height_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:, 1])] = lidar_pcl_top[:, 2]/float(np.abs(configs.lim_z[1]-configs.lim_z[0]))

    ## step 3 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    img_height = (height_map * 256).astype(np.uint8)
    #cv2.imshow("height map", img_height)
    #cv2.waitKey(0)

    # Compute density layer of the BEV map
    density_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))
    _, _, counts = np.unique(lidar_pcl_copy[:, 0:2], axis=0, return_index=True, return_counts=True)
    normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(64)) 
    density_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:, 1])] = normalizedCounts
        
    # assemble 3-channel bev-map from individual maps
    bev_map = np.zeros((3, configs.bev_height, configs.bev_width))
    bev_map[2, :, :] = density_map[:configs.bev_height, :configs.bev_width]  # r_map
    bev_map[1, :, :] = height_map[:configs.bev_height, :configs.bev_width]  # g_map
    bev_map[0, :, :] = intensity_map[:configs.bev_height, :configs.bev_width]  # b_map

    # expand dimension of bev_map before converting into a tensor
    s1, s2, s3 = bev_map.shape
    bev_maps = np.zeros((1, s1, s2, s3))
    bev_maps[0] = bev_map

    bev_maps = torch.from_numpy(bev_maps)  # create tensor from birds-eye view
    input_bev_maps = bev_maps.to(configs.device, non_blocking=True).float()
    return input_bev_maps


