from imports import *
from popups import *

##############################################
######### Factories & Custom Classes #########
##############################################

# TODO: Fix long Press Issue
### Long Press Button for getting to settings
class LongpressButton(Factory.Button):
    __events__ = ('on_long_press', )
    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def do_request_pin(self):
        KeypadPopup().open()

    pass

### Drink Grid Label
class DrinkLabelNumber(Label):

    def __init__(self, **kwargs):
        super(DrinkLabelNumber, self).__init__(**kwargs)
        self.font_size = 32
        # size_hint_y: None
        self.text_size= self.width, None
        # self.height= self.texture_size[1]
        self.halign='center'
        self.valign='center'
        self.font_name= 'assets/fonts/NCAAMichiganStSpartans.otf'
        self.size_hint=(.61, None)
        self.bind(size=self.setter('text_size'))
        
### Drink Grid Button
class DrinkButton(Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(DrinkButton, self).__init__(**kwargs)
        self.text_size= self.width, None
        # self.height= self.texture_size[1]
        self.size_hint=(1, None)
        self.font_name= 'assets/fonts/NCAAMichiganStSpartans.otf'
        # self.halign='left'
        self.valign='center'
        self.font_size = 32
        self.bind(size=self.setter('text_size'))
   
### Drink Grid Rating
class DrinkRating(Label):
    
    def __init__(self, **kwargs):
        super(DrinkRating, self).__init__(**kwargs)
        self.size_hint=(1, None)
        self.text_size= self.width, None
        # self.height= self.texture_size[1]
        self.font_name= 'assets/fonts/NCAAMichiganStSpartans.otf'
        self.halign='center'
        self.valign='center'
        self.font_size = 32
        self.bind(size=self.setter('text_size'))
        
### Scroll View for Drink Grid Layout
class DrinksScrollView(ScrollView):
    
    def __init__(self, id, jsonData, **kwargs):
        super(DrinksScrollView,self).__init__(**kwargs)
        self.id=id
        self.jsonData=jsonData
        self.pos_hint= {'left': .9, 'bottom': 1}
        self.do_scroll_x= False
        self.bar_width= 10
        self.bar_color= .9,.9,.9,.9
        self.add_widget(DrinksGridLayout(jsonData=self.jsonData))

### Mixed Drink Grid Layout
class DrinksGridLayout(GridLayout):  
      
    def __init__(self, jsonData, **kwargs):
        super(DrinksGridLayout, self).__init__(**kwargs)
        self.jsonData=jsonData
        self.cols = 1
        self.size_hint_y= None
        self.valign= 'top'
        self.spacing= 0, 0
        self.padding= 0, 0
        self.row_default_height= '70dp'
        self.row_force_default= True
        self.bind(minimum_height=self.setter('height'))     # Key to scrolling effect
        
        for index, drink in enumerate(self.jsonData):
            gridItem = DrinksGridItem(drink["name"], index+1)
            self.add_widget(gridItem)
            
    # def printStuff(self):
    #     print("IDK")
    
    def set_drink_name(self, name):
        # self.drinkName = name
        print("Name: {0}".format("123"))
        
    def on_release(self):
        print("Released")
        # print(self.DN.text)

### Drinks Grid Item
class DrinksGridItem(ButtonBehavior, GridLayout):
    def __init__(self, name, index, **kwargs):
        super(DrinksGridItem,self).__init__(**kwargs)
        self.name = name
        self.index = index
        self.cols=3
        self.add_widget(DrinkLabelNumber(text="{0}".format(index)))
        self.add_widget(DrinkButton(text=" {0}".format(name)))
        self.add_widget(DrinkRating(text="3/5"))
        
    def on_release(self):
        print("Button pressed: {0},{0}".format(self.name, self.index))
        l_ingredients = "Ingredients: "
        popup = DrinkPopup()
        popup.selectedDrink = self.name
        for drink in drinks_list["mixed_drinks_list"]:
            if drink["name"] == self.name:
                popup.ingredientsArray = drink["ingredients"]
                popup.details = drink["details"]
                # print(drink["ingredients"][name])
        popup.open()
        
### Mixed Drinks Box Layout
class MixedDrinksBoxLayout(BoxLayout):
    
    def __init__(self, **kwargs):
        super(MixedDrinksBoxLayout, self).__init__(**kwargs)
        self.orientation= 'vertical'
        self.spacing= 10
        self.size_hint= .8, .66
        self.pos_hint= {'left': 1, 'bottom': .9}
        self.add_widget(DrinksScrollView(id='mixedDrinksScrollView',jsonData=drinks_list["mixed_drinks_list"]))

### Soda Drink Grid Layout
class SodaBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(SodaBoxLayout, self).__init__(**kwargs)
        self.orientation= 'vertical'
        self.spacing= 10
        self.size_hint= .8, .66
        self.pos_hint= {'right': .9, 'bottom': .9}
        self.add_widget(DrinksScrollView(id='sodaScrollView',jsonData=drinks_list["soda_list"]))

    pass

### Shots Drink Grid Layout
class ShotsBoxLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(ShotsBoxLayout, self).__init__(**kwargs)
        self.orientation= 'vertical'
        self.spacing= 10
        self.size_hint= .8, .66
        self.pos_hint= {'right': 1, 'bottom': .9}
        self.add_widget(DrinksScrollView(id='shotsScrollView',jsonData=drinks_list["shots_list"]))

    pass

# class DrinkGridLayout(GridLayout):
#
#     def __init__(self, **kwargs):
#         super(DrinkGridLayout, self).__init__(**kwargs)
#
#     def build_drink_list(self, drinks_list, screen):
#         for drink in drinks_list:
#             self.add_widget(DrinkButton(text=drink["name"]))


# class DrinkScrollView(ScrollView):
#
#     def __init__(self, **kwargs):
#         super(DrinkScrollView, self).__init__(**kwargs)
#
#     def build_drink_grid_layout(self, drinks_list, screen):
#         # GL =
#         # for drink in drinks_list:
#             self.add_widget(DrinkGridLayout().build_drink_list(drinks_list, screen))
            # self.add_widget(DrinkButton(text=drink["name"]))
            # screen.add_widget(DrinkButton(text=drink["name"]))

# class ConfigLiquidSlider(Slider):
#     def __init__(self, **kwargs):
#         Slider.__init__(self, **kwargs)
#         self.min = 0
#         self.max = 1750
#         self.step = 1
#         self.disabled = True
#         self.orientation = 'horizontal'
#         self.background_horizontal = 'assets/design/Sliders/EmptyCursor.PNG'
#         self.background_disabled_horizontal = 'assets/design/Sliders/EmptyCursor.PNG'
#         self.cursor_size = (0,0)
#         self.value_track = True
#         self.value_track_width = dp(13)