import os

import numpy as np
import beutools.Datahandling as dt

def calc():
    saveName = input("Save to? ")
    f = lambda d: float(eval(d))
    length = f(input("length in m = ?"))
    lambdaVar = f(input("lambda in m = ?"))
    theta = lambda dx, l: np.arctan(dx / l)
    D = lambda k, dx, l, lmd: (lmd * k / np.sin(theta(dx, l)))
    D_alt = lambda k, dx, l, lmd: (lmd * k / (dx / l))

    dt.createSaveFile(saveName)
    dt.addToSaveFile(saveName, "calculated width in m \n")
    ctn = "y"
    while ctn == "y":
        order = f(input("Order k= ?"))
        deltaX = abs(f(input("Delta X in m = ?")))
        dt.addToSaveFile(saveName, "\n D = " + str(D(order, deltaX, length, lambdaVar)))
        dt.addToSaveFile(saveName, "\n D_alt = " + str(D_alt(order, deltaX, length, lambdaVar)))
        ctn = input("continue? (y/n)")


calc()
