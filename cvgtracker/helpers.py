# import os
import string
import random
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt


def read_log(log='converge.log', n1=0, n2=1):  # read the "converge.log" file to plot trend

    try:
        openlog = open(log, 'r')
    except IOError:
        print " %s is missing " % log

    xar = []
    yar = []
    # print openlog
    fread = open('converge.log', 'r')
    for line in fread:
        if len(line) > 1 and not line.lower().startswith('no'):
            a = line.split('\t')
            x = a[n1]
            y = a[n2]
            xar.append(float(x))
            yar.append(float(y))

    openlog.close()
    return xar, yar


def randomstring(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def plot_log(log='converge.log', n1=0, n2=1):
    x, y = read_log(log=log, n1=n1, n2=n2)
    plt.plot(x, y, 'o-', linewidth=2)
    plt.savefig('cvg.png')
