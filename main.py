from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView, FileChooserController
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
import os, boto3

class FileList(FileChooserListView):
    def __init__(self, **kwargs):
        super(FileChooserListView, self).__init__(**kwargs)
        root = FloatLayout(size=self.size)
        self.button = Button(text="Upload", pos_hint={'x': .9, 'y': .95}, size_hint=(.1, .05))
        self.button.bind(on_press=self.upload)
        self.api_secret_input = TextInput(multiline=False, text="AWS API Secret Key", pos_hint={'x': 0.7, 'y': 0.95}, size_hint=(.2, .05))
        self.api_access_input = TextInput(multiline=False, text="AWS API Access Key", pos_hint={'x': 0.5, 'y': 0.95}, size_hint=(.2, .05))
        self.bucket_input = TextInput(multiline=False, text="Bucket Name", pos_hint={'x': 0.3, 'y': 0.95}, size_hint=(.2, .05))
        self.add_widget(self.button)
        self.add_widget(self.api_access_input)
        self.add_widget(self.api_secret_input)
        self.add_widget(self.bucket_input)
    def entry_touched(self, entry, touch):
        if os.path.isfile(entry.path):
            if entry.path not in self.selection:
                self.selection.append(entry.path)
                print self.selection
            else:
                self.selection.remove(entry.path)
    def update(self, dt):
        for entry in self._items:
            if entry.path in self.selection:
                entry.is_selected = True
            elif entry.path not in self.selection:
                entry.is_selected = False
    def upload(self, instance):
        files = self.selection
        s3 = boto3.resource('s3', aws_access_key_id=self.api_access_input.text,
                            aws_secret_access_key=self.api_secret_input.text)
        for i in files:
            with open(i, 'rb') as inf:
                print i.split('\\')[-1]
                s3.Bucket(self.bucket_input.text).put_object(Key=i.split('\\')[-1], Body=inf)

#Even color, odd color SELECTED: [0.5, 0.5, 0.5, 0.1] [1.0, 1.0, 1.0, 0.0]

class S3App(App):
    def build(self):
        files = FileList()
        Clock.schedule_interval(files.update, 1.0 / 60.0)
        return files

def main():
    S3App().run()

if __name__ == "__main__":
    main()