import csv
import http.server
import os
import socketserver
import urllib.parse
import uuid

from config import leggi_config
from domande import leggi_domande, prepara_risposte, seleziona_domande

config = leggi_config()
domande_tutte = leggi_domande()
PORT = config["porta_server"]
HOST = config["host_server"]

# In memoria: utenti con risposte
sessioni = {}


class QuizHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/quiz"):
            self.mostra_domande()
        elif self.path == "/":
            self.mostra_login()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith("/login"):
            self.gestisci_login()
        elif self.path.startswith("/risposte"):
            self.gestisci_risposte()
        else:
            self.send_error(404)

    def mostra_login(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
            <html><body>
            <h2>Inserisci codice identificativo:</h2>
            <form method='POST' action='/login'>
                <input name='codice' required />
                <input type='submit' value='Inizia quiz' />
            </form>
            </body></html>
        """)

    def gestisci_login(self):
        lunghezza = int(self.headers["Content-Length"])
        dati = self.rfile.read(lunghezza).decode()
        codici = urllib.parse.parse_qs(dati)
        codice = codici.get("codice", [""])[0]

        if codice:
            session_id = str(uuid.uuid4())
            sessioni[session_id] = {
                "codice": codice,
                "domande": seleziona_domande(domande_tutte, config),
                "risposte": []
            }
            self.send_response(302)
            self.send_header("Location", f"/quiz?session={session_id}&i=0")
            self.end_headers()
        else:
            self.send_error(400, "Codice mancante")

    def mostra_domande(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        session_id = query.get("session", [None])[0]
        indice = int(query.get("i", [0])[0])

        if session_id not in sessioni:
            self.send_error(403, "Sessione non trovata")
            return

        sessione = sessioni[session_id]
        domande = sessione["domande"]

        if indice >= len(domande):
            self.salva_risposte(session_id)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Quiz completato!</h2></body></html>")
            return

        domanda = domande[indice]
        risposte = prepara_risposte(domanda, config)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"""
            <html><body>
            <form method='POST' action='/risposte?session={session_id}&i={indice}'>
            <h3>{domanda['testo']}</h3>
        """.encode())

        for r in risposte:
            self.wfile.write(f"<input type='radio' name='risposta' value='{r}' required> {r}<br>".encode())

        self.wfile.write(b"<br><input type='submit' value='Avanti'></form></body></html>")

    def gestisci_risposte(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        session_id = query.get("session", [None])[0]
        indice = int(query.get("i", [0])[0])

        lunghezza = int(self.headers["Content-Length"])
        dati = self.rfile.read(lunghezza).decode()
        risposta = urllib.parse.parse_qs(dati).get("risposta", [""])[0]

        if session_id not in sessioni:
            self.send_error(403, "Sessione non trovata")
            return

        sessione = sessioni[session_id]
        sessione["risposte"].append(risposta)

        self.send_response(302)
        self.send_header("Location", f"/quiz?session={session_id}&i={indice + 1}")
        self.end_headers()

    def salva_risposte(self, session_id):
        if not config.get("salva_file_risposte", True):
            return

        sessione = sessioni[session_id]
        codice = sessione["codice"]
        risposte = sessione["risposte"]
        domande = sessione["domande"]
        nome_file = config.get("nome_file_output", "risposte_utenti.csv")

        esiste = os.path.exists(nome_file)
        with open(nome_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            if not esiste:
                writer.writerow(["Codice", "Id Domanda", "Domanda", "Risposta data", "Corretta"])

            for domanda, risposta in zip(domande, risposte):
                writer.writerow([
                    codice,
                    domanda["id"],
                    domanda["testo"],
                    risposta,
                    "SI" if risposta == domanda["corretta"] else "NO"
                ])


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), QuizHandler) as httpd:
        print(f"Server attivo su http://{HOST}:{PORT}")
        httpd.serve_forever()
