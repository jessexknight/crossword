import random
import sys
import csv
import matplotlib.pyplot as plt
from cycler import cycler

class CrossWord:
  BLANK = '.'
  MAXWORDS = 20
  MAXITER = 100
  SOLN = True
  C_BKGD = (1.0, 1.0, 1.0)
  C_GRID = (0.0, 0.0, 0.0)
  C_TEXT = (0.0, 0.2, 0.2)

  def __init__(self, iwords):
    self.words = iwords
    self.arr = CrossWordGenArray(iwords, self.BLANK)
    self.fig, self.ax = plt.subplots(1, 2)
    self.fig.show(False)

  def opt_gen_arr(self):
    iwords = list(self.words)
    self.words = list([])
    for k in range(self.MAXITER):
      attempt = CrossWordGenArray(iwords, self.BLANK)
      attempt.gen_arr()
      if len(attempt.owords) >= len(self.words):
        if (attempt.len() * attempt.wid()) < (self.arr.len() * self.arr.wid()):
          self.arr = attempt
          self.words = attempt.owords

  def gen_fig(self):

    self.fig.hold(True)
    self.fig.set_facecolor(self.C_BKGD)
    for a in range(len(self.ax)):
      self.ax[a].axis('off')
      self.ax[a].set_prop_cycle(cycler('color',[self.C_GRID]))

    self.add_grid_to_fig(self.ax[0])
    self.add_words_to_fig(self.ax[1])

    self.ax[0].axis('equal')
    plt.show(block = True)
    self.fig.show(True)

  def add_grid_to_fig(self, ax):
    for y in range(self.arr.len()):
      for x in range(self.arr.wid()):
        if self.arr.arr[y][x] != self.arr.blank:
          self.add_box_to_fig(ax, y, x)
    for w in range(len(self.arr.yxd)):
      self.ax[0].text(self.arr.yxd[w][1] + 0.1, self.arr.len() - self.arr.yxd[w][0] - 0.1,
                      str(w + 1), fontsize = 10, color = self.C_TEXT,
                      horizontalalignment = 'left', verticalalignment = 'top')

  def add_box_to_fig(self, ax, y, x):
    ymax = self.arr.len()
    yy = [ymax - y, ymax - y - 1]
    xx = [x, x + 1]
    ax.plot([xx[0], xx[0]], yy, clip_on = False)
    ax.plot([xx[1], xx[1]], yy, clip_on = False)
    ax.plot(xx, [yy[0], yy[0]], clip_on = False)
    ax.plot(xx, [yy[1], yy[1]], clip_on = False)
    if self.SOLN:
      ax.text(x + 0.5, ymax - y - 0.5, str(self.arr.arr[y][x]), fontsize = 20, color = self.C_TEXT,
              horizontalalignment = 'center', verticalalignment = 'center')

  def add_words_to_fig(self, ax):

    for w in range(len(self.words)):
      ax.text(0, self.MAXWORDS - w, (str(w+1) + ") " + self.words[w]), fontsize = 15, color = self.C_TEXT,
              horizontalalignment = 'left', verticalalignment = 'center')
      ax.set_ylim([0, self.MAXWORDS])

  def print_words(self):
    for y in range(len(self.words)):
      for x in range(len(self.words[y])):
        sys.stdout.write(self.words[y][x])
      sys.stdout.write("\n")


class CrossWordGenArray:

  def __init__(self, iwords, blank):
    ilenwid = 2*self.string_array_n(iwords)
    self.vdir = False
    self.blank = blank
    self.iwords = list(iwords)
    self.owords = list([])
    self.yxd = list([])
    self.arr = [[self.blank for x in range(ilenwid)] for y in range(ilenwid)]

  def toggle_vdir(self):
    self.vdir = not self.vdir

  def len(self):
    return len(self.arr)

  def wid(self):
    return len(self.arr[0])

  def gen_arr(self):
    ww = random.choice(list(range(len(self.iwords))))
    self.add_word_to_arr(ww, self.len()/2, self.wid()/2)

    added = 1
    while added & (len(self.iwords) > 0):
      added = self.select_add_word()
    self.crop()

  def select_add_word(self):
    windex = self.rand_order(len(self.iwords))

    for w in range(len(self.iwords)):
      ww = windex[w]
      kindex = self.rand_order(self.len()*self.wid())
      for k in range(len(kindex)):
        x = kindex[k] % self.wid()
        y = (kindex[k]-x) / self.wid()
        for t in range(len(self.iwords[ww])):
          if self.arr[y][x] == self.iwords[ww][t]:
            if self.check_add_word(ww, t, y, x):
              return 1
    return 0

  def check_add_word(self, ww, t, y, x):
    word = self.iwords[ww]
    if self.vdir:
      for k in range(len(word)):
        yy = y + k - t
        intersect = (k == t)
        if self.arr[yy][x] == word[k]:
          intersect = 1
        elif self.arr[yy][x] != self.blank:
          return 0

        if k == 0:
          if self.arr[yy-1][x] != self.blank:
            return 0
          elif self.arr[yy][x+1] != self.blank and self.arr[yy][x-1] == self.blank:
            return 0

        if k == len(word)-1:
          if self.arr[yy+1][x] != self.blank:
            return 0

        if not intersect:
          if self.arr[yy][x+1] != self.blank or self.arr[yy][x-1] != self.blank:
            return 0

      self.add_word_to_arr(ww, y-t, x)
      return 1
        
    else:
      for k in range(len(word)):
        xx = x + k - t
        intersect = (k == t)
        if self.arr[y][xx] == word[k]:
          intersect = 1
        elif self.arr[y][xx] != self.blank:
          return 0

        if k == 0:
          if self.arr[y][xx-1] != self.blank:
            return 0
          elif self.arr[y+1][xx] != self.blank and self.arr[y-1][xx] == self.blank:
            return 0

        if k == len(word)-1:
          if self.arr[y][xx+1] != self.blank:
            return 0

        if not intersect:
          if self.arr[y+1][xx] != self.blank or self.arr[y-1][xx] != self.blank:
            return 0

      self.add_word_to_arr(ww, y, x-t)
      return 1

  def add_word_to_arr(self, ww, yy, xx):
    y = yy
    x = xx
    for t in range(len(self.iwords[ww])):
      self.arr[y][x] = self.iwords[ww][t]
      if self.vdir:
        y += 1
      else:
        x += 1
    self.change_list_word(ww)
    self.yxd.append([yy, xx, self.vdir])
    self.toggle_vdir()

  def crop(self):
    ymin = self.len(),
    xmin = self.wid()
    for y in range(len(self.arr)):
      for x in range(len(self.arr[y])):
        if self.arr[y][x] != self.blank:
          ymin = min(ymin, y)
          xmin = min(xmin, x)
    for w in range(len(self.yxd)):
      self.yxd[w][0] = self.yxd[w][0] - ymin
      self.yxd[w][1] = self.yxd[w][1] - xmin

    self.arr = zip(*[list(row) for row in self.arr if any(e != self.blank for e in row)])
    self.arr = zip(*[list(col) for col in self.arr if any(e != self.blank for e in col)])

  def change_list_word(self, index):
    self.owords.append(self.iwords[index])
    self.iwords.pop(index)

  def print_arr(self):
    for y in range(len(self.arr)):
      for x in range(len(self.arr[y])):
        sys.stdout.write(self.arr[y][x])
      sys.stdout.write("\n")

  @staticmethod
  def rand_order(maxval):
    order = range(maxval)
    random.shuffle(order)
    return order

  @staticmethod
  def string_array_n(stringarray):
    n = 0
    for s in range(len(stringarray)):
      n += len(stringarray[s])
    return n


wordlistfile = 'words.csv'
with open(wordlistfile,'rb') as f:
  words = [word.upper() for word in csv.reader(f).next()]
  xword = CrossWord(words)
  xword.opt_gen_arr()
  print("----------")
  xword.print_words()
  print("----------")
  xword.gen_fig()



