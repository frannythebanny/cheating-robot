from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line

from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.clock import Clock, mainthread

import time
import json
import threading


class HBoxWidget(Widget):
    """Documentation for HBoxWidget
    
    """
    def __init__(self, **kwargs):
        super(HBoxWidget, self).__init__(**kwargs)

        self.l0_width = 0.0001
        self.l1_width = 0.0001
        self.l2_width = 0.0001
        self.l3_width = 0.0001
        self.l4_width = 0.0001
        self.l5_width = 0.0001
        self.l6_width = 0.0001
        self.l7_width = 0.0001
        self.l8_width = 0.0001
        self.l9_width = 0.0001
        
        print(self.ids)
        
        self.update_hangman(5)


    def update_hangman(self, lines_to_draw):

        for i in range(lines_to_draw):
            setattr(self, 'l' + str(i) + '_width', 2)

        
class VBoxWidget(Widget):
    """Documentation for VBoxWidget
    
    """
    def __init__(self, **kwargs):
        super(VBoxWidget, self).__init__(**kwargs)
        self.start_thread()
        
    def start_thread(self):
        threading.Thread(target=self.get_text_thread, args=()).start()

    def get_text_thread(self):
        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.get_game_status, 2)

    def update_game_status(self, req, results):

        word_status = results["word_status"]

        game_status = results["game_status"]
        guessed_letters = results["guessed_letters"]

        # Update guessed status
        word_status_label = self.ids.word_status
        word_status_label.text = word_status
        
        # Update guessed status
        guessed_letters_label = self.ids.guessed_letters
        guessed_letters_label.text = guessed_letters

        # Update hangman drawing
        # TODO !

        
    def get_game_status(self, dt):

        headers = {'Content-type': 'application/json'}
        req = UrlRequest('http://195.169.210.194:1234/1',
                         on_success=self.update_game_status,
                         req_headers=headers)

            
class GameView(BoxLayout):
    """Documentation for GameView
    
    """
    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)

    stop = threading.Event()

        
class HangmanApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()
    
    def build(self):
        return GameView()
     
if __name__ == '__main__':
    HangmanApp().run()
