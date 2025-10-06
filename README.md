# Lotteria Domande

Questo progetto fornisce un'applicazione per rispondere a domande a scelta multipla lette da un file CSV. Le risposte vengono valutate in base a un sistema configurabile e il punteggio viene aggiornato dinamicamente.

## 📂 Struttura del Progetto
```
quiz_project/
│── main.py          # Avvio della GUI
│── quiz.py          # Logica del quiz
│── config.py        # Gestione della configurazione
│── domande.csv      # File con le domande
│── config.ini       # File di configurazione
```

## 📦 Requisiti

Assicurati di avere Python 3 installato. Installa le dipendenze richieste con:

```sh
pip install -r requirements.txt
```
(Nota: Attualmente non ci sono dipendenze esterne.)

## 🚀 Avvio del Progetto

Esegui il file `main.py` per avviare l'applicazione:

```sh
python main.py
```

## 📜 Formato del file `domande.csv`

Il file delle domande deve avere il seguente formato con `;` come delimitatore:

```csv
Id Domanda;Domanda;Risposta giusta;Risposta sbagliata 1;Risposta sbagliata 2;Risposta sbagliata 3;Peso domanda
1;Qual è la capitale d'Italia?;Roma;Milano;Napoli;Torino;2
2;Chi ha scritto 'La Divina Commedia'?;Dante Alighieri;Petrarca;Boccaccio;Manzoni;3
```

## ⚙️ Configurazione (`config.ini`)

Il file `config.ini` permette di personalizzare il comportamento del quiz:

```ini
[Settings]
punteggio_corretta = 10
punteggio_errata = -5
randomizza_risposte = True
```

- **punteggio_corretta**: Punti assegnati per una risposta corretta (moltiplicato per il peso della domanda).
- **punteggio_errata**: Punti sottratti per una risposta errata.
- **randomizza_risposte**: Se `True`, mescola l'ordine delle risposte per ogni domanda.

## 🛠 Struttura dei File Python

### `config.py` - Lettura della Configurazione
Gestisce la lettura delle impostazioni da `config.ini`.

### `quiz.py` - Logica del Quiz
Carica le domande da `domande.csv`, prepara le risposte e applica la logica di punteggio.

### `main.py` - GUI con Tkinter
Avvia l'interfaccia grafica, mostra le domande e gestisce l'interazione con l'utente.

## 📌 Funzionamento dell'Applicazione
1. Il programma carica le domande e la configurazione.
2. Mostra a schermo una domanda con le risposte multiple.
3. L'utente seleziona una risposta e conferma.
4. Il punteggio viene aggiornato in base alla risposta.
5. Alla fine, viene mostrato il punteggio totale.
