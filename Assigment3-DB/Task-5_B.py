import psycopg2

# connect to the database
CONNECTION = "dbname=ski_db user=postgres password=secret host=localhost port=5432"

conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

query = """
    SELECT show_chunks('skipass_telemetry');
    """
cursor.execute(query) # execute

# print the select query
chunks = cursor.fetchall()
for chunk in chunks:
    print(f" - {chunk[0]}")

cursor.close()
conn.close()
