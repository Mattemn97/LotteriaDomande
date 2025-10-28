import csv
import random
import configparser
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import os

# === Lettura configurazione ===
config = configparser.ConfigParser()
config.read("config.ini")

punteggio_corretta = int(config.get("Settings", "punteggio_corretta"))
punteggio_errata = int(config.get("Settings", "punteggio_errata"))
randomizza_risposte = config.getboolean("Settings", "randomizza_risposte")
numero_domande = int(config.get("Settings", "numero_domande"))
mostra_punteggio_finale = config.getboolean("Settings", "mostra_punteggio_finale")
mostra_risposte_corrette = config.getboolean("Settings", "mostra_risposte_corrette")
porta_server = int(config.get("Settings", "porta_server"))
host_server = config.get("Settings", "host_server")
tempo_sessione_minuti = int(config.get("Settings", "tempo_sessione_minuti"))
salva_file_risposte = config.getboolean("Settings", "salva_file_risposte")
nome_file_output = config.get("Settings", "nome_file_output")
debug_mode = config.getboolean("Settings", "debug_mode")
colore_primario = config.get("Settings", "colore_primario")


# === Setup Flask ===
app = Flask(__name__)
app.secret_key = "supersegreto"
app.permanent_session_lifetime = timedelta(minutes=tempo_sessione_minuti)

# === Lettura domande ===
def carica_domande():
    domande = []
    with open("domande.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            domande.append(row)
    random.shuffle(domande)  # ordine casuale delle domande
    return domande[:numero_domande]

# === Rotte ===

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        codice = request.form["codice"]
        session["codice"] = codice
        return redirect(url_for("quiz"))
    return render_template("login.html", colore_primario=colore_primario)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "codice" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        domande = carica_domande()
        for d in domande:
            risposte = [
                d["Risposta giusta"],
                d["Risposta sbagliata 1"],
                d["Risposta sbagliata 2"],
                d["Risposta sbagliata 3"]
            ]
            if randomizza_risposte:
                random.shuffle(risposte)
            d["risposte"] = risposte
        session["domande"] = domande
        return render_template("quiz.html", domande=domande, tempo_sessione_minuti=tempo_sessione_minuti, colore_primario=colore_primario)


    else:
        domande = session.get("domande", [])
        codice = session["codice"]
        punteggio_totale = 0
        risultati = []

        for d in domande:
            risposta_data = request.form.get(f"domanda_{d['Id Domanda']}", "")
            corretta = (risposta_data == d["Risposta giusta"])
            punteggio = punteggio_corretta if corretta else punteggio_errata
            punteggio_totale += punteggio

            risultati.append({
                "Codice": codice,
                "Id Domanda": d["Id Domanda"],
                "Domanda": d["Domanda"],
                "Risposta data": risposta_data,
                "Corretta": "Sì" if corretta else "No",
                "Punteggio ottenuto": punteggio
            })

        # Salvataggio su file CSV
        if salva_file_risposte:
            file_exists = os.path.exists(nome_file_output)
            with open(nome_file_output, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["Codice", "Id Domanda", "Domanda", "Risposta data", "Corretta", "Punteggio ottenuto"], delimiter=";")
                if not file_exists:
                    writer.writeheader()
                writer.writerows(risultati)
        return render_template("result.html", punteggio=punteggio_totale,  colore_primario=colore_primario, mostra_punteggio=mostra_punteggio_finale)


@app.route("/logout")
def logout():
    session.pop("codice", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=host_server, port=porta_server, debug=debug_mode)
