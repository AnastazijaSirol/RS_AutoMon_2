from datetime import datetime

def count_entrances(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT camera_id, COUNT(*)
        FROM readings
        WHERE is_entrance = 1
        GROUP BY camera_id
    """)
    return cur.fetchall()


def count_exits(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT camera_id, COUNT(*)
        FROM readings
        WHERE is_exit = 1
        GROUP BY camera_id
    """)
    return cur.fetchall()


def speeding_vehicles(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT vehicle_id, camera_id, speed, speed_limit
        FROM readings
        WHERE is_camera = 1
          AND speed > speed_limit
    """)
    return cur.fetchall()


def avg_rest_time(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT camera_id,
               AVG(
                 (strftime('%s', timestamp_exit) -
                  strftime('%s', timestamp_entrance)) / 60.0
               )
        FROM readings
        WHERE is_restarea = 1
          AND timestamp_exit IS NOT NULL
        GROUP BY camera_id
    """)
    return cur.fetchall()


def get_all_vehicles(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT vehicle_id
        FROM readings
    """)
    return [row[0] for row in cur.fetchall()]


EXPECTED_TRAVEL_TIMES = {
    ("PULA-ENTRANCE", "RIJEKA-EXIT"): 90,
    ("PULA-ENTRANCE", "UMAG-EXIT"): 60,
    ("UMAG-ENTRANCE", "RIJEKA-EXIT"): 70,
    ("UMAG-ENTRANCE", "PULA-EXIT"): 60,
    ("RIJEKA-ENTRANCE", "UMAG-EXIT"): 70,
    ("RIJEKA-ENTRANCE", "PULA-EXIT"): 90,
}


def detect_fast_vehicles(conn):
    results = []
    cur = conn.cursor()

    vehicles = get_all_vehicles(conn)

    for vehicle_id in vehicles:

        cur.execute("""
            SELECT camera_id, timestamp
            FROM readings
            WHERE vehicle_id = ?
              AND is_exit = 1
            ORDER BY timestamp ASC
        """, (vehicle_id,))
        exits = cur.fetchall()

        for exit_cam, exit_ts in exits:
            t_exit = datetime.strptime(exit_ts, "%Y-%m-%d %H:%M:%S")

            cur.execute("""
                SELECT camera_id, timestamp
                FROM readings
                WHERE vehicle_id = ?
                  AND is_entrance = 1
                  AND timestamp < ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (vehicle_id, exit_ts))
            entry = cur.fetchone()

            if not entry:
                continue

            entry_cam, entry_ts = entry
            route = (entry_cam, exit_cam)

            if route not in EXPECTED_TRAVEL_TIMES:
                continue

            t_entry = datetime.strptime(entry_ts, "%Y-%m-%d %H:%M:%S")

            total_time = (t_exit - t_entry).total_seconds() / 60

            cur.execute("""
                SELECT timestamp_entrance, timestamp_exit
                FROM readings
                WHERE vehicle_id = ?
                  AND is_restarea = 1
                  AND timestamp_entrance >= ?
                  AND timestamp_exit <= ?
                  AND timestamp_exit IS NOT NULL
            """, (vehicle_id, entry_ts, exit_ts))

            rest_time = 0
            for start, end in cur.fetchall():
                t1 = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
                t2 = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                rest_time += (t2 - t1).total_seconds() / 60

            actual = total_time
            expected = EXPECTED_TRAVEL_TIMES[route]

            if actual <= 0:
                continue

            if actual < expected:
                results.append({
                    "vehicle_id": vehicle_id,
                    "route": route,
                    "actual": round(actual, 2),
                    "expected": expected
                })

    return results
