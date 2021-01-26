from requests import get
from json import loads
from PyQt5 import QtWidgets
from dict import Ui_widget
from sys import argv, exit

"""
=>word, audio, (meanings)
=>partOfSpeech, (definitions)
=>definition, example, (in/none)synonyms
"""
class window(QtWidgets.QWidget):
    def __init__(self):
        super(window,self).__init__()
        self.ui=Ui_widget()
        self.ui.setupUi(self)

        self.ui.findword.clicked.connect(self.searcher)
        self.ui.pagesize.currentIndexChanged[str].connect(self.manual)
        self.ui.backpage.clicked.connect(self.back)
        self.ui.nextpage.clicked.connect(self.nextt)
    def searcher(self):
        self.currentpage=1
        self.word=self.ui.entersign.text()
        if self.word!="Enter a word..." and self.word!="Not a word!":
            self.text=loads(get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{str(self.word)}").text)

            if len(self.text)==3:
                self.ui.entersign.setText("Not a word!")
                self.ui.explanation.setText("")
                self.ui.example.setText("")
                self.ui.synonyms.setText("")
                self.ui.nextpage.setDisabled(True)
                self.ui.backpage.setDisabled(True)
                self.ui.pagesize.clear()
                self.ui.pagesize.setDisabled(True)
            else:            
                self.ui.pagesize.clear()
                self.pages=len(self.text[0]["meanings"])
                for i in range(1,self.pages+1):
                    self.ui.pagesize.addItem(str(i))
                if self.pages>1:
                    self.ui.pagesize.setDisabled(False)

                self.loader()
        else:
            self.ui.entersign.setText("Not a word!")
    def loader(self):
        self.ui.explanation.setText(f"""Part of Speech: {self.text[0]["meanings"][self.currentpage-1]["partOfSpeech"].capitalize()}\nDefinition: {self.text[0]["meanings"][self.currentpage-1]["definitions"][0]["definition"].capitalize()}""")
        if "example" in self.text[0]["meanings"][self.currentpage-1]["definitions"][0]:
            self.ui.example.setText(f"""Use in sentence:\n{self.text[0]["meanings"][self.currentpage-1]["definitions"][0]["example"].capitalize()}.""")
        if "synonyms" in self.text[0]["meanings"][self.currentpage-1]["definitions"][0]:
                counter=1
                self.ui.synonyms.setText(f"""Synonyms:\n1. {self.text[0]["meanings"][self.currentpage-1]["definitions"][0]["synonyms"][0].capitalize()}\n""")
                for i in self.text[0]["meanings"][self.currentpage-1]["definitions"][0]["synonyms"]:
                    counter+=1
                    self.ui.synonyms.setText(f"{self.ui.synonyms.toPlainText()}{counter}. {i.capitalize()}\n")
        else:
            self.ui.synonyms.setText("")
        if self.currentpage==1:
            self.ui.backpage.setDisabled(True)
        elif self.currentpage!=1:
            self.ui.backpage.setDisabled(False)
        if self.currentpage==self.pages:
            self.ui.nextpage.setDisabled(True)
        elif self.currentpage!=self.pages:
            self.ui.nextpage.setDisabled(False)
    def back(self):
        self.currentpage-=1
        self.ui.pagesize.setCurrentText(str(self.currentpage))
        self.loader()
    def nextt(self):
        self.currentpage+=1
        self.ui.pagesize.setCurrentText(str(self.currentpage))
        self.loader()
    def manual(self,commandpage):
        if len(self.ui.pagesize)>0:
            self.currentpage=int(commandpage)
            self.loader()
if __name__=="__main__":
    app=QtWidgets.QApplication(argv)
    win=window()
    win.show()
    exit(app.exec_())
