import json
from ...config import JSON_DATABASE_NAME


class JsonFileDatabaseConnector:
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_DATABASE_NAME, "r") as file:
            return json.load(file)

    def save(self, entity: object) -> int:
        """
        Save data in json file
        :param entity: object ConvertedPricePLN
        :return: id in json file dict
        """
        next_id = max([int(key) for key in self._data.keys()]) + 1
        values = {
            'id': next_id,
            'currency': entity.currency,
            'rate': entity.currency_rate,
            'price_in_pln': entity.price_in_pln,
            'date': entity.currency_rate_fetch_date,
        }
        data = self._data
        data[str(next_id)] = values
        with open(JSON_DATABASE_NAME, 'r+') as f:
            f.seek(0)
            json.dump(data, f, indent=2)
        return next_id


    def get_all(self) -> list[...]:
        """
        Get all values from the file and convert from dict -> list
        :return: list of all values from file
        """
        return list(self._data.values())


    def get_by_id(self) -> ...:
        raise NotImplementedError()

