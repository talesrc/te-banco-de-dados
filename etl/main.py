from models.publisher import Publisher
from models.platform import Platform
from models.region import Region
from models.game import Game
from models.sale import Sale

from logger import logger

from database import init_db, clean_db, create_record, db_session
import pandas as pd
import boto3
import time
import os

REGIONS = ["North_America", "Europe", "Japan", "Others"]
SHEET_NAME = "vgsales.csv"

def get_id(session: any, name: str, table_name: str):
    match table_name:
        case "game":
            query = session.query(Game.id).filter(Game.name == name)
        case "platform":
            query = session.query(Platform.id).filter(Platform.name == name)
        case "publisher":
            query = session.query(Publisher.id).filter(Publisher.name == name)
        case "region":
            query = session.query(Region.id).filter(Region.name == name)
        case _:
            raise Exception("You MUST give a valid table name!!")
    return int(query.first()[0])


def populate_regions_table() -> None:
    start_time = time.time()
    logger.info("Populating regions table...")
    for region in REGIONS:
        record = Region(region=region)
        create_record(record)
    finish_time = time.time()
    logger.info(f"Concluded after {(finish_time - start_time):.2f} seconds")

def populate_platform_table(df) -> None:
    start_time = time.time()
    logger.info("Populating platform table...")
    platforms = df[['Platform']].drop_duplicates().to_records()
    for platform in platforms:
        record = Platform(name=platform[1])
        create_record(record)
    finish_time = time.time()
    logger.info(f"Concluded after {(finish_time - start_time):.2f} seconds")

def populate_publisher_table(df) -> None:
    start_time = time.time()
    logger.info("Populating publisher table...")
    publishers = df[['Publisher']].drop_duplicates().to_records()
    for publisher in publishers:
        record = Publisher(name=publisher[1])
        create_record(record)
    finish_time = time.time()
    logger.info(f"Concluded after {(finish_time - start_time):.2f} seconds")

def populate_games_table(df) -> None:
    start_time = time.time()
    logger.info("Populating games table...")
    games = df[[
        'Name','Year','Genre'
    ]].drop_duplicates().to_records()

    for game in games:
        record = Game(name=game[1], year=game[2], genre=game[3])
        create_record(record)
    finish_time = time.time()
    logger.info(f"Concluded after {(finish_time - start_time):.2f} seconds")

def populate_sales_table(session: any, df: any) -> None:
    start_time = time.time()
    logger.info("Populating sales table...")
    rows = df.drop_duplicates().to_records()
    for row in rows:
        for region in range(7, 11):
            record = Sale(
                sales=float(row[region]),
                region_id=(region - 6), #pegar o indice do array regions como id
                publisher_id=get_id(session, row[6], "publisher"),
                game_id=get_id(session, row[2], "game"),
                platform_id=get_id(session, row[3], "platform"),
            )
            create_record(record)
    finish_time = time.time()
    logger.info(f"Concluded after {finish_time - start_time:.2f} seconds")


if __name__ == '__main__':
    s3_client = boto3.client('s3')
    logger.info("Getting historical data...")
    s3_object = s3_client.get_object(
        Bucket="videogame-sales-tebd", 
        Key=SHEET_NAME
    )

    with open(SHEET_NAME, "wb") as file:
        file.write(s3_object["Body"].read())

    logger.info("Transforming data...")
    df = pd.read_csv(SHEET_NAME)
    df.astype({'Year':'Int32'})

    values = {
        "X360": "Xbox 360",
        "XB": "Xbox",
        "XOne": "Xbox One",
        "WiiU": "Nintendo Wii U",
        "Wii": "Nintendo Wii",
        "TG16": "TurboGrafx-16",
        "SNES": "Super Nintendo Entertainment System",
        "SCD": "Sega CD",
        "SAT": "Sega Saturn",
        "PSV": "Playstation Vita",
        "PSP": "Playstation Portable",
        "PS4": "Playstation 4",
        "PS3": "Playstation 3",
        "PS2": "Playstation 2",
        "PS": "Playstation",
        "PC": "Computador",
        "NG": "Neo Geo",
        "NES": "Nintendo Entertainment System",
        "N64": "Nintendo 64",
        "GG": "Game Gear",
        "GEN": "Sega Genesis",
        "GC": "Nintendo GameCube",
        "GBA": "GameBoy Advanced",
        "GB": "GameBoy",
        "DS": "Nintendo DS",
        "DC": "Dreamcast",
        "3DS": "Nintendo 3DS",
        "3DO": "Panasonic 3DO",
        "2600": "Atari 2600"
    }
    df['Platform'].replace(values, inplace=True)

    df.dropna(inplace=True)

    clean_db()
    init_db()

    populate_publisher_table(df)
    populate_platform_table(df)
    populate_regions_table()
    populate_games_table(df)
    populate_sales_table(db_session, df)

    os.remove(SHEET_NAME)
