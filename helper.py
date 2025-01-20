from datetime import datetime

class Helper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _generate_key_by_timestamp(self, target_datetime: datetime) -> str:
        """Generate a key in 'YYYYMMDD' format from a datetime object."""
        return target_datetime.strftime('%Y%m%d')