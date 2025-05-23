import csv
import random


def leggi_domande(file_csv="domande.csv"):
    """Legge le domande da un file CSV e le restituisce in una lista di dizionari."""
    domande = []

    with open(file_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            domande.append({
                "id": row["Id Domanda"],
                "testo": row["Domanda"],
                "corretta": row["Risposta giusta"],
                "errate": [
                    row["Risposta sbagliata 1"],
                    row["Risposta sbagliata 2"],
                    row["Risposta sbagliata 3"]
                ],
                "peso": int(row["Peso domanda"])
            })

    return domande


def prepara_risposte(domanda, config):
    """Prepara l'elenco delle risposte, mescolandole se richiesto dalla config."""
    risposte = [domanda["corretta"]] + [r for r in domanda["errate"] if r]

    if config.get("randomizza_risposte", True):
        random.shuffle(risposte)

    return risposte


def seleziona_domande(domande, config):
    """Restituisce solo il numero di domande richiesto dalla configurazione."""
    num = config.get("numero_domande", len(domande))
    return random.sample(domande, min(num, len(domande)))
