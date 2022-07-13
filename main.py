import copy
import json

import PySimpleGUI as sg

from PySimpleGUI import Frame


def log(msg: str):
    print(msg)


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
    return sg.T(txt, **label_config, **kwargs)


def nav_bar():
    return sg.Frame("File Management",
                    [[B("Export Biome Source To JSON", key="export"), B("Save Project", key="save")]])


def cont_bracket():
    return sg.Frame("", [[sg.B("Add Continentalness Bracket", expand_x=True, expand_y=True, auto_size_button=True,
                               key="add_cont_bracket")],
                         [sg.T("from: "), sg.Input(expand_x=True, expand_y=True, key="from_cont"), sg.T("to: "),
                          sg.Input(expand_y=True, size=10, key="to_cont")]], element_justification="center",
                    expand_x=True, expand_y=True)


def remove_frame():
    return sg.Frame("", [[sg.B("Remove Entry", expand_x=True, expand_y=True, key="remove_entry")],
                         [sg.T("Cont row:"), sg.Input(key="remove_cont", expand_x=True), sg.T("Eros row:"),
                          sg.Input("Eros.", key="remove_eros", expand_x=True)]])


def eros_bracket():
    return sg.Frame("", [[sg.B("Add Erosion Bracket", expand_x=True, expand_y=True, key="add_eros_bracket")],
                         [sg.T("from: "), sg.Input(expand_x=True, expand_y=True, key="from_eros"), sg.T("to: "),
                          sg.Input(expand_y=True, size=10, key="to_eros")]], element_justification="center",
                    expand_x=True, expand_y=True)


def ec_modification_frames() -> tuple[Frame, Frame]:
    return modification_frame("Remove", "rm", "Continentalness", "cont", "Erosion", "eros", "ec"), \
           modification_frame("Add", "add", "Continentalness", "cont", "Erosion", "eros", "ec")


def th_modification_frames() -> tuple[Frame, Frame]:
    return modification_frame("Remove", "rm", "Temperature", "temp", "Humidity", "hum", "th"), \
           modification_frame("Add", "rm", "Temperature", "temp", "Humidity", "hum", "th")


def modification_frame(modification: str, modification_key: str, column_name: str, column_key: str, row_name: str,
                       row_key: str, key_prefix: str):
    return sg.Frame(f"{modification}", [
        [sg.Frame(f"Column ({column_name})",
                  [[sg.Combo([f"{i + 1}" for i in range(5)], key=f"{column_key}_{modification_key}_column"),
                    sg.B(f"{modification} Column", key=f"{column_key}_{modification_key}", expand_x=True,
                         expand_y=True)]]),
         sg.Frame("Individual Entry",
                  [[sg.T("Row:"),
                    sg.Combo([f"{i + 1}" for i in range(5)], key=f"{key_prefix}_{modification_key}_indi_row"),
                    sg.T("Column:"),
                    sg.Combo([f"{i + 1}" for i in range(5)], key=f"{key_prefix}_{modification_key}_indi_column"),
                    sg.B(f"{modification} Individual", key=f"{key_prefix}_{modification_key}_indi")]]),
         sg.Frame(f"Row ({row_name})",
                  [[sg.Combo([f"{i + 1}" for i in range(5)], key=f"{row_key}_{modification_key}_row"),
                    sg.B(f"{modification} Row", key=f"{row_key}_{modification_key}", expand_x=True, expand_y=True)]])]],
                    expand_x=True, element_justification="center")


class EverestApplication:
    def __init__(self):
        self.CONFIG = load_or_create_config()
        self.brackets: list[list[sg.Element]] = []

    def regen_brackets(self, key_prefix: str):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for _, _ in enumerate(old_row):
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def regen_brackets_without_row(self, key_prefix: str, delete_y):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            if y == delete_y:
                continue
            row = []
            for _, _ in enumerate(old_row):
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def regen_brackets_without_column(self, key_prefix: str, delete_x):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for x in range(len(old_row)):
                if x == delete_x:
                    continue
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def regen_brackets_without_entry(self, key_prefix: str, delete_x, delete_y):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for x in range(len(old_row)):
                if x == delete_x and y == delete_y:
                    continue
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def regen_brackets_and_add_column(self, key_prefix: str, after_x):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for x in range(len(old_row)):
                if x == after_x:
                    row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                    count += 1
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def regen_brackets_and_add_row(self, key_prefix: str, after_row):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for x in range(len(old_row)):
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1

            new_brackets.append(row)

            if y == after_row:
                print("here")
                row = []
                for x in range(5):
                    row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                    count += 1
                new_brackets.append(row)

        self.brackets = new_brackets

    def regen_brackets_and_add_entry(self, key_prefix: str, after_x, after_y):
        new_brackets = []
        count: int = 0

        for y, old_row in enumerate(self.brackets):
            row = []
            for x in range(len(old_row)):
                if x == after_x and y == after_y:
                    row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                    count += 1
                row.append(B(f"{key_prefix}{count}", key=f"{key_prefix}{count}"))
                count += 1
            new_brackets.append(row)

        self.brackets = new_brackets

    def process_values_and_create_window(self, window, event, values):
        window.close()
        match event:
            case "cont_rm":
                self.regen_brackets_without_column("ec", int(values["cont_rm_column"]) - 1)

            case "eros_rm":
                self.regen_brackets_without_row("ec", int(values["eros_rm_row"]) - 1)

            case "ec_rm_indi":
                self.regen_brackets_without_entry("ec", int(values["ec_rm_indi_row"]) - 1,
                                                  int(values["ec_rm_indi_column"]) - 1)

            case "cont_add":
                self.regen_brackets_and_add_column("ec", int(values["cont_add_column"]) - 1)

            case "eros_add":
                self.regen_brackets_and_add_row("ec", int(values["eros_add_row"]) - 1)

            case "ec_add_indi":
                self.regen_brackets_and_add_entry("ec", int(values["ec_add_indi_row"]) - 1,
                                                  int(values["ec_add_indi_column"]) - 1)

            case _:
                print(event, values)
                self.regen_brackets("ec")

        layout = [
            [nav_bar()],
            [Label("Terrain Parameters", font="times 18")],
            [*ec_modification_frames()],
            [Label("increasing continentalness left-right, increasing erosion top to bottom",
                   font="arial 16")],
            *self.brackets
        ]

        return sg.Window("Everest", layout, resizable=True, auto_size_text=True, auto_size_buttons=True)

    def run(self):
        self.brackets = [[B(f"Button{y * 5 + x}", key=f"EC${y * 5 + x}", pad=(20, 5)) for x in range(5)] for y in
                         range(5)]

        layout = [
            [nav_bar()],
            [Label("Terrain Parameters", font="times 18")],
            [*ec_modification_frames()],
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
