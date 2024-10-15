import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

#start my_app 
my_app = QApplication(sys.argv) 
#open webpage 
initurl = 'https://www.google.co.jp'

# setting browser
browser = QWebEngineView()
browser.load(QUrl(initurl))        
browser.resize(1000,600)
browser.move(100,100)

browser.show() 
#sys exit function 
sys.exit(my_app.exec_()) #https://sho10case.com/2019/04/05/https-sho10case-com-programingschol-1-4-browser/
