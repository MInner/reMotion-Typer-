import sys
from PyQt4 import QtGui, QtCore
import popplerqt4
import time

def sensor_data_generator():
    for line in open('log2.txt'):
        time.sleep(0.1)
        yield line.split()[3]

data = sensor_data_generator()

class PageListner(QtCore.QThread):
    """ A single-thread listner. Watches data from opengazer. 
    If can see page turn, emits signal.
    """

    page_turned = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.counter = [-1]*10 # size of floating window

    def return_on_page_turn(self):
        """ Must return controll when new page movement is detected"""
        for num in data:
            self.counter.pop(0)
            self.counter.append(num) # floating window
            print(num)
            if self.counter.count('7') > 1 and self.counter.count('5') > 1:
                break

    def run(self):
        self.return_on_page_turn()
        self.page_turned.emit('data')

class PdfViewGui(QtGui.QWidget):
    """Return a Scrollarea showing the first page of the specified PDF file."""
    
    def __init__(self, filename):

        super(PdfViewGui, self).__init__()
        self.label = QtGui.QLabel()
        
        self.doc = popplerqt4.Poppler.Document.load(filename)
        self.doc.setRenderHint(popplerqt4.Poppler.Document.Antialiasing)
        self.doc.setRenderHint(popplerqt4.Poppler.Document.TextAntialiasing)
        
        self.n = 0
        self.render_page()

        self.listen_for_next_page()
        
        self.area = QtGui.QScrollArea()
        self.area.setWidget(self.label)
        self.area.setWindowTitle(filename)
        
    def on_page_turned(self):
        self.n += 1
        self.render_page()
        self.listen_for_next_page()

    def listen_for_next_page(self):
        self.page_turn_listner = PageListner()
        self.page_turn_listner.page_turned.connect(self.on_page_turned)
        self.page_turn_listner.start()

    def render_page(self):
        page = self.doc.page(self.n)
        image = page.renderToImage()
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

def main():
    app = QtGui.QApplication(sys.argv)
    argv = QtGui.QApplication.arguments()
    if len(argv) < 2:
        sys.exit(2)
    
    filename = argv[-1]
    g = PdfViewGui(filename)
    g.area.show()
    print("before exec")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
