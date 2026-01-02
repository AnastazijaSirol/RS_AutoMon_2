# Camera Service

## Opis
Camera-service je mikroservis zadužen za simulaciju prolaska vozila pored nadzornih kamera na autocesti.

Na temelju podataka iz entrance-service, servis odlučuje hoće li vozilo proći pored kamere.

Implementirane su dvije kamere:
- Kamera Rijeka (CAMERA1)
- Kamera Umag (CAMERA2)

## Odgovornosti
- Obrada podataka s ulaza
- Generiranje prolaska pored kamera
- Slanje podataka na MQTT topic `traffic/camera`

## Komunikacija
- MQTT
- Subscribe:
  - `traffic/entrance`
- Publish:
  - `traffic/camera`

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