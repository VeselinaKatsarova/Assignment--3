import psycopg2

# Database
conn = psycopg2.connect(
    dbname="ski_db",
    user="postgres",
    password="secret",
    host="localhost"
)



query_create_sensordata_table = """
    CREATE TABLE skipass_telemetry (
        scan_time TIMESTAMPTZ NOT NULL,
        skipass_id UUID NOT NULL,
        resort TEXT NOT NULL,
        lift TEXT,
        gate TEXT,
        reservation_id INT,
        client_id INT,
        scan_status TEXT,
        metadata JSONB,
        PRIMARY KEY (scan_time, skipass_id)
    );
                                    """

query_create_sensordata_hypertable = "SELECT create_hypertable('skipass_telemetry', 'scan_time');"

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS skipass_telemetry CASCADE;") # drop the table if already exist
cursor.execute(query_create_sensordata_table)
cursor.execute(query_create_sensordata_hypertable)
# commit changes to the database to make changes persistent
conn.commit()
cursor.close()

# Print it when it is done
print("Completed")
