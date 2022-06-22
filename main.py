import json

import PySimpleGUI as sg


# just so porting to better logging isn't a pain
def log(msg: str):
    print(log)


def load_or_create_config() -> dict | None:
    try:
        f = open("config.json", "r")
        log("found config")
        return json.load(f)
    except FileNotFoundError:
        sg.Popup("No config.json found. First-time init will be done. ")
        # initialize namespace
        layout = [
            [sg.T(
                "choose a namespace. most namespaces are all lowercase, and a single word. (this can be changed later)")],
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


label_config: dict = {"justification": "center", "auto_size_text": True, "expand_x": True, "text_color": "white"}
button_config: dict = {"expand_x": True, "expand_y": True}


def B(txt: str, **kwargs):
    return sg.B(txt, **button_config, **kwargs)


def Label(txt: str, **kwargs):
    return sg.T(txt,**label_config, **kwargs)


cont_bracket = sg.Column([[sg.B("Add Continentalness Bracket")], [sg.T("from: "), sg.Input(expand_y=False, size=10), sg.T("to: "), sg.Input(expand_y=False, size=10)]], justification="center", element_justification="center", expand_x=True, expand_y=True)
erosion_bracket = sg.Column([[sg.B("Add Erosion Bracket")], [sg.T("from: "), sg.Input(expand_y=False, size=10), sg.T("to: "), sg.Input(expand_y=False, size=10)]], justification="center", element_justification="center", expand_x=True, expand_y=True)

CONFIG = [
    [Label("Terrain Parameters", font="times 18")],
    [cont_bracket, erosion_bracket],
    [Label("increasing continentalness left-right, increasing erosion top to bottom", size=12)],
    [*[B("Placeholder") for i in range(5)]],
    [*[B("Placeholder") for i in range(5)]],
    [*[B("Placeholder") for i in range(5)]]
]


class EverestApplication:
    def __init__(self):
        self.CONFIG = load_or_create_config()

    def run(self):
        layout = [
            [sg.T("here")]
        ]
        window = sg.Window("Everest", CONFIG, resizable=True, auto_size_text=True, auto_size_buttons=True)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                self.clean_up()
                return

    def clean_up(self):
        return


app = EverestApplication()
app.run()
