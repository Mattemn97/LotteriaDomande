import tkinter as tk
from tkinter import messagebox
from config import leggi_config
from quiz import leggi_domande, prepara_risposte

class QuizApp:
    """Classe che gestisce l'interfaccia grafica del quiz."""
    
    def __init__(self, root, domande, config):
        self.root = root
        self.domande = domande
        self.punteggio = 0
        self.domanda_corrente = 0
        self.config = config
        
        self.label_domanda = tk.Label(root, text="", wraplength=400, font=("Arial", 12), justify="center")
        self.label_domanda.pack(pady=20)

        self.var_risposta = tk.StringVar()
        self.bottoni_risposte = []

        for _ in range(6):
            btn = tk.Radiobutton(root, text="", variable=self.var_risposta, value="", font=("Arial", 10))
            btn.pack(anchor="w", padx=50)
            self.bottoni_risposte.append(btn)

        self.btn_conferma = tk.Button(root, text="Conferma", command=self.verifica_risposta, font=("Arial", 10))
        self.btn_conferma.pack(pady=20)

        self.label_punteggio = tk.Label(root, text=f"Punteggio: {self.punteggio}", font=("Arial", 12))
        self.label_punteggio.pack(pady=10)

        self.carica_domanda()

    def carica_domanda(self):
        """Carica una nuova domanda nell'interfaccia."""
        if self.domanda_corrente < len(self.domande):
            domanda = self.domande[self.domanda_corrente]
            self.label_domanda.config(text=domanda["testo"])
            
            risposte = prepara_risposte(domanda, self.config["randomizza_risposte"])
            
            for i, (btn, risposta) in enumerate(zip(self.bottoni_risposte, risposte)):
                btn.config(text=risposta, value=risposta)
                btn.pack()

            self.var_risposta.set(None)
        else:
            messagebox.showinfo("Quiz Terminato", f"Il quiz è finito! Punteggio finale: {self.punteggio}")
            self.root.quit()

    def verifica_risposta(self):
        """Verifica la risposta selezionata e aggiorna il punteggio."""
        risposta_selezionata = self.var_risposta.get()
        
        if not risposta_selezionata:
            messagebox.showwarning("Attenzione", "Seleziona una risposta!")
            return

        domanda = self.domande[self.domanda_corrente]
        if risposta_selezionata == domanda["corretta"]:
            self.punteggio += self.config["punteggio_corretta"] * domanda["peso"]
        else:
            self.punteggio += self.config["punteggio_errata"] * domanda["peso"]

        self.label_punteggio.config(text=f"Punteggio: {self.punteggio}")
        self.domanda_corrente += 1
        self.carica_domanda()

if __name__ == "__main__":
    config = leggi_config()
    domande = leggi_domande()

    root = tk.Tk()
    root.title("Quiz")
    app = QuizApp(root, domande, config)
    root.mainloop()
