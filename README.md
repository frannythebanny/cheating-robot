# Cheating Robot Project - Radboud 2015

Franziska Burger, Josca Snippe, Volker Strobel

This is the code for the HRI project 'Cheating Robot' (Radoud
University) -- a framework for studying the halo effect in human-robot
interaction based on the game hangman.

For the implementation of the experimental framework, Aldebaran’s Nao
robot was programmed with Nao's Python SDK 1.14.52. The robot is
capable of interacting autonomously with the users by using speech
recognition and speech synthesis. Additionally, an application with a
graphical user interface (GUI) that displays the Hangman game status
for the participant is included. It also allows the experimenter to
change the parameters of the interaction (social vs. neutral) and
monitor the game.

The code consists of three majors parts:

- The hangman game that runs on a PC and the NAO (base folder) 
- The server and data base that runs on a PC (folder `Server/`)
- The kivy app that runs on a tablet, mobile phone or PC (folder `GUI`)

The idea of the server is to enable the NAO and the the mobile phone
app to communicate with each other and to keep track of the game
states:

![Architecture](https://raw.githubusercontent.com/Pold87/cheating-robot/master/architecture.png "Architecture")

To run the code, first start the server (run `Server/run_flask.py`),
then start the app (`GUI/main.py`), and finally the game (`game.py`).

## Important Files and Folders

- `Server/run_flask.py`: Initializes the server (default IP: http://127.0.0.1:1235/). If you want to see the current game state, browse to: http://127.0.0.1:1235/1, the settings are found at: http://127.0.0.1:1235/settings. If you want to use the framework with a real NAO and a mobile phone, you have to use a public ip address for your server.
- `global_settings.py`: Global settings -- for example, specifies if a real NAO is available or the IP address of the server.
- `game.py`: This is the main file that starts the social interaction and the game.
- `abort.py`: Sometimes the NAO does not stop listening when the script crashes, running abort.py usually helps then.
- `GUI/main.py`: Runs the kivy app.

Python dependencies:
flask, flask_restful, sqlalchemy, cython, kivy, etc. (install them with `pip`)
