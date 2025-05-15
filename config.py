import configparser


def leggi_config(file_ini="config.ini"):
    """Legge il file di configurazione e restituisce i parametri come dizionario."""
    config = configparser.ConfigParser()
    config.read(file_ini)

    return {
        # Punteggi
        "punteggio_corretta": int(config["Settings"]["punteggio_corretta"]),
        "punteggio_errata": int(config["Settings"]["punteggio_errata"]),

        # Risposte
        "randomizza_risposte": config["Settings"].getboolean("randomizza_risposte", fallback=True),
        "numero_domande": int(config["Settings"].get("numero_domande", 0)),

        # Output risultati
        "mostra_punteggio_finale": config["Settings"].getboolean("mostra_punteggio_finale", fallback=True),
        "mostra_risposte_corrette": config["Settings"].getboolean("mostra_risposte_corrette", fallback=False),

        # Server
        "porta_server": int(config["Settings"].get("porta_server", 8080)),
        "host_server": config["Settings"].get("host_server", "0.0.0.0"),

        # Sicurezza e accesso
        "tempo_sessione_minuti": int(config["Settings"].get("tempo_sessione_minuti", 15)),
        "richiedi_conferma_codice": config["Settings"].getboolean("richiedi_conferma_codice", fallback=True),

        # Salvataggio su file
        "salva_file_risposte": config["Settings"].getboolean("salva_file_risposte", fallback=True),
        "nome_file_output": config["Settings"].get("nome_file_output", "risposte_utenti.csv"),

        # Debug
        "debug_mode": config["Settings"].getboolean("debug_mode", fallback=False)
    }
