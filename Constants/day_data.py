day_checker = {
    "Sa": "Saturday",
    "Su": "Sunday",
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
}

day_list = ["Saturday", "Sunday", "Monday",
            "Tuesday", "Wednesday", "Thursday", "Friday"]


def get_short_day_name(day: str) -> str:
    for short, full in day_checker.items():
        if full == day:
            return short
