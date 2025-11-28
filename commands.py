import tkinter
from tkinter import *
from tkinter import filedialog
import json

#-------------------------------- BUTTON FUNC --------------------------------#
class ButtonFunc:
    def __init__(self, root, overview_canvas, log_canvas, button_use, button_edit, header_1, column_1, column_2, note_dic, note_label):
        self.column_1 = column_1
        self.column_2 = column_2
        self.button_load = ""
        self.header = header_1
        self.note_dic = note_dic
        self.note_label = note_label
        self.overview_canvas = overview_canvas
        self.button_use = button_use
        self.button_edit = button_edit
        self.popup = None
        self.rainbow = StringVar(value="no")
        self.npc_category = ["npc", 6]
        self.action_category = ["actions", 0]
        self.animal_category = ["animals", 9]
        self.item_category = ["items", 12]
        self.player_category = ["player", 15]
        self.master = root
        self.loading_data = ""
        self.load_status = False
        self.button_config = {
            "actions": [],
            "npc": [],
            "animals": [],
            "items": [],
            "player": [],
        }

    # -------------------------------- NPC --------------------------------#
    def new_npc(self):
        self.popup = Toplevel(self.master)
        self.popup.geometry("200x100")
        npc_name_entry = Entry(master=self.popup, width=25)
        npc_name_entry.pack()
        create_npc_button = Button(master=self.popup,
                                   text="NPC erstellen",
                                   command= lambda: self.create_new_button(npc_name_entry.get(), category=self.npc_category))
        create_npc_button.pack()

    # -------------------------------- ACTION --------------------------------#
    def extract_cost_gain(self, spinboxes, ap_spinbox):
        data = {}

        for color, spin in spinboxes.items():
            value = int(spin.get())
            if value < 0:
                data[f"cost_{color}"] = abs(value)
            elif value > 0:
                data[f"gain_{color}"] = value

        ap = int(ap_spinbox.get())
        if ap < 0:
            data["cost_ap"] = abs(ap)
        elif ap > 0:
            data["gain_ap"] = ap
        if self.rainbow.get():
            data["flex"] = self.rainbow.get()
        return data
    def new_action(self):
        self.popup = Toplevel(self.master)
        self.popup.geometry("550x390")
        action_name_label = Label(master=self.popup, text="Name der Fähigkeit oder Aktion.")
        action_name_label.grid(row= 0, column=0 ,columnspan=3 ,sticky="w")
        action_name_entry = Entry(master=self.popup, width=30)
        action_name_entry.grid(row= 1, column=0 ,columnspan=3 ,sticky="w")

        action_description_label = Label(master=self.popup, text="Beschreibung der Fähigkeit oder Aktion.")
        action_description_label.grid(row=2, column=0, columnspan=3, sticky="w")
        action_description_entry = Entry(master=self.popup, width=30)
        action_description_entry.grid(row=3, column=0, columnspan=3, sticky="w")

        note_description_label = Label(master=self.popup, text="Definieren sie den festen Verbrauch oder Zuwachs an Noten beim ausführen der Aktion.")
        note_description_label.grid(row=4, column=0, columnspan=3, sticky="w")
        colors = ["red", "green", "blue", "gold", "black", "white", "rainbow"]
        spinboxes = {}
        for i, color in enumerate(colors):
            Label(master=self.popup, text=color.capitalize()).grid(row=5 + i, column=0, sticky="w")
            spinbox = Spinbox(master=self.popup, from_=-99, to=99, width=5)
            spinbox.delete(0, "end")
            spinbox.insert(0, 0)
            spinbox.grid(row=5 + i, column=1, sticky="w")
            spinboxes[color] = spinbox

        rainbow_label = Label(master=self.popup, text="Beim ausführen der Aktion, werden variable Kosten oder Gewinne erwartet?")
        rainbow_label.grid(row=12, column=0, columnspan=3, sticky="w")

        Radiobutton(master=self.popup, text="Yes", value="yes", variable=self.rainbow).grid(row=13, column=0, sticky="w")
        Radiobutton(master=self.popup, text="No", value="no", variable=self.rainbow).grid(row=13, column=1, sticky="w")

        ap_label = Label(master=self.popup, text="Definieren sie den festen Verbrauch oder zuwachs an Aktionspunkten beim ausführen der Aktion.")
        ap_label.grid(row=14, column=0, columnspan=3, sticky="w")
        ap_spinbox_label = Label(master=self.popup, text="Aktionspunkte")
        ap_spinbox_label.grid(row=15, column=0, sticky="w")
        ap_spinbox = Spinbox(master=self.popup, from_=-99, to=99, width=5)
        ap_spinbox.delete(0, "end")
        ap_spinbox.insert(0, 0)
        ap_spinbox.grid(row=15, column=1, sticky="w")

        create_action_button = Button(master=self.popup,
                                      text="Aktion erstellen",
                                      command=lambda: self.create_new_button(
                                          action_name_entry.get(),
                                          category=self.action_category,
                                          description=action_description_entry.get(),
                                          **self.extract_cost_gain(spinboxes, ap_spinbox)))

        create_action_button.grid(row=99, column=2)


    # -------------------------------- ANIMAL --------------------------------#
    def new_animal(self):
        self.popup = Toplevel(self.master)
        self.popup.geometry("200x100")
        animal_name_entry = Entry(master=self.popup, width=25)
        animal_name_entry.pack()
        create_animal_button = Button(master=self.popup,
                                      text="Tier erstellen",
                                      command=lambda: self.create_new_button(animal_name_entry.get(), category=self.animal_category))
        create_animal_button.pack()

    # -------------------------------- ITEM --------------------------------#
    def new_item(self):
        self.popup = Toplevel(self.master)
        self.popup.geometry("200x100")
        item_name_entry = Entry(master=self.popup, width=25)
        item_name_entry.pack()
        create_item_button = Button(master=self.popup,
                                      text="Item erstellen",
                                      command=lambda: self.create_new_button(item_name_entry.get(), category=self.item_category))
        create_item_button.pack()
    # -------------------------------- Player --------------------------------#
    def new_player(self):
        self.popup = Toplevel(self.master)
        self.popup.geometry("200x100")
        player_name_entry = Entry(master=self.popup, width=25)
        player_name_entry.pack()
        create_player_button = Button(master=self.popup,
                                      text="Mitspieler erstellen",
                                      command=lambda: self.create_new_button(player_name_entry.get(), category=self.player_category))
        create_player_button.pack()
    # -------------------------------- BUTTON CREATE --------------------------------#
    def create_new_button(self, button_name, category, **kwargs):
        if not self.load_status:
            if button_name == "":
                return
            if button_name in [btn["name"] for btn in self.button_config[category[0]]]:
                return
            self.popup.destroy()
        index = len(self.button_config[category[0]])
        if "row" in kwargs and "column" in kwargs:
            row = kwargs["row"]
            col = kwargs["column"]
        else:
            row = (index // 2) + 3
            col = (index % 2) + category[1]
        # -------------------------------- DYNAMIC BUTTON FUNC --------------------------------#
        def on_button_click(name=button_name):
            data = next((item for item in self.button_config[category[0]] if item["name"] == name))
            self.data = data
            def use_click():
                colors = ["red", "green", "blue", "gold", "black", "white"]
                for i in kwargs:
                    if i.split("_")[0] == "gain":
                        if i.split("_")[1] in colors:
                            self.note_dic[i.split("_")[1].capitalize()] += 1
                            self.note_label[i.split("_")[1].capitalize()]["count"].config(text=self.note_dic[i.split("_")[1].capitalize()])
                        elif i.split("_")[1] == "ap":
                            pass
                        else:
                            continue
                    elif i.split("_")[0] == "cost":
                        if i.split("_")[1] in colors:
                            self.note_dic[i.split("_")[1].capitalize()] -= 1
                            self.note_label[i.split("_")[1].capitalize()]["count"].config(text=self.note_dic[i.split("_")[1].capitalize()])
                        elif i.split("_")[1] == "ap":
                            pass
                        else:
                            continue
                    elif i.split("_")[0] == "flex":
                        if kwargs[i]:
                            self.popup = Toplevel(self.master)
                            self.popup.geometry("550x390")
                    else:
                        continue


            def edit_click():
                self.button_edit.config(state="disabled")
                self.popup = Toplevel(self.master)
                self.popup.geometry("550x390")
                name_label = Label(master=self.popup,text="Name")
                name_label.grid(row=0, column=0)
                name_entry = Entry(master=self.popup)
                name_entry.grid(row=0, column=1)
                name_entry.insert(END, name)
                row_i = 0
                entries = {}
                for i in kwargs:
                    column_i = 0
                    row_i += 1
                    if i == "row" or i == "column":
                        continue
                    else:
                        kwargs_label = Label(master=self.popup, text=i)
                        kwargs_label.grid(row=row_i,column=column_i)
                        column_i += 1
                        e = Entry(master=self.popup)
                        e.grid(row=row_i, column=column_i)
                        e.insert(END, kwargs[i])
                        entries[i] = e


                def edit_accept_button():
                    index_num = next(
                        (index for (index, d) in enumerate(self.button_config[category[0]]) if d["name"] == name), None)
                    self.button_config[category[0]][index_num]["name"] = name_entry.get()
                    entries_dic = {k: v.get() for (k, v) in entries.items()}
                    self.button_config[category[0]][index_num].update(entries_dic)
                    self.popup.destroy()
                def edit_cancel_button():
                    self.popup.destroy()
                accept_button = Button(master=self.popup ,text="Anwenden", command=edit_accept_button)
                accept_button.grid(row=row_i+1, column=0)
                cancel_button = Button(master=self.popup ,text="Abbrechen", command=edit_cancel_button)
                cancel_button.grid(row=row_i+1, column=1)

            self.header.config(
                text=data['name'],
                anchor="center"
            )
            self.column_1.config(
                text=data['description']
            )
            keys = list(self.data.keys())
            idx = keys.index("column")
            impact = ""
            for item in keys[idx+1:]:
                impact += f"{item}: {self.data[item]}\n"
            self.column_2.config(
                text= impact
            )

            self.button_use.config(state="normal", command=use_click)
            self.button_edit.config(state="normal", command=edit_click)


        new_button = Button(master=self.master, text=button_name, width=12, command=on_button_click)
        new_button.grid(row= row,column=col, sticky="nw")
        new_button.grid_propagate(False)
        # -------------------------------- BUTTON DATA --------------------------------#
        base_data = {
        "description": "",
        "row": row,
        "column": col
        }
        base_data.update(kwargs)

        self.button_config[category[0]].append({
            "name": button_name,
            **base_data
        })
        self.load_status = False

    # -------------------------------- SAVE --------------------------------#
    def save(self):
        with open("data.json", "w") as json_file:
            json.dump(self.button_config, json_file)
    # -------------------------------- LOAD --------------------------------#
    def load(self):
        self.loading_data = filedialog.askopenfilename()
        if not self.loading_data:
            return
        with open(self.loading_data, "r") as json_file:
            self.button_load = json.load(json_file)
        for key, items in self.button_load.items():
            if key == self.npc_category[0]:
                category_load = self.npc_category
            elif key == self.item_category[0]:
                category_load = self.item_category
            elif key == self.action_category[0]:
                category_load = self.action_category
            elif key == self.animal_category[0]:
                category_load = self.animal_category
            elif key == self.player_category[0]:
                category_load = self.player_category
            else:
                continue
            for item in items:
                name = item["name"]
                kwargs = {k: v for k, v in item.items() if k != "name"}
                self.load_status = True
                self.create_new_button(name, category_load, **kwargs)



