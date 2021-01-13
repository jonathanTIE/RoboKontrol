"""Module externals.py - gestion de lecture et écriture dans les fichiers
    + création de sous-process"""

import os
import subprocess
import shutil
import random
import lxml.etree as ET

MODULE_PATH = os.path.dirname(__file__)

DEFAULT_FILE_PATH = "{}/default_settings.xml".format(MODULE_PATH)
PERSONAL_FILE_PATH = "{}/data/settings.xml".format(MODULE_PATH)

def generate_personal_settings():
    """Génère un fichier de paramètres personnel, si il n'existe pas,
    ou si des paramètres manquent"""
    deflt_st = settings_from_file(DEFAULT_FILE_PATH)
    if not os.path.exists(PERSONAL_FILE_PATH):
        settings_to_file(PERSONAL_FILE_PATH, deflt_st)
    else:
        per_st = settings_from_file(PERSONAL_FILE_PATH)
        new_setts = [key for key in deflt_st if key not in per_st.keys()]
        for sett in new_setts:
            per_st[sett] = deflt_st[sett]
        settings_to_file(PERSONAL_FILE_PATH, per_st)

def get_settings():
    """Récupère les paramètres depuis le fichier de paramètres"""
    generate_personal_settings()
    return settings_from_file(PERSONAL_FILE_PATH)

def set_settings(settings_dict):
    """Enregistre les paramètres dans le fichier de paramètres"""
    settings_to_file(PERSONAL_FILE_PATH, settings_dict)

def settings_from_file(file_path):
    """Récupérer les paramètres à partir d'un fichier"""
    settings = {}
    try:
        root = ET.parse(file_path).getroot()
        for setting in root.findall('setting'):
            nom = setting.attrib.get('nom')
            field = setting.find("field").text
            settings[nom] = field
    except Exception as exc:
        print(exc)
    return settings

def settings_to_file(path, settings):
    """Sauvegarde des évènements Evt dans un fichier (*.xml)
    (génération par xml ElementTree)"""
    root = ET.Element("settings")
    for obj in settings:
        obj_xml = ET.Element("setting")
        obj_xml.set('nom', obj)
        field = ET.SubElement(obj_xml, "field")
        field.text = settings[obj]
        root.append(obj_xml)
    tree = ET.ElementTree(root)
    with open(path, "wb") as save:
        tree.write(save, pretty_print=True)

def exec_simu(st_dict):
    """Exécute un simulateur en parallèle"""
    char_seq = [ chr(random.randint(65, 90)) for _ in range(0, 7)]
    rbt_name = "".join(char_seq)
    try:
        if os.path.exists(st_dict["Chemin Simulateur"]):
            if shutil.which("python3"):
                subprocess.Popen(["python3", st_dict["Chemin Simulateur"], rbt_name])
            else:
                subprocess.Popen(["python", st_dict["Chemin Simulateur"], rbt_name])
    except Exception as exc:
        print(exc)