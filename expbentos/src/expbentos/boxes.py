import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from .database import *


class StantionBox(toga.Box):

    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN, padding=20))

        self.bentos_switch = toga.Switch('Бентос', value=True, style=Pack(padding=5), on_change=self.add_bentos)
        self.fito_switch = toga.Switch('Фитопланктон', style=Pack(padding=(5,0)))
        self.zoo_switch = toga.Switch('Зоопланктон', style=Pack(padding=(5,0)))

        expedition_title = toga.Label('Дон март 2023', style=Pack(padding=(5,0), text_align=CENTER))

        self.date = toga.DatePicker(style=Pack(padding=(5,0)))
        items_stantion = [str(i) for i in Stantion.select()]
        self.stantions = toga.Selection(items=items_stantion, on_select=self.change_stantion, style=Pack(padding=(5,0)))

        self.num = toga.TextInput(placeholder='№', style=Pack(padding=(5,0), flex=1))
        self.depth = toga.TextInput(placeholder='Глубина', style=Pack(padding=(5,0), flex=1))
        self.N = toga.TextInput(placeholder='N', style=Pack(padding=(5,0), flex=1))
        self.E = toga.TextInput(placeholder='E', style=Pack(padding=(5,0), flex=1))

        self.bentos_box = BentosBox(style=Pack(direction=COLUMN, padding=(5,0)))
        button_save = toga.Button('Сохранить', on_press=self.save, style=Pack(padding=4, flex=1))

        self.add(
            toga.Box(children=[expedition_title, self.date, self.stantions], style=Pack(direction=COLUMN)),
            toga.Box(children=[self.bentos_switch, self.fito_switch, self.zoo_switch], style=Pack(direction=ROW)),
            toga.Box(children=[self.num, self.depth], style=Pack(direction=ROW)),
            toga.Box(children=[self.N, self.E], style=Pack(direction=ROW)),
            toga.Box(children=[self.bentos_box, button_save], style=Pack(direction=COLUMN))
        )

    def change_stantion(self, widget):
        st = Stantion.select().where(Stantion.num == self.stantions.value.replace('Станция ', ''))
        self.depth.value = st[0].depth
        print(st[0].depth)

    def add_bentos(self, widget):
        if widget.value:
            for child in self.bentos_box.children:
                child.style.update(visibility='visible')
        else:
            for child in self.bentos_box.children:
                child.style.update(visibility='hidden')

    def save(self, widget):
        data = {
            'num': self.num.value,
            'N': self.N.value,
            'E': self.E.value,
            'bentos': self.bentos_switch.value,
            'fito': self.fito_switch.value,
            'zoo': self.zoo_switch.value,
            'depth': self.depth.value,
            'coat': self.bentos_box.coat.value,
            'date': self.date.value
        }
        Stantion.create(**data)
        items_stantion = [str(i) for i in Stantion.select()]
        self.stantions.items = items_stantion
        print(
            f'{self.fito_switch.value=}\n{self.bentos_switch.value=}\n{self.E=}\n{self.coat=}\n'
            f'{self.bentos=}\n{self.depth=}\n{self.date=}')


class BentosBox(toga.Box):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.coat = toga.TextInput(placeholder='Грунт', style=Pack(flex=1))
        self.bentos = toga.MultilineTextInput(placeholder='Живые')
        self.add(self.coat)
        self.add(self.bentos)
