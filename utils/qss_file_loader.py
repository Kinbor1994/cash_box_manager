
from pathlib import Path

def load_stylesheet(path: str):
    """
    Read file content using pathlib and handle potential errors.

    Args:
        path (str): The path to the stylesheet file.

    Returns:
        str: The stylesheet content if successful, or an empty string if an error occurs.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If there are insufficient permissions to read the file.
        IOError: If any other I/O error occurs during file reading.
    """
    try:
        file = Path(path)
        if file.exists():
            with file.open('r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Le fichier '{path}' n'existe pas.")
    except PermissionError:
        print(f"Erreur: Permission insuffisante pour lire le fichier '{path}'.")
    except IOError as e:
        print(f"Erreur lors de la lecture du fichier '{path}': {e}")

    return ""  