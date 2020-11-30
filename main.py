import datetime as dt


class Record:

    def __init__(self, amount, comment, date=""):
        self.amount = amount
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, "%d.%m.%Y").date()
        self.comment = comment


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if 7 > (today - record.date).days >= 0:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """Возвращает остаток калорий на сегодня."""
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал"
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):

    USD_RATE = 60.  # Курс доллар США.
    EURO_RATE = 70.  # Курс Евро.

    def get_today_cash_remained(self, currency, usd_rate=USD_RATE, euro_rate=EURO_RATE):
        """Возвращает остаток денег на сегодня."""
        cash_remained = self.limit - self.get_today_stats()

        currency_type = currency
        if currency == "usd":
            cash_remained /= usd_rate
            currency_type = "USD"
        elif currency_type == "eur":
            cash_remained /= euro_rate
            currency_type = "Euro"
        elif currency_type == "rub":
            # cash_remained /= 1.00
            currency_type = "руб"
        else:
            raise ValueError(f"Неизвестный тип валюты: {currency_type}")

        if cash_remained > 0:
            return f"На сегодня осталось {cash_remained:.2f} {currency_type}"
        elif cash_remained == 0:
            return "Денег нет, держись"
        else:
            return f"Денег нет, держись: твой долг {cash_remained:.2f} {currency_type}"
