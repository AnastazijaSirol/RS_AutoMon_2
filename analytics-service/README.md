# Analytics Service (CLI)

## Opis
Analytics-service je CLI aplikacija koja služi kao korisničko sučelje sustava.
Servis dohvaća podatke iz baze i prikazuje analitičke informacije o prometu na autocesti.

Ovaj servis predstavlja frontend aplikacije.

## Funkcionalnosti
- Broj vozila na ulazima
- Broj vozila na izlazima
- Detekcija prekoračenja brzine pored kamera
- Izračun prosječnog vremena zadržavanja na odmorištima
- Detekcija vozila koja su vozila brže od dopuštenog tijekom putovanja

## Komunikacija
- Direktan pristup bazi (read-only)
- Ne koristi MQTT

## Pokretanje

- koristiti Command Prompt

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

## Konfiguracija
- primjer konfiguracije nalazi se u `app/.env.example` datoteci
