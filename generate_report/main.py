import psycopg2
import pandas as pd

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="game_sales",
            user="postgres",
            password="mysecretpassword"
        )
        cursor = conn.cursor()
        return cursor
    except Exception as e:
        print("Error: Unable to connect to the database.")
        print(e)
        exit()

def sql_query(cursor, query):
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print("Error: Unable to fetch data from the database.")
        print(e)
        cursor.close()
        exit()

def generate_dataframe_from_query(data, columns):
    try:
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        print("Error: Unable to create the report.")
        print(e)
        cursor.close()
        exit()

def generate_report_from_query(cursor, query, columns, report_name):
    data = sql_query(cursor, query)
    df = generate_dataframe_from_query(data, columns)
    df.to_csv(report_name, index=False)

if __name__ == "__main__":
    reports = [
        {
            "report_name": "sales_per_region_report.csv",
            "query": "SELECT regions.region_name, SUM(sales.sales_number) as total FROM sales INNER JOIN regions ON sales.region_id = regions.region_id GROUP BY regions.region_name;",
            "columns": ["Região", "Total de vendas (em milhões)"]
        },
        {
            "report_name": "sales_per_game_report.csv",
            "query": "SELECT games.game_name, SUM(sales.sales_number) as total FROM sales INNER JOIN games ON sales.game_id = games.game_id GROUP BY games.game_name;",
            "columns": ["Jogo", "Total de vendas (em milhões)"]
        },
        {
            "report_name": "sales_per_year_report.csv",
            "query": "SELECT games.game_year, SUM(sales.sales_number) as total FROM sales INNER JOIN games ON sales.game_id = games.game_id GROUP BY games.game_year;",
            "columns": ["Ano", "Total de vendas (em milhões)"]
        },
        {
            "report_name": "sales_per_platform_report.csv",
            "query": "SELECT platforms.platform_name, SUM(sales.sales_number) as total FROM sales INNER JOIN platforms ON sales.platform_id = platforms.platform_id GROUP BY platforms.platform_name;",
            "columns": ["Plataforma", "Total de vendas (em milhões)"]
        },
        {
            "report_name": "sales_per_publisher_report.csv",
            "query": "SELECT publishers.publisher_name, SUM(sales.sales_number) as total FROM sales INNER JOIN publishers ON sales.publisher_id = publishers.publisher_id GROUP BY publishers.publisher_name;",
            "columns": ["Publicador", "Total de vendas (em milhões)"]
        }
    ]

    cursor = connect_to_db()
    for report in reports:
        generate_report_from_query(cursor, report["query"], report["columns"], report["report_name"])

    cursor.close()
