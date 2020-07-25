### Generic Imports
import kivy
import json
import base64
import random
import csv
import time
from functools import partial
# from kivy import require
from tinydb import TinyDB, Query
from kivy.storage.jsonstore import JsonStore

### Kivy UIX and Primary Module Imports
from kivy.app import App
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import Settings
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import *
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.widget import Widget

### Other Kivy Module Imports
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.metrics import dp, sp
from kivy.properties import *

# Imports the settings, users, and drinks via json
import sys
sys.path.append('databases/')
from settingsjson import *
from drinks import *

# Import the kv_files directory
# ROOT_PATH = os.path.dirname(__file__)
# KV_FILES = os.path.join(ROOT_PATH, 'kv_files')
# KV_CLASSES = [c[:-3] for c in os.listdir(KV_FILES)
#     if c.endswith('.kv')]

# Raspberry Pi Imports
# import RPi.GPIO as GPIO

### Define the config parser for settings
config = ConfigParser()

### Define the Screen Manager
sm = ScreenManager(transition = SlideTransition(duration = 0.70))

### Define a TinyDB Database & Query for searching
users = TinyDB('databases/users.json')
drinks = TinyDB('databases/users.json')
Users = Query()
PinQuery = Query()

### JSON Files
# drinksStore = JsonStore()

### CSV Files
csvDB = './databases/database.csv'

### Globals
green = (0.09411,0.270588,0.231372,1)   # rgba(24,69,59,255) / 255 (Forest Green)
white = (1,1,1,1)                       # rbga(0, 0, 0, 255) / 255 (Pure White)
currentUserName = ''                    # Current sessions user name (TODO: Fix this global)
currentUserCredits = '9999'             # Current sessions user credits (TODO: Fix this global)

### Set the window color and to fullscreen without the top menu
from kivy.core.window import Window
Window.size = (800, 480)                # x = 800px, y = 480px
Window.borderless = True                # Make the window borderless
Window.clearcolor = green               # Set the background color to forest green

### Mark as true to see what the program is doing in better detail
commenting = False
