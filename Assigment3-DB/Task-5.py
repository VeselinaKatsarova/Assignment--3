import psycopg2

# connection to the database
CONNECTION = "dbname=ski_db user=postgres password=secret host=localhost port=5432"

conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

query = """
SELECT
  time_bucket('1 hour', scan_time) AS bucket,
  client_id,
  COUNT(*) AS scans
FROM skipass_telemetry
GROUP BY bucket, client_id
ORDER BY bucket;
"""
cursor.execute(query) # execute the query

# print the select
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()

