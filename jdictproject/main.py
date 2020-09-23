import sys
import traceback

from PyQt5.QtGui import QFont
from jamdict import Jamdict
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QLabel, QLineEdit, QWidget, \
    QMessageBox, QTabWidget, QListWidget, QComboBox, QInputDialog, QHBoxLayout, QGridLayout
from jdictproject.database import connectDB, newTable, insertWord, listTable, deleteWord, dropTable, selectWord, \
    getTables, exportCSV
from jdictproject.tokenize import toTokensDictionary
from jdictproject.translate import toRomaji, toKatakana, toHiragana, toFurigana
from PyQt5.QtCore import Qt


# TODO work on GUI aesthetics

def new_excepthook(type, value, tb):
    # By default, Qt does not output any errors, this prevents that
    traceback.print_exception(type, value, tb)


class Window(QMainWindow):
    sys.excepthook = new_excepthook

    con = connectDB()

    Rtext, Ktext, Htext, Ftext = [None for _ in range(4)]

    def __init__(self):
        super(QWidget, self).__init__()

        globalFont = QFont("Times New Roman", 11)
        globalFont.setWeight(18)
        QApplication.setFont(globalFont)

        # Creating tabs and layouts
        self.layout = QVBoxLayout(self)
        self.Hlayout = QHBoxLayout(self)
        self.HDBlayout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.MainTab = QWidget()
        self.DBTab = QWidget()
        self.tabs.addTab(self.MainTab, "Translate")
        self.tabs.addTab(self.DBTab, "Saved Words")

        self.MainTab.layout = QVBoxLayout(self)
        self.MainTab.layout.addLayout(self.Hlayout)
        self.DBTab.layout = QGridLayout()

        # Defining QLabels
        self.insertionBox = QLineEdit()
        self.romajiBox = QLabel()
        self.romajiBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.katakanaBox = QLabel()
        self.katakanaBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.hiraganaBox = QLabel()
        self.hiraganaBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.furiganaBox = QLabel()
        self.furiganaBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.entriesBox = QLabel()
        self.entriesBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.entriesBox.setWordWrap(True)
        self.charsBox = QLabel()
        self.charsBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.charsBox.setWordWrap(True)

        recordFont = QFont("Times New Roman", 15)
        recordFont.setWeight(18)
        self.romajiLabel = QLabel("Romaji")
        self.romajiLabel.setFont(recordFont)
        self.katakanaLabel = QLabel("Katakana")
        self.katakanaLabel.setFont(recordFont)
        self.hiraganaLabel = QLabel("Hiragana")
        self.hiraganaLabel.setFont(recordFont)
        self.furiganaLabel = QLabel("Furigana")
        self.furiganaLabel.setFont(recordFont)
        self.entriesLabel = QLabel("Entries")
        self.entriesLabel.setFont(recordFont)
        self.charsLabel = QLabel("Characters")
        self.charsLabel.setFont(recordFont)
        self.romajiLabelDB = QLabel("Romaji")
        self.romajiLabelDB.setFont(recordFont)
        self.katakanaLabelDB = QLabel("Katakana")
        self.katakanaLabelDB.setFont(recordFont)
        self.hiraganaLabelDB = QLabel("Hiragana")
        self.hiraganaLabelDB.setFont(recordFont)
        self.furiganaLabelDB = QLabel("Furigana")
        self.furiganaLabelDB.setFont(recordFont)
        self.entriesLabelDB = QLabel("Entries")
        self.entriesLabelDB.setFont(recordFont)
        self.charsLabelDB = QLabel("Characters")
        self.charsLabelDB.setFont(recordFont)

        self.romajiBoxDB = QLabel()
        self.romajiBoxDB.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.katakanaBoxDB = QLabel()
        self.katakanaBoxDB.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.hiraganaBoxDB = QLabel()
        self.hiraganaBoxDB.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.furiganaBoxDB = QLabel()
        self.furiganaBoxDB.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.entriesBoxDB = QLabel()
        self.entriesBoxDB.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.entriesBoxDB.setWordWrap(True)
        self.charsBoxDB = QLabel()
        self.charsBoxDB.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.charsBoxDB.setWordWrap(True)

        # Globally accessible text from insertionBox in MainTab
        global text
        text = self.insertionBox.text

        # For switching tables in DBTab
        self.tableDropDown = QComboBox()
        self.tableDropDown.setDuplicatesEnabled(False)
        for item in getTables(self.con):
            self.tableDropDown.addItem(repr(item).strip("('',)"))
        self.DBTab.layout.addWidget(self.tableDropDown)

        # List of saved words in selected table in DBTab
        self.listWords = QListWidget()
        self.listWords.setFixedWidth(145)
        self.listWords.itemSelectionChanged.connect(self.selectionView)
        self.DBTab.layout.addWidget(self.listWords)
        self.listWordsAdd()
        self.tableDropDown.currentTextChanged.connect(lambda: self.listWordsAdd())

        # Adding widgets to tab layouts
        self.MainTab.layout.addWidget(self.insertionBox)
        self.MainTab.layout.addWidget(self.romajiLabel)
        self.MainTab.layout.addWidget(self.romajiBox)
        self.MainTab.layout.addWidget(self.katakanaLabel)
        self.MainTab.layout.addWidget(self.katakanaBox)
        self.MainTab.layout.addWidget(self.hiraganaLabel)
        self.MainTab.layout.addWidget(self.hiraganaBox)
        self.MainTab.layout.addWidget(self.furiganaLabel)
        self.MainTab.layout.addWidget(self.furiganaBox)
        self.MainTab.layout.addWidget(self.entriesLabel)
        self.MainTab.layout.addWidget(self.entriesBox)
        self.MainTab.layout.addWidget(self.charsLabel)
        self.MainTab.layout.addWidget(self.charsBox)

        self.DBTab.layout.addWidget(self.entriesLabelDB, 0, 1)
        self.DBTab.layout.addWidget(self.entriesBoxDB, 1, 1)
        self.DBTab.layout.addWidget(self.katakanaLabelDB, 2, 1)
        self.DBTab.layout.addWidget(self.katakanaBoxDB, 3, 1)
        self.DBTab.layout.addWidget(self.hiraganaLabelDB, 4, 1)
        self.DBTab.layout.addWidget(self.hiraganaBoxDB, 5, 1)
        self.DBTab.layout.addWidget(self.furiganaLabelDB, 6, 1)
        self.DBTab.layout.addWidget(self.furiganaBoxDB, 7, 1)
        self.DBTab.layout.addWidget(self.romajiLabelDB, 8, 1)
        self.DBTab.layout.addWidget(self.romajiBoxDB, 9, 1)
        self.DBTab.layout.addWidget(self.charsLabelDB, 10, 1)
        self.DBTab.layout.addWidget(self.charsBoxDB, 11, 1)

        # Creating buttons, connecting them to functions
        newTableButton = QPushButton("New List", self)
        newTableButton.setFixedWidth(145)
        self.DBTab.layout.addWidget(newTableButton)
        newTableButton.clicked.connect(self.newTableButtonClicked)

        deleteButton = QPushButton("Delete", self)
        deleteButton.setFixedWidth(145)
        self.DBTab.layout.addWidget(deleteButton)
        deleteButton.clicked.connect(self.deleteItemClicked)

        deleteTableButton = QPushButton("Delete List", self)
        deleteTableButton.setFixedWidth(145)
        self.DBTab.layout.addWidget(deleteTableButton)
        deleteTableButton.clicked.connect(self.deleteTableClicked)

        exportButton = QPushButton("Export to CSV", self)
        exportButton.setFixedWidth(145)
        self.DBTab.layout.addWidget(exportButton)
        exportButton.clicked.connect(self.clickExportCSV)

        translationButton = QPushButton("Translate", self)
        translationButton.setFixedWidth(145)

        saveButton = QPushButton("Save Word", self)
        saveButton.setFixedWidth(145)

        self.Hlayout.addWidget(translationButton)
        self.Hlayout.addWidget(saveButton)
        translationButton.clicked.connect(self.translationButtonClicked)
        saveButton.clicked.connect(self.saveButtonClicked)

        # Window setup
        self.widget = QWidget()
        self.widget.setWindowTitle("Japanese Lookup Tool")

        self.MainTab.setLayout(self.MainTab.layout)
        self.DBTab.setLayout(self.DBTab.layout)
        self.layout.addWidget(self.tabs)
        self.widget.setLayout(self.layout)
        self.widget.setMinimumSize(400, 700)
        self.widget.show()

    def translationButtonClicked(self, text):
        if self.insertionBox.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("There is no word to translate!")
            msg.exec_()
        else:
            jmd = Jamdict()
            text = self.insertionBox.text()

            Window.Rtext = toRomaji(text)
            Window.Ktext = toKatakana(text)
            Window.Htext = toHiragana(text)
            result = jmd.lookup(text)

            text = toTokensDictionary(text)

            separater = ""
            Window.Ftext = toFurigana(text)
            Window.Ftext = separater.join(Window.Ftext)

            if result == None:
                result = jmd.lookup(Window.Ktext)
            if result == None:
                result = jmd.lookup(Window.Htext)

            Window.Etext = repr(result.entries).strip("[]")
            Window.Ctext = repr(result.chars).strip("[]")

            self.romajiBox.setText(Window.Rtext)
            self.katakanaBox.setText(Window.Ktext)
            self.hiraganaBox.setText(Window.Htext)
            self.furiganaBox.setText(Window.Ftext)
            self.entriesBox.setText(Window.Etext)
            self.charsBox.setText(Window.Ctext)

            return Window.Rtext, Window.Ktext, Window.Htext, Window.Ftext

    def saveButtonClicked(self):
        if len(getTables(self.con)) == 0:
            msg = QMessageBox()
            msg.setText("No lists to save to!")
            msg.exec_()
            return
        if Window.Rtext:
            tables = getTables(self.con)
            tables = [t[0] for t in tables]
            table, ok = QInputDialog.getItem(self, "List option",
                                             "Choose list to save to:", tables, 0, False)
            if ok and table:
                msg = QMessageBox()
                insertWord(self.con, table, self.Rtext, self.Ktext, self.Htext, self.Ftext, self.Etext, self.Ctext)
                msg.setText("Word saved to " + table)
                msg.exec_()
                if self.currentTable().strip("''") == table:
                    self.listWords.addItem(repr(self.Rtext).strip("''"))
        else:
            msg = QMessageBox()
            msg.setText("There is no translated word to save!")
            msg.exec_()

    def newTableButtonClicked(self):
        nameNewTable, ok = QInputDialog.getText(self, 'New list', 'Enter new list name:')
        if self.tableDropDown.findText(nameNewTable) == -1:
            self.tableDropDown.addItem(nameNewTable)
            newTable(self.con, nameNewTable)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Error creating list")
            msg.exec_()

    def deleteItemClicked(self):
        if self.listWords.selectedItems() != 0:
            for item in self.listWords.selectedItems():
                deleteWord(self.con, self.listWords.currentItem().text(), self.currentTable())
                self.listWords.takeItem(self.listWords.row(item))
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("There is no word selected to delete!")
            msg.exec_()

    def deleteTableClicked(self):
        table = self.currentTable()
        confirm = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete " + table + "?",
                                       QMessageBox.Yes, QMessageBox.Cancel)
        if confirm == QMessageBox.Yes:
            index = self.tableDropDown.findText(table.strip("''"))
            self.tableDropDown.removeItem(index)
            dropTable(self.con, table)

    def updateDBTabList(self, input):
        if type(input) is list:
            self.romajiBoxDB.setText(input[0])
            self.katakanaBoxDB.setText(input[1])
            self.hiraganaBoxDB.setText(input[2])
            self.furiganaBoxDB.setText(input[3])
            self.entriesBoxDB.setText(input[4])
            self.charsBoxDB.setText(input[5])
        else:
            self.romajiBoxDB.setText(input)
            self.katakanaBoxDB.setText(input)
            self.hiraganaBoxDB.setText(input)
            self.furiganaBoxDB.setText(input)
            self.entriesBoxDB.setText(input)
            self.charsBoxDB.setText(input)

    def selectionView(self):
        if self.listWords.selectedItems() != 0 and self.listWords.currentItem() is not None and self.currentTable() is not None:
            list = selectWord(self.con, self.listWords.currentItem().text(), self.currentTable())
            if list:
                self.updateDBTabList(list)

    def currentTable(self):
        if self.tableDropDown.currentText() is not None:
            return repr(self.tableDropDown.currentText())
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Create a list to be able to save words")
            msg.exec_()
            return None

    def listWordsAdd(self):
        self.updateDBTabList("")
        if len(getTables(self.con)) != 0 and self.currentTable() is not None:
            wordList = listTable(self.con, self.currentTable())
            self.listWords.clear()
            for word in wordList:
                self.listWords.addItem(repr(word).strip("'()',"))

    def clickExportCSV(self):
        exportCSV(self.con, self.currentTable())
        msg = QMessageBox()
        msg.setWindowTitle("Export successful")
        msg.setText("Exported as " + self.currentTable().strip("''") + ".csv")
        msg.exec_()


def run():
    app = QApplication(sys.argv)
    GUI = Window()

    sys.exit(app.exec_())


run()
