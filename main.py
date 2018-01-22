from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.mainWindowGUI import Ui_MainWindow
import sys
import os
from gui.lib import *
from MoneyPy import *
import datetime

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window of the application. Contains all global parameters of the GUI application.
    """

    def __init__(self, parent=None):
        """
        Initializes the main window and sets up the entire GUI application.
        :param parent: No parent
        :return: None
        """
        # Initiate parent class
        super(MainWindow, self).__init__(parent)

        # Setup GUI
        self.setupUi(self)
        self.setWindowIcon(QIcon('./img/icon.png'))
        self.setGeometry(100, 100, 800, 600)
        self.statusBar()
        self.change_qss('actionAqua')

        # Connections
        self.confirmBtnAddExpense.clicked.connect(self.add_expense)
        self.confirmBtnAddIncome.clicked.connect(self.add_income)

        

    def change_qss(self, theme):
        themes = {'actionAqua': './gui/css/aqua/aqua.qss',
                  'actionBasicWhite': './gui/css/basicWhite/basicWhite.qss',
                  'actionBlueGlass': './gui/css/blueGlass/blueGlass.qss',
                  'actionDarcula': './gui/css/darcula/darcula.qss',
                  'actionDark': './gui/css/dark/darkstyle.qss',
                  'actionDarkBlue': './gui/css/darkBlue/style.qss',
                  'actionDarkBlueFreeCAD': './gui/css/darkBlue(FreeCAD)/stylesheet.qss',
                  'actionDarkGreen': './gui/css/darkGreen/darkGreen.qss',
                  'actionDarkGreenFreeCAD': './gui/css/darkGreen(FreeCAD)/stylesheet.qss',
                  'actionDarkOrange': './gui/css/darkOrange/darkOrange.qss',
                  'actionDarkOrangeFreeCAD': './gui/css/darkOrange(FreeCAD)/stylesheet.qss',
                  'actionLight': './gui/css/light/light.qss',
                  'actionLightBlueFreeCAD': './gui/css/lightBlue(FreeCAD)/stylesheet.qss',
                  'actionLightGreenFreeCAD': './gui/css/lightGreen(FreeCAD)/stylesheet.qss',
                  'actionLightOrangeFreeCAD': './gui/css/lightOrange(FreeCAD)/stylesheet.qss',
                  'actionMachinery': './gui/css/machinery/machinery.qss',
                  'actionMinimalist': './gui/css/minimalist/Minimalist.qss',
                  'actionNightMapping': './gui/css/nightMapping/style.qss',
                  'actionWombat': './gui/css/wombat/stylesheet.qss',
                  }
        # for i in themes.keys():
        #     eval('self.{}.setChecked(False)'.format(i))
        # eval('self.{}.setChecked(True)'.format(theme))

        qss = open_qss(themes[theme])
        app.setStyleSheet(qss)

    def add_expense(self):
        year = self.calendarAddExpense.selectedDate().year()
        month = self.calendarAddExpense.selectedDate().month()
        day = self.calendarAddExpense.selectedDate().day()
        date = datetime.date(year, month, day)
        value = float(get_text(self.valueAddExpense))
        category = get_text(self.categoryAddExpense)
        description = get_text(self.descriptionAddExpense)
        account = get_text(self.accountAddExpense)
        observations = get_text(self.observationsAddExpense)
        transaction = Expense(date, value, category, description, account, observations)
        self.add_transaction(transaction)

    def add_income(self):
        year = self.calendarAddIncome.selectedDate().year()
        month = self.calendarAddIncome.selectedDate().month()
        day = self.calendarAddIncome.selectedDate().day()
        date = datetime.date(year, month, day)
        value = float(get_text(self.valueAddIncome))
        category = get_text(self.categoryAddIncome)
        description = get_text(self.descriptionAddIncome)
        account = get_text(self.accountAddIncome)
        observations = get_text(self.observationsAddIncome)
        transaction = Income(date, value, category, description, account, observations)
        self.add_transaction(transaction)

    def add_transaction(self, transaction):
        wb = Workbook()
        wb.add_transaction(transaction)
        wb.save_and_quit()
        message_title = "Transaction added"
        message_body = "Your transaction was added"
        QMessageBox.information(self, message_title, message_body, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())