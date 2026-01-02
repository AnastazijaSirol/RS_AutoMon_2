# RS AutoMon – Mikroservisna arhitektura

## Opis projekta
RS AutoMon je simulacijska aplikacija za praćenje prometa na autocesti Pula-Rijeka-Umag.

Projekt simulira kretanje vozila od ulaza na autocestu, preko kamera i odmorišta, do izlaza s autoceste te omogućuje analizu prikupljenih podataka.

Aplikacija je transformirana iz monolitne arhitekture u mikroservisnu arhitekturu temeljenu na asinkronoj komunikaciji putem message brokera (MQTT).

## Mikroservisna arhitektura

Aplikacija je podijeljena na sljedeće mikroservise:

- **entrance-service**  
  Simulira ulazak vozila na autocestu (Pula, Rijeka, Umag)

- **camera-service**  
  Simulira prolazak vozila pored nadzornih kamera

- **exit-service**  
  Simulira izlazak vozila s autoceste (Pula, Rijeka, Umag)

  - **restarea-service**  
  Simulira zaustavljanje vozila na odmorištima

- **storage-service**  
  Centralni servis za trajnu pohranu svih podataka u bazu podataka

- **analytics-service (CLI)**  
  Korisničko sučelje u obliku CLI aplikacije za analizu podataka

Svaki mikroservis nalazi se u vlastitom direktoriju s vlastitim virtualnim okruženjem

## Komunikacija između mikroservisa

Komunikacija je asinkrona i temelji se na **MQTT message brokeru (Mosquitto)**.

### MQTT topic-i:
- `traffic/entrance` – ulazak na autocestu
- `traffic/camera` – prolazak pored kamera
- `traffic/restarea` – zaustavljanje na odmorištima
- `traffic/exit` – izlazak s autoceste

## Baza podataka

U ovom projektu korištena je jedna zajednička baza podataka (SQLite), kojom upravlja **storage-service**.
Ostali mikroservisi nemaju direktan pristup bazi, već komuniciraju s njom asinkrono preko MQTT poruka. 
Time se zadržala jasna podjela odgovornosti, izbjeglo se dijeljenje baze između servisa i pojednostavljena je analizu podataka.

## Dijagram arhitekture
U repozitoriju je priložen dijagram mikroservisne arhitekture koji prikazuje:
- mikroservise
- MQTT broker kao centralnu točku komunikacije
- bazu podataka
- smjerove komunikacije između servisa

## Dokumnetacija MQTT topica

U ovom projektu nema HTTP endpointova, već MQTT topici preko kojih mikroservisi razmjenjuju poruke. 

### Topic: **traffic/entrance**

Publisher: 
- entrance-service

Subscribers:
- camera-service
- exit-service
- restarea-service
- storage-service

Poruka se šalje kada vozilo uđe na autocestu.

Primjer poruke:

{
  "camera_id": "PULA-ENTRANCE",
  "camera_location": Ulaz Pula,
  "vehicle_id": PU723MD,
  "timestamp": "2026-01-02 12:30:45",
  "is_entrance": True
}

### Topic: **traffic/restarea**

Publisher: 
- restarea-service

Subscribers:
- storage-service

Poruka se šalje kada se vozilo zaustavi na odmorištu.

Primjer poruke:

{
  "camera_id": RESTAREA1,
  "camera_location": Odmorište Pula,
  "vehicle_id": PU723md,
  "is_restarea": True,
  "timestamp_entrance": "2026-01-02 12:30:45",
  "timestamp_exit": "2026-01-02 12:37:32",
}

### Topic: **traffic/exit**

Publisher: 
- exit-service

Subscribers:
- restarea-service
- storage-service

Poruka se šalje kada vozilo izađe s autoceste.

Primjer poruke:

{
  "camera_id": PULA-EXIT,
  "camera_location": Izlaz Pula,
  "vehicle_id": PU723MD,
  "timestamp": "2026-01-02 12:30:45",
  "is_exit": True
}