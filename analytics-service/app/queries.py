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

def get_vehicle_entry_exit(conn, vehicle_id):
    cur = conn.cursor()

    cur.execute("""
        SELECT camera_id, timestamp
        FROM readings
        WHERE vehicle_id = ?
          AND is_entrance = 1
        ORDER BY timestamp ASC
        LIMIT 1
    """, (vehicle_id,))
    entry = cur.fetchone()

    cur.execute("""
        SELECT camera_id, timestamp
        FROM readings
        WHERE vehicle_id = ?
          AND is_exit = 1
        ORDER BY timestamp DESC
        LIMIT 1
    """, (vehicle_id,))
    exit_ = cur.fetchone()

    return entry, exit_

def get_restarea_time(conn, vehicle_id):
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp_entrance, timestamp_exit
        FROM readings
        WHERE vehicle_id = ?
          AND is_restarea = 1
          AND timestamp_exit IS NOT NULL
    """, (vehicle_id,))

    total = 0
    for start, end in cur.fetchall():
        t1 = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        total += (t2 - t1).total_seconds() / 60

    return total

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

    vehicles = get_all_vehicles(conn)

    for vehicle_id in vehicles:
        entry, exit_ = get_vehicle_entry_exit(conn, vehicle_id)

        if not entry or not exit_:
            continue

        entry_cam, entry_ts = entry
        exit_cam, exit_ts = exit_

        route = (entry_cam, exit_cam)
        if route not in EXPECTED_TRAVEL_TIMES:
            continue

        t_entry = datetime.strptime(entry_ts, "%Y-%m-%d %H:%M:%S")
        t_exit = datetime.strptime(exit_ts, "%Y-%m-%d %H:%M:%S")

        total_time = (t_exit - t_entry).total_seconds() / 60
        rest_time = get_restarea_time(conn, vehicle_id)

        actual_travel = total_time - rest_time
        expected = EXPECTED_TRAVEL_TIMES[route]

        if actual_travel < expected:
            results.append({
                "vehicle_id": vehicle_id,
                "route": route,
                "actual": round(actual_travel, 2),
                "expected": expected
            })

    return results
