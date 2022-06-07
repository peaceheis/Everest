import json

import PySimpleGUI as sg

CONFIG = {}

def init_config():
    try:
        config = json.load(open("config.json", "r"))
        CONFIG["namespace"] = config["namespace"]
    except FileNotFoundError:
        namespace_init_layout = [
            [sg.T("choose a namespace (this can be changed later)")],
            [sg.Input(key="namespace")],
            [sg.B("create")]
        ]
        window = sg.Window('Everest', namespace_init_layout, grab_anywhere=True, finalize=True)

        with open("config.json", "w") as f:
            event, values = window.read()
            CONFIG["namespace"] = values["namespace"]
            json.dump(CONFIG, f)


init_config()
