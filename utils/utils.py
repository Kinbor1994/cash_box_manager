import json
from pathlib import Path

import shutil
from imports import QIcon

current_period_id_file = Path("current_period_data.ksb")

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

months = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Decembre"
]

def get_month_name(month_number: int) -> str:
    """
    Returns the name of the month corresponding to the given month number.

    Args:
        `month_number (int):` The number of the month (1 to 12).

    Returns:
        str: The name of the month, or "Invalid month number" if the number is not between 1 and 12.
    """
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    else:
        return "Invalid month number"
    
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
        
def save_database():
    
    # Chemin vers la base de données originale
    source = 'db.db'

    # Chemin vers la destination de la sauvegarde
    destination = 'backup_database.db'

    # Copier le fichier de base de données pour créer une sauvegarde
    shutil.copyfile(source, destination)

def write_id_to_file(id_value: str):
    """
    Write the given ID to a .ksb file.

    Args:
        id_value (int): The ID to be written to the file.
    
    Raises:
        ValueError: If the ID value is empty.
        IOError: If there is an error writing to the file.
    """
    try:
        if not id_value:
            raise ValueError("The ID value cannot be empty.")
        
        file = current_period_id_file
        if file.exists():
            file.write_text(id_value, encoding="utf-8")

    except ValueError as ve:
        raise ve
    except IOError as io_err:
        raise io_err
    except Exception as e:
        raise e


def read_id_from_file() -> int:
    """
    Read the ID from a .ksb file.

    Returns:
        int: The ID read from the file, or an empty string if an error occurs.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        file = current_period_id_file
        if not file.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        return int(file.read_text())

    except FileNotFoundError as fnf_err:
        raise fnf_err
    except IOError as io_err:
        raise io_err
    except Exception as e:
        raise e

if __name__ == "__main__":
    # Example usage
    file_path = "example_file.ksb"
    id_value = "12345"

    # Write the ID to the file
    write_id_to_file(id_value)

    # Read the ID from the file
    retrieved_id = read_id_from_file()
    print(f"The retrieved ID is: {retrieved_id}")

