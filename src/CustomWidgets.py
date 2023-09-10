import os

from PyQt5 import sip
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QPushButton

from CustomFuncs import *

class CustomGroupBox(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("border: 0px solid;")
        self.setTitle("")
        self.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout1 = QHBoxLayout()
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItem1)
        self.label = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.horizontalLayout1.addWidget(self.label)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItem2)

        self.verticalLayout.addLayout(self.horizontalLayout1)

        self.horizontalLayout2 = QHBoxLayout()
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem3)
        self.pushButton = QPushButton(self)
        self.pushButton.setToolTip('Like')
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(check_path("./img/icons/like_black.png")), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(32, 32))
        self.pushButton.setStyleSheet('''
			QPushButton:hover{background-color: #eeeeee;}
            QPushButton:pressed{padding-left:2px;padding-top:2px;}
		''')
        self.horizontalLayout2.addWidget(self.pushButton)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem4)

        self.verticalLayout.addLayout(self.horizontalLayout2)

        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

    def show_img(self, image_path, scale='1,1'):
        pixmap = QPixmap(image_path)
        scale_w, scale_h = scale.split(',')
        pixmap = pixmap.scaled(float(scale_w) * pixmap.width(), float(scale_h) * pixmap.height())
        self.label.setPixmap(pixmap)

    def set_text(self, text):
        self.pushButton.setText(text)

class DisplayController(QWidget):
    def __init__(self, grid_layout):
        super().__init__()

        self.grid_layout = grid_layout

    def verify_root(self, file_root):

        self.file_root = file_root
        self.sub_dirs = sorted(os.listdir(self.file_root))
        
        # --------> Verify the requirement 1 of the selected directory

        # Create a flag indicating if the subdir is existing meanwhile there is no file and the number of image under subdir is consistent
        subdir_exist_nofile_samenum = True if len(self.sub_dirs) != 0 else False # (1) Subdir/file is existing

        num_image, i = 0, 0
        for sub_dir in self.sub_dirs: # (2) There is no file and the number of image under subdir is consistent
            if os.path.isfile(os.path.join(self.file_root, sub_dir)):
                subdir_exist_nofile_samenum = False
                break
            else:
                if i == 0:
                    num_image = len(os.listdir(os.path.join(self.file_root, sub_dir)))
                else:
                    if num_image != len(os.listdir(os.path.join(self.file_root, sub_dir))):
                        subdir_exist_nofile_samenum = False
                        break
                i+=1

        if not subdir_exist_nofile_samenum:
            QMessageBox.critical(self, 'Error!', 'The selected directory should only include several sub-directories with the same number of images!')
        else:

            self.displayed_imgs = sorted(os.listdir(os.path.join(self.file_root, self.sub_dirs[0])))

            # --------> Verify the requirement 2 of the selected directory.

			# Create a flag indicating if the images of subdirs are one_to_one_matching
            one_to_one_matching = True

            for i in range(1, len(self.sub_dirs)):
                for img in self.displayed_imgs:
                    if not img in os.listdir(os.path.join(self.file_root, self.sub_dirs[i])):
                        one_to_one_matching = False

            if not one_to_one_matching:
                QMessageBox.critical(self, 'Error!', 'The image in each sub-directory should be one-to-one matching!')

        return len(self.sub_dirs), num_image
        
    def init_groupbox(self):

        first_img = self.displayed_imgs[0]
        for i in range(len(self.sub_dirs)):
            
			# Instantiating the objects
            exec('self.groupBox{} = CustomGroupBox()'.format(i))
            # Add 'index' property to each button of Groupbox
            exec('self.groupBox{}.pushButton.setProperty("index", {})'.format(i, i))
			# Show the image
            exec('self.groupBox{}.show_img(self.file_root + "/{}/{}")'.format(i, self.sub_dirs[i], first_img))
            # Set the text
            # exec('self.groupBox{}.set_text(self.sub_dirs['.format(i) + str(i) + '])')
            # Add widget to layout
            point = index2point(i, math.ceil(math.sqrt(len(self.sub_dirs))))
            exec('self.grid_layout.addWidget(self.groupBox{}, '.format(i) + str(point[0]) + ', ' + str(point[1]) + ', ' + '1, 1)')

    def reset_groupbox(self):
        for i in reversed(range(self.grid_layout.count())):
            widgetToRemove = self.grid_layout.itemAt(i).widget()
            # Removing the objects
            self.grid_layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
            sip.delete(widgetToRemove)

    def rerender_groupbox(self, cur_index, scale):
        if scale == '' or is_invaild_scale(scale):
            scale = '1,1' 
        cur_img = self.displayed_imgs[cur_index]
        for i in range(len(self.sub_dirs)):
            exec('self.groupBox{}.show_img(self.file_root + "/{}/{}","{}")'.format(i, self.sub_dirs[i], cur_img, scale))

    def rearrange_groupbox(self, cur_index, scale, column):
        if scale == '' or is_invaild_scale(scale):
            scale = '1,1' 
        cur_img = self.displayed_imgs[cur_index]
        
        for i in range(len(self.sub_dirs)):
            
			# Instantiating the objects
            exec('self.groupBox{} = CustomGroupBox()'.format(i))
            # Add 'index' property to each button of Groupbox
            exec('self.groupBox{}.pushButton.setProperty("index", {})'.format(i, i))
			# Show the image
            exec('self.groupBox{}.show_img(self.file_root + "/{}/{}","{}")'.format(i, self.sub_dirs[i], cur_img, scale))
            # Set the text
            # exec('self.groupBox{}.set_text(self.sub_dirs['.format(i) + str(i) + '])')
            # Add widget to layout
            point = index2point(i, column)
            exec('self.grid_layout.addWidget(self.groupBox{}, '.format(i) + str(point[0]) + ', ' + str(point[1]) + ', ' + '1, 1)')