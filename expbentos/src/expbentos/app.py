"""
Приложения для ведения полевого дневника
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, HIDDEN, NONE, VISIBILITY_CHOICES
from .database import *
from .boxes import *
from .journal import *

class ExpBentos(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        create_database()

        main_box = toga.Box(style=Pack(direction=COLUMN))

        journal = JournalBox()

        container = toga.OptionContainer()
        container.add('Журнал', journal)

        main_box.add(container)


        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.size = (300, 500)
        self.main_window.show()



class ExpBentos_old(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        create_database()



        journal_btn = toga.Button('Экспедиционный журнал')


        main_box = toga.Box(style=Pack(direction=COLUMN))
        self.stantion_box = StantionBox()

        container = toga.OptionContainer()

        container.add('Журнал', self.stantion_box)
        main_box.add(container)


        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.size = (300, 500)
        self.main_window.show()





def main():
    return ExpBentos()
    # return ExpBentos_old()


