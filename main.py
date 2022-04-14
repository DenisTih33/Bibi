from PyQt5.QtWidgets import(
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, 
    QListWidget, QFileDialog
)

import os
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN

app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy Editor')

lb_image = QLabel('Картинка')
lw_files = QListWidget()

btn_folder = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/б')

v_lay_1 = QVBoxLayout()  #для кнопки и списка изображений
v_lay_2 = QVBoxLayout()  #для надписи "картинка"
g_lay = QHBoxLayout()  #для книпок
layout = QHBoxLayout()  #основной гориз лайаут

v_lay_1.addWidget(btn_folder)
v_lay_1.addWidget(lw_files)

g_lay.addWidget(btn_left)
g_lay.addWidget(btn_right)
g_lay.addWidget(btn_flip)
g_lay.addWidget(btn_sharp)
g_lay.addWidget(btn_bw)

v_lay_2.addWidget(lb_image)
v_lay_2.addLayout(g_lay)

layout.addLayout(v_lay_1)
layout.addLayout(v_lay_2)

win.setLayout(layout)

workdir = '' 
def chooseWorkdir():
	global workdir 
	workdir = QFileDialog.getExistingDirectory()

def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
def showFilenamesList():
    chooseWorkdir()
    extensions = ['.jpg', '.jpeg', '.png']
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

class ImageProcessor():
    def __init__(self):
     self.image = None
     self.dir = None
     self.filename = None
     self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)        
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)        
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)        
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)        
        self.showImage(image_path)

workimage = ImageProcessor()

def showChoseImage():
    global workdir
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        
        image_path = os.path.join(workdir, filename)
        workimage.loadImage(workdir,filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChoseImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_folder.clicked.connect(showFilenamesList)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharp)


win.show()
app.exec_()