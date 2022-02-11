from tkinter import *
import glob
import re
from tkinter.messagebox import showinfo

global root
root = Tk()
root.geometry("650x400")
root.title("Wpisywanie słówek")

def mode1():
    files_list = glob.glob("#slowka#*.txt")

    word_var = StringVar()
    translation_var = StringVar()

    def create_file():              #tworzy plik tekstowy
        INPUT = tex_file_name.get("1.0", "end-1c")
        if len(INPUT) > 0 and len(INPUT) < 26:
            f = open(f"#slowka#{INPUT}.txt", "a")
            f.close()
            files_list_refresh()
        else:
            showinfo("NAZWA", "Zmień nazwę")

    def files_list_refresh():       #odświerza listę plików
        lbx_files_list.delete(0, END)
        files_list = glob.glob("#slowka#*.txt")
        for count, file in enumerate(files_list, 1):
            f_file = file[8:-4]
            lbx_files_list.insert(count, f"{count} - {f_file}")

    def open_file():                #otwiera plik tekstowy
        lbx_file_title.delete(0, END)
        lbx_file_content.delete(0, END)

        files_list = glob.glob("#slowka#*.txt")
        lbx_files_list.curselection()
        INPUT = lbx_files_list.get(ACTIVE)
        INPUT = INPUT[0]
        INPUT = int(INPUT)
        file = files_list[INPUT-1]

        number = INPUT

        if number != INPUT:
            lbx_file_content.delete(0, END)

        i = 1

        with open(file) as lines:
            for line in lines:
                splitted_line = line.rstrip()
                splitted_line = splitted_line.split("%")

                word = splitted_line[0:1]
                word = str(word)
                word = word[2:-2]

                translation = splitted_line[1:2]
                translation = str(translation)
                translation = translation[2:-2]

                lbx_file_content.insert(i, f"{word} - {translation}")
                lbx_file_title.insert(1, file[8:-4])
                i += 1

        but_submit_word = Button(root, text="ᐅ", width=20,command=submit_word_translation)
        but_submit_word.place(x=280, y=86)
        but_edit_content = Button(root, width=20, text="Edytuj plik", command=edit_file)
        but_edit_content.place(x=280, y=116)

    def submit_word_translation():  #wprowadza słówka do pliku
        lbx_file_content.delete(0, END)

        files_list = glob.glob("#slowka#*.txt")
        lbx_files_list.curselection()
        INPUT = lbx_files_list.get(ACTIVE)
        INPUT = INPUT[0]
        INPUT = int(INPUT)
        file = files_list[INPUT-1]

        number = INPUT

        word = word_var.get()
        translation = translation_var.get()

        if len(word) > 0 and len(translation) > 0:
            f = open(file, "a")
            f.write(f"{word}%{translation}\n")
            f.close()
            word_var.set("")
            translation_var.set("")

            i = 0

            with open(file) as lines:
                for line in lines:
                    splitted_line = line.rstrip()
                    splitted_line = splitted_line.split("%")

                    word = splitted_line[0:1]
                    word = str(word)
                    word = word[2:-2]

                    translation = splitted_line[1:2]
                    translation = str(translation)
                    translation = translation[2:-2]

                    if len(word) > 0 and len(translation) > 0:
                        lbx_file_content.insert(i, f"{word} - {translation}")
                        i += 1

    def edit_file():                #edycja pliku
        tex_file_content = Text(root, width=22, height=20)
        tex_file_content.place(x=452, y=36)

        files_list = glob.glob("#slowka#*.txt")
        lbx_files_list.curselection()
        INPUT = lbx_files_list.get(ACTIVE)
        INPUT = INPUT[0]
        INPUT = int(INPUT)
        file = files_list[INPUT-1]

        number = INPUT

        with open(file, 'r') as f:
            tex_file_content.insert(INSERT, f.read())

        def save_changes():
            input = tex_file_content.get('1.0', 'end-1c')
            f = open(file, "w")
            f.write(input)
            f.close()
        
        def exit_editing():
            lbx_file_content.delete(0, END)
            but_save_changes.destroy()
            but_exit_editing.destroy()
            tex_file_content.destroy()

            i = 1
            with open(file) as lines:
                for line in lines:
                    splitted_line = line.rstrip()
                    splitted_line = splitted_line.split("%")

                    word = splitted_line[0:1]
                    word = str(word)
                    word = word[2:-2]

                    translation = splitted_line[1:2]
                    translation = str(translation)
                    translation = translation[2:-2]

                    lbx_file_content.insert(i, f"{word} - {translation}")
                    lbx_file_title.insert(1, file[8:-4])
                    i += 1

        but_save_changes = Button(root, width=9, text="Zapisz", command=save_changes)
        but_save_changes.place(x=280, y=146)
        but_exit_editing = Button(root, width=9, text="Wyjdź", command=exit_editing)
        but_exit_editing.place(x=357, y=146)

    lab_create_file = Label(root, text="Wprowadź nazwę tworzonego pliku:")
    tex_file_name = Text(root, width=20, height=1)
    but_submit = Button(root, text="ᐅ", command=create_file, width=10)
    lab_files = Label(root, text="Lista dostępnych plików: ", height=1)
    but_open_file = Button(root, text="ᐅ", command=open_file, width=10)
    lbx_files_list = Listbox(root, width=40, height=15)
    lab_type_word = Label(root, text=f"Wpisz słówko/tłumaczenie:")
    tex_type_word = Entry(root, width=24, textvariable=word_var)
    tex_type_translation = Entry(root, width=24, textvariable=translation_var)
    lab_file_content = Label(root, text="Plik:")
    lbx_file_title = Listbox(root, width=20, height=1)
    lbx_file_content = Listbox(root, width=30, height=20)

    lab_create_file.place(x=10, y=10)
    tex_file_name.place(x=10, y=40)
    but_submit.place(x=175, y=36)
    lab_files.place(x=10, y=90)
    but_open_file.place(x=175, y=86)
    lbx_files_list.place(x=10, y=115)
    lab_type_word.place(x=280, y=10)
    tex_type_word.place(x=280, y=40)
    tex_type_translation.place(x=280, y=60)
    lab_file_content.place(x=450, y=10)
    lbx_file_title.place(x=510, y=10)
    lbx_file_content.place(x=450, y=35)

    files_list_refresh()

def mode2():
    translation_mode = 1

    files_list = glob.glob("#slowka#*.txt")

    translation_var = StringVar()

    def files_list_refresh():       #odświerza listę plików
        lbx_files_list.delete(0, END)
        files_list = glob.glob("#slowka#*.txt")
        for count, file in enumerate(files_list, 1):
            f_file = file[8:-4]
            lbx_files_list.insert(count, f"{count} - {f_file}")

    lab_files = Label(root, text="Lista dostępnych plików: ", height=1)
    lab_files.place(x=10, y=10)

    lbx_files_list = Listbox(root, width=40, height=20)
    lbx_files_list.place(x=10, y=36)

    files_list_refresh()

but_config_mode = Button(root, width=10, text="Konfiguracja", command=mode1)
but_config_mode.place(x=10, y=365)

but_learning_mode = Button(root, width=10, text="Nauka", command=mode2)
but_learning_mode.place(x=100, y=365)

root.mainloop()
