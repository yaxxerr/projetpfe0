import psycopg2

try:
    conn = psycopg2.connect(
        dbname="prjpfedb",
        user="admin0",
        password="admin0",
        host="localhost",
        port="5432"
    )
    print("✅ PostgreSQL connection successful.")
except Exception as e:
    print("❌ Connection failed:")
    print(e)
