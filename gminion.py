import kivy
kivy.require('1.2.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

import brain_of_minion
# TODO: Make enter key do the search.
# TODO: Strip line breaks out of searches.
# TODO: Clear results between searches.
# TODO: Provide notification when there are no results. (Put search
#    terms inside of --search term--

class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    info = StringProperty()
    search_label = ObjectProperty()
    search_box = ObjectProperty()
    search_results = ObjectProperty()
    search_button = ObjectProperty()
    # search_title = ObjectProperty()
    
    def do_action(self):
        self.search_label.text = 'My label after button press'
        self.info = 'New info text'

def open_file(button):
    brain_of_minion.open_file(button.text, graphical=True)

class GMinion(App):
    controller = None

    def get_results(self):
        # TODO: Add a status bar...
        # debug = dir(self.controller.search_results)
        # self.controller.search_title.text = str(debug)
        
        search_text = str(self.controller.search_box.text)
        if len(search_text) <= 1:
            return
        
        files = brain_of_minion.find_files(filter=[search_text])
    
        file_list = '\n'.join(files) 
        # results = TextInput(text=file_list, multiline=True)
        # self.controller.search_results.add_widget(results)
        # for file in files:

        # lay_o = GridLayout(
        #         cols = 1, 
        #         size_hint_y = 2,
        #        )
#         lay_o = BoxLayout()
#         lay_o.orientation = 'vertical'
#         lay_o.size_hint_y = 2
        # scrolly = ScrollView()
        # scrolly.add_widget(lay_o)

        for file in files:
            result = Button(text=file)
            result.bind(on_press=open_file)
            result.size_hint = (1, None)

 #             lay_o.add_widget(result)
            self.controller.search_results.add_widget(result)

#         self.controller.search_results.add_widget(lay_o)

    def build(self):
        self.controller = Controller(info='Hello world') 
        self.controller.search_button.on_press=self.get_results
        self.controller.search_box.on_text_validate=self.get_results

        # self.get_results()
        return self.controller 

if __name__ == '__main__':
    GMinion().run()
