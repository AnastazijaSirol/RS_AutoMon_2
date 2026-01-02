# RestArea Service

## Opis
Restarea-service je mikroservis zadužen za simulaciju zaustavljanja vozila na odmorištima.

Na temelju ulaza i izlaza vozila, servis određuje hoće li se vozilo zaustaviti na odmorištu.

Implementirana su dva odmorišta:
- Odmorište Pula (REASTAREA1)
- Odmorište Rijeka (RESTAREA2)

## Odgovornosti
- Obrada podataka s ulaza i izlaza
- Generiranje podataka zaustavljanja vozila na odmorištima
- Slanje događaja na MQTT topic `traffic/restarea`

## Komunikacija
- MQTT
- Subscribe:
  - `traffic/entrance`
  - `traffic/exit`
- Publish:
  - `traffic/restarea`

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