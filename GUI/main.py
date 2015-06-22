from __future__ import division

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from kivy.base import EventLoop 

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle

from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.clock import Clock, mainthread
from kivy.core.window import Window

import time
import json
import threading

class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    
    def send_settings(self, participant_name, game_variant, condition):
        
        params = {
            'participant_name': str(participant_name),
            'game_variant': game_variant,  # Evil, good, or normal hangman?
            'condition': int(condition),  # Social or neutral robot?
            'participant_number': 1
        }

        data = json.dumps(params)

        url = 'http://195.169.210.194:1234/settings'
        headers = {'Content-type': 'application/json'}
        
        req = UrlRequest(url,
                         req_headers=headers,
                         req_body=data,
                         method='PUT')

        req.wait()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        
        pass

class HangmanScreenmanager(ScreenManager):
    def __init__(self, **kwargs):
        super(HangmanScreenmanager, self).__init__(**kwargs)


class MySettings(FloatLayout):
    def __init__(self, **kwargs):
        super(MySettings, self).__init__(**kwargs)   

class MyWidget(FloatLayout):
    """
    Documentation for HBoxWidget
    """

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

        self.pink = (173 / 255, 41 / 255, 110 / 255, 255 / 255)
        Window.clearcolor = self.pink
        
        self.start_thread()

    def start_thread(self):
        threading.Thread(target=self.get_text_thread, args=()).start()

    def get_text_thread(self):
        # call my_callback every 0.5 seconds
        Clock.schedule_interval(self.get_game_status, 2)


    def update_hangman(self, lines_to_draw):

        self.parent.ids.hangman_img.source = str(lines_to_draw) + '.png'

    def update_game_status(self, req, results):


        word_status = results["word_status"]
        wrong_letters = results["wrong_letters"]
        num_wrong_letters = results["num_wrong_letters"]
        game_status = results["game_status"]

        # Update guessed status
        word_status_label = self.parent.ids.word_status
        word_status_label.text = word_status
        
        # Update guessed status
        wrong_letters_label = self.parent.ids.wrong_letters
        wrong_letters_label.text = "Wrong:\n" + wrong_letters

        # Update game status
        game_status = results["game_status"]
        game_over_label = self.parent.ids.game_over

        # Won, lost, or still running?

        if game_status == 1:
            game_over_label.text = "WINNER"
        elif game_status == 0:
            game_over_label.text = "GAME OVER"
            word_status_label.text = "Word was:\n" + word_status
                        
        else:
            game_over_label.text = ""
            
        self.update_hangman(num_wrong_letters)

        
    def get_game_status(self, dt):

        headers = {'Content-type': 'application/json'}
        req = UrlRequest('http://195.169.210.194:1234/1',
                         on_success=self.update_game_status,
                         req_headers=headers)

        
class HangmanApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        self.root.stop.set()
    
    def build(self):
        # return GameView()
        return HangmanScreenmanager()
     
if __name__ == '__main__':
    HangmanApp().run()
