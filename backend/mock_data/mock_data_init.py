import json
# from random import random
import random
from main.database import db_manager as dbm
from main.database import db_collectors, db_collectibles
from flask import jsonify
from main import auth
from main.error import OK
from main.privelage import COLLECTOR, MANAGER, ADMIN
from sqlalchemy import text


def read_sql_file(filename):
    with open(filename, "r") as file:
        return file.read()


def execute_sql_file(filename):
    engine, conn, metadata = dbm.db_connect()

    commands = read_sql_file(filename).split(";")  # Split commands by ';'
    with engine.connect() as connection:
        for command in commands:
            # Skip executing empty command caused by the split
            if command.strip() == "":
                continue

            try:
                connection.execute(text(command))
            except Exception as e:
                print(f"Error executing command: {command.strip()}")
                print("Error message:", e)

    # commands = read_sql_file(filename)
    # # cursor = conn.cursor()
    # cursor = conn.execute(commands)
    # cursor.close()


def generate_demo():
    # Generage users for demo, two ADMIN and 1 MANAGER and 3 COLLECTOR accounts
    auth.register_collector("ds@gmail.com", None, "dyllanson", privelage=COLLECTOR)
    auth.register_collector("ua@gmail.com", None, "uguudei", privelage=MANAGER)
    auth.register_collector("sz@gmail.com", None, "stella", privelage=COLLECTOR)
    auth.register_collector("mx@gmail.com", None, "meng", privelage=COLLECTOR)
    auth.register_collector("gw@gmail.com", None, "greg", privelage=ADMIN)

    # Update user info
    db_collectors.update_collector(
        1,
        username="uso",
        first_name="Dyllanson",
        last_name="So",
        phone="8083742129",
        address="696 Londonderry Avenue",
        profile_picture="https://robohash.org/utomniseos.png?size=50x50&set=set1",
    )
    db_collectors.update_collector(
        2,
        username="uamar",
        first_name="Uguudei",
        last_name="Amarbayasgalan",
        phone="5189304696",
        address="26 Bultman Terrace",
        profile_picture="https://robohash.org/cumqueaccusamusvoluptas.png?size=50x50&set=set1",
    )
    db_collectors.update_collector(
        3,
        username="szhang",
        first_name="Stella",
        last_name="Zhang",
        phone="8045288315",
        address="6 Bunting Plaza",
        profile_picture="https://robohash.org/nesciuntculpaat.png?size=50x50&set=set1",
    )
    db_collectors.update_collector(
        4,
        username="mxiao",
        first_name="Meng",
        last_name="Xiao",
        phone="6246014987",
        address="79 Mariners Cove Center",
        profile_picture="https://robohash.org/sedquodamet.png?size=50x50&set=set1",
    )
    db_collectors.update_collector(
        5,
        username="gwhite",
        first_name="Gregory",
        last_name="Whitehead",
        phone="8083742129",
        address="696 Londonderry Avenue",
        profile_picture="https://robohash.org/autemutet.png?size=50x50&set=set1",
    )


    # Collectors will instantiate 20 more collectors
    execute_sql_file("./mock_data/collectors.sql")

    # Populates db with 5 campaigns
    execute_sql_file("./mock_data/campaigns.sql")

    # Populates campaignes with 100 randomly allocatedc collectibles
    # execute_sql_file("./mock_data/collectibles.sql")
    generate_collectibles()

    # Populates the first 20 collectors with 500 randomly allocated collectibles to their collections
    execute_sql_file("./mock_data/collections.sql")

    # Populates the first 20 collectors with 300 randomly allocated collectibles to their wantlists
    execute_sql_file("./mock_data/wantlist.sql")

    return (
        jsonify(
            msg=""" manager account and 3 test accounts added. id's: 1, 2, 3, 4 Mock data initialised! """
        ),
        OK,
    )

def generate_collectibles(num_collectibles=100, num_campaigns=5):
    f = open('./mock_data/collectibles.json')
    collectibles = random.sample(json.load(f), num_collectibles)

    for collectible_id in range(0, num_collectibles):
        campaign_id = random.randrange(1, num_campaigns + 1)
        photo_id = random.randrange(300)

        db_collectibles.register_collectible(
            campaign_id,
            collectibles[collectible_id]["name"],
            collectibles[collectible_id]["paragraph"],
            f"https://picsum.photos/id/{photo_id}/300/200",
        )

    f.close()
