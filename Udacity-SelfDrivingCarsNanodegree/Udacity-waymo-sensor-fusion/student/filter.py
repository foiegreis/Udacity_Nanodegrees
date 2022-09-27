# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
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

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        self.dim_state = params.dim_state
        self.dt = params.dt # time increment
        self.q = params.q # process noise variable for Kalman filter Q

    def F(self):
        """
        Defines the System State matrix F
        - constant velocity model
        - dim_state = 6
        - x  = (px, py, pz, vx, vy, vz)
        
        [ 1  0  0 dt  0  0]
        [ 0  1  0  0  dt 0]
        [ 0  0  1  0  0 dt]
        [ 0  0  0  1  0  0]
        [ 0  0  0  0  1  0]
        [ 0  0  0  0  0  1]
        
        :return:    F      state matrix, np.matrix
        """

        F = np.matrix([[1,  0,  0,  self.dt, 0,  0 ],
                       [0,  1,  0,  0,  self.dt, 0 ],
                       [0,  0,  1,  0,  0,  self.dt],
                       [0,  0,  0,  1,  0,  0 ],
                       [0,  0,  0,  0,  1,  0 ],
                       [0,  0,  0,  0,  0,  1]])
        return F
      
    def Q(self):
        """
        Defines the Process Noise Covariance Matrix Q
        - dim_state = 6
        - Q(Dt) = Int[0, Dt](F * Q * F.transpose) dt =
        
        [1/3(dt^3)q     0           0    1/2(dt^2)q      0          0    ]
        [0          1/3(dt^3)q      0         0      1/2(dt^2)q     0    ]
        [0              0      1/3(dt^3)q     0          0    1/2(dt^2)q ]
        [1/2(dt^2)q     0           0       dt*q         0          0    ]
        [0          1/2(dt^2)q      0         0        dt*q         0    ]
        [0              0       1/2(dt^2)q    0          0         dt*q  ]
        
        [q3, 0,  0,  q2, 0,  0 ]
        [0,  q3, 0,  0,  q2, 0 ]
        [0,  0,  q3, 0,  0,  q2]
        [q2, 0,  0,  qt, 0,  0 ]
        [0,  q2, 0,  0,  qt, 0 ]
        [0,  0,  q2, 0,  0,  qt]
        
        :return:    Q     state matrix, np.matrix
        """
        dt = self.dt
        q  = self.q
        q3 = ((dt**3)/3) * q
        q2 = ((dt**2)/2) * q
        qt  = dt * q
        
        Q = np.matrix([[q3, 0,  0,  q2, 0,  0 ],
                       [0,  q3, 0,  0,  q2, 0 ],
                       [0,  0,  q3, 0,  0,  q2],
                       [q2, 0,  0,  qt, 0,  0 ],
                       [0,  q2, 0,  0,  qt, 0 ],
                       [0,  0,  q2, 0,  0,  qt]])
        
        return Q


    def predict(self, track):
        """
        Predict step: predicts state x and estimation error covariance matrix P to next timestep
        
        :param:   track     track class object, holds x and P values
        :type:    track     <class.Track> object
        """
        x = track.x
        P = track.P
        F = self.F()
        Q = self.Q()
        
        #perform the predict step
        x = F * x     #project the state ahead
        P = F * P * F.transpose() + Q #project the error ahead
        
        #set values
        track.set_x(x)
        track.set_P(P)
        

    def update(self, track, meas):
        """
        Update step: performs the measurement update step
        
        :param:   track    track class object, holds x and P values
        :type:    track    <class.Track> object
        
        :param:   meas     measurements class object, holds z and R values
        :type:    meas     <class.Measurements> object
        """
        
        x = track.x
        P = track.P
        z = meas.z
        H = meas.sensor.get_H(x)                            #measurement function matrix
        
        #perform the update step
        gamma = self.gamma(track, meas)                     #gamma residual
        S = self.S(track, meas, H)                          #covariance of residual
        K = P * H.transpose() * np.linalg.inv(S)            #Kalman gain
        x = x + K * gamma                                   #state update
        I = np.identity(self.dim_state)                     #identity matrix
        P = (I - K * H) * P                                 #covariance update
        
        #set values
        track.set_x(x)
        track.set_P(P)
        
    
    def gamma(self, track, meas):
        """
        calculates and returns the residual gamma
        - gamma = z - h(x) in the non linear case (camera)
        - gamma = z - (H * x) in the linear case (lidar)
        
        :param:     track       track class object
        :type:      track       <class.Track>
        
        :param:     meas        measurement class object
        :type:      meas        <class.Measurement>
        
        :return:    gamma       residual gamma
        """
        x = track.x
        z = meas.z
        
        gamma = z - meas.sensor.get_hx(x)
        return gamma
        

    def S(self, track, meas, H):
        """
        calculates and returns covariance of residual uncertainty matrix S
        - S = (H * P * Htranspose) + R
        
        :param:     track       track class object
        :type:      track       <class.Track>
        
        :param:     meas        measurement class object
        :type:      meas        <class.Measurement>
        
        :param:     H           measurement function matrix
        :type:      H           np.matrix
        
        :return:    S           residual uncertainty matrix
        """
        
        R = meas.R      #measurement covariance matrix
        P = track.P     #initial uncertainty
        
        S = (H * P * H.transpose()) + R
        return S
        
        
