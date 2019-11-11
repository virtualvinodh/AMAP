import cv2
import numpy as np
from scipy.spatial.distance import cdist


class Features(object):

    def __init__(self):
        super(Features, self).__init__()
        self.features = []

    def extractSIFT(self, image):
        # sift = cv2.xfeatures2d.SIFT_create(nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=100, sigma=2.6)
        sift = cv2.xfeatures2d.SIFT_create()
        # Extract SIFT Keypoints and Descriptors
        pts, des = sift.detectAndCompute(image, None)

        pts = self.unpack_keypoints(pts)

        self.features = [pts, des]
        return self.features

    def unpack_keypoints(self, arr):
        keypoints = np.array([], dtype=float).reshape(0, 2)
        for points in arr:
            tmp = np.array([points.pt[0], points.pt[1]], dtype=float)
            keypoints = np.vstack((keypoints, tmp))
            # print([points.size, points.response])
        return keypoints

    def compare_descr(self, feat1, feat2):
        thres = 0.99
        status = True
        final_points = np.array([], dtype=int).reshape(0, 1)
        final_qpoints = np.array([], dtype=int).reshape(0, 1)
        while status:
            valid_points = np.array([], dtype=int).reshape(0, 1)
            qpoints = np.array([], dtype=int).reshape(0, 1)
            count = 0
            for f1 in range(feat1.shape[0]):
                dist = cdist(np.asarray(feat1[f1, :], dtype=int).reshape(1, 128), feat2)
                sort_dist = np.sort(dist)
                sort_arg = np.argsort(dist)
                if sort_dist[0, 0] < thres * sort_dist[0, 1]:
                    valid_points = np.vstack((valid_points, sort_arg[0, 0].flatten()))
                    qpoints = np.vstack((qpoints, f1))
                    count += 1
            if count > 0:
                feat2 = np.delete(feat2, valid_points, axis=0)
            else:
                status = False
                
            final_qpoints = np.vstack((final_qpoints, qpoints))
            final_points = np.vstack((final_points, valid_points))

            del qpoints
            del valid_points
        
        return np.hstack((final_points, final_qpoints))
    
    def compare_descr_paaa(self, feat1, feat2, no_of_pts):
        final_points = np.array([], dtype=int).reshape(0, 1)
        final_qpoints = np.array([], dtype=int).reshape(0, 1)
        for f1 in range(feat1.shape[0]):
            dist = cdist(np.asarray(feat1[f1, :], dtype=int).reshape(1, 128), feat2)
            # sort_dist = np.sort(dist)
            sort_arg = np.argsort(dist)
            a = np.array(sort_arg.flatten()[0:no_of_pts], ndmin=2)
            final_points = np.vstack((final_points, a.T))
            tmp = np.ones((no_of_pts, 1), dtype=int) * f1
            final_qpoints = np.vstack((final_qpoints, tmp))
        
        return np.hstack((final_points, final_qpoints))
        
    def create_areas(self, *args):
        # arg[0] = (reduced points, corresponding query points)
        # arg[1] = book points
        # arg[2] = query points,
        # arg[3] = query dimensions
        points = args[0]
        book_points = args[1]
        query_points = args[2]
        dims = args[3]
        
        x1 = book_points[points[:, 0], 0] - query_points[points[:, 1], 0]
        y1 = book_points[points[:, 0], 1] - query_points[points[:, 1], 1]
        x2 = book_points[points[:, 0], 0] + (dims[1] - query_points[points[:, 1], 0])
        y2 = book_points[points[:, 0], 1] + (dims[0] - query_points[points[:, 1], 1])
        
        bboxes = np.vstack((x1, x2, y1, y2))
        return bboxes
