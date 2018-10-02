
from PyQt5.QtWidgets import  QPushButton, QTextEdit
# from PyQt5.QtGui import  QTextCursor
		


# Button Icon
class myIconButton(QPushButton):
	"""docstring for myIconButton"""
	def __init__(self):
		super(myIconButton, self).__init__()
		pass
		
# Button with context menu

class myButtonMenu(myIconButton):
		def __init__(self):
			super(myButtonMenu, self).__init__()
			pass
	
# Button with context menu

class myTextEdit(QTextEdit):
		def __init__(self):
			super(myTextEdit, self).__init__()
			pass
	

# class myTextEditCursor(QTextEdit):
# 		def __init__(self):
# 			super(myTextEditCursor, self).__init__()
# 			myCursor = self.textCursor()
# 			myCursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
# 			self.setTextCursor(myCursor)

