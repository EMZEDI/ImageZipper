# Author: Shahrad Mohammadzadeh
# A python script that zips an unlimited files under a directory to a tgz file
import os 
import sys
import zipfile
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import ntpath

class MyApp(QWidget):
	def __init__(self):

		super().__init__()
		self.window_width, self.window_height = 600, 200
		self.setMinimumSize(self.window_width, self.window_height)

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.options = ('Files to zip (choose the files first and destination later and launch)', 
		'Folder to zip (choose folder first and destination later and launch)')

		self.combo = QComboBox()
		self.combo.addItems(self.options)
		layout.addWidget(self.combo)

		btn = QPushButton('Launch')
		btn.clicked.connect(self.launchDialog)
		layout.addWidget(btn)

	def launchDialog(self):
		option = self.options.index(self.combo.currentText())

		if option == 0:
			self.getFileNames()
		elif option == 1:
			self.getDirectory()
		else:
			print('Got Nothing')
	
	def finalLaunchDialog(self):
		###

		self.options = ('Destination folder of zip file (choose and launch)')

		self.combo = QComboBox()
		self.combo.addItems(('Destination folder of zip file (choose and launch)', None))
		

		btn = QPushButton('zip and finish!')
		btn.clicked.connect(self.finalLaunchDialog)
		###

		option = self.options.index(self.combo.currentText())

		if option == 0:
			return(self.getDestinationDir())
		else:
			print('Got Nothing')

	def getFileNames(self):
		file_filter = 'Data File (*.jpg *.png)'
		response = QFileDialog.getOpenFileNames(
			parent=self,
			caption='Select a data file',
			directory=os.getcwd(),
			filter=file_filter,
			initialFilter='Data File (*.jpg *.png)'
		)
		
		# returns a list of paths.
		return self.filesinfo(response[0])

	def getDirectory(self):
		response = QFileDialog.getExistingDirectory(
			self,
			caption='Select a folder'
		)
		
		# returns a string of the path of the dir
		return self.dirinfo(response)

	def getDestinationDir(self):
		# same as getDirectory
		response = QFileDialog.getExistingDirectory(
			self,
			caption='Select a folder'
		)
		
		# returns a string of the path of the dir
		return response

	def dirinfo(self, dirpath):
		# gets the path of the dir and returns a tuple of 
		# (list of the paths of the files, list of the names of the files)
		# returns the result to the zipper function
		files_list = [f for f in os.listdir(dirpath) if os.isfile(os.join(dirpath, f))]
		def path_leaf(path):
			head, tail = ntpath.split(path)
			return tail or ntpath.basename(head)

		return self.zipper((files_list, [path_leaf(i) for i in files_list]))

	def filesinfo(self, list_of_paths):
		# gets the list of paths of the files and returns a tuple of
		# (list of the paths of the files, list of the names of the files)
		# returns the result to the zipper function
		def path_leaf(path):
			head, tail = ntpath.split(path)
			return tail or ntpath.basename(head)

		return self.zipper((list_of_paths, [path_leaf(i) for i in list_of_paths]))

	def zipper(self, file_paths_names):
		# given the tuple of the file paths and names it zips the given files
		# and saves to the inputted directory 
		path_list, name_list = file_paths_names
		destination_path = self.finalLaunchDialog()
		# we have the destination string and the inputs 
		# zip the files
		i = 1
		destination = (destination_path + "/Paco'sZip.tgz")
		while os.path.exists(destination):
			i += 1
			destination = ((destination_path + "/Paco'sZip{0}.tgz").format(i))
		with zipfile.ZipFile(destination, 'w') as zipMe:        
			for i in range(len(path_list)):
				zipMe.write(path_list[i], compress_type=zipfile.ZIP_DEFLATED, arcname=name_list[i])
		sys.exit(app.exec_())


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet('''
		QWidget {
			font-size: 18px;
		}
	''')
	
	myApp = MyApp()
	myApp.show()

	try:
		sys.exit(app.exec_())
	except SystemExit:
		print('Closing Window...')