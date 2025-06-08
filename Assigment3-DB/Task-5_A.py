import psycopg2

# connect to the database
CONNECTION = "dbname=ski_db user=postgres password=secret host=localhost port=5432"

conn = psycopg2.connect(CONNECTION)
conn.autocommit = True
cursor = conn.cursor()

# drop already existed view
cursor.execute("DROP MATERIALIZED VIEW IF EXISTS scans_hourly;")

# create the new view
query_create_materialized = """
        CREATE MATERIALIZED VIEW scans_hourly
        WITH (timescaledb.continuous) AS
        SELECT
            time_bucket('1 hour', scan_time) AS bucket,
            reservation_id,
            client_id,
            COUNT(*) AS total_scans
        FROM skipass_telemetry
        GROUP BY bucket, reservation_id, client_id;
        """
cursor.execute(query_create_materialized) # executing

# conn.commit()
cursor.close()
conn.close()

# print when it is done
print("Created successfully.")
