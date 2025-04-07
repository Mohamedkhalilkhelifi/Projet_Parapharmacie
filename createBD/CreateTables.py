import mysql.connector

# Connexion à MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='',
    port='3300'
)

mycursor = mydb.cursor()


mycursor.execute("USE parapharmacie")

# Table des utilisateurs
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        idUser INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")

# Table des produits
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS produit (
        idProd INT AUTO_INCREMENT PRIMARY KEY,
        nameProd VARCHAR(255) NOT NULL,
        prix FLOAT NOT NULL,
        qteStock INT NOT NULL,
        status VARCHAR(255) NOT NULL
    )
""")

# Table des commandes
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS commandeProd (
        idCmd INT AUTO_INCREMENT PRIMARY KEY,
        idUser INT NOT NULL,
        dateCmd DATETIME DEFAULT CURRENT_TIMESTAMP,
        statusCmd VARCHAR(50) NOT NULL,
        FOREIGN KEY (idUser) REFERENCES users(idUser) ON DELETE CASCADE
    )
""")

# Table des lignes de commande (association produits - commandes)
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS ligneCommande (
        idLigne INT AUTO_INCREMENT PRIMARY KEY,
        idCmd INT NOT NULL,
        idProd INT NOT NULL,
        quantite INT NOT NULL,
        prixUnitaire FLOAT NOT NULL,
        FOREIGN KEY (idCmd) REFERENCES commandeProd(idCmd) ON DELETE CASCADE,
        FOREIGN KEY (idProd) REFERENCES produit(idProd) ON DELETE CASCADE
    )
""")

# Table des livraisons
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS livraison (
        idLivraison INT AUTO_INCREMENT PRIMARY KEY,
        idCmd INT NOT NULL,
        adresse VARCHAR(255) NOT NULL,
        ville VARCHAR(100) NOT NULL,
        codePostal VARCHAR(10) NOT NULL,
        statusLivraison VARCHAR(50) NOT NULL,
        FOREIGN KEY (idCmd) REFERENCES commandeProd(idCmd) ON DELETE CASCADE
    )
""")

# Table des paiements
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS paiement (
        idPaiement INT AUTO_INCREMENT PRIMARY KEY,
        idCmd INT NOT NULL,
        montant FLOAT NOT NULL,
        moyenPaiement VARCHAR(50) NOT NULL,
        statusPaiement VARCHAR(50) NOT NULL,
        FOREIGN KEY (idCmd) REFERENCES commandeProd(idCmd) ON DELETE CASCADE
    )
""")

print("Base de données et tables créées avec succès !")

# Fermeture de la connexion
mydb.close()
