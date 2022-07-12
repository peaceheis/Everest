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


def nav_bar():
    return sg.Frame("nav", [[B("Cont-Eros"), B("Temp-Humidity"), B("Weirdness-Depth")]])


def cont_bracket():
    return sg.Frame("", [[sg.B("Add Continentalness Bracket", expand_x=True, expand_y=True,auto_size_button=True, key="add_cont_bracket")], [sg.T("from: "), sg.Input(expand_x=True, expand_y=True, key="from_cont"), sg.T("to: "), sg.Input(expand_y=True, size=10, key="to_cont")]], element_justification="center", expand_x=True, expand_y=True)


def remove_frame():
    return sg.Frame("", [[sg.B("Remove Entry", expand_x=True, expand_y=True, key="remove_entry")], [sg.T("Cont row:"), sg.Input("Cont.", key="remove_cont", expand_x=True), sg.T("Eros row:"), sg.Input("Eros.", key="remove_eros", expand_x=True)]])


def eros_bracket():
    return sg.Frame("", [[sg.B("Add Erosion Bracket", expand_x=True, expand_y=True, key="add_eros_bracket")], [sg.T("from: "), sg.Input(expand_x=True, expand_y=True, key="from_eros"), sg.T("to: "), sg.Input(expand_y=True, size=10, key="to_eros")]], element_justification="center", expand_x=True, expand_y=True)


class EverestApplication:
    def __init__(self):
        self.CONFIG = load_or_create_config()
        self.brackets = []

    def regen_brackets(self, key_prefix: str, delete_x, delete_y):
        new_brackets = []
        x_count = 0
        y_count = 0
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for x, button in enumerate(old_row):
                if x == delete_x and y == delete_y:
                    continue
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def process_values_and_create_window(self, window, event, values):
        match event:
            case "add_cont_bracket":
                window["add_cont_bracket"].update("here we are?")
            case "add_eros_bracket":
                pass
            case "remove_entry":
                window.close()
                self.regen_brackets("EC", int(values["remove_eros"]), int(values["remove_cont"]))
                layout = [
                    [sg.Frame("nav", [[B("Cont-Eros"), B("Temp-Humidity"), B("Weirdness-Depth")]])],
                    [Label("Terrain Parameters", font="times 18")],
                    [cont_bracket(), remove_frame(), eros_bracket()],
                    [Label("increasing continentalness left-right, increasing erosion top to bottom",
                           font="arial 16")],
                    *self.brackets
                ]
                return sg.Window("Everest", layout, resizable=True, auto_size_text=True, auto_size_buttons=True)

            case _:
                print(event, values)

    def run(self):
        self.brackets = [[B(f"Button{y * 5 + x}", key=f"EC${y * 5 + x}", pad=(20, 5)) for x in range(5)] for y in range(5)]

        layout = [
            [nav_bar()],
            [Label("Terrain Parameters", font="times 18")],
            [cont_bracket(), remove_frame(), eros_bracket()],
            [Label("increasing continentalness left-right, increasing erosion top to bottom", font="arial 16")],
            *self.brackets
        ]

        window = sg.Window("Everest", layout, resizable=True, auto_size_text=True, auto_size_buttons=True)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                self.clean_up()
                return
            window = self.process_values_and_create_window(window, event, values)

    def clean_up(self):
        return

app = EverestApplication()
app.run()
