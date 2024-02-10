from datetime import datetime

class DateUtils:

    @staticmethod
    def convert_string_to_datetime(date_string):
        try:
            return datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError as e:
            print(f"Error converting '{date_string}' to datetime: {e}")
            raise