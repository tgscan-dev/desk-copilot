import json


class KVStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save_data()

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()


if __name__ == "__main__":
    store = KVStore("data.json")

    # store.set('name', 'John')
    # store.set('age', 30)

    name = store.get("nam2e") is not None
    age = store.get("age")
    print(name, age)
