#!/bin/python2

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot(ax, xs, ys, ylabel, plttype="plot", color='r', xticklabels=[]):
  if plttype == "scatter":
    ax.scatter(xs, ys, s=5, marker=".", color=color)
  else:
    ax.plot(xs, ys, color=color)
  if len(xticklabels) > 0:
    ax.xaxis.set_ticks(xs)
    ax.xaxis.set_ticklabels(xticklabels)
  ax.set_ylabel(ylabel)
  for tl in ax.get_yticklabels():
    tl.set_color(color)

def plot_twin(ax, xs, ys, ylabel, plttype="plot", color='b'):
  ax2 = ax.twinx()
  plot(ax2, xs, ys, ylabel, plttype, color)

def subplots():
  return plt.subplots()
