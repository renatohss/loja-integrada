import json
from typing import Dict

db: Dict = json.load(open("database.json"))


class Database:

    @staticmethod
    def get(key: str):
        return db.get(key, None)

    @staticmethod
    def save(data):
        db[data["id"]] = data
        with open("database.json", "w") as file:
            json.dump(db, file)
