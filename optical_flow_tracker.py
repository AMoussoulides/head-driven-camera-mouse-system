
from math import sqrt

import numpy as np

import cv2
from numpy.core.fromnumeric import trace

def point_in_rect(rect,pt):
    logic = rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]
    return logic

MAX_CORNERS = 30

CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.3)

class Tracker:
    """Lucas-Kanade sparse optical flow tracker"""

    
    def __init__(self):
        self.track_len = 5
        self.tracks = []
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=CRITERIA)
        self.feature_params = dict(maxCorners=MAX_CORNERS,
                                   qualityLevel=0.1,
                                   minDistance=2,
                                   blockSize=7)
    
   

    def update_tracks(self, img_old, img_new,face_rect):
        """Update tracks."""
        # Get old points, using the latest one.
        points_old = np.float32([track[-1]
                                 for track in self.tracks]).reshape(-1, 1, 2)

        # Get new points from old points.
        points_new, _st, _err = cv2.calcOpticalFlowPyrLK(
            img_old, img_new, points_old, None, **self.lk_params)

        # Get inferred old points from new points.
        points_old_inferred, _st, _err = cv2.calcOpticalFlowPyrLK(
            img_new, img_old, points_new, None, **self.lk_params)

        # Compare between old points and inferred old points
        error_term = abs(
            points_old - points_old_inferred).reshape(-1, 2).max(-1)
        point_valid = error_term < 1

        new_tracks = []
        for track, (x, y), good_flag in zip(self.tracks, points_new.reshape(-1, 2), point_valid):
            # Track is good?
            if not good_flag:
                continue

            # New point is good, add to track.
            
            track.append((x, y))

            # Need to drop first old point?
            if len(track) > self.track_len:
                del track[0]

            # Track updated, add to track groups.
            new_tracks.append(track)

        # New track groups got, do update.
        self.tracks = new_tracks

    def get_new_tracks(self,p1,p2):
        """Get new tracks every detect_interval frames."""
        # Using mask to determine where to look for feature points.
        #mask = np.zeros_like(frame)
        #mask[roi[0]:roi[1], roi[2]:roi[3]] = 255

        #mask[ycoord:ycoord+hcoord, xcoord:xcoord+wcoord] = 255

        # Get good feature points.
        # feature_points = cv2.goodFeaturesToTrack(
        #     frame, mask=mask, **self.feature_params)
        
        feature_points = [p1,p2]
        # if feature_points is not None:

        #     cv2.cornerSubPix(frame, feature_points, (5, 5), (-1, -1), CRITERIA)

        #     if len(feature_points) < MAX_CORNERS:

        for x, y in np.float32(feature_points).reshape(-1, 2):
            self.tracks.append([(x, y)])




