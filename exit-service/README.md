# Exit Service

## Opis
Exit-service je mikroservis zadužen za simulaciju izlazaka vozila s autoceste.

Na temelju podataka s ulaza i kamera, servis određuje na kojem izlazu vozilo napušta autocestu.

Implementirani su izlazi:
- Pula
- Rijeka
- Umag

## Odgovornosti
- Obrada ulaza i kamera
- Generiranje izlazaka vozila
- Slanje događaja na MQTT topic `traffic/exit`

## Komunikacija
- MQTT
- Subscribe:
  - `traffic/entrance`
  - `traffic/camera`
- Publish:
  - `traffic/exit`

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
