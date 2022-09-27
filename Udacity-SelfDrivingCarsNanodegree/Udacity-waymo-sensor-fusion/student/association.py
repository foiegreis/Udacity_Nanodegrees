# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Data association class with single nearest neighbor association and gating based on Mahalanobis distance
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
#
#
# student: github/foiegreis
# ----------------------------------------------------------------------
#

# imports
import numpy as np
from scipy.stats.distributions import chi2
import math
# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import misc.params as params

class Association:
    '''Data association class with single nearest neighbor association and gating based on Mahalanobis distance'''
    def __init__(self):
        self.association_matrix = np.matrix([])
        self.unassigned_tracks = []
        self.unassigned_meas = []
        
    def associate(self, track_list, meas_list, KF):
        """
        Performs data association with single nearest neighbor association and gating based on Mahalanobis distance
        
        The association matrix will store all Mahalanobis distances between tracks and measurements
        
        Association steps:
            - replace association_matrix with the actual association matrix based on Mahalanobis distance (see below) for all tracks and all measurements
            - update list of unassigned measurements and unassigned tracks
        """
        #------------------------------------------------------------------------------
        #SINGLE TRACK
        # the following only works for at most one track and one measurement
        #self.association_matrix = np.matrix([]) # reset matrix
        #self.unassigned_tracks = [] # reset lists
        #self.unassigned_meas = []
        
        #if len(meas_list) > 0:
         #   self.unassigned_meas = [0]
        #if len(track_list) > 0:
         #   self.unassigned_tracks = [0]
        #if len(meas_list) > 0 and len(track_list) > 0:
         #   self.association_matrix = np.matrix([[0]])
        
        #Step 3 ----------------------------------------------------------------------
        #MULTITRACK
        #from lesson

        N = len(track_list) # N tracks
        M = len(meas_list) # M measurements
        self.unassigned_tracks = list(range(N))
        self.unassigned_meas = list(range(M))

        # initialize association matrix
        self.association_matrix = np.inf*np.ones((N,M))

        # loop over all tracks and all measurements to set up association matrix
        for i in range(N):
            track = track_list[i]
            for j in range(M):
                meas = meas_list[j]
                dist = self.MHD(track, meas, KF)
                if self.gating(dist, meas.sensor):
                    self.association_matrix[i,j] = dist
        
        #----------------------------------------------------------------------------
                
    def get_closest_track_and_meas(self):
        """
        The SNN algorithm calculates all distnces between tracks and measurements (association matrix in from self.associate(), then iteratively updates the closest association pair
        
        Find closest track and measurement:
            - find minimum entry in association matrix
            - delete row and column
            - remove corresponding track and measurement from unassigned_tracks and unassigned_meas
            - return this track and measurement
        
        The minimum entry in the association matrix will represent the closest track to each measurement. After finding it, we'll must delete the rows and columns corresponding to that track-measure pair.
        We'll also delete the corresponding track and measure id from the unassinged track and measure lists.
        In self.associate_and_update(), this process will be run iteratively untill A is empty.
        """
        #--------------------------------------------------------------------
        #SINGLE TRACK
        # the following only works for at most one track and one measurement
        #update_track = 0
        #update_meas = 0
        # remove from list
        #self.unassigned_tracks.remove(update_track)
        #self.unassigned_meas.remove(update_meas)
        #self.association_matrix = np.matrix([])
        
        #Step 3 -----------------------------------------------------------
        #MULTITRACK
        #from lesson
        
        A = self.association_matrix
        #gating
        if np.min(A) == np.inf:
            return np.nan, np.nan

        # get indices of minimum entry
        ind_track, ind_meas = np.unravel_index(np.argmin(A, axis=None), A.shape)

        # delete row and column for next update
        A = np.delete(A, ind_track, 0)
        A = np.delete(A, ind_meas, 1)
        self.association_matrix = A

        # update this track with this measurement
        update_track = self.unassigned_tracks[ind_track]
        update_meas = self.unassigned_meas[ind_meas]

        # remove this track and measurement from list
        self.unassigned_tracks.remove(update_track)
        self.unassigned_meas.remove(update_meas)
        #-----------------------------------------------------------------

        return update_track, update_meas
    
    def gating(self, MHD, sensor):
        """
        Returns True if measurement lies inside gate, otherwise False
        """
        #Step 3 --------------------------------------------------------
        # check if measurement lies inside gate
        return MHD < chi2.ppf(params.gating_threshold, df=sensor.dim_meas)
        
        #-----------------------------------------------------------------
        
    def MHD(self, track, meas, KF):
        """
        Calculates and returns Mahalanobis distance
        """
        #Step 3 --------------------------------------------------------
        H = meas.sensor.get_H(track.x)
        gamma = KF.gamma(track, meas)
        MHD = math.sqrt(gamma.transpose() * np.linalg.inv(KF.S(track,meas,H)) * gamma) # Mahalanobis distance formula
        return MHD
        #-----------------------------------------------------------------
        
    
    def associate_and_update(self, manager, meas_list, KF):
        # associate measurements and tracks
        self.associate(manager.track_list, meas_list, KF)
    
        # update associated tracks with measurements
        while self.association_matrix.shape[0]>0 and self.association_matrix.shape[1]>0:
            
            # search for next association between a track and a measurement
            ind_track, ind_meas = self.get_closest_track_and_meas()
            if np.isnan(ind_track):
                print('---no more associations---')
                break
            track = manager.track_list[ind_track]
            
            # check visibility, only update tracks in fov
            if not meas_list[0].sensor.in_fov(track.x):
                continue
            
            # Kalman update
            print('update track', track.id, 'with', meas_list[ind_meas].sensor.name, 'measurement', ind_meas)
            KF.update(track, meas_list[ind_meas])
            
            # update score and track state
            manager.handle_updated_track(track)
            
            # save updated track
            manager.track_list[ind_track] = track
            
        # run track management
        manager.manage_tracks(self.unassigned_tracks, self.unassigned_meas, meas_list)
        
        for track in manager.track_list:
            print('track', track.id, 'score =', track.score)
