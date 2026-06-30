import customtkinter as ctk
import pywinstyles
from PIL import Image
import minecraft_launcher_lib
import os
import subprocess

# Variables globales
PSEUDO = "player"
VERSION = "alpha.1.0.0"

roaming_directory = os.getenv('APPDATA')
minecraft_directory = os.path.join(roaming_directory, ".CubexLauncher")

if not os.path.exists(minecraft_directory):
    os.makedirs(minecraft_directory)
    print(f"Dossier créé avec succès : {minecraft_directory}")
else:
    print(f"Le dossier existe déjà : {minecraft_directory}")

# Apparence
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Fenêtre principale
app = ctk.CTk()
app.title("Cubex Launcher")
app.geometry("1200x600")
app.iconbitmap("icons/box.ico")
app._fg_color = "#b8d8be"
app.configure(fg_color="#c8e1cc")

app.update()
pywinstyles.change_header_color(app, color="green")

# Récupération de la liste des versions de Minecraft
# On récupère toutes les versions et on filtre pour n'avoir que les "releases" (versions stables)
all_versions_raw = minecraft_launcher_lib.utils.get_version_list()
liste_versions = [v["id"] for v in all_versions_raw if v["type"] == "release"]


def play_button():
    # On récupère la version actuellement sélectionnée dans le menu déroulant
    version_choisie = option_version.get()
    print(f"Démarrage du jeu en version : {version_choisie}...")

    # On génère les options de test
    options = minecraft_launcher_lib.utils.generate_test_options()

    # On génère la commande avec la version choisie
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        version_choisie, minecraft_directory, options
    )

    # On exécute la commande pour lancer le jeu
    subprocess.run(minecraft_command)


def install_minecraft():
    # On récupère la version actuellement sélectionnée dans le menu déroulant
    version_choisie = option_version.get()
    print(f"Installation de la version {version_choisie} en cours...")

    minecraft_launcher_lib.install.install_minecraft_version(version_choisie, minecraft_directory)
    print("Installation faite avec succès !")


# Design de l'interface
frame_bg = ctk.CTkFrame(app, width=500, height=800, fg_color="#b8d8be")
frame_bg.place(relx=0.5, rely=0.50, anchor="center")

label_version = ctk.CTkLabel(app, text="Cubex Launcher  :  " + VERSION)
label_version.grid(row=0, column=0)

logocubex = ctk.CTkImage(
    light_image=Image.open("icons/box.ico"),
    dark_image=Image.open("icons/box.ico"),
    size=(200, 200)
)

label_image = ctk.CTkLabel(master=app, image=logocubex, text="", fg_color="#b8d8be")
label_image.place(relx=0.5, rely=0.20, anchor="center")

# Gestion du pseudo dynamique
pseudo_var = ctk.StringVar()


def mettre_a_jour_label(*args):
    label_pseudo.configure(text="     pseudo :  " + pseudo_var.get())


pseudo_var.trace_add("write", mettre_a_jour_label)

label_pseudo = ctk.CTkLabel(master=app, text="     pseudo :  ")
label_pseudo.grid(row=0, column=2)

pseudo = ctk.CTkEntry(
    app, placeholder_text="Pseudo", height=30, width=130, textvariable=pseudo_var, fg_color="#b8d8be",
    bg_color="#b8d8be"
)
pseudo.place(relx=0.5, rely=0.45, anchor="center")

# Boutons et Menus
button_start = ctk.CTkButton(app, text="Start", command=play_button, width=200, height=80)
button_start.place(relx=0.5, rely=0.65, anchor="center")

# Correction effectuée : suppression des parenthèses sur command=install_minecraft
button_ins = ctk.CTkButton(app, text="Install la version sélectionnée", command=install_minecraft, width=200, height=40)
button_ins.place(relx=0.5, rely=0.80, anchor="center")

# Menu déroulant contenant toutes les versions (Correction effectuée : values=liste_versions sans crochets supplémentaires)
option_version = ctk.CTkOptionMenu(app, values=liste_versions)
option_version.place(relx=0.5, rely=0.90, anchor="center")

app.mainloop()