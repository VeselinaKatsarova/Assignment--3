import mysql.connector
import psycopg2

# MariaDB database
maria_conn = mysql.connector.connect(
    user="root",
    password="my-secret-pw",
    host="localhost",
    port=3306,
    database="ski_hotel"
)
maria_cursor = maria_conn.cursor(dictionary=True) # connectiong to the database

# database info
pg_conn = psycopg2.connect(
    dbname="ski_db",
    user="postgres",
    password="secret",
    host="localhost",
    port=5432
)
pg_cursor = pg_conn.cursor() # connectiong to the database

#Tables from database
tables = [
    ("Ski_pass", ["type_pass", "price"]),
    ("Pass_info", ["pass_id", "location", "difficulty", "size"]),
    ("Ski_pass_info", ["type_pass", "pass_id"]),
    ("Reservation", ["reservation_id", "name", "num_room", "people_num", "arraival_date", "departure_date", "total_price", "num_people_ski", "type_pass"]),
    ("Clients", ["client_id", "first_name", "last_name", "email", "telephon", "reservation_id"]),
    ("Rooms", ["room_id", "type_room", "bets", "price"]),
    ("Room_description", ["description_id", "size", "bathroom", "wifi", "tv"]),
    ("Number_room", ["num_room_id", "room_id", "description_id", "reservation_id"]),
    ("Review", ["review_id", "comment", "rating_room", "rating_ski_pass", "reservation_id"])
]

# adding the tables in the new database
for table, columns in tables:
    print(f"Migrating {table}")
    try:
        maria_cursor.execute(f"SELECT {', '.join(columns)} FROM {table}")
        rows = maria_cursor.fetchall()

        for row in rows:
            placeholders = ', '.join(['%s'] * len(columns))
            col_list = ', '.join(columns)
            try:
                # Special handling for Room_description to convert integers to booleans
                if table == "Room_description":
                    bool_fields = {"bathroom", "wifi", "tv"}
                    values = tuple(
                        bool(row[col]) if col in bool_fields else row[col]
                        for col in columns
                    )
                else:
                    values = tuple(row[col] for col in columns)

                pg_cursor.execute(
                    f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) ON CONFLICT DO NOTHING",
                    values
                )
            except Exception as e:
                print(f"  Error inserting into {table}: {e}")
                pg_conn.rollback()
            else:
                pg_conn.commit()

    except Exception as e:
        print(f"  Error reading from {table}: {e}")

maria_cursor.close()
pg_cursor.close()
maria_conn.close()
pg_conn.close()

# When the process is finished print - Completed
print("Completed")
