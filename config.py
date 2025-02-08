import configparser

def leggi_config(file_ini="config.ini"):
    """Legge il file di configurazione e restituisce i parametri."""
    config = configparser.ConfigParser()
    config.read(file_ini)

    return {
        "punteggio_corretta": int(config["Settings"]["punteggio_corretta"]),
        "punteggio_errata": int(config["Settings"]["punteggio_errata"]),
        "randomizza_risposte": config["Settings"].getboolean("randomizza_risposte")
    }
