import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from .database import *


class JournalBox(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN, padding_right=10, padding_bottom=5))
        self.date = toga.DatePicker(style=Pack(padding=(5,0)))
        self.expedition_box = ExpeditionBox()
        self.data_box = DataBox()
        button_save = toga.Button('Сохранить', on_press=self.save, style=Pack(padding=(5, 0)))

        self.add(self.date)
        self.add(self.expedition_box)
        self.add(self.data_box)
        self.add(button_save)

    def save(self, widget):
        self.data_box.save()
        if self.data_box.bentos_switch.value:
            self.data_box.bentos_box.save()
        self.expedition_box.refresh_stantion()


class ExpeditionBox(toga.Box):

    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN))
        self.expedition = toga.Selection(on_select=self.refresh_stantion, style=Pack(padding_top=5, flex=1))
        add_expedition_btn = toga.Button('➕', on_press=self.show_add, style=Pack(padding_top=4, width=30))
        self.title_expedition = toga.TextInput(placeholder='название экспедиции', style=Pack(padding_top=5, flex=1))
        btn_ok = toga.Button('ok', on_press=self.add_expedition, style=Pack(padding_top=4, width=30))

        row1 = toga.Box(children=[self.expedition, add_expedition_btn], style=Pack(direction=ROW))
        self.row2 = toga.Box(children=[self.title_expedition, btn_ok], style=Pack(direction=ROW))
        self.add(row1)
        self.refresh_from_db()

    def show_add(self, widget=None):
        if self.row2 in self.children:
            self.remove(self.row2)
        else:
            self.add(self.row2)

    def add_expedition(self, widget=None):
        Expedition.create(title=self.title_expedition.value)
        self.remove(self.row2)
        self.refresh_from_db()

    def refresh_stantion(self, widget=None):
        try:
            data_box: DataBox = self.parent.data_box
        except AttributeError:
            return
        expedition = Expedition.select().where(Expedition.title == self.expedition.value)
        data_box.stantion.items = [str(i) for i in Stantion.select().where(Stantion.expedition == expedition)]

    def refresh_from_db(self):
        self.expedition.items = [str(i) for i in Expedition.select()]


class DataBox(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN))

        self.stantion = toga.Selection(style=Pack(padding_top=5))

        self.bentos_switch = toga.Switch('Бентос', value=True, on_change=self.add_bentos_box)
        self.fito_switch = toga.Switch('Фитопланктон')
        self.zoo_switch = toga.Switch('Зоопланктон')
        self.checkboxes_box = toga.Box(
            children=[self.bentos_switch, self.fito_switch, self.zoo_switch],
            style=Pack(padding_top=5)
        )

        self.num = toga.TextInput(placeholder='№', style=Pack(flex=1, padding_top=5, padding_right=3))
        self.depth = toga.TextInput(placeholder='Глубина', style=Pack(flex=1, padding_top=5))
        self.N = toga.TextInput(placeholder='N', style=Pack(flex=1, padding_top=5, padding_right=3))
        self.E = toga.TextInput(placeholder='E', style=Pack(flex=1, padding_top=5))
        self.stantion_info_box = toga.Box(style=Pack(direction=COLUMN))
        self.stantion_info_box.add(
            toga.Box(children=[self.num, self.depth], style=Pack(direction=ROW)),
            toga.Box(children=[self.N, self.E], style=Pack(direction=ROW)),
        )

        self.bentos_box = BentosBox()

        self.add(self.stantion)
        self.add(self.checkboxes_box)
        self.add(self.stantion_info_box)
        self.add(self.bentos_box)


    def add_bentos_box(self, widget=None):
        if self.bentos_box in self.children:
            self.remove(self.bentos_box)
        else:
            self.add(self.bentos_box)

    def save(self):
        expedition = Expedition.select().where(Expedition.title == self.parent.expedition_box.expedition.value)
        data = {
            'num': self.num.value,
            'N': self.N.value,
            'E': self.E.value,
            'bentos': self.bentos_switch.value,
            'fito': self.fito_switch.value,
            'zoo': self.zoo_switch.value,
            'depth': self.depth.value,
            'expedition': expedition,
            'date': self.parent.date.value
        }
        Stantion.create(**data)

class BentosBox(toga.Box):

    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN, padding_top=5))
        self.coat = toga.TextInput(placeholder='Грунт', style=Pack(padding_top=5))
        self.bentos = toga.MultilineTextInput(placeholder='Живые', style=Pack(padding_top=5))
        self.add(self.coat)
        self.add(self.bentos)

    def save(self):

        stantion = Stantion.select().where(Stantion.num == self.parent.stantion.value.replace('Станция ', ''))
        print([i for i in stantion])
        # Bentos.create(coat=self.coat.value, bentos=self.bentos.value, stantion_id=stantion)

class NewWindow():
    """ create new window toga"""



