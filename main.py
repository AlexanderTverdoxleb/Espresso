import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.sp()

    def sp(self):
        self.setGeometry(200, 200, 800, 800)
        self.load_table()

    def get_table_from_db(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        result = cur.execute("""SELECT products.ID,
        name_variety AS 'Название сорта',
        flavor_description AS 'Описание вкуса',
        roast_degree AS 'Степень обжарки',
        is_milled AS 'Молотый',price AS 'Цена',
        package_volume AS 'Обьем',
        unit AS 'Единица измерения в упаковке' 
        FROM products INNER JOIN coffee_varieties ON products.variety_id = coffee_varieties.ID 
        INNER JOIN packages ON products.package_id = packages.ID""").fetchall()
        columns = [i[0] for i in cur.description]
        con.close()
        return columns, result

    def load_table(self):
        title, data = self.get_table_from_db()
        self.table_widget.setColumnCount(len(title))
        self.table_widget.setHorizontalHeaderLabels(title)
        self.table_widget.setRowCount(0)
        for i, row in enumerate(data):
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table_widget.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
