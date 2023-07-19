from reportlab.pdfgen import canvas
import psycopg2
import os
import csv  


DATABASE = os.environ["DATABASE"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_HOST = os.environ["DATABASE_HOST"]
DATABASE_PORT = os.environ["DATABASE_PORT"]

if __name__ == "__main__":
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        database=DATABASE,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )

    cur = conn.cursor()

    sql = "SELECT * FROM sales"
    output_query = f"COPY ({sql}) TO STDOUT WITH CSV HEADER DELIMITER ';'"


    with open("report.csv", "w") as file:
        cur.copy_expert(output_query, file)
