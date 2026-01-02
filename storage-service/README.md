# Storage Service

## Opis
Storage-service je mikroservis zadužen za trajnu pohranu svih podataka u sustavu.
Servis sluša sve MQTT topic-e i sprema podatke u bazu podataka.

Ovaj servis predstavlja centralni sloj sustava.

## Odgovornosti
- Slušanje svih događaja (ulazi, kamere, izlazi, odmorišta)
- Validacija i pohrana podataka u bazu

## Komunikacija
- MQTT
- Subscribe:
  - `traffic/entrance`
  - `traffic/camera`
  - `traffic/restarea`
  - `traffic/exit`

## Pokretanje

- koristiti Command Prompt

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Konfiguracija
- primjer konfiguracije nalazi se u `storage/.env.example` datoteci
