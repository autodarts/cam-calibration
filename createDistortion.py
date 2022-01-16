#!/usr/bin/env python
import os

import cv2
import numpy as np
import glob
import json
from tqdm import tqdm


class CreateDistortion:
    folder = "calibrationImages"
    CHECKERBOARD = (6, 9)  # Defining the dimensions of checkerboard
    width = 1920
    height = 1080

    def generateDistortionJson(self, width, height):
        self.width = width
        self.height = height

        distortion = []

        directory_contents = os.listdir(self.folder)
        for x in directory_contents:
            distortion.append(self.createDistortion(x, width, height))

        with open('distortion.json', 'w') as f:
            json.dump(distortion, f, indent=4)

        print("Creating distortion.json done.")

    def createDistortion(self, subfolder, width, height):
        self.width = width
        self.height = height

        print("Start generating distortion for cam {}...".format(subfolder))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Creating vector to store vectors of 3D points for each checkerboard image
        objpoints = []
        # Creating vector to store vectors of 2D points for each checkerboard image
        imgpoints = []

        # Defining the world coordinates for 3D points
        objp = np.zeros((1, self.CHECKERBOARD[0] * self.CHECKERBOARD[1], 3), np.float32)
        objp[0, :, :2] = np.mgrid[0:self.CHECKERBOARD[0], 0:self.CHECKERBOARD[1]].T.reshape(-1, 2)
        prev_img_shape = None

        filePath = "{}/{}/*.jpg".format(self.folder, subfolder)

        # Extracting path of individual image stored in a given directory
        images = glob.glob(filePath)
        for fname in tqdm(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD,
                                                     cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

            """
            If desired number of corner are detected,
            we refine the pixel coordinates and display 
            them on the images of checker board
            """
            if ret == True:
                objpoints.append(objp)
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, self.CHECKERBOARD, corners2, ret)

        h, w = img.shape[:2]

        """
        Performing camera calibration by 
        passing the value of known 3D points (objpoints)
        and corresponding pixel coordinates of the 
        detected corners (imgpoints)
        """
        try:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        except cv2.error as e:
            print("No valid picture found in {}", subfolder)

        obj = dict(
            K=mtx.tolist(),
            d=dist.tolist()[0],
            width=self.width,
            height=self.height,
            camera=subfolder
        )

        return obj
