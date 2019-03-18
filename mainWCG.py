import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from wcA2 import Ui_MainWindow
#import matplotlib.image as mpimg
from wordCloudAlgo import final_funcs

class MyFirstGuiProgram(Ui_MainWindow):
    stopWords = []
    WordCloudObj = None
    mpltr = None

    def __init__(self, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        # set up the radio buttons 
        self.set_radio_buttons_default()
        self.makeCloud.clicked.connect(self.plot_word_cloud)
        self.addStopWord.clicked.connect(self.addToStopWordList)
        self.deleteStopWord.clicked.connect(self.removeFromStopWordList)
        self.saveCloud.clicked.connect(self.saveWordCloud)

    def set_radio_buttons_default(self):
        self.bigramRB.setChecked(True)
        self.rectangularRB.setChecked(True)

    def plot_data(self):
        #img=mpimg.imread('wc.png')
        self.mpl.canvas.ax.imshow(img)
        self.mpl.canvas.draw()
    
    def plot_word_cloud(self):
        raw_text = self.textInput.toPlainText()
        self.mpltr = self.mpl.canvas
        self.WordCloudObj = final_funcs(self,raw_text, self.mpltr, bad_words_list = self.stopWords)
    
    def saveWordCloud(self):
        if self.WordCloudObj == None:
            print("Please generate word cloud first!")
        else:
            fig_name = self.saveCLoudName.text()
            if fig_name == "" or fig_name == " ":
                fig_name = "word_cloud"
            self.mpltr.fig.savefig(fig_name + ".png")
     
    def addToStopWordList(self):
        word = self.stopWordInput.text()
        if not word in self.stopWords:
            self.stopWords.append(word)    
            self.stopWordList.addItem(word)
            self.stopWordInput.clear()

    def removeFromStopWordList(self):
        for SelectedItem in self.stopWordList.selectedItems():
            print(SelectedItem.text())
            self.stopWordList.takeItem(self.stopWordList.row(SelectedItem))
            self.stopWords.remove(SelectedItem.text())    
            self.stopWordInput.clear()
            #self.stopWordList.takeItem(word)
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(window)

    window.show()
    sys.exit(app.exec_())