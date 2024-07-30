import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import pandas as pd
from sklearn.cluster import KMeans

sys.path.append("E:\Project\OOC\LEDs_Data_Processing\LED_Decode")


class Point:
    def __init__(self):
        self.centerArray = []  # Initialize centerArray here
        self.height = None
        self.width = None

    def preprocess(self, img_path):
        img = cv2.imread(img_path)
        self.height, self.width = img.shape[:2]
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imageConvert = cv2.convertScaleAbs(image, alpha=255.0 / np.max(image))
        _, threshold_imageConvert = cv2.threshold(
            imageConvert, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        contours, hierarchy = cv2.findContours(
            threshold_imageConvert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        _, threshold_imageOrg = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        contours, hierarchy = cv2.findContours(
            threshold_imageOrg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        averageAreaContour = np.mean([cv2.contourArea(c) for c in contours])
        print(f"averageAreaContour: {averageAreaContour}")
        boundingBox = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > averageAreaContour / 10:
                x, y, w, h = cv2.boundingRect(contour)
                boundingBox.append((x, y, w, h))
                cv2.rectangle(imageConvert, (x, y), (x + w, y + h), (255, 255, 0), 2)

        ledArea = 0

        for box in boundingBox:
            x, y, w, h = box
            if h > ledArea:
                ledArea = h
            center = (x + w // 2, y + h // 2)
            self.centerArray.append(center)
        print(f"centerArray: {self.centerArray}")

        cv2.namedWindow("Frame1", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Frame1", 800, 800)
        cv2.imshow("Frame1", imageConvert)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def testAlgorithm(self):
        """K-Means Algorithm"""

        n = len(self.centerArray)
        print(f"n: {n}")
        inertias = []

        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, random_state=0).fit(self.centerArray)
            inertias.append(kmeans.inertia_)

        # plt.plot(range(1, 11), inertias, marker="o")
        # plt.title("Elbow method")
        # plt.xlabel("Number of clusters")
        # plt.ylabel("Inertia")
        # plt.show()

    def plotCenter(self):
        """Plot centerArray. Can it use the list(zip())?"""

        # x_coords = [point[0] for point in self.centerArray]
        # y_coords = [point[1] for point in self.centerArray]
        # data = list(zip(x_coords, y_coords))

        plt.figure(figsize=(10, 14))  # Adjust figure size as needed

        # Create scatter plot
        plt.scatter(*zip(*self.centerArray), marker="o", color="blue", s=10)

        # Set title and axis labels
        plt.title("Scatter Plot of CenterArray")
        plt.xlabel("X-axis (1080)")
        plt.ylabel("Y-axis (1439)")
        plt.show()


def main(img_path):
    obj = Point()
    obj.preprocess(img_path)
    obj.plotCenter()
    obj.testAlgorithm()


if __name__ == "__main__":
    main("LED_Decode/led_image/LEDID_4_RoI_adjusted.jpg")
