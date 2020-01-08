import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("books.ui", self)
        con = sqlite3.connect("books.db")
        cur = con.cursor()
        r = cur.execute(f"SELECT id, title, author, id_genre, year FROM about_books").fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Id", "Title", "Author", "Genre", "Year"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(r):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if j == 3:
                    genre = cur.execute(f"SELECT name_of_genre FROM genres WHERE id = {elem}").fetchone()
                    genre, = genre
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(genre)))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        con.commit()
        con.close()
        self.pushButton.clicked.connect(self.search)

    def search(self):
        author = self.lineEdit.text()
        book = self.lineEdit_2.text()
        con = sqlite3.connect("books.db")
        cur = con.cursor()
        if author != '' and book == '':
            about = cur.execute(f"SELECT * FROM about_books WHERE author = '{author}'").fetchone()
        elif author == '' and book != '':
            about = cur.execute(f"SELECT * FROM about_books WHERE title = '{book}'").fetchone()
        elif author != '' and book != '':
            about = cur.execute(f"SELECT * FROM about_books WHERE title = '{book}' and author = '{author}'").fetchone()
        if about != None:
            self.label_8.setText(str(about[1]))
            self.label_9.setText(str(about[2]))
            genr = cur.execute(f"SELECT name_of_genre FROM genres WHERE id = {about[3]}").fetchone()
            genr, = genr
            self.label_11.setText(str(genr))
            print(1)
            pixmap = QPixmap()
            pixmap.loadFromData(about[4])
            self.label_7.setPixmap(pixmap)
            self.label_10.setText(str(about[5]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
