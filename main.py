#-------------------------------- IMPORT --------------------------------#
from tkinter import *
from tkinter import ttk
from commands import ButtonFunc

#-------------------------------- ROOT --------------------------------#
FONT = ("Arial", 21, "normal")

#-------------------------------- NOTES COUNT --------------------------------#
class Notes:
    def __init__(self):
        self.color_dic = {
            "Red": 0,
            "Green": 0,
            "Blue": 0,
            "Gold": 0,
            "Black": 0,
            "White": 0,
        }

    def increase_color(self, name):
        self.color_dic[name] += 1
        self.update_labels()

    def decrease_color(self, name):
        if self.color_dic[name] > 0:
            self.color_dic[name] -= 1
        self.update_labels()

    def update_labels(self):
        for name, widgets in note_widgets.items():
            widgets["count"].config(text=str(self.color_dic[name]))
notes = Notes()
#-------------------------------- ROOT --------------------------------#
root = Tk()
root.title("Pen and Paper Tracker")
root.maxsize()
root.state("zoomed")
root.rowconfigure(99,weight=1)
root.columnconfigure(index= [0,1,6,7,9,10,12,13,15,16], minsize="100", weight=0)
root.columnconfigure(index= [3,4], minsize=300, weight=0)

#-------------------------------- HEAD --------------------------------#
head_label_1 = Label(root, text="Kampf", font=FONT)
head_label_1.grid(row= 0, column=0, columnspan=2)

head_label_2 = Label(root, text="Übersicht", font=FONT)
head_label_2.grid(row= 0, column=3, columnspan=2)

head_label_3 = Label(root, text="NPC's", font=FONT)
head_label_3.grid(row= 0, column=6, columnspan=2)

head_label_4 = Label(root, text="Tiere", font=FONT)
head_label_4.grid(row= 0, column=9, columnspan=2)

head_label_5 = Label(root, text="Items", font=FONT)
head_label_5.grid(row= 0, column=12, columnspan=2)

head_label_6 = Label(root, text="Mitspieler", font=FONT)
head_label_6.grid(row= 0, column=15, columnspan=2)
#-------------------------------- ÜBERSICHT --------------------------------#

log_frame = ttk.Frame(root)
log_frame.grid(row=3, column=3, columnspan=2, rowspan=10, padx=10, pady=10, sticky="nsew")
log_scroll = ttk.Scrollbar(master=log_frame)
log_scroll.pack(side="right", fill="y")
log_canvas = Canvas(
    master= log_frame,
    bg= "white",
    yscrollcommand= log_scroll.set,
    highlightthickness=1)
log_canvas.pack(fill="both", expand=True)

note_log_frame = ttk.Frame(root)
note_log_frame.grid(row=14, column=3, columnspan=2, rowspan=2, padx=10, pady=10, sticky="nsew")

note_log_canvas = Canvas(note_log_frame, height=30)
note_log_canvas.pack(fill="both", expand=True)
note_widgets = {}

box_width = 93
box_height = 30
padding = 0

for i, (color, count) in enumerate(notes.color_dic.items()):
    x0 = padding + i * (box_width + padding)
    y0 = padding
    x1 = x0 + box_width
    y1 = y0 + box_height
    note_log_canvas.create_rectangle(x0,y0,x1,y1, fill=color.lower(), outline="black")
    note_count_label = Label(master=note_log_canvas,fg="grey", text=str(count), font=("Arial", 12, "bold"), bg=color.lower())
    note_count_label.place(x=(x0+x1)//2, y=y0 +17, anchor="center")
    button_minus = Button(note_log_canvas, text="-", command= lambda n = color: notes.decrease_color(n), width=2, font=("Arial", 12, "bold"))
    button_minus.place(x=x0, y=y1 - 30)
    button_plus = Button(note_log_canvas, text="+", command= lambda n = color: notes.increase_color(n), width=2, font=("Arial", 12, "bold"))
    button_plus.place(x=x0+63, y=y1 - 30)
    note_widgets[color] = {"count": note_count_label, "minus": button_minus, "plus": button_plus}


overview_frame = ttk.Frame(root)
overview_frame.grid(row=16, column=3, columnspan=2, rowspan=10, padx=10, pady=10, sticky="nsew")
overview_scroll = ttk.Scrollbar(overview_frame)
overview_scroll.pack(side="right", fill="y")

overview_canvas = Canvas(
    master= overview_frame,
    bg= "white",
    yscrollcommand= overview_scroll.set,
    highlightthickness=1
)

overview_canvas.pack(fill="both", expand=True)
overview_scroll.config(command=overview_canvas.yview)

header_frame = Frame(overview_canvas)
overview_canvas.create_window((0,0),window=header_frame, anchor="nw")
header_frame.columnconfigure(0, weight=1, minsize=280)
header_frame.columnconfigure(1, weight=1, minsize=283)
header_frame.rowconfigure(1,weight=1, minsize=248)
header_1 = Label(master=header_frame, background="antique white", text="Name", bd=1, relief="solid")
header_1.grid(row=0, column=0, sticky="nsew")

header_2 = Label(master=header_frame, background="antique white", text="Auswirkung", bd=1, relief="solid")
header_2.grid(row=0, column=1, sticky="nsew")

column_1 = Label(master=header_frame, background="lavender", text="", bd=1, relief="solid")
column_1.grid(row=1, column=0, sticky="nsew")

column_2 = Label(master=header_frame, background="lavender", text="", bd=1, relief="solid")
column_2.grid(row=1, column=1, sticky="nsew")

#-------------------------------- ÜBERSICHT_BUTTON --------------------------------#
use_button = Button(master=root, text="Anwenden", width=25, state="disabled")
use_button.grid(row=26, column=3)
edit_button = Button(master=root, text="Bearbeiten", width=25, state="disabled")
edit_button.grid(row=26, column=4)


#-------------------------------- BOTTOM BUTTON CLASS --------------------------------#
button_actions = ButtonFunc(root=root, overview_canvas=overview_canvas,log_canvas=log_canvas, button_use=use_button, button_edit=edit_button, header_1=header_1, column_1=column_1, column_2=column_2)
#-------------------------------- BOTTOM BUTTONS --------------------------------#
new_action_button = Button(text="Neue Aktion", command= button_actions.new_action)
new_action_button.grid(row=99, column=0, columnspan=2, sticky="s")

new_npc_button = Button(text="Neuer NPC", command= button_actions.new_npc)
new_npc_button.grid(row=99, column=6, columnspan=2, sticky="s")

new_animal_button = Button(text="Neues Tier", command= button_actions.new_animal)
new_animal_button.grid(row=99, column=9, columnspan=2, sticky="s")

new_item_button = Button(text="Neues Item", command= button_actions.new_item)
new_item_button.grid(row=99, column=12, columnspan=2, sticky="s")

new_player_button = Button(text="Neuer Mitspieler", command= button_actions.new_player)
new_player_button.grid(row=99, column=15, columnspan=2, sticky="s")
#-------------------------------- SAVE AND LOAD BUTTON --------------------------------#
save_button = Button(master=root, text="Speichern", width=25, command=button_actions.save)
save_button.grid(row=99, column=3, sticky="s")
load_button = Button(master=root, text="Laden", width=25, command=button_actions.load)
load_button.grid(row=99, column=4, sticky="s")
#-------------------------------- LINE --------------------------------#

horizontal_header_line = Frame(root, height=1, bg="grey")
horizontal_header_line.grid(row=1, column=0, columnspan=17, sticky="ew", pady=(5, 10))

vertical_line_1 = Frame(root, height=1, bg="grey")
vertical_line_1.grid(row=0, column=2, rowspan=100, sticky="ns", padx=5)

vertical_line_2 = Frame(root, height=1, bg="grey")
vertical_line_2.grid(row=0, column=5, rowspan=100, sticky="ns", padx=5)

vertical_line_3 = Frame(root, height=1, bg="grey")
vertical_line_3.grid(row=0, column=8, rowspan=100, sticky="ns", padx=5)

vertical_line_4 = Frame(root, height=1, bg="grey")
vertical_line_4.grid(row=0, column=11, rowspan=100, sticky="ns", padx=5)

vertical_line_5 = Frame(root, height=1, bg="grey")
vertical_line_5.grid(row=0, column=14, rowspan=100, sticky="ns", padx=5)




root.mainloop()