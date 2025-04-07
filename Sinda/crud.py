import os
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Connexion à MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
    port='3300',
    database="parapharmacie"
)
mycursor = mydb.cursor()

# Configuration Tcl/Tk
os.environ["TCL_LIBRARY"] = r"C:\Users\HP-PC\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Users\HP-PC\AppData\Local\Programs\Python\Python313\tcl\tk8.6"


# Interface Tkinter
root = tk.Tk()
root.title("Gestion Parapharmacie")
root.geometry("1000x1000")

# Fonction d'ajout de produit
def ajouter_produit():
    name = entry_nom.get()
    prix = entry_prix.get()
    qte = entry_qte.get()
    status = entry_status.get()
    mycursor.execute("INSERT INTO produit (nameProd, prix, qteStock, status) VALUES (%s, %s, %s, %s)", (name, prix, qte, status))
    mydb.commit()
    afficher_produits()

# Fonction de mise à jour d'un produit
def update_produit():
    selected_item = tree_produits.selection()
    if selected_item:
        item = tree_produits.item(selected_item)
        idProd = item['values'][0]
        name = entry_nom.get()
        prix = entry_prix.get()
        qte = entry_qte.get()
        status = entry_status.get()
        mycursor.execute("UPDATE produit SET nameProd = %s, prix = %s, qteStock = %s, status = %s WHERE idProd = %s", (name, prix, qte, status, idProd))
        mydb.commit()
        afficher_produits()

# Fonction d'affichage des produits
def afficher_produits():
    for row in tree_produits.get_children():
        tree_produits.delete(row)
    mycursor.execute("SELECT * FROM produit")
    for row in mycursor.fetchall():
        tree_produits.insert("", tk.END, values=row)

# Fonction de suppression d'un produit
def supprimer_produit():
    selected_item = tree_produits.selection()
    if selected_item:
        item = tree_produits.item(selected_item)
        idProd = item['values'][0]
        mycursor.execute("DELETE FROM produit WHERE idProd = %s", (idProd,))
        mydb.commit()
        afficher_produits()

# Fonction d'ajout de commande
def ajouter_commande():
    user_id = entry_user_id.get()
    status = entry_status_cmd.get()
    mycursor.execute("INSERT INTO commandeProd (idUser, statusCmd) VALUES (%s, %s)", (user_id, status))
    mydb.commit()
    afficher_commandes()

# Fonction de mise à jour d'une commande
def update_commande():
    selected_item = tree_commandes.selection()
    if selected_item:
        item = tree_commandes.item(selected_item)
        idCmd = item['values'][0]
        status = entry_status_cmd.get()
        mycursor.execute("UPDATE commandeProd SET statusCmd = %s WHERE idCmd = %s", (status, idCmd))
        mydb.commit()
        afficher_commandes()

# Fonction d'affichage des commandes
def afficher_commandes():
    for row in tree_commandes.get_children():
        tree_commandes.delete(row)
    mycursor.execute("SELECT * FROM commandeProd")
    for row in mycursor.fetchall():
        tree_commandes.insert("", tk.END, values=row)

# Fonction de suppression d'une commande
def supprimer_commande():
    selected_item = tree_commandes.selection()
    if selected_item:
        item = tree_commandes.item(selected_item)
        idCmd = item['values'][0]
        mycursor.execute("DELETE FROM commandeProd WHERE idCmd = %s", (idCmd,))
        mydb.commit()
        afficher_commandes()

# Interface graphique des produits
frame_produits = tk.LabelFrame(root, text="Gestion des Produits", padx=10, pady=10)
frame_produits.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(frame_produits, text="Nom:").grid(row=0, column=0)
entry_nom = tk.Entry(frame_produits)
entry_nom.grid(row=0, column=1)

tk.Label(frame_produits, text="Prix:").grid(row=1, column=0)
entry_prix = tk.Entry(frame_produits)
entry_prix.grid(row=1, column=1)

tk.Label(frame_produits, text="Quantité:").grid(row=2, column=0)
entry_qte = tk.Entry(frame_produits)
entry_qte.grid(row=2, column=1)

tk.Label(frame_produits, text="Status:").grid(row=3, column=0)
entry_status = tk.Entry(frame_produits)
entry_status.grid(row=3, column=1)

tk.Button(frame_produits, text="Ajouter", command=ajouter_produit).grid(row=4, column=0)
tk.Button(frame_produits, text="Supprimer", command=supprimer_produit).grid(row=4, column=1)
tk.Button(frame_produits, text="Mettre à jour", command=update_produit).grid(row=4, column=2)

columns_produits = ("ID", "Nom", "Prix", "Quantité", "Status")
tree_produits = ttk.Treeview(frame_produits, columns=columns_produits, show="headings")
for col in columns_produits:
    tree_produits.heading(col, text=col)
tree_produits.grid(row=5, column=0, columnspan=3)

afficher_produits()

# Interface graphique des commandes
frame_commandes = tk.LabelFrame(root, text="Gestion des Commandes", padx=10, pady=10)
frame_commandes.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(frame_commandes, text="ID Utilisateur:").grid(row=0, column=0)
entry_user_id = tk.Entry(frame_commandes)
entry_user_id.grid(row=0, column=1)

tk.Label(frame_commandes, text="Status Commande:").grid(row=1, column=0)
entry_status_cmd = tk.Entry(frame_commandes)
entry_status_cmd.grid(row=1, column=1)

tk.Button(frame_commandes, text="Ajouter", command=ajouter_commande).grid(row=2, column=0)
tk.Button(frame_commandes, text="Supprimer", command=supprimer_commande).grid(row=2, column=1)
tk.Button(frame_commandes, text="Mettre à jour", command=update_commande).grid(row=2, column=2)

columns_commandes = ("ID", "ID Utilisateur", "Date", "Status")
tree_commandes = ttk.Treeview(frame_commandes, columns=columns_commandes, show="headings")
for col in columns_commandes:
    tree_commandes.heading(col, text=col)
tree_commandes.grid(row=3, column=0, columnspan=3)

afficher_commandes()

root.mainloop()
