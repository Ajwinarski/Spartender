### Import required items
from imports import *

### Import custom items
from factories import *
from helpers import *
from popups import *
from screens import *


### The Spartender Application
class SpartenderApp(App):

    # App data and variables
    primary = green                         # Primary color used in UI
    secondary = white                       # Secondary color used in UI
    loggedInUserName = ""                   # Current sessions user name
    loggedInUserCredits = 0                 # Current sessions user credits

    # keyboard = Popup(content=Button(text='1'),
    #     size_hint=(None, None), size=(360, 360))

    # Info for the Settings config
    def build_config(self, config):
        # Initialize the Settings tab
        config.setdefaults('settings', {
            'partyMode': False,
            'pinMode': True,
            'darkMode': True})
            # 'numericexample': 10,
            # 'optionsexample': 'option2',
            # 'stringexample': 'some_string',
            # 'pathexample': '/some/path'

        # Initialize the Users tab
        config.setdefaults('users', {
            'entername': '',
            'enterpin': False,
            'userslist': '',
            'userscredits': 0})
        
    #TODO: Add and remove setting based on if I am the one accessing settings
    # def close_settings(self, *args):
        
    #     def __init__(self, *args):
    #         super(SpartenderApp, self).__init__(*args)
    #         self.stop
    #         print("C")
        
        # try:
        # p = App.settings_popup
        # p.dismiss()
        # except AttributeError:
            # pass # Settings popup doesn't exist
        
        # return True

    # Add the Settings pages
    def build_settings(self, settings):
        # Add Setting panels
        settings.add_json_panel('General',
                                self.config,
                                data=settings_json)
        settings.add_json_panel('Users',
                                self.config,
                                data=users_json)
        # settings.add_json_panel('Template',
        #                         self.config,
        #                         data=template_json)
        # Use this is modify the settings appearance
        # settings.pos_hint = ({"right": 1, "center_y": .5})
        # settings.size_hint = (0.9, 0.9)
        pass

    # Setup the Settings and Pages
    def build(self):
        # TODO: FIX THE SETTINGS PANEL SO THAT THERE IS A quit()
        Setter = SettingsWithSidebar
        self.settings_cls = Setter
        # self.add_kivy_panel()

        # self.settings_cls = SettingsWithSidebar
        # self.settings_cls.add_widget(self, button1)
        # self.settings.add_interface(self)
        self.use_kivy_settings = False

        # Menu Pages
        mainPage = MainScreen(name = "main")
        drinksPage = DrinksScreen(name='drinks')
        configPage = ConfigScreen(name='config')

        # Drinks Pages
        mixedDrinksPage = MixedDrinksScreen(name='mixedDrinks')
        shotsDrinksPage = ShotsDrinksScreen(name='shotsDrinks')
        sodaDrinksPage = SodaDrinksScreen(name='sodaDrinks')

        # Additional Pages
        self.keypadPage = KeypadPopup()

        # Make the global Screen Manager
        self.sm = sm

        ### Add the screen widgets
        # Main screen pages
        sm.add_widget(mainPage)
        sm.add_widget(drinksPage)
        sm.add_widget(configPage)

        # Drinks screen pages
        sm.add_widget(mixedDrinksPage)
        sm.add_widget(shotsDrinksPage)
        sm.add_widget(sodaDrinksPage)

        # Set the first page to be main
        sm.current = "main"

        return self.sm

    # Hides the given widget from the view
    def hideWidget(self, wid, hide):
        if hide:
            wid.opacity, wid.disabled = 0, True
        elif not hide:
            wid.opacity, wid.disabled = 1, False
        pass

    # Swap the primary and secondary colors
    def changeColorMode(self, wid, _color):
        for item in wid:
            item.color = _color
        # Swaps the primary and secondary colors
        # self.primary, self.secondary = self.secondary, self.primary
        # colorObject.color = self.primary
        pass

    # Triggered when a setting has been changed
    def on_config_change(self, config, section, key, value):
        # IF: The config passed is the local config
        if config is self.config:
            token = (section, key)

            # Logic for Party Mode
            if token == ('settings', 'partyMode'):
                # Define the screen(s) and button(s) you want to hide and modify
                mainScreen = self.sm.get_screen('main')
                configWid = mainScreen.ids.configBtn
                settingsWid = mainScreen.ids.settingsBtn
                drinksButton = mainScreen.ids.drinksBtn
                drinksImage = mainScreen.ids.drinksImg
                widgets = [configWid, settingsWid]

                # Call the function to hide config button here
                for wid in widgets:
                    self.hideWidget(wid, int(value))

                if int(value):
                    drinksButton.size_hint = (.9, 45)
                    drinksImage.source = './assets/design/DrinksBtnLarge.PNG'
                else:
                    drinksButton.size_hint = (.38, .45)
                    drinksImage.source = './assets/design/DrinksBtn.PNG'

                # Used to check the partyMode value in our .ini file
                # print(config.get('settings', 'partyMode'))
                pass

            # TODO: Complete the dark mode 
            # Logic for dark Mode
            elif token == ('settings', 'darkMode'):

                widgets = []
                # List the pages and items on those pages
                # that need to be changed here

                ## Main Screen widgets
                mainScreen = self.sm.get_screen('main')
                titleLabel = mainScreen.ids.title

                ## Drink Screen widgets
                drinksScreen = self.sm.get_screen('drinks')
                nameLabel = drinksScreen.ids.nameTxt

                ## Drink Screen widgets
                configScreen = self.sm.get_screen('config')
                vodkaLabel = configScreen.ids.label_vodka_value
                rumLabel = configScreen.ids.label_rum_value
                soda1Label = configScreen.ids.label_soda1_value
                soda2Label = configScreen.ids.label_soda2_value
                widgets = [titleLabel, nameLabel, vodkaLabel,
                            rumLabel, soda1Label, soda2Label]

                if int(value):
                    self.changeColorMode(widgets, self.secondary)
                    Window.clearcolor = self.primary

                else:
                    self.changeColorMode(widgets, self.primary)
                    Window.clearcolor = self.secondary

            # Logic for new users entering there pins
            elif token == ('users', 'enterpin'):

                if int(value):
                    config.set('users', 'enterpin', False)
                    name = config.get('users', 'entername')
                    settingsPin = KeypadPopup(title='Enter your pin (Cannot be changed later!)')
                    settingsPin.popupType = 'create'
                    if name != 'name':
                        settingsPin.user = name
                    settingsPin.open()

            # Logic for entering credits for a user
            elif token == ('users', 'userscredits'):

                if int(value):
                    # Get the selected name from the list
                    _name = config.get('users', 'userslist')
                    # Open the database for reading and writing
                    # _data = csv_database()
                    # new_row = _data.get_row("Austin")
                    # print("Row containing Austin: {new_row}")


                    print(f"User {_name} has been given {value} credits")

### Run the app
if __name__ == '__main__':
    SpartenderApp().run()
