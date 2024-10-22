from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import sqlite3

background = "#06283D"
framebg = "#EDEDED"
framefg = "#06283D"


def connect_db():
    conn = sqlite3.connect('student_registration.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       registration_no TEXT,
                       name TEXT,
                       birthdate TEXT,
                       cpf TEXT,
                       class TEXT,
                       father_name TEXT,
                       mother_name TEXT)''')
    conn.commit()
    conn.close()


def save_to_db():
    conn = sqlite3.connect('student_registration.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO students 
                      (registration_no, name, birthdate, cpf, class, father_name, mother_name) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (Registration.get(), Name.get(), Nasc.get(), Cpf.get(), Turma.get(), F_Name.get(), M_Name.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Salvo", "Dados salvos com sucesso!")


def search_student():
    search_term = Search.get()
    conn = sqlite3.connect('student_registration.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE registration_no = ? OR name = ?", (search_term, search_term))
    results = cursor.fetchall()
    conn.close()

    results_window = Toplevel(root)
    results_window.title("Resultados da Pesquisa")
    results_window.geometry("600x400")
    results_window.config(bg=background)

    if results:
        for student in results:
            student_frame = Frame(results_window, bg=framebg)
            student_frame.pack(pady=5, fill=X)

            Label(student_frame, text=f"Registro Nº: {student[1]}, Nome: {student[2]}", bg=framebg, fg=framefg).pack(
                side=LEFT)

            # Botão de excluir
            delete_button = Button(student_frame, text="Excluir", bg="red",
                                   command=lambda reg_no=student[1]: delete_student(reg_no))
            delete_button.pack(side=RIGHT)
    else:
        Label(results_window, text="Nenhum aluno encontrado", bg=framebg, fg=framefg).pack(pady=2)


def delete_student(reg_no):
    conn = sqlite3.connect('student_registration.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE registration_no = ?", (reg_no,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")


def Exit():
    root.destroy()


def showimage():
    global filename
    global img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file", filetypes=(
    ("JPG File", ".jpg"), ("PNG File", ".png"), ("All Files", "*.txt")))
    img = Image.open(filename)
    resized_image = img.resize((256, 256))
    photo2 = ImageTk.PhotoImage(resized_image)
    lbl.config(image=photo2)
    lbl.image = photo2


def Clear():
    Name.set('')
    Nasc.set('')
    Cpf.set('')
    F_Name.set('')
    M_Name.set('')
    Turma.set("Selecione a turma")
    saveButton.config(state='normal')
    img1 = PhotoImage(file="./assets/user.png")
    lbl.config(image=img1)
    lbl.image = img1
    img = ""


def Save():
    if Name.get() == "" or Cpf.get() == "" or Turma.get() == "Selecione a turma" or Nasc.get() == "" or M_Name.get() == "":
        messagebox.showerror("Tente novamente", "Algum campo está em branco!")
    else:
        save_to_db()
        Clear()


root = Tk()
root.title("Cadastro de Alunos")
root.geometry("1250x700+210+100")
root.config(bg=background)

Label(root, text="CADASTRO DE ALUNO", width=10, height=2, bg="#FAF9F6", fg="black", font="arial 20").pack(side=TOP,
                                                                                                          fill=X)

Search = StringVar()
Entry(root, textvariable=Search, width=15, bd=2, font="arial 20").place(x=820, y=15)
imageicon3 = PhotoImage(file="./assets/search.png")
Srch = Button(root, text="Pesquisar", compound=LEFT, image=imageicon3, width=123, bg="#68ddfa", font="arial 13 bold",
              command=search_student)
Srch.place(x=1060, y=15)

imageicon4 = PhotoImage(file="./assets/refresh-arrow.png")
Update_button = Button(root, image=imageicon4, bg="#c36464")
Update_button.place(x=110, y=15)

Label(root, text="Registro Nº:", font="arial 13", fg=framebg, bg=background).place(x=30, y=150)
Label(root, text="Data:", font="arial 13", fg=framebg, bg=background).place(x=500, y=150)

Registration = StringVar()
Date = StringVar()

reg_entry = Entry(root, textvariable=Registration, width=15, font="arial 10")
reg_entry.place(x=160, y=152)

today = date.today()
d1 = today.strftime("%d/%m/%Y")
date_entry = Entry(root, textvariable=Date, width=15, font="arial 10")
date_entry.place(x=550, y=152)
Date.set(d1)

obj = LabelFrame(root, text="Detalhes do Aluno", font=20, bd=2, width=900, bg=framebg, fg=framefg, height=250,
                 relief=GROOVE)
obj.place(x=30, y=200)

Label(obj, text="Nome:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj, text="Data de Nascimento:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=100)
Label(obj, text="CPF:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=150)
Label(obj, text="Turma:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=50)

Name = StringVar()
name_entry = Entry(obj, textvariable=Name, width=20, font="arial 10")
name_entry.place(x=160, y=50)

Nasc = StringVar()
nasc_entry = Entry(obj, textvariable=Nasc, width=20, font="arial 10")
nasc_entry.place(x=160, y=100)

Cpf = StringVar()
cpf_entry = Entry(obj, textvariable=Cpf, width=20, font="arial 10")
cpf_entry.place(x=160, y=150)

Turma = Combobox(obj, values=["1", "2", "3", "4", "5", "6", "7", "8", "9"], font="Roboto 10", width=17, state="r")
Turma.place(x=600, y=50)
Turma.set("Selecione a turma")


obj2 = LabelFrame(root, text="Detalhes do Responsável", font=20, bd=2, width=900, bg=framebg, fg=framefg, height=220,
                  relief=GROOVE)
obj2.place(x=30, y=470)

Label(obj2, text="Nome do pai:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=50)
F_Name = StringVar()
f_entry = Entry(obj2, textvariable=F_Name, width=20, font="arial 10")
f_entry.place(x=160, y=50)

Label(obj2, text="Nome da mãe:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=50)
M_Name = StringVar()
M_entry = Entry(obj2, textvariable=M_Name, width=20, font="arial 10")
M_entry.place(x=630, y=50)


f = Frame(root, bd=3, bg="black", width=256, height=256, relief=GROOVE)
f.place(x=1000, y=150)

img = PhotoImage(file="./assets/user.png")
lbl = Label(f, bg="white", image=img)
lbl.place(x=0, y=0)


Button(root, text="Upload", width=19, height=2, font="arial 12 bold", bg="lightblue", command=showimage).place(x=1000,
                                                                                                               y=415)
saveButton = Button(root, text="Salvar", width=19, height=2, font="arial 12 bold", bg="lightgreen", command=Save)
saveButton.place(x=1000, y=495)
Button(root, text="Reset", width=19, height=2, font="arial 12 bold", bg="lightpink", command=Clear).place(x=1000, y=575)
Button(root, text="Sair", width=19, height=2, font="arial 12 bold", bg="grey", command=Exit).place(x=1000, y=655)

connect_db()

root.mainloop()
