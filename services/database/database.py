import json
from typing import Dict


class Database:
    db: Dict = json.load(open("database.json"))

    def get(self, key: str):
        return self.db.get(key, None)

    def save(self, data):
        self.db[data["id"]] = data
        with open("database.json", "w") as file:
            json.dump(self.db, file)
