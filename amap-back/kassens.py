# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 15:26:47 2018

@author: gares
"""
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import os
from enum import Enum

def sliceImage(img):
    scheibe = img[:,int(img.shape[1] / 2):int(img.shape[1] / 2) + 1]
    flat_list = [item for sublist in scheibe for item in sublist]
    #print(flat_list)
    plt.plot(flat_list)
    plt.show()

def filterGabor(img, lineHeight, shift, theta, folder, shouldWriteImage):
    scaled_kernel = cv2.getGaborKernel(ksize = (int(4 * lineHeight), int(4 * lineHeight)),
                                       sigma = lineHeight * 1, # laut paper * 1; aber bei syntetische Daten ist 0.5 besser
                                       theta = np.pi * theta,
                                       lambd = 2*lineHeight,
                                       gamma = 0.5,
                                       psi   = shift * np.pi,
                                       ktype = cv2.CV_32F)
    #print(scaled_kernel)
    if (shouldWriteImage):
        cv2.imshow('gabor kernel (scaled)', scaled_kernel)
        cv2.imwrite(folder + "gabor_kernel.png", scaled_kernel * 255)
        #plt.show()
    scaled_filtered_img = cv2.filter2D(img, cv2.CV_32F, scaled_kernel)
    #sliceImage(scaled_kernel)
    #cv2.imshow('scaled filtered image', scaled_filtered_img)
    return scaled_filtered_img

def findLineEndings(img, lineHeight, theta):
    kernel_lineEnding = cv2.getGaborKernel(ksize = (int(10 * lineHeight), int(10 * lineHeight)),
                                       sigma = lineHeight * 1.5,
                                       theta = np.pi * (theta + 0.5),
                                       lambd = lineHeight * 7,
                                       gamma = 0.2,
                                       psi   = np.pi * 0.5,
                                       ktype = cv2.CV_32F)
    #print(scaled_kernel)
    scaled_filtered_img = cv2.filter2D(img, cv2.CV_32F, kernel_lineEnding)
    #sliceImage(scaled_kernel)
    #cv2.imshow('scaled filtered image', scaled_filtered_img)
    return scaled_filtered_img


class Engine(object):
    def __init__(self, parameters):
        self.parameters = parameters
    def __call__(self, label_1, line_1, label_2, line_2, scale, theta):
        result = mergeLines(label_1, line_1, label_2, line_2, scale, theta)
        return result

class Pixel:
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.neighbours = []

    def __str__(self):
        return "(" + str(self.col) + ", " + str(self.row) + ")"

    def __repr__(self):
        return str(self)

    def __eq__(self, obj):
        return isinstance(obj, Pixel) and obj.col == self.col and obj.row == self.row

    def __mul__(self, other):
        self.col = self.col * other
        self.row = self.row * other
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        self.col = self.col + other
#        self.row = self.row + other
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def addNeighbour(self, pixel):
        isinstance(pixel, Pixel)
        self.neighbours.append(pixel)
        pixel.neighbours.append(self)

class LineType(Enum):
    BASE_LINE = 0
    MID_LINE = 1
    TOP_LINE = 2
    INTER_LINE = 3

class Line:
    def __init__(self, col, row, lineType):
        p = Pixel(col, row)
        self.pixels = [p]
        self.lineType = lineType
        self.leftMost = p
        self.rightMost = p
        self.upperMost = p
        self.lowerMost = p
        self.end = p
        self.start = p
        self.ends = []
        self.norm_vector = ()
        self.direction_vector = ()
        self.already_written = False

    def __str__(self):
        result = "["
        for e in self.pixels:
            result = result + str(e) + ", "
        result = result[:-2]
        result = result + "]"
        return result

    def __repr__(self):
        return str(self)

    def completeLine(self):
        visited = []
        self.ends = self.__findEndOfLine(visited, self.pixels[0])
        self.end = self.getEndOfLine()
        self.start = self.getStartOfLine()
        if (self.end == self.start and len(self.pixels) > 1):
            print("ERROR: could not find all endings!. Pxels: " + str(len(self.pixels)))
        return self.__calcNormalVector()

    def __calcNormalVector(self):
        count = 0
        avg_dy = 0
        avg_dx = 0
        avg_m = 0
        avg_b = 0
        for i in range(0, len(self.pixels) - 1):
            for j in range(i, len(self.pixels) - 1):
                p_1 = self.pixels[i]
                p_2 = self.pixels[j]
                direction_vector = Pixel(p_2.col - p_1.col, p_2.row - p_1.row)
                length = math.sqrt(math.pow(direction_vector.col, 2) + math.pow(direction_vector.row, 2))
                if (length < 5):
                    continue
                count = count + 1
                m = direction_vector.row / direction_vector.col if (direction_vector.col != 0) else 0
                b = p_1.row - (m * p_1.col)
                avg_m = avg_m + m
                avg_b = avg_b + b
                denominator = gcd(direction_vector.row, direction_vector.col)
                denominator = denominator if (denominator != 0) else 1
                avg_dy = avg_dy + (direction_vector.row / denominator)
                avg_dx = avg_dx + (direction_vector.col / denominator)
        if (count > 0):
            avg_m = avg_m / count
            avg_b = avg_b / count
            avg_dy = avg_dy / count
            avg_dx = avg_dx / count
#            print("Start: " + str(self.start) + "; End: " + str(self.end) + "; Slope: " + str(avg_m) + "; Offset: " + str(avg_b))
        else:
            print("Line irrelevant: " + str(len(self.pixels)))
            return False
#        print("Left Most: " + str(self.leftMost) + "; Right Most: " + str(self.rightMost))
#        avg_dy = (avg_m * self.leftMost.col + avg_b) - (avg_m * self.rightMost.col + avg_b)
#        avg_dx = ((self.leftMost.row - avg_b) / avg_m) - ((self.rightMost.row - avg_b) / avg_m) if avg_m > 0 else self.leftMost.col - self.rightMost.col
        self.norm_vector = (avg_dy, -avg_dx)
        self.direction_vector = (avg_dx, avg_dy)
        return True
#        print("Normal vector: " + str(self.norm_vector))
#        tmp = Pixel(int(np.round(self.norm_vector[0])), int(np.round(self.norm_vector[1])))
#        img = np.zeros((3500, 4900, 3), np.uint8)
#        shift = 400
#        added = connectTwoPixels(Pixel(tmp.col * -5, tmp.row * -5) + shift, tmp * 5 + shift)
#        for p in self.pixels:
#            img[p.row, p.col] = (255, 0, 0)
#        print(added)
#        for a in added:
#            if a[1] < img.shape[1] and a[0] < img.shape[0] and a[0] > 0 and a[1] > 0:
#                img[a[0], a[1]] = (0, 0, 255)
#        img[np.round(tmp.row), np.round(tmp.col)] = 255
#        cv2.imwrite("/home/gares/Dokumente/MasterThesis/results/norm_vector_" + str(self.pixels[0]) + ".png" , img)

    def isInMargin(self, line, distance):
        isinstance(line, Line)
        count = 0
        n_0 = np.divide(self.norm_vector, math.sqrt(math.pow(self.norm_vector[0], 2) + math.pow(self.norm_vector[1], 2)))
#        print("N_0: " + str(n_0))
        p = (self.pixels[0].col, self.pixels[0].row)
        if (np.dot(p, self.norm_vector) < 0):
            n_0 = np.dot(n_0, -1)
        d = np.dot(p, n_0)
#        if (not self.already_written):
#            self.already_written = True
#            img = np.zeros((3500, 4900, 3), np.uint8)
#        for i in range(0, img.shape[0] - 1):
#            for j in range(0, img.shape[1] - 1):
#                if (np.abs(np.dot(n_0, (j, i)) - d) < distance):
#                    img[i, j] = (255, 255, 255)
#            for p in self.pixels:
#                img[p.row, p.col] = (0, 0, 255)
#            cv2.imwrite("/home/gares/Dokumente/MasterThesis/results/margin_" + str(self.start) + ".png", img)
        for pixel in line.pixels:
            tmp = (pixel.col, pixel.row)
            result = np.dot(n_0, tmp) - d
            if np.abs(result) < distance:
#                print("Dot Product: " + str(np.dot(n_0, tmp)) + "; Result: " + str(result))
#                print("Endpoint: " + str(self.end))
#                print("Startpoint: " + str(line.start))
                count = count + 1
#        print("Is in margin: " + str(count > len(line.pixels) * 0.7))
#        print("Shape: " + str(img.shape[0]) + " times " + str(img.shape[1]))
#        if (count > len(line.pixels) * 0.7):
#            for j in range(0, img.shape[0] - 1):
#                for i in range(0, img.shape[1] - 1):
#                    if (np.abs(np.dot(n_0, (i, j)) - d) < distance):
#                        if (i < img.shape[1] and j < img.shape[0]):
#                            img[j, i] = (255, 255, 255)
        return count > len(line.pixels) * 0.7

    def addPixel(self, col, row):
        tmp = Pixel(col, row)
        if (tmp not in self.pixels):
            self.pixels.append(tmp)
            if (col < self.leftMost.col):
                self.leftMost = tmp
            if (col > self.rightMost.col):
                self.rightMost = tmp
            if (row < self.upperMost.row):
                self.upperMost = tmp
            if (row > self.lowerMost.row):
                self.lowerMost = tmp
            for p in self.pixels:
                deltaCol = np.abs(p.col - tmp.col)
                deltaRow = np.abs(p.row - tmp.row)
                if ((deltaCol == 1 or deltaCol == 0 ) and (deltaRow == 1 or deltaRow == 0)):
                    p.addNeighbour(tmp)
#        else:
#            print("Not Added: " + str(tmp))

    def hasTwoNeighbours(self, pixel):
        isinstance(pixel, Pixel)
        return len(pixel.neighbours) > 1

    def getEndOfLine(self):
        if (len(self.ends) == 1 and self.pixels[0] not in self.ends):
            self.ends.append(self.pixels[0])
        result = self.ends[0]
#        for pixel in self.ends:
#            deltaWidth = pixel.col - result.col
#            deltaHeight = pixel.row - result.row
#            if (deltaWidth > 0 or deltaHeight > 0):
#                result = pixel
        return result

    def getStartOfLine(self):
        if (len(self.ends) == 1 and self.pixels[len(self.pixels) - 1] not in self.ends):
            self.ends.append(self.pixels[len(self.pixels) - 1])
        result = self.ends[len(self.ends) - 1]
#        for pixel in self.ends:
#            # I need a better way to find the start pixel
#            deltaWidth = pixel.col - result.col
#            deltaHeight = pixel.row - result.row
#            if (deltaWidth < 0 or deltaHeight < 0):
#                result = pixel
        return result

    def __findEndOfLine(self, visited, p):
        isinstance(p, Pixel)
        finished = False
        toDo = self.pixels.copy()
        ends = []
        e = p
        while (not finished):
#            print("Done: " + str(len(visited)) + " of " + str(len(self.pixels)))
            if (all(x in visited for x in e.neighbours)):
#                print("Visited all Neighbours.")
                ends.append(e)
                if (len(toDo) > 0):
                    e = toDo[0]
            if (len(visited) == len(self.pixels)):
                finished = True
            n = next((x for x in e.neighbours if x not in visited and (x.col == e.col or x.row == e.row)), None)
            if (n is None):
                for t in e.neighbours:
                    if (t in visited):
                        continue
                    n = t
                    break
#            print("Visited: " + str(e) + ". Now changing to " + str(n))
            if (n is not None):
                visited.append(n)
                toDo.remove(n)
                e = n
            else:
                finished = True
#        print("Found Endings: " + str(ends))
        return ends


    def distance(self, line, orientation):
        isinstance(line, Line)
        shortest, dis = self.__shortesDistances(line)
        endPixel = shortest[0]
        startPixel = shortest[1]
#        theta = math.atan2(endPixel[1] - startPixel[1], endPixel[0] - startPixel[0])
#        print("Theta: " + str(theta))
        connectingVector = (startPixel.col - endPixel.col, startPixel.row - endPixel.row)
        angle = angle_between(connectingVector, (0, 1)) / np.pi
        weight = 1 + (np.abs(orientation - angle) * 3)
        result = dis * weight
#        print("From: " + str(endPixel) + " to " + str(startPixel) + "; Weight: " + str(weight) + "; result = " + str(result))
        return result

    def __shortesDistances(self, line):
        distance_list = []
        points = []
        dis_1 = math.sqrt(math.pow(self.end.col - line.end.col, 2) + math.pow(self.end.row - line.end.row, 2))
        distance_list.append(dis_1)
        points.append((self.end, line.end))
        dis_2 = math.sqrt(math.pow(self.end.col - line.start.col, 2) + math.pow(self.end.row - line.start.row, 2))
        distance_list.append(dis_2)
        points.append((self.end, line.start))
        dis_3 = math.sqrt(math.pow(self.start.col - line.end.col, 2) + math.pow(self.start.row - line.end.row, 2))
        distance_list.append(dis_3)
        points.append((self.start, line.end))
        dis_4 = math.sqrt(math.pow(self.start.col - line.start.col, 2) + math.pow(self.start.row - line.start.row, 2))
        distance_list.append(dis_4)
        points.append((self.start, line.start))
        idx = np.argmin(distance_list)
        return points[idx], distance_list[idx]

    def merge(self, line):
        isinstance(line, Line)
        shortest, dis = self.__shortesDistances(line)
        endPixel = shortest[0]
        startPixel = shortest[1]
#        print("From: " + str(endPixel) + " to " + str(startPixel))
        addedPixels = connectTwoPixels(endPixel, startPixel)
        for p in addedPixels:
            self.addPixel(p[1], p[0])
        for pixel in line.pixels:
            self.addPixel(pixel.col, pixel.row)
        return addedPixels

def connectTwoPixels(fromPixel, toPixel):
    isinstance(fromPixel, Pixel)
    isinstance(toPixel, Pixel)
    addedPixels = []
    width = toPixel.col - fromPixel.col
    height = toPixel.row - fromPixel.row
    slope = height / width if width != 0 and height != 0 else 1
#        print("Slope: " + str(slope) + " from " + str(endPixel) + " (" + self.lineType.name + ") " + " to " + str(startPixel) + " (" + line.lineType.name + ") ")
    b = fromPixel.row - (slope * fromPixel.col)
    if (width == 0):
        for i in range(0, np.abs(height)):
            col = fromPixel.col
            row = int(fromPixel.row + i * (height / np.abs(height)))
            if (row, col) not in addedPixels:
                addedPixels.append((row, col))
    elif (height == 0):
        for i in range(0, np.abs(width)):
            col = int(fromPixel.col + i * (width / np.abs(width)))
            row = fromPixel.row
            if (row, col) not in addedPixels:
                addedPixels.append((row, col))
    else:
        for i in range(0, np.abs(width)):
            col = int(fromPixel.col + i * (width / np.abs(width)))
            row = int(slope * col + b)
            if (row, col) not in addedPixels:
                addedPixels.append((row, col))
            tmp = row - int(slope * (col + 1) + b) if width > 0 else row - int(slope * (col - 1) + b)
            newRow = 0
            for j in range(1, np.abs(tmp)):
                newRow = int(row - (j * (tmp / np.abs(tmp))))
                if (newRow, col) not in addedPixels:
                    addedPixels.append((newRow, col))
            decimalSlope = np.abs(slope) - np.floor(np.abs(slope))
            if (row < int(slope * col + b + (decimalSlope * (i + 1)))):
                y = newRow if newRow > 0 else row
                y = y - 1 if slope > 0 else y + 1
                row = int(np.ceil(y)) if y > 0 else int(np.floor(y))
                if (row, col) not in addedPixels:
                    addedPixels.append((row, col))
    return addedPixels

def blurImage(img, lineHeight):
    blur_height = int(lineHeight)
    blur_width = int(3*lineHeight)
    if (blur_height % 2 != 1):
        blur_height = blur_height + 1
    if (blur_width % 2 != 1):
        blur_width = blur_width + 1
    print("height: " + str(blur_height) + "; width: " + str(blur_width))
    blur = cv2.GaussianBlur(img,(blur_width, blur_height),0)
    #cv2.imshow('blurred image', blur)
    #cv2.imwrite("/home/gares/Dokumente/MasterThesis/result_inverted_blurred.png", blur)
    return blur

def gcd(x, y):
   while(y):
       x, y = y, x % y

   return x

def mean_positive(L):
    # Get all positive numbers into another list
    pos_only = [y for x in L for y in x if y > 0]
    #pos_only = [x for x in L if x > 0]
    if pos_only:
        return sum(pos_only) /  len(pos_only)
    else:
        return 0

def mean_negative(L):
    # Get all positive numbers into another list
    neg_only = [y for x in L for y in x if y < 0]
    #neg_only = [x for x in L if x < 0]
    if neg_only:
        return sum(neg_only) /  len(neg_only)
    else:
        return 0

def reject_outliers(data, m=2):
    mean = np.mean(data)
    sd = np.std(data)
    final_list = [y for x in data for y in x if (y > mean - m * sd)]
    final_list = [y for x in data for y in x if (y < mean + m * sd)]
    return final_list

def getThreshold(scaled_filtered_img):
    min_value = np.min(scaled_filtered_img)
    max_value = np.max(scaled_filtered_img)
    print("Höchster Wert im response: " + str(max_value))
    print("Kleinster Wert im response: " + str(min_value))
    overall_average = np.average(scaled_filtered_img)
    print("Shape of image: " +str(scaled_filtered_img.shape))
    print("length of rejectedoutliers: " + str(len(reject_outliers(scaled_filtered_img, 40))))
    #shifted_image = reject_outliers(scaled_filtered_img, 40) - overall_average
    shifted_image = scaled_filtered_img - overall_average
    #plt.plot(shifted_image)
    positive_avg = mean_positive(shifted_image)
    negative_avg = mean_negative(shifted_image)
    print("Overall Std: ", np.std(scaled_filtered_img))
    print("Overall Average of Result: ", overall_average)
    print("Positiv Average of Result: ", positive_avg)
    print("Negativ Average of Result: ", negative_avg)
    plt.axhline(y=positive_avg*1.2)
    plt.axhline(y=negative_avg*1.2)
    plt.axhline(y=overall_average)
    #plt.show()
    threshold_pos = positive_avg * 1.2 + overall_average
    threshold_neg = negative_avg * 1.6 + overall_average
    plt.axhline(y=threshold_pos)
    plt.axhline(y=threshold_neg)
    plt.axhline(y=overall_average)
    return threshold_pos, threshold_neg, overall_average

def getThresholdAvg(scaled_filtered_img, threshold):
    overall_average = np.average(scaled_filtered_img)
    print("Average: " + str(overall_average))
    return (overall_average + np.abs(overall_average) * threshold), (overall_average - np.abs(overall_average) * threshold), overall_average
    #return 0, 0


def getThresholdMaxMinReduction(scaled_filtered_img, threshold):
#    overall_average = np.average(scaled_filtered_img)
#    min_val = np.min(scaled_filtered_img)
#    max_val = np.max(scaled_filtered_img)
    min_val, max_val, overall_average = getMinMaxAvgOfImage(scaled_filtered_img)
#    print("Average: " + str(overall_average))
    return (max_val - np.abs(max_val) * threshold), (min_val + np.abs(min_val) * threshold), overall_average
    #return 0, 0

def getMinMaxAvgOfImage(scaled_filtered_img):
    minimum = float('inf')
    maximum = float('-inf')
    avg = 0.0
    for y in range(0, scaled_filtered_img.shape[0] - 1):
        for x in range(0, scaled_filtered_img.shape[1] - 1):
            avg = avg + scaled_filtered_img[y,x]
            if scaled_filtered_img[y,x] < minimum:
                minimum = scaled_filtered_img[y,x]
            if scaled_filtered_img[y,x] > maximum:
                maximum = scaled_filtered_img[y,x]
    avg = avg / (scaled_filtered_img.shape[0] * scaled_filtered_img.shape[1])
    return minimum, maximum, avg

def getThresholdNonMaximum(scaled_filtered_img, threshold):
    values = []
    for y in range(0, scaled_filtered_img.shape[0] - 1):
        for x in range(0, scaled_filtered_img.shape[1] - 1):
            values.append(scaled_filtered_img[y,x])
    values.sort()
    threshold_neg = values[threshold]
    threshold_pos = values[len(values) - threshold]
    return threshold_pos, threshold_neg, values[int(len(values)/20)]

def calcHessian(scaled_filtered_img):
    dxx = cv2.Sobel(scaled_filtered_img, cv2.CV_8UC1, 2, 0, 5)
    dyy = cv2.Sobel(scaled_filtered_img, cv2.CV_8UC1, 0, 2, 5)
    dxy = cv2.Sobel(scaled_filtered_img, cv2.CV_8UC1, 1, 1, 5)
    for y in range(0, scaled_filtered_img.shape[0] - 1):
        for x in range(0, scaled_filtered_img.shape[1] - 1):
            hessian_Matrix = np.array([[dxx[y,x], dxy[y,x]], [dxy[y,x], dyy[y,x]]])
            hessian = np.mat(hessian_Matrix)
            w,v = np.linalg.eig(hessian)
            M = np.linalg.multi_dot([w,v])
            print(angle_between((0,1), np.squeeze(np.asarray(M))) * 180/np.pi)
            v = np.squeeze(np.asarray(v[:,0].transpose()))
            y_1 = int(y + v[0])
            x_1 = int(x + v[1])
            cv2.arrowedLine(scaled_filtered_img, (y,x), (y_1, x_1), (0,0,255), 1)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def avgLineHeight(img):
    img_row_sum = np.sum(img,axis=1).tolist()

    plt.plot(img_row_sum)
    plt.show()

    gradients = [];
    for i in range(len(img_row_sum) - 1):
        gradients.append(np.abs(img_row_sum[i+1] - img_row_sum[i]))

    plt.plot(gradients)
    plt.show()

    abs_max = max(gradients)
    print("Highest value: " + str(abs_max))

    max_vals = [];
    for j in range(len(gradients) - 1):
        if (gradients[j] > gradients[j+1]):
            if (gradients[j] > (abs_max / 2)):
                max_vals.append(j)

    summe = 0
    print("Anzahl Max Values: " + str(len(max_vals)))
    for i in range(0, len(max_vals) - 1, 2):
        summe = summe + (max_vals[i + 1] - max_vals[i])

    avg = summe * 2 / len(max_vals)
    print("Durchschnitt: " + str(avg))
    #avg = 10
    print("Max Values: " + str(max_vals))
    return avg

def nonMaximalSupress(image,NHoodSize):
    #
    dX, dY = NHoodSize
    M, N = image.shape
    for x in range(0,M-dX+1):
        for y in range(0,N-dY+1):
            window = image[x:x+dX, y:y+dY]
            if np.sum(window)==0:
                localMax=0
            else:
                localMax = np.amax(window)
            maxCoord = np.argmax(window)
            # zero all but the localMax in the window
            window[:] = 0
            window.flat[maxCoord] = localMax
    return image

def findLineComponents(lineImage, secondOrder, topAndBase, theta, scale, path, endings, shouldBeTmpImagesWritten):
    output = cv2.connectedComponentsWithStats(lineImage, 8, cv2.CV_32S)
    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]
    # The second cell is the label matrix
    labels = output[1]
    # The third cell is the stat matrix
    stats = output[2]
    # The fourth cell is the centroid matrix
    #centroids = output[3]
    # Map component labels to hue val
#    label_hue = np.uint8(179*labels/np.max(labels))
#    blank_ch = 255*np.ones_like(label_hue)
#    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
#    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
#    labeled_img[label_hue==0] = 0
    labeled_img = np.zeros((lineImage.shape[0], lineImage.shape[1], 3), np.uint8)
    for y in range(0, labels.shape[0]):
        for x in range(0, labels.shape[1]):
            if (labels[y,x] == 0):
                continue
            if (labels[y,x] % 3 == 0):
                labeled_img[y,x] = (255, 0, 0)
            elif (labels[y,x] % 3 == 1):
                labeled_img[y,x] = (0, 0, 255)
            else:
                labeled_img[y,x] = (0, 255, 0)

    if (shouldBeTmpImagesWritten):
        cv2.imwrite(path + "_Components.png", labeled_img)

    components = dict()

    if num_labels == 0:
        print("No connected componentes found.")
        return components
#    lineNumber = 0
    print("Creating Lines...")
    for y in range(0, labels.shape[0]):
        for x in range(0, labels.shape[1]):
            #Skip Background
            if (labels[y,x] == 0):
                continue
            #Skip small components
#            if (stats[labels[y,x], cv2.CC_STAT_AREA] < scaled_filtered_img.shape[1] * 0.02):
#                continue
            if (stats[labels[y,x], cv2.CC_STAT_AREA] < scale):
                continue
            if (labels[y,x] not in components):
                lineType = LineType.BASE_LINE
                if (topAndBase):
                    if (secondOrder[y,x] < 0):
                        lineType = LineType.TOP_LINE
                    else:
                        lineType = LineType.BASE_LINE
                else:
                    if (secondOrder[y,x] < 0):
                        lineType = LineType.MID_LINE
                    else:
                        lineType = LineType.INTER_LINE
                line = Line(x, y, lineType)
                components[labels[y,x]] = line
            else:
                components[labels[y,x]].addPixel(x,y)

    tmp = np.zeros((lineImage.shape[0], lineImage.shape[1], 3), np.uint8)
    for label, line in components.items():
        for p in line.pixels:
            tmp[p.row, p.col] = (255, 0, 0) if line.lineType == LineType.TOP_LINE or line.lineType == LineType.MID_LINE else (0, 0, 255)

    if (shouldBeTmpImagesWritten):
        cv2.imwrite(path + "_removedSmall.png", tmp)

    #Complete Lines
    toBeRemoved = []
    for label, line in components.items():
        if (not line.completeLine()):
            toBeRemoved.append(label)
            continue
        vector = line.direction_vector if not endings else line.norm_vector
        vector = (vector[0], vector[1] * -1) # Since coordinate system is inverted
        angle = angle_between(vector, (0, 1)) / np.pi
#        print("Label: " + str(label))
#        print("Angle: " + str(angle) + "; Vector: " + str(vector) + "; Dif: " + str(np.abs(angle - theta) % 1))
        if (np.abs(angle - theta % 1) > 0.035):
#        if (np.abs(angle - theta) % 1 > 0.1):
#            print("... removed")
            toBeRemoved.append(label)
    for label in toBeRemoved:
        del components[label]

    tmp = np.zeros(lineImage.shape, np.uint8)
    for label, line in components.items():
        for p in line.pixels:
            tmp[p.row, p.col] = 255

    if (shouldBeTmpImagesWritten):
        cv2.imwrite(path + "_removedWrongAngle.png", tmp)

    print("... Lines Completed. Merging " + str(len(components.items())) + " Lines...")
    toBeRemoved = []
    distance = []
    added = []
    addedImg = np.zeros(lineImage.shape, np.uint8)
    parameters = []

    for label, line in components.items():
#        print(str(label) + " of " +  str(len(components)))
        for label_2, line_2 in components.items():
            idx = (label, label_2) if (label < label_2) else (label_2, label)
            if label == label_2 or idx in distance or line.distance(line_2, theta) > scale * 3:
                continue
            distance.append(idx)
            parameters.append((label, line, label_2, line_2, scale, theta))

    print("Start Merging... " + str(len(parameters)))
#    n = 300
    res = []
#    for chunk in [parameters[i:i + n] for i in range(0, len(parameters), n)]:
#        print("Chunk " + str(len(chunk)))
#        pool = Pool(4)
#        res.extend(pool.map(mergeHelper, chunk))
#        # Ok parameter liste ist nicht das Problem.
#        pool.close()
#        pool.join()
#        pool.terminate()

#    if (len(parameters) <= 200):
#        pool = Pool(4)
#        res = pool.map(mergeHelper, parameters)
#    else:
    mergeMap = dict()
    for p in parameters:
        res.append(mergeHelper(p, mergeMap))

#    for label, line in components.items():
#        calcHoughLines(line, lineImage, path, out)

    print("... Lines Merged")
    for added, toBeRemoved, dis in res:
        for p in added:
            if (p[0] < lineImage.shape[0] and p[1] < lineImage.shape[1]):
                addedImg[p[0], p[1]] = 255
                lineImage[p[0], p[1]] = 100
#        if (len(distance) > 0):
#        print("Removing Components: " + str(toBeRemoved))
        for l in toBeRemoved:
            if (l in components):
                del components[l]

    tmp = np.zeros((lineImage.shape[0], lineImage.shape[1], 3), np.uint8)
    for label, line in components.items():
        for p in line.pixels:
            tmp[p.row, p.col] = (255, 0, 0) if line.lineType == LineType.TOP_LINE or line.lineType == LineType.MID_LINE else (0, 0, 255)

    if (shouldBeTmpImagesWritten):
        cv2.imwrite(path + "_removedMerged.png", tmp)
        cv2.imwrite(path + "_added.png", addedImg)
    return components

def calcHoughLines(line, orig_img, path, out):
    isinstance(line, Line)
    img = np.zeros(orig_img.shape, np.uint8)
    for l in line.pixels:
        img[l.row, l.col] = 1
    houghLines = cv2.HoughLinesP(img, 1, np.pi / 180, 120, None, 1, orig_img.shape[1])

    if houghLines is not None:
        for i in range(0, len(houghLines)):
            l = houghLines[i][0]
            cv2.line(out, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv2.LINE_AA)

def mergeHelper(parameters, mergedMap):
    return mergeLines(*parameters, mergedMap)

def mergeLines(label, line, label_2, line_2, scale, theta, mergeMap):
    dis = line.distance(line_2, theta)
#    print("From: " + str(label) + ", To: " + str(label_2))
#    print("Distanz: " + str(dis) + "; threshold: " + str(scale * 1.5))
    added = []
    toBeRemoved = []
#    if (dis <= scale * 3 and line.lineType is line_2.lineType):
#    tmp = np.zeros((1500, 900, 3), np.uint8)
    # Tried distance factors: 10, 5
    if (line.lineType is line_2.lineType and line.isInMargin(line_2, scale * 1) and dis <= scale * 3 ):
#        print("Line: " + str(label) + "; Endpoint: " + str(line.end))
#        print("Line 2: " + str(label_2) + "; Startpoint: " + str(line_2.start))
#        print("Line: " + str(label) + " Line 2: " + str(label_2))
        if(label in mergeMap):
#            print("Already merged... " + str(label))
            tmp = mergeMap[label]
            added = tmp.merge(line_2)
            tmp.completeLine()
            mergeMap[label_2] = tmp
        else:
#            print("New merged...")
            added = line.merge(line_2)
            line.completeLine()
            mergeMap[label_2] = line
#        for a in added:
#            tmp[a[0], a[1]] = (0, 255, 0)
#        cv2.imwrite("/home/gares/Dokumente/MasterThesis/results/margin_" + str(line.start) + "_" + str(line_2.start) + ".png", tmp)
#        print("Added: " + str(len(added)) + "; Merged: " + str(len(line.pixels)) + " pixels.")
        toBeRemoved.append(label_2)
    return added, toBeRemoved, 0

def thresholding(scaled_filtered_img):
    stepSize = int(scaled_filtered_img.shape[0] / 10)
    window_size = int(scaled_filtered_img.shape[0] / 10)
    window_shape = (window_size, window_size)
    for y in range(0, scaled_filtered_img.shape[0], stepSize):
        for x in range(0, scaled_filtered_img.shape[1], stepSize):
            window = scaled_filtered_img[y:y + window_shape[1], x:x + window_shape[0]]
            threshold_pos, threshold_neg, avg = getThresholdMaxMinReduction(window, 0.6)
#                    print("Average of response map: ", avg)
#                    print("Positiv threshold of response map: ", threshold_pos)
#                    print("Negativ threshold of response map: ", threshold_neg)

#                    sliceImage(scaled_filtered_img)

            for y_2 in range(0, window.shape[0]):
                for x_2 in range(0, window.shape[1]):
                    tmp = scaled_filtered_img[y + y_2, x + x_2]
                    scaled_filtered_img[y + y_2, x + x_2] = tmp if ((tmp >= threshold_pos or tmp <= threshold_neg) and np.abs(tmp) > 5 ) else avg
    return scaled_filtered_img

def getZeroCrossings(scaled_filtered_img, filePath, shouldWriteImage = True):
    dx = cv2.Sobel(scaled_filtered_img, cv2.CV_32F, 1, 0, 1)
    dy = cv2.Sobel(scaled_filtered_img, cv2.CV_32F, 0, 1, 1)
    if (shouldWriteImage):
        sliceImage(dx)
        sliceImage(dy)
    energy_x = 0.0
    energy_y = 0.0
    for y in range(0, scaled_filtered_img.shape[0] - 1):
        for x in range(0, scaled_filtered_img.shape[1] - 1):
            energy_x = energy_x + dx[y, x]*dx[y, x]
            energy_y = energy_y + dy[y, x]*dy[y, x]
    energy_x = np.sqrt(energy_x)
    energy_y = np.sqrt(energy_y)
    print("X-Direction: " + str(energy_x) + "; y-Direction: " + str(energy_y))
    m = np.max(dx)
#    ret, img = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    if (energy_x > energy_y):
        tmp = cv2.convertScaleAbs(dx, alpha=255/m)
        if (shouldWriteImage):
            cv2.imwrite(filePath + "_dx.png", tmp)
    else:
        tmp = cv2.convertScaleAbs(dy, alpha=255/m)
        if (shouldWriteImage):
            cv2.imwrite(filePath + "_dy.png", tmp)

    ## Finding zero crossings in x-direction
    marked_Pixels = []
    for y in range(0, scaled_filtered_img.shape[0] - 1):
        for x in range(0, scaled_filtered_img.shape[1] - 1):
            if (energy_x > energy_y):
                if (dx[y, x] == 0.0):
                    if (dx[y, x - 1] * dx[y, x + 1] < 0.0):
                        marked_Pixels.append((y,x))
                else:
                    if (dx[y , x] * dx[y, x + 1] < 0.0):
                        marked_Pixels.append((y,x))
            else:
                if (dy[y, x] == 0.0):
                    if (dy[y - 1, x] * dy[y + 1, x] < 0.0):
                        marked_Pixels.append((y,x))
                else:
                    if (dy[y , x] * dy[y + 1, x] < 0.0):
                        marked_Pixels.append((y,x))
    return marked_Pixels

def skeletonize(img):
    """ OpenCV function to return a skeletonized version of img, a Mat object"""

    #  hat tip to http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

    img = img.copy() # don't clobber original
    skel = img.copy()

    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

    while True:
        eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img[:,:] = eroded[:,:]
        if cv2.countNonZero(img) == 0:
            break

    return skel

def findTopAndBaseLines(img, scale, theta):
    return findLines(img, scale, 0.5, theta)

def findMidAndInterLines(img, scale, theta):
    return findLines(img, scale, 1.0, theta)

def findAndDrawTopBaseLines(img, scale, theta):
    return drawDetectedLines(img, findLines(img, scale, 0.5, theta))

def findAndDrawMidInterLines(img, scale, theta):
    return drawDetectedLines(img, findLines(img, scale, 1.0, theta))

def findAndDrawAllLines(img, scale, theta):
    tmp = findTopAndBaseLines(img, scale, theta)
    tmp2 = findMidAndInterLines(img, scale, theta)
    tmp = {**tmp, **tmp2}
    return drawDetectedLines(img, tmp)

def convoveGablet(img, scale, psi, theta):
    img = 255-img
    ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    blur = th2

    return filterGabor(blur, scale, psi, theta, "", False)

def convertResponseMap(responseMap):
    m = np.max(responseMap)
    tmp = cv2.convertScaleAbs(responseMap, alpha=255/m)
    return tmp

def findLines(img, scale, psi, theta):

    scaled_filtered_img = convoveGablet(img, scale, psi, theta)

    #Second Order Derivitiv before Thresholding
    secondOrderDerivitiv = cv2.Laplacian(scaled_filtered_img, cv2.CV_32F)

    ## Thresholding
    ## In case of syntetic image, thresholding makes it worse
    scaled_filtered_img = thresholding(scaled_filtered_img)

    ## Find Pixels that are the line (zero crossings)
    marked_Pixels = getZeroCrossings(scaled_filtered_img, "", False)

    lines = np.zeros(scaled_filtered_img.shape, np.uint8)
    for m in marked_Pixels:
        lines[m[0], m[1]] = 255


    components = findLineComponents(lines, secondOrderDerivitiv, psi == 0.5, theta, scale, "", False, False)
    return components

def drawDetectedLines(img, lines):
    print("Components found. Now writing lines to original image...")
    backtorgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    for label, line in lines.items():
        for p in line.pixels:
            backtorgb[p.row, p.col] = (255, 0, 0) if line.lineType == LineType.TOP_LINE or line.lineType == LineType.MID_LINE else (0, 0, 255)

    return backtorgb

'''
folder_str = "/home/gares/Dokumente/MasterThesis/Manuskript Images/"
#folder_str = "/home/gares/Dokumente/MasterThesis/Syntetic Images/"
folder_results = "/home/gares/Dokumente/MasterThesis/results/"
#imageName = "LeipzigTestImage.png"
#imageName = "LeipzigTestImageCutout.png"
#imageName = "LeipzigTestImageLineBlock.png"
#imageName = "LeipzigTestImageLineDiag.png"
#imageName = "Test_Sample_U_Heidelberg.jpg"
imageName = "ICDAR_2019_Plutarchus_Vitae_illustrium_virorum_Plutarchus_(0046_-0120_)_btv1b8446958b_193.jpeg"
#imageName = "NanYuanChun.png"
#imageName = "linesCurved_step_46_background_130_foreground_120_0.00015.png"
#imageName = "linesCurved_step_46_background_130_foreground_120_0.00025.png"
#imageName = "linesCurved_step_46_background_130_foreground_120_0.00035.png"
#imageName = "linesCurved_step_46_background_150_foreground_100_0.00015.png"
#imageName = "linesCurved_step_46_background_150_foreground_100_0.00025.png"
#imageName = "linesCurved_step_46_background_150_foreground_100_0.00035.png"
#imageName = "linesCurved_step_46_background_200_foreground_50_0.00015.png"
#imageName = "linesCurved_step_46_background_200_foreground_50_0.00025.png"
#imageName = "linesCurved_step_46_background_200_foreground_50_0.00035.png"
#imageName = "linesCurved_step_46_background_255_foreground_0_0.00015.png"
#imageName = "linesCurved_step_46_background_255_foreground_0_0.00025.png"
#imageName = "linesCurved_step_46_background_255_foreground_0_0.00035.png"
imageAsStr = folder_str + imageName
#lineImage = cv2.cvtColor(lineImage, cv2.COLOR_BGR2GRAY)

scales = range(11, 30, 2)
#scales = [23]
shifts = [0.5, 1.0]
#shifts = [1.0]
thetas = [0.5, 0.75, 1.0, 1.25]
#thetas = [0.5]
for scale in scales:
    for theta in thetas:
        allComponents = dict()
        lineImage = cv2.imread(imageAsStr, cv2.CV_8UC1)
        #rows, cols = lineImage.shape
        #M = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
        #lineImage = cv2.warpAffine(lineImage, M, (cols, rows))
        img = 255-lineImage

        #blur = blurImage(img, avg)
        ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        blur = th2

        lineEndings = findLineEndings(blur, scale, theta)
        sod_LineEnding = cv2.Laplacian(lineEndings, cv2.CV_32F)
        filteredLineEnding = thresholding(lineEndings)
        marked_Pixels_endLines = getZeroCrossings(filteredLineEnding, "")
        foundEndings = np.zeros(lineImage.shape, np.uint8)
        for m in marked_Pixels_endLines:
            foundEndings[m[0], m[1]] = 255

        for psi in shifts:
            print("################# Scale: " + str(scale) + " ##### Theta: " + str(theta) + " ##### Shift: " + str(psi))
            targetName = ""
            if (psi == 0.5):
                targetName = "Top_And_Base"
            else:
                targetName = "Mid_And_Inter"

            folderPath = folder_results + "/" + imageName + "/" + targetName + "/" + "Theta" + str(theta) + "/"
            os.makedirs(name=folderPath , exist_ok=True)

            scaled_filtered_img = filterGabor(blur, scale, psi, theta, folderPath, True)
            print("Plotting Reponse Slice")
            sliceImage(scaled_filtered_img)
            print("Finished Plotting Response Slice.")
            m = np.max(scaled_filtered_img)
            tmp = cv2.convertScaleAbs(scaled_filtered_img, alpha=255/m)
            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_responsMap.png", tmp)
            response_map = scaled_filtered_img.copy()
            #calcHessian(scaled_filtered_img)

            #cv2.imwrite(folder_results + "result_" + imageName + "_" + targetName + "_scale" + str(scale) + "_responseMap.png", scaled_filtered_img)
            #print(scaled_filtered_img)

            #Second Order Derivitiv before Thresholding
            secondOrderDerivitiv = cv2.Laplacian(scaled_filtered_img, cv2.CV_32F)

            ## Thresholding
            ## In case of syntetic image, thresholding makes it worse
            scaled_filtered_img = thresholding(scaled_filtered_img)
#            print("Plotting Threshold Slice")
#            sliceImage(scaled_filtered_img)
#            print("Finished Plotting Threshold Slice.")
            m = np.max(scaled_filtered_img)
            tmp = cv2.convertScaleAbs(scaled_filtered_img, alpha=255/m)
            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_threshold.png", tmp)

            #threshold_pos, threshold_neg, avg = getThresholdNonMaximum(scaled_filtered_img, 20)
#            threshold_pos, threshold_neg, avg = getThreshold(scaled_filtered_img)
#            for y in range(0, scaled_filtered_img.shape[0] - 1):
#                for x in range(0, scaled_filtered_img.shape[1] - 1):
#                    tmp = scaled_filtered_img[y, x]
#                    scaled_filtered_img[y, x] = tmp if (tmp >= threshold_pos or tmp <= threshold_neg) else 0

            # Find Zero Crossings
            marked_Pixels = getZeroCrossings(scaled_filtered_img, folderPath + imageName + "_scale" + str(scale))


            print("Marked pixels as line: " + str(len(marked_Pixels)))
            #sliceImage(scaled_filtered_img)

            lines = np.zeros(scaled_filtered_img.shape, np.uint8)
            allFoundings = np.zeros(scaled_filtered_img.shape, np.uint8)
            lines_values = []
            for m in marked_Pixels:
#                lineImage[m[0], m[1]] = 0
#                blur[m[0], m[1]] = 255
                lines[m[0], m[1]] = 255
#                allFoundings[m[0], m[1]] = 255
                lines_values.append(response_map[m[0], m[1]])

            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_Lines.png", lines)
            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_Endings.png", foundEndings)

            components = findLineComponents(lines, secondOrderDerivitiv, targetName, theta, scale, folderPath + imageName + "_scale" + str(scale), False, True)

            allComponents = {**allComponents, **components}

            print("Writing results...")
            components_Of_Endings = findLineComponents(foundEndings, sod_LineEnding, "Endings", theta, scale, folderPath + imageName + "_scale" + str(scale), True, True)

            print("Components found. Now writing lines to original image...")
            backtorgb = cv2.cvtColor(lineImage, cv2.COLOR_GRAY2RGB)

            fixed_lines = np.zeros(scaled_filtered_img.shape, np.uint8)
            fixed_lineEndings = np.zeros(scaled_filtered_img.shape, np.uint8)
            for label, line in components.items():
                for p in line.pixels:
                    allFoundings[p.row, p.col] = 255
                    fixed_lines[p.row, p.col] = 255
                    backtorgb[p.row, p.col] = (255, 0, 0) if line.lineType == LineType.TOP_LINE or line.lineType == LineType.MID_LINE else (0, 0, 255)

            for label, line in components_Of_Endings.items():
                for p in line.pixels:
                    allFoundings[p.row, p.col] = 255
                    fixed_lineEndings[p.row, p.col] = 255
                    backtorgb[p.row, p.col] = (255, 0, 0) if line.lineType == LineType.TOP_LINE or line.lineType == LineType.MID_LINE else (0, 0, 255)
    #            for windowImage in components:
    #                ((upper_most, left_most), (lower_most,right_most)) = components[windowImage]
    #                crop_orig_img = lineImage[upper_most:lower_most, left_most:right_most]
    #                cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_compIdx_" + str(windowImage) + "result.png", crop_orig_img)
            #cv2.imshow("Filtered Lines", lines)
            #cv2.imshow("Lines", lineImage)
            #cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_result.png", lineImage)
            os.makedirs(name=folderPath , exist_ok=True)
            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_result.png", backtorgb)
            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_Lines_fixed.png", fixed_lines)
            cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_Endings_fixed.png", fixed_lineEndings)
        folderPath = folder_results + "/" + imageName + "/Combined/" + "Theta" + str(theta) + "/"
        cv2.imwrite(folderPath + imageName + "_scale" + str(scale) + "_All.png", allFoundings)
        #cv2.imshow("Blurred with Lines", blur)

        #sliceImage(blur)
        #sliceImage(scaled_filtered_img)

#            plt.axhline(y=threshold_pos)
#            plt.axhline(y=threshold_neg)
#            plt.axhline(y=avg)
#            print("Response map and derivetive of it:")
        plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()
'''