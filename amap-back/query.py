import cv2
import numpy as np
from shapely.geometry import Polygon as poly
from skimage.measure import compare_ssim as ssim
from feat import Features


class Query(object):

    def __init__(self, parent=None):
        super(Query, self).__init__()
        self.finalbb = None
        self.bookim = None
        self.query = None
        # self.pageno = None

    def processQuery(self, query, target):
        qim = cv2.imread(query)
        tim = cv2.imread(target)

        self.bookim = tim
        self.query = qim

        feat = Features()
        qP, qD = feat.extractSIFT(qim)
        tP, tD = feat.extractSIFT(tim)

        # Compare features
        points = feat.compare_descr_paaa(qD, tD, 15)
        # Extract areas of interest
        bboxes = feat.create_areas(points, tP, qP, qim.shape)
        nmsBB = self.nms(bboxes)
        sim = self.ssimilarity(nmsBB)

        # bboxes2 = self.create_areas(points, tP, qP, qim.shape, tim.shape)

        # self.finalbb = np.array([]).reshape(0, 5)
        self.finalbb = np.hstack((nmsBB, sim))
        sr = np.argsort(sim, axis=0)[::-1]
        # self.finalbb = np.argsort(-self.finalbb[:, 4])
        return self.finalbb[sr, :]

    def nms(self, bboxes):
        # Perform Non-Maximum Supression to the bounding boxes
        finalbb = np.array([], dtype=float).reshape(0, 4)
        while bboxes.shape[1] > 0:
            idx = np.array([], dtype=int).reshape(0, 1)
            poly1 = poly([(bboxes[0, 0], bboxes[2, 0]),
                          (bboxes[1, 0], bboxes[2, 0]),
                          (bboxes[1, 0], bboxes[3, 0]),
                          (bboxes[0, 0], bboxes[3, 0])])
            for m in range(bboxes.shape[1]):
                poly2 = poly([(bboxes[0, m], bboxes[2, m]),
                              (bboxes[1, m], bboxes[2, m]),
                              (bboxes[1, m], bboxes[3, m]),
                              (bboxes[0, m], bboxes[3, m])])

                if poly1.intersects(poly2):
                    inter = poly1.intersection(poly2)
                    un = poly1.union(poly2)
                    a1 = inter.area
                    a2 = un.area
                    iou = a1 / a2
                    if iou >= 0.2:
                        idx = np.vstack((idx, m))
            try:
                x1 = np.mean(bboxes[0, idx])
                x2 = np.mean(bboxes[1, idx])
                y1 = np.mean(bboxes[2, idx])
                y2 = np.mean(bboxes[3, idx])
                finalbb = np.vstack((finalbb, (x1, x2, y1, y2)))
            except:
                pass
            bboxes = np.delete(bboxes, idx, axis=1)
            del idx

        return finalbb

    def ssimilarity(self, bboxes):
        bookim_gray = cv2.cvtColor(self.bookim, cv2.COLOR_BGR2GRAY)
        query_gray = cv2.cvtColor(self.query, cv2.COLOR_BGR2GRAY)
        sims = np.zeros((bboxes.shape[0], 1), dtype=float)
        count = 0
        bboxes = np.around(bboxes, decimals=0).astype(int)
        for bb in bboxes:
            try:
                segment = bookim_gray[bb[2]:bb[3], bb[0]:bb[1]]
                segment = cv2.resize(segment, (self.query.shape[1], self.query.shape[0]), 0, 0, cv2.INTER_CUBIC)

                s = ssim(query_gray, segment)
                sims[count, 0] = s
                count += 1
            except:
                print("Invalid Segment")
            finally:
                pass

        return sims

    def create_areas(self, *args):
        # arg[0] = (reduced points, corresponding query points)
        # arg[1] = book points
        # arg[2] = query points,
        # arg[3] = query dimensions
        # arg[4] = doc image dimensions
        points = args[0]
        book_points = args[1]
        query_points = args[2]
        dims = args[3]
        docdims = args[4]

        x1 = book_points[points[:, 0], 0] - query_points[points[:, 1], 0]
        y1 = book_points[points[:, 0], 1] - query_points[points[:, 1], 1]
        x2 = book_points[points[:, 0], 0] + (dims[1] - query_points[points[:, 1], 0])
        y2 = book_points[points[:, 0], 1] + (dims[0] - query_points[points[:, 1], 1])

        bboxes = np.vstack((x1, x2, y1, y2))
        return bboxes
