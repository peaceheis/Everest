import json

import PySimpleGUI as sg


class EverestApplication:
    def __init__(self):
        self.CONFIG = self.load_or_create_config()

    def load_or_create_config(self) -> dict:
        try:
            f = open("config.json", "r")
            return json.load(f)
        except FileNotFoundError:
            sg.Popup("No config.json found. First-time init will be done. ")
            # initialize namespace
            layout = [
                [sg.T("choose a namespace. most namespaces are all lowercase, and a single word. (this can be changed later)")],
                [sg.Input(key="namespace")],
                [sg.Button("submit")]
            ]
            namespace_window = sg.Window("Everest", layout)
            event, values = namespace_window.read()
            if event == sg.WINDOW_CLOSED:
                return
            config = {"namespace": values["namespace"]}
            with open("config.json", "w") as f:
                json.dump(config, f)
                namespace_window.close()

            sg.Popup("Successfully initialized config!")
            return config

    def run(self):
        layout = [
            [sg.T("here")]
        ]
        window = sg.Window("Everest", layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                self.clean_up()
                return

    def clean_up(self):
        return


app = EverestApplication()
app.run()
