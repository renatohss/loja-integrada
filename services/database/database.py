import json


class Database:

    @staticmethod
    def get_database():
        return json.load(open("database.json"))

    def get(self, key: str):
        db = self.get_database()
        return db.get(key, None)

    def save(self, key: str, data):
        db = self.get_database()
        db[key] = data
        with open("database.json", "w") as file:
            json.dump(db, file)
