import json
from pathlib import Path

from imports import QIcon

config_file = Path("config.json")
init_solde_file = Path("initial_balance.json")

secret_questions = [
    ('Quel est le nom de votre premier animal de compagnie ?', 1),
    ('Quelle est le nom de jeune fille de votre mère ?', 2),
    ('Quel est le prénom de votre père ?', 3),
    ('Quel est le nom de votre école primaire ?', 4),
    ('Quel est le nom de votre meilleur ami d’enfance ?', 5),
    ('Quel est le nom de la rue où vous avez grandi ?', 6),
    ('Quel est le nom de votre premier professeur ?', 7),
    ('Quel est le modèle de votre première voiture ?', 8),
    ('Quelle est votre ville natale ?', 9),
    ('Quel est le nom de votre premier emploi ?', 10),
    ('Quel est le nom de votre chanteur ou groupe préféré ?', 11),
    ('Quelle est votre couleur préférée ?', 12),
    ('Quel est le nom de votre animal de compagnie actuel ?', 13),
    ('Quel est le nom de votre lieu de vacances préféré ?', 14),
    ('Quel est le prénom de votre grand-parent préféré ?', 15)
]

def set_app_icon(self):
        icon_path = Path("resources/icons/icon_3.ico")  
        self.setWindowIcon(QIcon(str(icon_path)))

def read_config_file_data():
    
    if config_file.exists():
        with config_file.open('r') as f:
            data = json.load(f)
        return data

def get_initial_balance():
    if init_solde_file.exists():
        with init_solde_file.open('r') as f:
            data = json.load(f)
        return data
    
def save_config_data(value_1:str, value_2:str):
    """
    Save data to config file.
    
    Args:
        `value_1` (str): key of the first key
        `value_2` (str): value of the first key
    """

    config = {
        "user_id": value_1,
        "user_name": value_2,
    }
    
    with config_file.open('w') as f:
        json.dump(config, f)
        
def set_init_balance_data(value:float):
    """
    Set the initial balance data to the init file.
    
    Args:
        `value` (float): amount value
    """

    config = {
        "solde": value,
    }
    
    with init_solde_file.open('w') as f:
        json.dump(config, f)