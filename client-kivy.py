from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.list import TwoLineListItem
from kivy.metrics import dp

import socket

from kivy.core.window import Window

loader = """
<Screen1>:
    name: 's1'
    MDTextField:
        id: n
        hint_text: "LED ID"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        multiline: False
    MDTextField:
        id: r
        hint_text: "RED value"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: g
        hint_text: "GREEN Value"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDTextField:
        id: b
        hint_text: "BLUE Value"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        multiline: False
    MDRectangleFlatButton:
        text: "CLEAR"
        font_size: '18sp'
        pos_hint: {'center_x':0.4, 'center_y':0.25}
        on_release: app.clear()
    MDRectangleFlatButton:
        text: "SEND"
        font_size: '18sp'
        pos_hint: {'center_x':0.6, 'center_y':0.25}
        on_release: app.send_message(n.text, r.text, g.text, b.text)
"""

Builder.load_string(loader)

class Screen1(Screen):
    pass

class ChatApp(MDApp):

    def build(self):
        # self.icon = "icon.png"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sm = ScreenManager()
        self.sm.add_widget(Screen1(name = 's1'))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        SERVER = "192.168.1.204"
        PORT = 5050
        self.client.connect((SERVER, PORT))
        print('Connected to server!')

        return self.sm

    def send_message(self, n, r, g, b):
        message = f"N{n} R{r} G{g} B{b}"
        print(message)
        msg = message.encode('utf-8')
        msg_len = len(msg)
        send_len = str(msg_len).encode('utf-8')
        send_len += b' ' * (64 - len(send_len))
        self.client.send(send_len)
        self.client.send(msg)
        self.sm.get_screen('s1').ids.n.text = ""
        self.sm.get_screen('s1').ids.r.text = ""
        self.sm.get_screen('s1').ids.g.text = ""
        self.sm.get_screen('s1').ids.b.text = ""

    def clear(self):
        self.sm.get_screen('s1').ids.n.text = ""
        self.sm.get_screen('s1').ids.r.text = ""
        self.sm.get_screen('s1').ids.g.text = ""
        self.sm.get_screen('s1').ids.b.text = ""

    def on_stop(self):
        print("App closed")
        self.client.send("!DC")

ChatApp().run()
