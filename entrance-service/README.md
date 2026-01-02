# Entrance Service

## Opis
Entrance-service je mikroservis zadužen za simulaciju ulazaka vozila na autocestu.

Implementirana su tri ulaza:
- Pula
- Rijeka
- Umag

## Odgovornosti
- Generiranje ulaza vozila
- Slanje podataka na MQTT topic `traffic/entrance`

## Komunikacija
- MQTT (asinkrona komunikacija)
- Publish:
  - `traffic/entrance`

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