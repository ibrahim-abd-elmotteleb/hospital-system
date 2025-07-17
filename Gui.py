import Project3 as main
import DataBase as DataBase
from tkinter import *
from tkinter import ttk
# pip install ttkthemes
from ttkthemes import themed_tk


def root_GUI():
    global root
    root = themed_tk.ThemedTk()
    root.title("Hospital System")
    root.resizable(False, False)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 840
    window_height = 500

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    global pass_word_frame
    pass_word_frame = ttk.Frame(root)
    global GUI_frame
    GUI_frame = ttk.Frame(root)
    global add_frame
    add_frame = ttk.Frame(root)
    global print_frame
    print_frame = ttk.Frame(root)
    global get_next_frame
    get_next_frame = ttk.Frame(root)
    global change_pass_frame
    change_pass_frame = ttk.Frame(root)
    global delete_frame
    delete_frame = ttk.Frame(root)

    for frame in (pass_word_frame, GUI_frame, add_frame, print_frame, get_next_frame, change_pass_frame, delete_frame):
        frame.grid(row=0, column=0, sticky='nsew')
    pass_word_GUI(pass_word_frame)
    root.mainloop()


def pass_word_GUI(pass_word_frame):
    pass_word_frame.tkraise()
    style = ttk.Style(GUI_frame)
    style.theme_use("clam")
    pass_word_text = ttk.Label(pass_word_frame, text='Enter Pass Word')
    pass_word_text.place(x=270, y=200)
    pass_word_entery = ttk.Entry(pass_word_frame)
    pass_word_entery.place(x=370, y=200)
    pass_word_button = ttk.Button(pass_word_frame, text='Enter', width=25,
                                  command=lambda: check_pass_word(pass_word_entery.get()))
    pass_word_button.place(x=230, y=350)
    back_button = ttk.Button(pass_word_frame, text='Exit',
                             width=25, command=lambda: exit(root))
    back_button.place(x=430, y=350)


def check_pass_word(pass_word):
    result = DataBase.execute_query(
        main.connection, "SELECT * FROM pasword_table;").fetchone()
    if pass_word == result[0]:
        GUI(GUI_frame)
        main.server_connection.close()
        main.connection.close()
        DataBase.create_server_connection(
            '127.0.0.1', '3306', 'root', DataBase.db_pw)
        DataBase.create_db_connection(
            '127.0.0.1', 'root', DataBase.db_pw, 'HospitalSystem')
    else:
        text = ttk.Label(pass_word_frame, text="Wrong Pass Word")
        text.place(x=250, y=400)


def GUI(GUI_frame):

    GUI_frame.tkraise()

    style = ttk.Style(GUI_frame)
    style.theme_use("clam")

    style_menu = Menu(GUI_frame)
    root.config(menu=style_menu)

    our_themes = ttk.Style().theme_names()

    theme_menu = Menu(style_menu, tearoff=0)
    style_menu.add_cascade(label="Themes", menu=theme_menu)

    for theme in our_themes:
        theme_menu.add_command(
            label=theme, command=lambda theme=theme: change_theme(theme, style))

    add_button = ttk.Button(GUI_frame, text='Add Patient',
                            width=25, command=lambda: add_form(add_frame))
    add_button.place(x=330, y=140)

    print_button = ttk.Button(GUI_frame, text='Print Patients',
                              width=25, command=lambda: print_form(print_frame))
    print_button.place(x=330, y=170)

    get_next_button = ttk.Button(GUI_frame, text='Get Next Patient',
                                 width=25, command=lambda: get_next_form(get_next_frame))
    get_next_button.place(x=330, y=200)

    delete_button = ttk.Button(GUI_frame, text='Delete Patient',
                               width=25, command=lambda: delete_form(delete_frame))
    delete_button.place(x=330, y=230)

    change_pass_word_button = ttk.Button(
        GUI_frame, text='Change Pass Word', width=25, command=lambda: change_pass_form(change_pass_frame))
    change_pass_word_button.place(x=330, y=260)

    exit_button = ttk.Button(GUI_frame, text='Exit',
                             width=25, command=lambda: exit(root))
    exit_button.place(x=330, y=290)


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


def change_theme(theme, style):
    style.theme_use(theme)


def add_form(add_frame):

    add_frame.tkraise()
    func_manager = main.manager()

    global text
    text = ttk.Label(add_frame)
    text.place(x=400, y=250)

    text.config(text="")

    clicked = StringVar()
    clicked2 = StringVar()
    ttk.Label(add_frame, text='Add Patient').pack()

    spec_text = ttk.Label(add_frame, text='Specialization')
    name_text = ttk.Label(add_frame, text='Name')
    stat_text = ttk.Label(add_frame, text='Status')

    spec_text.place(x=40, y=40)
    name_text.place(x=40, y=80)
    stat_text.place(x=40, y=120)

    spec_menu = ttk.Combobox(add_frame, width=27, textvariable=clicked)
    spec_menu['values'] = (main.spec_menu_values)
    name_entry = ttk.Entry(add_frame)
    stat_entry = ttk.Combobox(add_frame, width=27, textvariable=clicked2)
    stat_entry['values'] = ('Normal', 'Urgent', 'Super Urgent')

    spec_menu.place(x=130, y=40)
    name_entry.place(x=130, y=80)
    stat_entry.place(x=130, y=120)

    sub_button = ttk.Button(add_frame, text='Submit', width=20, command=lambda: func_manager.add(
        spec_menu.get(), name_entry.get(), stat_entry.get(), add_frame))
    sub_button.place(x=250, y=330)

    back_button = ttk.Button(add_frame, text='Back to menu',
                             width=20, command=lambda: back(GUI_frame, add_frame))
    back_button.place(x=450, y=330)


def print_form(print_frame):
    print_frame.tkraise()
    func_manager = main.manager()

    clicked = StringVar()

    ttk.Label(print_frame, text='Print Patients').pack()

    spec_text = ttk.Label(print_frame, text='Choose Specialization')
    spec_text.place(x=40, y=40)

    spec_menu = ttk.Combobox(print_frame, width=27, textvariable=clicked)
    spec_menu['values'] = (main.spec_menu_values)
    spec_menu.place(x=170, y=40)

    print_button = ttk.Button(print_frame, text='Print', width=20,
                              command=lambda: func_manager.print(spec_menu.get(), print_frame))
    print_button.place(x=250, y=330)

    back_button = ttk.Button(print_frame, text='Back to menu',
                             width=20, command=lambda: back(GUI_frame, print_frame))
    back_button.place(x=450, y=330)


def get_next_form(get_next_frame):
    get_next_frame.tkraise()
    func_manager = main.manager()

    clicked = StringVar()

    ttk.Label(get_next_frame, text='Get next Patient').pack()

    spec_text = ttk.Label(get_next_frame, text='Choose Specialization')
    spec_text.place(x=40, y=40)

    spec_menu = ttk.Combobox(get_next_frame, width=27, textvariable=clicked)
    spec_menu['values'] = (main.spec_menu_values)
    spec_menu.place(x=170, y=40)

    print_button = ttk.Button(get_next_frame, text='Get next patient', width=20,
                              command=lambda: func_manager.get_next(spec_menu.get(), get_next_frame))
    print_button.place(x=250, y=330)

    back_button = ttk.Button(get_next_frame, text='Back to menu',
                             width=20, command=lambda: back(GUI_frame, get_next_frame))
    back_button.place(x=450, y=330)


def delete_form(delete_frame):
    delete_frame.tkraise()
    func_manager = main.manager()

    clicked = StringVar()

    ttk.Label(delete_frame, text='Delete Patient').pack()

    spec_text = ttk.Label(delete_frame, text='Choose Specialization')
    spec_text.place(x=40, y=40)

    name_text = ttk.Label(delete_frame, text='Name')
    name_text.place(x=40, y=80)
    name_entry = ttk.Entry(delete_frame)
    name_entry.place(x=170, y=80)

    spec_menu = ttk.Combobox(delete_frame, width=27, textvariable=clicked)
    spec_menu['values'] = (main.spec_menu_values)
    spec_menu.place(x=170, y=40)

    delete_button = ttk.Button(delete_frame, text='delete patient', width=20, command=lambda: func_manager.delete(
        spec_menu.get(), delete_frame, name_entry.get()))
    delete_button.place(x=250, y=330)

    back_button = ttk.Button(delete_frame, text='Back to menu',
                             width=20, command=lambda: back(GUI_frame, delete_frame))
    back_button.place(x=450, y=330)


def change_pass_form(change_pass_frame):
    change_pass_frame.tkraise()
    func_manager = main.manager()

    old_pass_text = ttk.Label(
        change_pass_frame, text='Enter Current Pass Word')
    old_pass_text.place(x=40, y=80)

    new_pass_text = ttk.Label(change_pass_frame, text='Enter New Pass Word')
    new_pass_text.place(x=40, y=120)

    old_pass_entry = ttk.Entry(change_pass_frame)
    old_pass_entry.place(x=190, y=80)

    new_pass_entry = ttk.Entry(change_pass_frame)
    new_pass_entry.place(x=190, y=120)

    enter_button = ttk.Button(change_pass_frame, text='Enter', width=20, command=lambda: func_manager.change_pass_word(
        old_pass_entry.get(), new_pass_entry.get(), change_pass_frame))
    enter_button.place(x=250, y=330)

    back_button = ttk.Button(change_pass_frame, text='Back to menu',
                             width=20, command=lambda: back(GUI_frame, change_pass_frame))
    back_button.place(x=450, y=330)


def back(root, current_root):
    root.tkraise()
    clear_frame(current_root)


def exit(root):
    root.destroy()


root_GUI()
