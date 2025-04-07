import os
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt

# Configuration Tcl/Tk
os.environ["TCL_LIBRARY"] = r"C:\Users\HP-PC\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Users\HP-PC\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

def Signin():
    user = username_entry.get()
    pwd = password_entry.get()

    if not user or not pwd:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        return

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password='',
            port=3300,
            database="parapharmacie"
        )
        mycursor = mydb.cursor()

        mycursor.execute("SELECT password FROM users WHERE username = %s", (user,))
        result = mycursor.fetchone()

        if result:
            stored_hash = result[0].encode('utf-8')
            if bcrypt.checkpw(pwd.encode('utf-8'), stored_hash):
                messagebox.showinfo("Succès", "Connexion réussie !")
            else:
                messagebox.showerror("Erreur", "Mot de passe ou Nom d'utilisateur incorrect")

        mydb.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Connexion BDD échouée : {err}")

def open_signup():
    root.destroy()
    os.system(f'python "{r"C:\Users\HP-PC\Desktop\GL\G1\S2\projet S2\Projet1\SignUp\SignUp.py"}"')

# Interface
root = tk.Tk()
root.title("Connexion")
root.geometry('1000x550+250+150')
root.config(bg="white")
root.resizable(False, False)

# Image avec fond
img = tk.PhotoImage(file="C:\\Users\\HP-PC\\Desktop\\GL\\G1\\S2\\projet S2\\Projet1\\images\\images1.png")
tk.Label(root, image=img, bg="white").place(x=80, y=120)

# Cadre du formulaire (agrandi)
frame = tk.Frame(root, width=420, height=400, bg='white', highlightbackground='gray')
frame.place(x=500, y=70)

# Titre
tk.Label(frame, text='Connexion', fg='#57a1f8', bg='white', font=('Arial', 24, 'bold')).place(x=130, y=20)

# Label + champ utilisateur
tk.Label(frame, text="Nom d'utilisateur", bg='white', fg='black', font=('Arial', 11)).place(x=40, y=90)
username_entry = tk.Entry(frame, width=35, border=1, relief='solid', font=('Arial', 11))
username_entry.place(x=40, y=115)

# Label + champ mot de passe
tk.Label(frame, text="Mot de passe", bg='white', fg='black', font=('Arial', 11)).place(x=40, y=170)
password_entry = tk.Entry(frame, width=35, border=1, relief='solid', font=('Arial', 11), show='*')
password_entry.place(x=40, y=195)

# Bouton de connexion
tk.Button(frame, width=35, pady=8, text="Se connecter", command=Signin, bg='#57a1f8', fg='white', font=('Arial', 10, 'bold')).place(x=40, y=255)

# Lien vers Sign Up
tk.Label(frame, text="Pas encore de compte ?", bg='white', font=('Arial', 9)).place(x=90, y=320)
tk.Button(frame, text='Inscription', bg='white', command=open_signup, fg='#57a1f8', borderwidth=0, cursor='hand2').place(x=230, y=318)

root.mainloop()
