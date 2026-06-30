import customtkinter as ctk
import pywinstyles
from PIL import Image
import minecraft_launcher_lib
import os
import subprocess
import threading
import sys

# Variables globales
PSEUDO = "player"
VERSION = "alpha.1.0.1"



def resource_path(relative_path):
    """ Permet d'obtenir le chemin absolu vers les ressources, indispensable pour auto-py-to-exe """
    try:

        base_path = sys._MEIPASS
    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




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
app.iconbitmap(resource_path("icons/box.ico"))  # Modifié avec resource_path
app._fg_color = "#b8d8be"
app.configure(fg_color="#c8e1cc")

app.update()
pywinstyles.change_header_color(app, color="green")

# Récupération de la liste des versions de Minecraft
all_versions_raw = minecraft_launcher_lib.utils.get_version_list()
liste_versions = [v["id"] for v in all_versions_raw if v["type"] == "release"]


maximum_value = 0


def set_status(status: str):
    button_ins.configure(text=status)


def set_progress(progress: int):
    if maximum_value > 0:
        progress_bar.set(progress / maximum_value)


def set_max(new_max: int):
    global maximum_value
    maximum_value = new_max


callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}





def play_button():
    version_choisie = option_version.get()
    print(f"Démarrage du jeu en version : {version_choisie}...")

    options = minecraft_launcher_lib.utils.generate_test_options()

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(
        version_choisie, minecraft_directory, options
    )

    subprocess.run(minecraft_command)


def action_installation():
    """Cette fonction effectue l'installation en arrière-plan"""
    version_choisie = option_version.get()
    button_ins.configure(state="disabled")

    minecraft_launcher_lib.install.install_minecraft_version(
        version=version_choisie,
        minecraft_directory=minecraft_directory,
        callback=callback
    )

    button_ins.configure(text="Installation faite !", state="normal")
    progress_bar.set(0)


def install_minecraft():
    # On lance l'installation dans un Thread séparé pour ne pas freeze l'UI
    thread = threading.Thread(target=action_installation)
    thread.start()



frame_bg = ctk.CTkFrame(app, width=500, height=800, fg_color="#b8d8be")
frame_bg.place(relx=0.5, rely=0.50, anchor="center")

label_version = ctk.CTkLabel(app, text="Cubex Launcher  :  " + VERSION)
label_version.grid(row=0, column=0)


logocubex = ctk.CTkImage(
    light_image=Image.open(resource_path("icons/box.ico")),
    dark_image=Image.open(resource_path("icons/box.ico")),
    size=(200, 200)
)

label_image = ctk.CTkLabel(master=app, image=logocubex, text="", fg_color="#b8d8be")
label_image.place(relx=0.5, rely=0.20, anchor="center")


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
button_start.place(relx=0.5, rely=0.61, anchor="center")

button_ins = ctk.CTkButton(app, text="Installer la version sélectionnée", command=install_minecraft, width=250,
                           height=40)
button_ins.place(relx=0.5, rely=0.74, anchor="center")

# Barre de progression
progress_bar = ctk.CTkProgressBar(app, width=250)
progress_bar.set(0)
progress_bar.place(relx=0.5, rely=0.81, anchor="center")

# Menu déroulant contenant toutes les versions
option_version = ctk.CTkOptionMenu(app, values=liste_versions)
option_version.place(relx=0.5, rely=0.90, anchor="center")

app.mainloop()
