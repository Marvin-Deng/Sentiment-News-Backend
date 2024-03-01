from datetime import datetime, timezone


class DateUtils:

    @staticmethod
    def convert_unix_to_utc(unix):
        utc_datetime = datetime.fromtimestamp(unix, tz=timezone.utc)
        return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def convert_datetime_to_string(datetime_str):
        input_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        day_without_leading_zero = str(input_datetime.day).lstrip('0')

        if input_datetime.hour == 0 and input_datetime.minute == 0:
            return input_datetime.strftime("%B {}, %Y".format(day_without_leading_zero))

        else:
            return input_datetime.strftime("%B {}, %Y at %H:%M UTC".format(day_without_leading_zero))
