# Entrance Service

## Opis
Entrance-service je mikroservis zadužen za simulaciju ulazaka vozila na autocestu.

Svaki ulaz (Pula, Rijeka, Umag) simuliran je kao zasebna asinkrona korutina.

## Zadaci
- Generiranje ulaza vozila
- Slanje podataka na MQTT topic `traffic/entrance`

## Komunikacija
- MQTT (asinkrona komunikacija)
- Publish:
  - `traffic/entrance`
- Subscribe:
  - nema

## Pokretanje

- koristiti Command Prompt

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```