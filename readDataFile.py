import numpy as np
import spc
import csv
import os

def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension


def readDataFile(file):
    
    if get_file_extension(file) == ".spc":
        f = spc.File(file)
        x1 = f.x
        y1 = f.sub[0].y

    elif get_file_extension(file) == ".csv":

        with open(file, newline='') as csvfile:
            f = list(csv.reader(csvfile, delimiter=','))
        try:
            y1 = f[23]
            x1 = np.asarray([float(i) for i in f[21]])
            y1 = np.asarray([float(i) for i in y1[0:len(y1) - 1]])

        except:
            x1 =[]
            y1 = []
            for row in f:
                x1 = np.append(x1, int(row[0].split('.')[0]))
                y1 = np.append(y1, row[1])
            y1 = [float(x) for x in y1]
            y1 = np.asarray(y1)
            x1 = np.asarray(x1)

        
    return x1, y1


        