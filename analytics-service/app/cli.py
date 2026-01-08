import typer
from database import get_connection
import queries
from queries import detect_fast_vehicles

app = typer.Typer()

@app.command()
def entrances():
    print("Broj vozila na ulazima:")
    conn = get_connection()
    for cam, count in queries.count_entrances(conn):
        typer.echo(f"{cam}: {count}")

@app.command()
def exits():
    print("Broj vozila na izlazima:")
    conn = get_connection()
    for cam, count in queries.count_exits(conn):
        typer.echo(f"{cam}: {count}")

@app.command()
def speeding():
    print("Vozila koja su prekoračila brzinu na kamerama:")
    conn = get_connection()
    rows = queries.speeding_vehicles(conn)

    if not rows:
        typer.echo("Nema prekoračenja.")
        return

    for v, cam, speed, limit in rows:
        typer.echo(
            f"{v} na {cam}: {speed} km/h (limit {limit})"
        )

@app.command()
def restareas():
    print("Prosječno vrijeme provedeno na odmorištima:")
    conn = get_connection()
    for cam, avg in queries.avg_rest_time(conn):
        typer.echo(f"{cam}: {avg:.2f} min")

@app.command()
def fast_travel():
    conn = get_connection()
    results = detect_fast_vehicles(conn)

    if not results:
        typer.echo("Nema prebrzih vozila.")
        return

    print("Vozila koja su putovala prebrzo:")

    for r in results:
        typer.echo(
            f"- {r['vehicle_id']} ruta "
            f"{r['route'][0]} -> {r['route'][1]} : "
            f"{r['actual']} min (očekivano {r['expected']} min)"
        )

def interactive_menu():
    while True:
        print("\nOdaberite opciju:")
        print("1 - Broj vozila na ulazima")
        print("2 - Broj vozila na izlazima")
        print("3 - Vozila koja su prekoračila brzinu")
        print("4 - Prosječno vrijeme na odmorištima")
        print("5 - Vozila koja su putovala prebrzo")
        print("0 - Izlaz")

        choice = input("Unesite broj: ").strip()

        if choice == "1":
            entrances()
        elif choice == "2":
            exits()
        elif choice == "3":
            speeding()
        elif choice == "4":
            restareas()
        elif choice == "5":
            fast_travel()
        elif choice == "0":
            print("Izlaz iz programa.")
            break
        else:
            print("Nepoznata opcija, pokušajte ponovno.")
