from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import sqlite3
from my_lists import *

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

with sqlite3.connect('db6.db') as db:
    sql = db.cursor()

TEXTFU = {'item': '', 'steel': '', 'diametr': '', 'width': ''}

LIST_RESULT: str = ''
LIST_PRICE: str = ''
LIST_COUNT: str = ''
LIST_SUM: str = ''
DIAMETR: str = ''
TOTAL: list = []


class MyRoot(BoxLayout):

    def print_result(self):
        TEXTFU['diametr'] = self.ids.diametr.text
        TEXTFU['width'] = self.ids.towchina.text
        TEXTFU['steel'] = self.ids.steel.text
        if TEXTFU['item'] == '':
            self.ids.text_result.text = f"Елемент {TEXTFU['diametr']} {TEXTFU['width']} {TEXTFU['steel']}"
        elif TEXTFU['diametr'] == 'Діаметр':
            self.ids.text_result.text = f"{TEXTFU['item']} Діаметр {TEXTFU['width']} {TEXTFU['steel']}"
        elif TEXTFU['width'] == 'Товщина':
            self.ids.text_result.text = f"{TEXTFU['item']} {TEXTFU['diametr']} Товщина {TEXTFU['steel']}"
        elif TEXTFU['steel'] == 'Сталь':
            self.ids.text_result.text = f"{TEXTFU['item']} {TEXTFU['diametr']} {TEXTFU['width']} Сталь"
        else:
            self.ids.text_result.text = f"{TEXTFU['item']} {TEXTFU['diametr']} {TEXTFU['width']} {TEXTFU['steel']}"
            self.check()

    def f_sendwich(self):
        global DIAMETR
        DIAMETR = 'Діаметр'
        self.ids.diametr.values = DIAM_snd_lst
        self.ids.tube.values = TUBE_snd_lst
        self.ids.trnk.values = TRNK_snd_list
        self.ids.koleno.values = KOLENO_snd_list
        self.ids.zkn.values = ZKN_snd_list
        self.ids.other.values = OTHER_snd_list
        self.ids.gola.color = [1, 1, 1, 1]
        self.ids.sndw.color = [0, 1, 0, 1]

    def f_gola(self):
        global DIAMETR
        DIAMETR = 'Діаметр_1'
        self.ids.diametr.values = DIAM_gola_lst
        self.ids.tube.values = TUBE_gola_lst
        self.ids.trnk.values = TRNK_gola_list
        self.ids.koleno.values = KOLENO_gola_list
        self.ids.zkn.values = ZKN_gola_list
        self.ids.other.values = OTHER_gola_list
        self.ids.sndw.color = [1, 1, 1, 1]
        self.ids.gola.color = [0, 1, 0, 1]

    def f_item(self, instance):
        TEXTFU['item'] = instance.text
        self.print_result()

    def ok_this(self):
        if TEXTFU['item'] != '' and TEXTFU['steel'] != '' and TEXTFU['width'] != '' and TEXTFU['diametr'] != '' and self.ids.text_count.text != '':
            global LIST_RESULT
            global LIST_PRICE
            global LIST_COUNT
            global LIST_SUM
            global TOTAL
            LIST_RESULT = f'{LIST_RESULT}{self.ids.text_result.text}\n'
            LIST_PRICE = f'{LIST_PRICE}{self.ids.text_price.text}\n'
            LIST_COUNT = f'{LIST_COUNT}{self.ids.text_count.text}\n'
            x = int(self.ids.text_count.text) * int(self.ids.text_price.text)
            TOTAL.append(x)
            LIST_SUM = f'{LIST_SUM}{str(x)}\n'
            self.ids.dump_result.text = LIST_RESULT
            self.ids.dump_price.text = LIST_PRICE
            self.ids.dump_count.text = LIST_COUNT
            self.ids.dump_sum.text = LIST_SUM
            self.ids.count.text = 'шт'
            self.ids.text_result.text = ''
            self.ids.text_count.text = ''
            self.ids.text_price.text = ''
            self.total_text()

    def count(self):
        self.ids.text_count.text = self.ids.count.text

    def check(self):
        try:
            o = f'SELECT "{TEXTFU["item"]}" FROM "{TEXTFU["steel"]}" WHERE {DIAMETR} == ? AND Товщина == ?'
            R = sql.execute(o, (TEXTFU['diametr'], TEXTFU['width'])).fetchone()
            self.ids.text_price.text = str(R[0])
        except TypeError:
            self.ids.total.text = 'T_error'
        except sqlite3.OperationalError:
            self.ids.total.text = 'O_error'

    def clear(self):
        global LIST_RESULT
        global LIST_PRICE
        global LIST_COUNT
        global LIST_SUM
        global TOTAL
        for key in TEXTFU.keys():
            TEXTFU[key] = ''
        LIST_RESULT = ''
        LIST_PRICE = ''
        LIST_COUNT = ''
        LIST_SUM = ''
        TOTAL = []

        self.ids.dump_result.text = ''
        self.ids.dump_count.text = ''
        self.ids.dump_price.text = ''
        self.ids.dump_sum.text = ''
        self.ids.total.text = ':::Total:::'
        self.ids.steel.text = 'Сталь'
        self.ids.towchina.text = 'Товщина'
        self.ids.diametr.text = 'Діаметр'
        self.ids.zkn.text = 'Закінчення'
        self.ids.trnk.text = 'Трійник'
        self.ids.tube.text = 'Труба'
        self.ids.krpg.text = 'Кріплення'
        self.ids.koleno.text = 'Коліно'
        self.ids.other.text = 'Інше'
        self.ids.count.text = 'шт'
        self.ids.text_result.text = ''
        self.ids.text_count.text = ''
        self.ids.text_price.text = ''

    def total_text(self):
        global TOTAL
        y = 0
        for i in TOTAL:
            y += i
        self.ids.total.text = str(y)


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return MyRoot()


if __name__ == '__main__':
    MyApp().run()
