import tkinter as tk
from tkinter import messagebox, PhotoImage, Label, Entry
import mysql.connector
import os
import bcrypt

# Configuration chemins Tcl/Tk
os.environ["TCL_LIBRARY"] = r"C:\Users\HP-PC\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Users\HP-PC\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

# Connexion MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
    port='3300',
    database="parapharmacie"
)
mycursor = mydb.cursor()

def signup():
    name = username.get()
    email_val = email.get()
    pswd = password.get()
    conf_pswd = conform_pass.get()
    role = role_var.get()

    if not name or not email_val or not pswd or not conf_pswd:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return

    if pswd != conf_pswd:
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
        return

    mycursor.execute("SELECT * FROM users WHERE email = %s", (email_val,))
    if mycursor.fetchone():
        messagebox.showerror("Erreur", "Cet email est déjà enregistré.")
        return

    hashed_pswd = bcrypt.hashpw(pswd.encode('utf-8'), bcrypt.gensalt())
    sql = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
    val = (name, email_val, hashed_pswd.decode('utf-8'), role)
    mycursor.execute(sql, val)
    mydb.commit()
    messagebox.showinfo("Succès", "Compte créé avec succès !")

def open_signin():
    root.destroy()
    os.system(f'python "{r"C:\Users\HP-PC\Desktop\GL\G1\S2\projet S2\Projet1\signIn\SignIn.py"}"')

def toggle_password_visibility(entry, eye_icon):
    if entry.cget('show') == '*':
        entry.config(show='')
        eye_icon.config(image=eye_open_icon)
    else:
        entry.config(show='*')
        eye_icon.config(image=eye_closed_icon)

# Fenêtre principale
root = tk.Tk()
root.title("SignUp")
root.geometry('1100x650')
root.config(bg="#fff")
root.resizable(False, False)

# Image gauche
img = PhotoImage(file="C:\\Users\\HP-PC\\Desktop\\GL\\G1\\S2\\projet S2\\Projet1\\images\\images.png")
Label(root, image=img, border=0, bg='white').place(x=80, y=150)

# Frame principal
frame = tk.Frame(root, width=430, height=580, bg='#fff')
frame.place(x=500, y=35)

# Titre
heading = Label(frame, text='Sign Up', fg='#57a1f8', bg='white', font=('Arial', 23, 'bold'))
heading.place(x=140, y=10)

# Style des champs
entry_style = {'width': 30, 'fg': 'black', 'border': 0, 'bg': 'white', 'font': ('Arial', 11)}
frame_style = {'width': 320, 'height': 2, 'bg': 'black'}

# === Username ===
Label(frame, text="Nom d'utilisateur", bg='white', fg='black', font=('Arial', 10)).place(x=35, y=70)
username = Entry(frame, **entry_style)
username.place(x=35, y=95)
tk.Frame(frame, **frame_style).place(x=35, y=120)

# === Email ===
Label(frame, text="Email", bg='white', fg='black', font=('Arial', 10)).place(x=35, y=135)
email = Entry(frame, **entry_style)
email.place(x=35, y=160)
tk.Frame(frame, **frame_style).place(x=35, y=185)


# Redimensionnement avec subsample (divise la taille) ou zoom (multiplie la taille)
# Chargement et réduction importante des icônes
eye_open_icon = PhotoImage(file="C:\\Users\\HP-PC\\Desktop\\GL\\G1\\S2\\projet S2\\Projet1\\images\\eye.png").subsample(17, 17)
eye_closed_icon = PhotoImage(file="C:\\Users\\HP-PC\\Desktop\\GL\\G1\\S2\\projet S2\\Projet1\\images\\hidden.png").subsample(17, 17)

# === Password ===
Label(frame, text="Mot de passe", bg='white', fg='black', font=('Arial', 10)).place(x=35, y=205)
password = Entry(frame, show='*', **entry_style)
password.place(x=35, y=230)
tk.Frame(frame, **frame_style).place(x=35, y=255)

eye_button = tk.Button(
    frame,
    image=eye_closed_icon,
    borderwidth=0,
    bg='white',
    command=lambda: toggle_password_visibility(password, eye_button)
)
eye_button.place(x=320, y=217)

# === Confirm Password ===
Label(frame, text="Confirmer mot de passe", bg='white', fg='black', font=('Arial', 10)).place(x=35, y=275)
conform_pass = Entry(frame, show='*', **entry_style)
conform_pass.place(x=35, y=300)
tk.Frame(frame, **frame_style).place(x=35, y=325)

eye_button_confirm = tk.Button(
    frame,
    image=eye_closed_icon,
    borderwidth=0,
    bg='white',
    command=lambda: toggle_password_visibility(conform_pass, eye_button_confirm)
)
eye_button_confirm.place(x=320, y=287)

# === Role ===
Label(frame, text="Rôle", bg='white', fg='black', font=('Arial', 10)).place(x=35, y=345)
role_var = tk.StringVar()
role_var.set("client")
roles_menu = tk.OptionMenu(frame, role_var, "client", "admin")
roles_menu.config(width=30, bg='white', fg='black', font=('Arial', 10))
roles_menu.place(x=35, y=370)

# === Bouton Sign up ===
tk.Button(frame, width=35, pady=7, text="Sign up", command=signup,
          border=0, bg='#57a1f8', fg='white').place(x=35, y=430)

# === Sign in ===
Label(frame, text="I have an account", fg='black', bg='white', font=('Arial', 9)).place(x=110, y=490)
tk.Button(frame, width=6, text='Sign in', border=0, bg='white',
          fg='#57a1f8', cursor="hand2", command=open_signin).place(x=230, y=490)

root.mainloop()
