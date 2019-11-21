from flask import Flask, jsonify, request
from flask_cors import CORS
from io import BytesIO
import json
import re
import shutil
import base64
import requests
import tesserocr as tes
from PIL import Image
import subprocess as sp
import os, sys
import cv2 as cv
import numpy as np
import csv
from query import Query
import skimage
import skimage.morphology
import math

import kassens

from datetime import datetime

#### Support black and white
import locale
locale.setlocale(locale.LC_ALL, "C")

import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    # __file__ refers to the file settings.py
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
    APP_STATIC = os.path.join(APP_ROOT, 'static')

    return APP_ROOT + ' ' + APP_STATIC + ' ' + 'OpenCV Version ' + cv. __version__ + 'Scikit_image version ' + skimage.__version__


@app.route('/amap/api/demo/<int:num>', methods=['GET'])
def amap_api(num):
    return "Your API works " + str(num)


def cv_decode_base64(url, mode=cv.COLOR_RGB2BGR, type="opencv"):
    if 'data:image' not in url:
        print('I am here')
        img_data = base64.b64encode(requests.get(request.json['url']).content)
        img_format = 'data:image/' + url.split('.')[-1] + ';base64'
    else:
        img_format, img_data = url.split(',')[0], url.split(',')[1]
    pil_image = Image.open(BytesIO(base64.b64decode(img_data)))

    if type == "opencv":
        img = cv.cvtColor(np.array(pil_image), mode)
    elif type == "nparray":
        img = np.array(pil_image)

    return img_format, img


def cv_encode_base64(img_format, img, type = "opencv"):
    extension = img_format.replace('data:image/', '').replace(';base64', '')

    print(extension)
    if extension == 'jpeg': # Check for other formats
        file_ext = '.jpg'
    else:
        file_ext = '.' + extension
    if type == "opencv":
        retval, img_output_64 = cv.imencode(file_ext, img) #change it to te image type using format
        img_data64 = base64.b64encode(img_output_64).decode('utf-8')
    elif type == "nparray":
        print(img)
        pil_img = Image.fromarray(img)
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")
        img_data64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    img_base64 = img_format + ',' + img_data64
    return img_base64


@app.route('/amap/api/upload', methods=['POST'])
def upload_image():
    return "success"

def topbase_lines(img, parameters):
    grey=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    print(parameters)

    return kassens.findAndDrawTopBaseLines(grey, parameters['scale'], parameters['theta'])

def hough_line(img, parameters):
    dst = img

    try:
        cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    except:
        cdst = img
        dst = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

    lines = cv.HoughLines(dst, 1, np.pi / 180, parameters['threshold'], None, 0, 0)

    print('The found lines are ')
    print(lines)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(cdst, pt1, pt2, (0,0,255), 1, cv.LINE_AA)

    return cdst

def hough_line_prob(img, parameters):
    dst = img

    try:
        cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    except:
        cdst = img
        dst = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

    print('The parameters of hough line prob are')
    print(parameters)

    lines = cv.HoughLinesP(dst, 1, np.pi / 180, threshold = parameters['threshold'], minLineLength = parameters['min_length'], maxLineGap = parameters['max_gap'])

    print('The found lines are ')
    print(lines)

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(cdst, (x1, y1), (x2, y2), (0, 0, 255), 1)

    return cdst

def midinter_lines(img, parameters):
    grey=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return kassens.findAndDrawMidInterLines(grey, parameters['scale'], parameters['theta'])

def all_lines(img, parameters):
    grey=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return kassens.findAndDrawAllLines(grey, parameters['scale'], parameters['theta'])

def opencv_binarization(img, parameters):
    ret, thresholded = cv.threshold(img, parameters['threshold'], 255, getattr(cv, parameters['type']))
    return thresholded


def canny(img, parameters):
    edges = cv.Canny(img, parameters['threshold1'], parameters['threshold2'], parameters['aperture_size'])
    return edges


def blur(img, parameters):
    blur = cv.blur(img, (parameters['kernelX'], parameters['kernelY']))
    return blur


def guassian_blur(img, parameters):
    blur = cv.GaussianBlur(img, (parameters['kernelX'], parameters['kernelY']), 0)
    return blur


def median_blur(img, parameters):
    blur = cv.medianBlur(img, parameters['kernel'])
    return blur


def bilateral_filter(img, parameters):
    blur = cv.bilateralFilter(img, parameters['kernel'], parameters['sigma'], parameters['sigma'])
    return blur


def orb_keypoints(img, parameters):
    orb = cv.ORB_create()
    grey=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    kp = orb.detect(grey,None)

    kp = cv.drawKeypoints(img,kp,None,color=(125,0,0), flags=0)
    return kp

def good_features_to_track(img, parameters):
    orb = cv.ORB_create()
    grey=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    corners = cv.goodFeaturesToTrack(grey,25,0.01,10)
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv.circle(img,(x,y),3,(0,125,0),-1)

    return img

def skeletonize(img, parameters):
    img = skimage.morphology.skeletonize(skimage.util.img_as_bool(skimage.util.invert(img)))

    return skimage.util.img_as_ubyte(skimage.util.invert(skimage.util.img_as_ubyte(img)))

def medial_axis(img, parameters):
    img = skimage.morphology.medial_axis(skimage.util.img_as_bool(skimage.util.invert(img)))

    return skimage.util.invert(skimage.util.img_as_ubyte(img))

def thin(img, parameters):
    img = skimage.morphology.thin(skimage.util.img_as_bool(skimage.util.invert(img)))

    return skimage.util.invert(skimage.util.img_as_ubyte(img))

def nonlocal_denoising_gray(img, parameters):
    img = cv.fastNlMeansDenoising(img,None,parameters['filter_strength'],parameters['template'],parameters['search'])

    return img

def nonlocal_denoising_color(img, parameters):
    img = cv.fastNlMeansDenoisingColored(img,None,parameters['filter_strength'], parameters['filter_strength_color'], parameters['template'],parameters['search'])

    return img

def add_random_noise(img, parameters):
    img = skimage.util.random_noise(img)

    if parameters['type'] == 'gaussian' or parameters['type'] == 'speckle':
        img = skimage.util.random_noise(img, mode=parameters['type'], mean = parameters['mean'], var = parameters['var'])
    elif parameters['type'] == 'salt' or parameters['type'] == 'pepper':
        img = skimage.util.random_noise(img, mode=parameters['type'], amount = parameters['amount'])
    elif parameters['type'] == 's&p':
        img = skimage.util.random_noise(img, mode=parameters['type'], amount = parameters['amount'], salt_vs_pepper = parameters['salt_vs_pepper'])

    return skimage.util.img_as_ubyte(img)

def histogram_eq_color(img, parameters):
    try:
        img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
        # equalize the histogram of the Y channel

        img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])

        # convert the YUV image back to RGB format
        equ = cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)
    except:
        equ = cv.equalizeHist(img)

    return equ


@app.route('/amap/api/processing', methods=['POST'])
def processing():
    parameters = json.loads(request.json['parameters'])
    process = request.json['processing'].replace(' ', '_').lower()

    print('Peforming from processing')

    ## Some processes need color
    ## As of now everything is read in greyscale
    ## Double check the below conversion thing

    # Include reading black and white images
    # Both of these need greyscale images
    if process in ['add_random_noise', 'skelotonize', 'medial_axis', 'thin']:
        img_format, img = cv_decode_base64(request.json['url'], type = "nparray")
    else:
        if process in ['canny', 'opencv_binarization']:
            try:
                img_format, img = cv_decode_base64(request.json['url'], mode=cv.COLOR_GRAY2BGR)
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) ## Not sure if this is correct
                print('reading as greyscale')
            except:
                img_format, img = cv_decode_base64(request.json['url'], mode=cv.COLOR_RGB2GRAY)
                print('reading as color')
        else:
            try:
                img_format, img = cv_decode_base64(request.json['url'])
                print('reading as color default')
            except:
                img_format, img = cv_decode_base64(request.json['url'], mode=cv.COLOR_GRAY2BGR)
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                print('reaidng as grayscale default')

    print('Calling the method ' + process)

    img_output = getattr(sys.modules[__name__], process)(img, parameters)

    print('Returning the results')

    if process in ['add_random_noise', 'skeletonize', 'medial_axis', 'thin']:
        return jsonify({'results': cv_encode_base64 (img_format, img_output, type = "nparray")})
    else:
        return jsonify({'results': cv_encode_base64 (img_format, img_output)})


def createFile(url, filename):
    img_format, img_data = url.split(',')[0], url.split(',')[1]

    extension = img_format.replace('data:image/', '').replace(';base64', '')
    print(extension)

    if extension == 'jpeg':  # Check for other formats
        file_ext = '.jpg'
    else:
        file_ext = '.' + extension

    filename = filename + file_ext

    imgdata = base64.b64decode(img_data)
    with open(filename, 'wb') as f:
        f.write(imgdata)


def contour(img, parameters):
    _, cnts, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE)

    cnt = cnts[-1]
    print(cnts)

    (x,y),radius = cv.minEnclosingCircle(cnt)

    print(x)
    print(y)
    print(radius)
    print(cv.__version__)
    print(hierarchy)

    return img

@app.route('/amap/api/writerid', methods=['POST'])
def writerid():
    parameters = json.loads(request.json['parameters'])
    process = request.json['processing'].replace(' ', '_').lower()

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top

    method = parameters['type']
    if method == 'SIFT':
        value = str(parameters['rotation'])
    else:
        value = str(parameters['keypoints'])

    if process == 'npnn':
        time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        known_f = APP_ROOT + '/npnn/known' + time
        unknown_f = APP_ROOT + '/npnn/unknown' + time

        print('Creating the following folders')
        print(APP_ROOT)
        print(known_f)
        print(unknown_f)

        known = 'known' + time
        unknown = 'unknown' + time

        os.mkdir(known_f)
        os.mkdir(unknown_f)

        os.mkdir(unknown_f + '/u1')
        if parameters['unknown']['type'] == 'imagesM':
            createFile(parameters['unknown']['url'], unknown_f + '/u1/some')
        elif parameters['unknown']['type'] == 'collectionBooks':
            for k, page in enumerate(parameters['unknown']['pages']):
                createFile(page, unknown_f + '/u1/some' + str(k))

        for i, image in enumerate(parameters['known']):
            if image['url'] != '' and image['type'] == 'imagesM':
                os.mkdir(known_f + '/k' + str(i))
                createFile(image['url'], known_f + '/k' + str(i) + '/some' + str(i))
            elif image['url'] != '' and image['type'] == 'collectionBooks':
                os.mkdir(known_f + '/k' + str(i))
                for j, page in enumerate(image['pages']):
                    print('inside book collection')
                    createFile(page, known_f + '/k' + str(i) + '/some' + str(i) + str(j))

        print(os.getcwd())

        result = 'result' + time + '.csv'

        print('FAST 80 ' + unknown + ' ' + known + ' ' + result)

        sp.run([APP_ROOT + '/npnn/' + 'Writer_Identification_WFA.exe' + ' ' + method + ' ' + value + ' ' + unknown + ' ' + known + ' ' + result], shell=True, check=True, cwd=APP_ROOT + '/npnn')

        shutil.rmtree(unknown_f)
        shutil.rmtree(known_f)

        print('Reading CSV files')

        result_file = APP_ROOT + '/npnn/' + 'result' + time + '.csv'
        print(result_file)

        with open(result_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile)

            match = {}

            for row in spamreader:
                if len(row) > 2:
                    index = row[1].split('k')[1]
                    match[index] = row[2]
                    print('| '.join(row))

        print(match)

        os.remove(result_file)

    return jsonify({'results': match})


def read_color_default(data):
    try:
        img_format, img = cv_decode_base64(data)
        print('reading as color default')
    except:
        img_format, img = cv_decode_base64(data, mode=cv.COLOR_GRAY2BGR)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        print('reading as grayscale default')

    return img


def dist(p1, p2):
    d = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
    return d

@app.route('/amap/api/keyword', methods=['POST'])
def keyword_spotting():
    parameters = json.loads(request.json['parameters'])

    image_base64 = parameters['page']['url']

    time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    createFile(image_base64, 'image' + time)

    boxes_all = []

    for i, image in enumerate(parameters['known']):
        if image['url'] != '':
            createFile(image['url'], 'query' + str(i) + time)

            qr = Query()
            # Results are of the form (x1, x2, y1, y2, similarity)
            results = qr.processQuery('query'+ str(i) + time + '.jpg', 'image'+ time+ '.jpg')

            print('The results are')
            print(results)
            print('The total resutls are')
            print(list(map(list, results)))

            #results_subset = [result for result in results if result[0][4] >= parameters['threshold']]
            results_subset = [result for result in results]

            print('The result subset is')
            print(results_subset)
            print(len(results_subset))

            boxes = []

            for result in results_subset:
                coord = result[0]
                boxes.append([coord[0], coord[2], abs(coord[1]-coord[0]), abs(coord[3]-coord[2]), coord[4]])

            os.remove('query'+ str(i) + time + '.jpg')

            #boxes_all.append(boxes)
            boxes_all.append(boxes)

    os.remove('image'+ time + '.jpg')

    return jsonify({'boxes': boxes_all})

def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
            np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")


@app.route('/amap/api/template', methods=['POST'])
def template_matching():
    parameters = json.loads(request.json['parameters'])

    print('Trying to finnd templates')

    img_rgb = read_color_default(parameters['page']['url'])

    if len(img_rgb.shape) == 3:
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    else:
        img_gray = img_rgb

    data = parameters['page']['url']

    #img_gray = read_color_default(parameters['page']['url'], gray = True)

    #img_format, img = cv_decode_base64(data, mode=cv.COLOR_GRAY2BGR)
    #img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    boxes_all = []

    print('Trying to finnd templates2')

    for i, image in enumerate(parameters['known']):
        print('getting parameters')
        if image['url'] != '':
            boxes = []

            template_rgb = read_color_default(image['url'])

            if len(template_rgb.shape) == 3:
                template_grey = cv.cvtColor(template_rgb, cv.COLOR_BGR2GRAY)
            else:
                template_grey = template_rgb

            w, h = template_grey.shape[::-1]

            res = cv.matchTemplate(img_gray, template_grey, cv.TM_CCOEFF_NORMED)
            print(res[0][0])
            #flatres = res.flatten()
            #count = int(len(flatres) * 0.001)
            #minVal = min(sorted(flatres,reverse=True)[:count])
            #print(minVal)
            #minVal = 0
            loc = np.where(res >= parameters['threshold'])

            print('iterating')
            print(len(list(zip(*loc[::-1]))))

            for pt in zip(*loc[::-1]):
                boxes.append([int(pt[0]), int(pt[1]), w, h])

            box_nms = np.asarray([np.asarray([b[0], b[1], b[0]+b[2], b[1]+b[3]]) for b in boxes])
            box_nms = non_max_suppression_fast(box_nms, 0.5)

            #print('NMS suppression')
            #print(box_nms)

            box_nms = [[b[0].item(), b[1].item(), abs(b[0] - b[2]).item(), abs(b[1] - b[3]).item()] for b in box_nms]

            #print(box_nms)

            boxes_all.append(box_nms)

    print('found templates')

    return jsonify({'boxes': boxes_all})


@app.route('/amap/api/segment/tesseract', methods=['POST'])
def segment_tesseract():
    if 'data:image' not in request.json['url']:
        image_base64 = base64.b64encode(requests.get(request.json['url']).content)
    else:
        image_base64 = re.sub('^data:image/.+;base64,', '', request.json['url'])
    image = Image.open(BytesIO(base64.b64decode(image_base64)))
    boxes_api = []
    print('Getting API request')
    with tes.PyTessBaseAPI(path='/usr/share/tesseract-ocr/4.00/tessdata') as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(request.json['mode'], True)
        print ('Found {} textline image components.'.format(len(boxes)))
        for i, (im, box, _, _) in enumerate(boxes):
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            arr = [box['x'], box['y'], box['w'], box['h']]
            #print(arr)
            boxes_api.append(arr)
    return jsonify({'boxes': boxes_api})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
