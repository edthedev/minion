import kivy
kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label

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
    search_title = ObjectProperty()
    


    def do_action(self):
        self.search_label.text = 'My label after button press'
        self.info = 'New info text'

class KivyMinion(App):
    controller = None

    def get_results(self):
        debug = dir(self.controller.search_results)
        self.controller.search_title.text = str(debug)
        
        search_text = str(self.controller.search_box.text)
        if len(search_text) > 1:
            files = brain_of_minion.get_files(filter=[search_text])

            for file in files:
                result = Label(text=file)
                self.controller.search_results.add_widget(result)

    def build(self):
        self.controller = Controller(info='Hello world') 
        self.controller.search_button.on_press=self.get_results
        # self.get_results()
        return self.controller 

if __name__ == '__main__':
    KivyMinion().run()
