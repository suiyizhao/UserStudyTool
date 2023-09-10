import os
import sys
import math

from PyQt5.uic import loadUi
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QMenu, QAction

from CustomWidgets import DisplayController
from CustomObjects import Task, TableWriter
from CustomFuncs import get_max_less_than_x, get_min_more_than_x, check_path

class MyWindow(QWidget):
	def __init__(self):
		super().__init__()

		self.init_ui()
		
		# Create a display controller to show the image
		self.controller = DisplayController(self.gridLayout)

		self.connect_singal_to_slot()

	def init_ui(self):

		self.ui = loadUi(check_path('./ui/MainWindow.ui'))

		# Initialize navigator bar and tool bar
		self.init_navibar()
		self.init_toolbar()
		self.init_statebar()

		# Initialize display area
		self.scrollAreaWidgetContents = self.ui.scrollAreaWidgetContents
		self.gridLayout = self.ui.gridLayout

	def init_navibar(self):
		# --> Navibar: from left to right
		self.navibar = self.ui.navibar
		self.navi_file = self.ui.navi_btn_file
		self.navi_edit = self.ui.navi_btn_edit
		self.navi_view = self.ui.navi_btn_view
		self.navi_help = self.ui.navi_btn_help

		# Add menu to navibar
		# Instantiate menu
		menu_file, menu_edit, menu_view, menu_help = QMenu(self), QMenu(self), QMenu(self), QMenu(self)

		# File menu creating
		# Instantiate action objects
		self.action_new_task = QAction(QIcon(check_path('./img/icons/task.png')), 'New Task', self)
		self.action_open_task = QAction(QIcon(check_path('./img/icons/task-filling.png')), 'Open Task', self)
		self.action_open_folder = QAction(QIcon(check_path('./img/icons/filefolder.png')), 'Open Folder', self)
		self.action_save = QAction(QIcon(check_path('./img/icons/save.png')), 'Save', self); self.action_save.setEnabled(False)
		self.action_export =  QAction(QIcon(check_path('./img/icons/export.png')), 'Export', self); self.action_export.setEnabled(False)
		# Add shortcut to action
		self.action_new_task.setShortcut('Ctrl+N')
		self.action_open_task.setShortcut('Ctrl+O')
		self.action_open_folder.setShortcut('Ctrl+Shift+O')
		self.action_save.setShortcut('Ctrl+S')
		self.action_export.setShortcut('Ctrl+E')
		# Add actions to menu
		menu_file.addAction(self.action_new_task)
		menu_file.addAction(self.action_open_task)
		menu_file.addAction(self.action_open_folder)
		menu_file.addSeparator()
		menu_file.addAction(self.action_save)
		menu_file.addAction(self.action_export)

		# Set menu
		self.navi_file.setMenu(menu_file)

		# Edit menu creating
		# Instantiate action objects
		self.action_previous = QAction(QIcon(check_path('./img/icons/previous.png')), 'Previous', self); self.action_previous.setEnabled(False)
		self.action_next = QAction(QIcon(check_path('./img/icons/next.png')), 'Next', self); self.action_next.setEnabled(False)
		self.action_previous_unrated = QAction(QIcon(check_path('./img/icons/previous_unrated.png')), 'Previous Unrated', self); self.action_previous_unrated.setEnabled(False)
		self.action_next_unrated = QAction(QIcon(check_path('./img/icons/next_unrated.png')), 'Next Unrated', self); self.action_next_unrated.setEnabled(False)
		self.action_cancel =  QAction(QIcon(check_path('./img/icons/cancel_like.png')), 'Cancel Like', self); self.action_cancel.setEnabled(False)
		self.action_auto =  QAction(QIcon(check_path('./img/icons/auto_green.png')), 'Auto Next', self); self.action_auto.setEnabled(False)
		# Add shortcut to action
		self.action_previous.setShortcut('Left')
		self.action_next.setShortcut('Right')
		self.action_previous_unrated.setShortcut('Ctrl+Left')
		self.action_next_unrated.setShortcut('Ctrl+Right')
		self.action_cancel.setShortcut('Ctrl+Z')
		self.action_auto.setShortcut('Space')
		# Add actions to menu
		menu_edit.addAction(self.action_previous)
		menu_edit.addAction(self.action_next)
		menu_edit.addAction(self.action_previous_unrated)
		menu_edit.addAction(self.action_next_unrated)
		menu_edit.addAction(self.action_cancel)
		menu_edit.addAction(self.action_auto)

		# Set menu
		self.navi_edit.setMenu(menu_edit)

		# View menu creating
		# Instantiate action objects
		self.action_hide_toolbar = QAction(QIcon(check_path('./img/icons/view-selected.png')), 'Tool Bar', self); self.is_hide_toolbar = False
		self.action_hide_statebar = QAction(QIcon(check_path('./img/icons/view-selected.png')), 'State Bar', self); self.is_hide_statebar = False
		# Add actions to menu
		menu_view.addAction(self.action_hide_toolbar)
		menu_view.addAction(self.action_hide_statebar)
		# Set menu
		self.navi_view.setMenu(menu_view)

		# Help menu creating
		# Instantiate action objects
		self.action_documentation = QAction(QIcon(check_path('./img/icons/document.png')), 'Documentation', self)
		self.action_about = QAction(QIcon(check_path('./img/icons/about.png')), 'About', self)
		# Add shortcut to action
		self.action_documentation.setShortcut('F2')
		self.action_about.setShortcut('F1')
		# Add actions to menu
		menu_help.addAction(self.action_documentation)
		menu_help.addAction(self.action_about)
		# Set menu
		self.navi_help.setMenu(menu_help)

	def init_toolbar(self):
		# --> Toolbar: from left to right
		self.toolbar = self.ui.toolbar
		self.btn_openfolder = self.ui.tool_btn_openfolder
		self.lineEdit_row = self.ui.tool_lineEdit_row
		self.lineEdit_column = self.ui.tool_lineEdit_column
		self.lineEdit_scale = self.ui.tool_lineEdit_scale

		self.btn_previous_unrated = self.ui.tool_btn_previous_unrated
		self.btn_previous = self.ui.tool_btn_previous
		self.btn_next = self.ui.tool_btn_next
		self.btn_next_unrated = self.ui.tool_btn_next_unrated
		self.lineEdit_serial = self.ui.tool_lineEdit_serial
		self.hScrollBar_serial = self.ui.tool_hScrollBar_serial

		self.btn_cancel = self.ui.tool_btn_cancel
		self.btn_auto = self.ui.tool_btn_auto
		self.btn_save = self.ui.tool_btn_save
		self.btn_export = self.ui.tool_btn_export

	def init_statebar(self):
		# --> Statebar: from top to bottom
		self.statebar = self.ui.statebar
		self.label_task_name = self.ui.state_label_task_name
		self.lineEdit_num_imgs = self.ui.state_lineEdit_num_imgs
		self.lineEdit_num_rated = self.ui.state_lineEdit_num_rated
		self.lineEdit_num_unrated = self.ui.state_lineEdit_num_unrated
		self.textBrowser_rated_list = self.ui.state_textBrowser_rated_list
		self.textBrowser_unrated_list = self.ui.state_textBrowser_unrated_list
		
	# Binding signals to slots
	def connect_singal_to_slot(self):
		# Navibar signals
		self.action_new_task.triggered.connect(self.slot_newtask)
		self.action_open_task.triggered.connect(self.slot_opentask)
		self.action_open_folder.triggered.connect(self.slot_openfolder)
		self.action_save.triggered.connect(self.slot_save)
		self.action_export.triggered.connect(self.slot_export)

		self.action_previous.triggered.connect(self.slot_previous)
		self.action_next.triggered.connect(self.slot_next)
		self.action_previous_unrated.triggered.connect(self.slot_previous_unrated)
		self.action_next_unrated.triggered.connect(self.slot_next_unrated)
		self.action_cancel.triggered.connect(self.slot_cancel)
		self.action_auto.triggered.connect(self.slot_auto)

		self.action_hide_toolbar.triggered.connect(self.slot_hide_toolbar)
		self.action_hide_statebar.triggered.connect(self.slot_hide_statebar)

		self.action_documentation.triggered.connect(self.slot_documentation)
		self.action_about.triggered.connect(self.slot_about)

		# Toolbar signals
		self.btn_openfolder.clicked.connect(self.slot_openfolder)
		self.lineEdit_column.editingFinished.connect(self.slot_lineEdit_column)
		self.lineEdit_scale.editingFinished.connect(self.slot_lineEdit_scale)

		self.btn_previous_unrated.clicked.connect(self.slot_previous_unrated)
		self.btn_previous.clicked.connect(self.slot_previous)
		self.btn_next.clicked.connect(self.slot_next)
		self.btn_next_unrated.clicked.connect(self.slot_next_unrated)
		self.lineEdit_serial.editingFinished.connect(self.slot_lineEdit_serial)
		self.hScrollBar_serial.sliderReleased.connect(self.slot_hScrollBar_serial_sliderReleased)
		self.hScrollBar_serial.valueChanged.connect(self.slot_hScrollBar_serial_valueChanged)

		self.btn_cancel.clicked.connect(self.slot_cancel)
		self.btn_auto.clicked.connect(self.slot_auto)
		self.btn_save.clicked.connect(self.slot_save)
		self.btn_export.clicked.connect(self.slot_export)

	def slot_newtask(self):

		'''
		Selecting a directory as root to be operated.
		The following two requirements should be met:
		1. The selected directory should only include several sub-directories with the same number of images
		2. The image in each sub-directory should be one-to-one matching
		'''

		file_root = QFileDialog.getExistingDirectory(self, 'Open a Folder', './')

		if file_root != '': # A directory has been opened, if it is '': nothing is selected

			# Verify if the above two requirements are met: if true, return (num_methods, num_imgs) else give the message.
			num_methods, num_imgs = self.controller.verify_root(file_root)

			# The selected directory have met the requirements, open the image and change the button state if the number of image is not equal to 0
			if num_imgs != 0:
				
				# Activate the button
				self.action_save.setEnabled(True)
				self.action_export.setEnabled(True)
				self.action_previous.setEnabled(True)
				self.action_next.setEnabled(True)
				self.action_previous_unrated.setEnabled(True)
				self.action_next_unrated.setEnabled(True)
				self.action_auto.setEnabled(True)

				self.lineEdit_column.setEnabled(True)
				self.lineEdit_scale.setEnabled(True)
				self.btn_previous_unrated.setEnabled(True)
				self.btn_previous.setEnabled(True)
				self.btn_next.setEnabled(True)
				self.btn_next_unrated.setEnabled(True)
				self.lineEdit_serial.setEnabled(True)
				self.hScrollBar_serial.setEnabled(True)
				self.btn_auto.setEnabled(True)
				self.btn_save.setEnabled(True)
				self.btn_export.setEnabled(True)

				self.lineEdit_num_imgs.setEnabled(True)
				self.lineEdit_num_rated.setEnabled(True)
				self.lineEdit_num_unrated.setEnabled(True)
				self.textBrowser_rated_list.setEnabled(True)
				self.textBrowser_unrated_list.setEnabled(True)

				# Set default value
				# Default row and column
				default_column = math.ceil(math.sqrt(num_methods))
				self.lineEdit_column.setPlaceholderText(str(default_column))
				default_row = math.ceil(num_methods / default_column)
				self.lineEdit_row.setPlaceholderText(str(default_row))
				# Default ScrollBar range and state
				self.hScrollBar_serial.setMinimum(1)
				self.hScrollBar_serial.setMaximum(num_imgs)
				self.hScrollBar_serial.setValue(1)
				# Default scrollArea contents
				self.scrollAreaWidgetContents.setStyleSheet('''
					background: white;
				''')

				# Set state bar
				self.lineEdit_num_imgs.setText(str(num_imgs))
				self.lineEdit_num_rated.setText(str(0))
				self.lineEdit_num_unrated.setText(str(num_imgs))
				self.textBrowser_rated_list.setStyleSheet('''
					color: red;
				''')
				self.textBrowser_rated_list.setText('Click "Like" for rating!')
				self.textBrowser_unrated_list.setText(str([i+1 for i in range(num_imgs)])[1:-1])

				# Set integer validator to lineEdit
				# Column lineEdit: nonzero positive integer
				validator_column = QRegExpValidator()
				validator_column.setRegExp(QRegExp('^\+?[1-9][0-9]*$'))
				self.lineEdit_column.setValidator(validator_column)
				# Scale lineEdit: [0.1-10],[0.1-10]
				validator_scale = QRegExpValidator()
				validator_scale.setRegExp(QRegExp('^(\d(\.\d{1})?|10)(\,)(\d(\.\d{1})?|10)$'))
				self.lineEdit_scale.setValidator(validator_scale)
				# Serial lineEdit: nonzero positive integer
				validator_serial = QRegExpValidator()
				validator_serial.setRegExp(QRegExp('^\+?[1-9][0-9]*$'))
				self.lineEdit_serial.setValidator(validator_serial)

				# Instantiate a Task(root_path, num_methods, num_imgs, cur_index, rated_list, unrated_list, auto_next, displayed_scale, displayed_column, result_dict)
				self.task = Task(file_root, num_methods, num_imgs, 0, [], [i+1 for i in range(num_imgs)], True, '1,1', default_column, {})

				# Display
				self.controller.init_groupbox()
				# Binding signals to slots
				for i in range(self.task.num_methods):
					exec('self.controller.groupBox{}.pushButton.clicked.connect(self.slot_like)'.format(i))
				
				# self.controller.reset_groupbox()
				# self.controller.rearrange_groupbox(self.task.cur_index, self.task.displayed_scale, self.task.displayed_column)
				# for i in range(self.task.num_methods):
				# 	exec('self.controller.groupBox{}.pushButton.clicked.connect(self.slot_like)'.format(i))

			else:
				
				if self.lineEdit_column.isEnabled():
					
					# Disable the button
					self.action_save.setEnabled(False)
					self.action_export.setEnabled(False)
					self.action_previous.setEnabled(False)
					self.action_next.setEnabled(False)
					self.action_previous_unrated.setEnabled(False)
					self.action_next_unrated.setEnabled(False)
					self.action_cancel.setEnabled(False)
					self.action_auto.setEnabled(False)

					self.lineEdit_column.setEnabled(False)
					self.lineEdit_scale.setEnabled(False)
					self.btn_previous_unrated.setEnabled(False)
					self.btn_previous.setEnabled(False)
					self.btn_next.setEnabled(False)
					self.btn_next_unrated.setEnabled(False)
					self.lineEdit_serial.setEnabled(False)
					self.hScrollBar_serial.setEnabled(False)
					self.btn_cancel.setEnabled(False)
					self.btn_auto.setEnabled(False)
					self.btn_save.setEnabled(False)
					self.btn_export.setEnabled(False)

					self.lineEdit_num_imgs.setEnabled(False)
					self.lineEdit_num_rated.setEnabled(False)
					self.lineEdit_num_unrated.setEnabled(False)
					self.textBrowser_rated_list.setEnabled(False)
					self.textBrowser_unrated_list.setEnabled(False)

					# Reset default value
					# Default row and column
					self.lineEdit_column.setPlaceholderText(str('1'))
					self.lineEdit_row.setPlaceholderText(str('1'))
					# Default ScrollBar range and state
					self.hScrollBar_serial.setMinimum(1)
					self.hScrollBar_serial.setMaximum(99)
					self.hScrollBar_serial.setValue(1)
					
					# Reset scrollArea
					self.controller.reset_groupbox()
					self.scrollAreaWidgetContents.setStyleSheet('''
						background: url( ''' + check_path('./img/background.png') + ''') no-repeat;
						background-position: center center;
					''')

	def slot_opentask(self):
		print('Open Task')

	def slot_openfolder(self):
		print('Open Folder')

	def slot_hide_toolbar(self):
		if self.is_hide_toolbar:
			self.is_hide_toolbar = False
			self.action_hide_toolbar.setIcon(QIcon(check_path('./img/icons/view-selected.png')))
			self.toolbar.show()
		else:
			self.is_hide_toolbar = True
			self.action_hide_toolbar.setIcon(QIcon(check_path('./img/icons/view-unselected.png')))
			self.toolbar.hide()

	def slot_hide_statebar(self):
		if self.is_hide_statebar:
			self.is_hide_statebar = False
			self.action_hide_statebar.setIcon(QIcon(check_path('./img/icons/view-selected.png')))
			self.statebar.show()
		else:
			self.is_hide_statebar = True
			self.action_hide_statebar.setIcon(QIcon(check_path('./img/icons/view-unselected.png')))
			self.statebar.hide()

	def slot_documentation(self):
		QMessageBox.information(self, 'Documentation', 'In preparation...')

	def slot_about(self):
		QMessageBox.information(self, 'About', 'User Study Tool\n\n Software: USTool\n Developer: Suiyi Zhao\n E-mail: meranderzhao@gmail.com\n Version: 1.0.0\n Language: Python 3.9')

	def slot_lineEdit_column(self):		
		if int(self.lineEdit_column.text()) > self.task.num_methods:
			self.lineEdit_column.setText(str(self.task.num_methods))
		
		self.task.displayed_column = int(self.lineEdit_column.text())
		self.btn_save.setEnabled(True)
		self.action_save.setEnabled(True)
		
		self.controller.reset_groupbox()
		self.controller.rearrange_groupbox(self.task.cur_index, self.task.displayed_scale, self.task.displayed_column)

	def slot_lineEdit_scale(self):
		self.task.displayed_scale = self.lineEdit_scale.text()
		self.btn_save.setEnabled(True)
		self.action_save.setEnabled(True)
		
		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)

	def slot_previous_unrated(self):
		self.task.cur_index = get_max_less_than_x(self.task.cur_index+1, self.task.unrated_list) - 1
		self.hScrollBar_serial.setValue(self.task.cur_index+1)

		self.subslot_reflash_appearance()

		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)

	def slot_previous(self):
		if self.lineEdit_serial.text() == '': # placeholderText
			if self.lineEdit_serial.placeholderText() == '1':
				self.task.cur_index = 0
				self.hScrollBar_serial.setValue(1)
			else:
				self.task.cur_index = int(self.lineEdit_serial.placeholderText()) - 2
				self.hScrollBar_serial.setValue(int(self.lineEdit_serial.placeholderText()) - 1)
		else: # text
			if self.lineEdit_serial.text() != '1':
				self.task.cur_index = int(self.lineEdit_serial.text()) - 2
				self.hScrollBar_serial.setValue(int(self.lineEdit_serial.text()) - 1)

		self.subslot_reflash_appearance()

		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)

	def slot_next(self):
		if self.lineEdit_serial.text() == '': # placeholderText
			if self.lineEdit_serial.placeholderText() == str(self.task.num_imgs):
				self.task.cur_index = self.task.num_imgs - 1
				self.hScrollBar_serial.setValue(self.task.num_imgs)
			else:
				self.task.cur_index = int(self.lineEdit_serial.placeholderText())
				self.hScrollBar_serial.setValue(int(self.lineEdit_serial.placeholderText()) + 1)
		else: # text
			if self.lineEdit_serial.text() != str(self.task.num_imgs):
				self.task.cur_index = int(self.lineEdit_serial.text())
				self.hScrollBar_serial.setValue(int(self.lineEdit_serial.text()) + 1)

		self.subslot_reflash_appearance()
		
		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)
	
	def slot_next_unrated(self):
		self.task.cur_index = get_min_more_than_x(self.task.cur_index+1, self.task.unrated_list) - 1
		self.hScrollBar_serial.setValue(self.task.cur_index+1)

		self.subslot_reflash_appearance()

		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)

	def slot_lineEdit_serial(self):
		if int(self.lineEdit_serial.text()) > self.task.num_imgs:
			self.lineEdit_serial.setText(str(self.task.num_imgs))
		
		self.task.cur_index = int(self.lineEdit_serial.text()) - 1
		self.hScrollBar_serial.setValue(int(self.lineEdit_serial.text()))

		self.subslot_reflash_appearance()
		
		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)

	def slot_hScrollBar_serial_sliderReleased(self):
		self.task.cur_index = self.hScrollBar_serial.value() - 1

		self.subslot_reflash_appearance()
		
		self.controller.rerender_groupbox(self.task.cur_index, self.task.displayed_scale)

	def slot_hScrollBar_serial_valueChanged(self):
		self.lineEdit_serial.setText(str(self.hScrollBar_serial.value()))

	def slot_cancel(self):	
		if self.btn_cancel.isEnabled():
			# Reset 'Like' Button color to black
			method_index = self.task.result_dict.get(self.task.cur_index)
			icon = QIcon()
			icon.addPixmap(QPixmap(check_path("./img/icons/like_black.png")), QIcon.Normal, QIcon.Off)
			exec('self.controller.groupBox{}.pushButton.setIcon(icon)'.format(method_index))

			self.btn_cancel.setEnabled(False)
			self.action_cancel.setEnabled(False)
			self.btn_save.setEnabled(True)
			self.action_save.setEnabled(True)

			# Remove from result dict
			del self.task.result_dict[self.task.cur_index]

			# Change the rated_list/unrated_list
			if not self.task.cur_index+1 in self.task.unrated_list:
				self.task.unrated_list.append(self.task.cur_index+1)
				self.task.unrated_list.sort()
			if self.task.cur_index+1 in self.task.rated_list:
				self.task.rated_list.remove(self.task.cur_index+1)
			# print('Cancel: ', self.task.rated_list, self.task.unrated_list, self.task.result_dict)

			# Write list to state bar
			self.lineEdit_num_rated.setText(str(len(self.task.rated_list)))
			self.lineEdit_num_unrated.setText(str(len(self.task.unrated_list)))
			self.textBrowser_unrated_list.setText(str(self.task.unrated_list)[1:-1])

			self.textBrowser_rated_list.setStyleSheet('''
				color: black;       
			''')
			self.textBrowser_unrated_list.setStyleSheet('''
				color: black;       
			''')
			if len(self.task.rated_list) == 0:
				self.textBrowser_rated_list.setStyleSheet('''
					color: red;
				''')
				self.textBrowser_rated_list.setText('Click "Like" for rating!')
			else:
				self.textBrowser_rated_list.setText(str(self.task.rated_list)[1:-1])

	def slot_auto(self):
		icon = QIcon()
		if self.task.auto_next:
			self.task.auto_next = False
			icon.addPixmap(QPixmap(check_path("./img/icons/auto_gray.png")), QIcon.Normal, QIcon.Off)
		else:
			self.task.auto_next = True
			icon.addPixmap(QPixmap(check_path("./img/icons/auto_green.png")), QIcon.Normal, QIcon.Off)

		self.btn_auto.setIcon(icon)
		self.action_auto.setIcon(icon)

	def slot_save(self):
		self.task.save()
		if self.task.save_path != '':
			self.btn_save.setEnabled(False)
			self.action_save.setEnabled(False)

		self.label_task_name.setText(os.path.basename(self.task.save_path).split('.')[0])

	def slot_export(self):
		writer = TableWriter(self.task.root_path)
		sum = [0 for i in range(self.task.num_methods)]
		for (key, value) in self.task.result_dict.items():
			sum[value] = sum[value] + 1
			writer.writeTable(key+1, value+1, 1)
		for j in range(self.task.num_methods):
			writer.writeTable(self.task.num_imgs+1, j+1, sum[j], is_body=False)
		writer.saveTable()

	def slot_like(self):

		# Activate the chosed button and table value
		icon = QIcon()
		# Reset
		if self.task.result_dict.get(self.task.cur_index) is not None:
			old_method_index = self.task.result_dict.get(self.task.cur_index)
			icon.addPixmap(QPixmap(check_path("./img/icons/like_black.png")), QIcon.Normal, QIcon.Off)
			exec('self.controller.groupBox{}.pushButton.setIcon(icon)'.format(old_method_index))
		# Activate
		clicked_button =  self.sender()
		cur_method_index = clicked_button.property('index')	
		icon.addPixmap(QPixmap(check_path("./img/icons/like_red.png")), QIcon.Normal, QIcon.Off)
		clicked_button.setIcon(icon)

		self.btn_cancel.setEnabled(True)
		self.action_cancel.setEnabled(True)
		self.btn_save.setEnabled(True)
		self.action_save.setEnabled(True)

		# Add to result dict
		self.task.result_dict[self.task.cur_index] = cur_method_index
		
		# Change the rated_list/unrated_list
		if not self.task.cur_index+1 in self.task.rated_list:
			self.task.rated_list.append(self.task.cur_index+1)
			self.task.rated_list.sort()
		if self.task.cur_index+1 in self.task.unrated_list:
			self.task.unrated_list.remove(self.task.cur_index+1)
		# print('Like: ', self.task.rated_list, self.task.unrated_list, self.task.result_dict)
		
		# Write list to state bar
		self.lineEdit_num_rated.setText(str(len(self.task.rated_list)))
		self.lineEdit_num_unrated.setText(str(len(self.task.unrated_list)))
		self.textBrowser_rated_list.setText(str(self.task.rated_list)[1:-1])
		
		self.textBrowser_rated_list.setStyleSheet('''
				color: black;       
			''')
		self.textBrowser_unrated_list.setStyleSheet('''
				color: black;       
			''')
		if len(self.task.unrated_list) == 0:
			self.textBrowser_unrated_list.setStyleSheet('''
				color: red;
			''')
			self.textBrowser_unrated_list.setText('Rating completed! <br> Click "Export" for final result!')
		else:
			self.textBrowser_unrated_list.setText(str(self.task.unrated_list)[1:-1])

		# Auto next
		if self.task.auto_next:
			self.slot_next()	

	def subslot_reflash_appearance(self):
		icon = QIcon()
		icon.addPixmap(QPixmap(check_path("./img/icons/like_black.png")), QIcon.Normal, QIcon.Off)
		for i in range(self.task.num_methods):
			exec('self.controller.groupBox{}.pushButton.setIcon(icon)'.format(i))

		self.btn_cancel.setEnabled(False)
		self.action_cancel.setEnabled(False)

		if self.task.cur_index+1 in self.task.rated_list:
			method_index = self.task.result_dict.get(self.task.cur_index)
			icon = QIcon()
			icon.addPixmap(QPixmap(check_path("./img/icons/like_red.png")), QIcon.Normal, QIcon.Off)
			exec('self.controller.groupBox{}.pushButton.setIcon(icon)'.format(method_index))

			self.btn_cancel.setEnabled(True)
			self.action_cancel.setEnabled(True)
	    
if __name__=="__main__": 
	app = QApplication(sys.argv)

	# Create the window
	w = MyWindow()

	# Display
	w.ui.show()

	app.exec()