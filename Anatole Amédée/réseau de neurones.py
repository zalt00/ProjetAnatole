#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 16:33:39 2021

@author: userlfa
"""

import numpy as np
import random
import matplotlib as mpl
import matplotlib.pyplot as plt



def squared_norme(vector):
    vector = np.array(vector)
    return np.sum(vector ** 2)

def erreur(X, P):
    return squared_norme(P * X - X)

def erreur2(image, network, label):
    return squared_norme(network * image - get_result(label))

def get_result(label):
    a = np.zeros(10, dtype=np.float64)
    a[label] = 1.
    return a

def grad(f, x, y, z, h):
    return np.array([
            f(x + h, y, z) - f(x, y, z),
            f(x, y + h, z) - f(x, y, z),
            f(x, y, z + h) - f(x, y, z)
        ])

def f(x, y, z):
    return x**2 + 3*y**2 + 4*z**3

def grad_erreur(f, X, P, h):
    err = f(X, P)
    gradient = P.copy()

    for i in range(gradient.shape[0]):
        for j in range(gradient.shape[1]):
            buffer = P.copy()
            buffer[i, j] += h
            gradient[i, j] = f(X, buffer) - err
            
    return gradient
    
def matrix2image(X):
    X = np.array(X, dtype=np.uint8).reshape((2, 2))
    image = np.zeros((2, 2, 3), dtype=np.uint8)
    
    image[:, :, 0] += X
    image[:, :, 1] += X
    image[:, :, 2] += X
    
    image *= 255
    image = 255 - image
    
    return image
    

def get_image(db, index):
    a = np.frombuffer(db[28*28 * index : 28*28 * (index + 1)], dtype=np.uint8).reshape((1, 28**2))
    a = np.matrix(a)
    return a

def get_label(db, index):
    return db[index]

def get_databases(training_filename, labels_filename):
    with open(training_filename, 'rb') as file:
        db1 = file.read()[16:]
    with open(labels_filename, 'rb') as file:
        db2 = file.read()[8:]
    return db1, db2

def train(network, db1, db2):
    N = 60000
    h = 0.1
    gradient = network.copy()
    buffer = network.copy()

    for i in range(N):
        image = get_image(db1, i)
        label = get_label(db2, i)
        
        err = erreur2(image, network, label)
    
        for x in range(gradient.shape[0]):
            for y in range(gradient.shape[1]):
                buffer[x, y] += h
                gradient[x, y] = erreur2(image, buffer, label) - err
                buffer[x, y] -= h
                
        network -= gradient
                

def get_network(width, height):
    m = np.tanh(np.linspace(-5.1, 5.1, width * height).reshape((width, height)))
    m = np.matrix(m)
    return m
    


def main():
    network = get_network(28 * 28, 10)
    db1, db2 = get_databases('train-images.idx3-ubyte', 'train-labels.idx1-ubyte')
    train(network, db1, db2)


if False:

    P = np.matrix([
            [4, 1, 1, 1],
            [0, 2, 1, 1],
            [0, 0, 3, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)
    
    X = np.matrix([
            [0],
            [0],
            [1],
            [1]
        ], dtype=np.float64)
    
    
    for i in range(1000):
        m = np.matrix([
            [random.randint(0, 1)],
            [random.randint(0, 1)],
            [random.randint(0, 1)],
            [random.randint(0, 1)]
        ], dtype=np.float64)
        P -= grad_erreur(erreur, m, P, 0.1)
        
    plt.imshow(matrix2image(X))
    
    results = P * X
    number_of_colored_squares = len(np.nonzero(results > 0.5)[0])
    print(f'il y a {number_of_colored_squares} carrés colorés en noir')
    plt.show()

    
    
    
    
