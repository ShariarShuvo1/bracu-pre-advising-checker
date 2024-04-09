import requests


def check_internet_connection(session: requests.sessions) -> bool:
    try:
        session.get("https://www.google.com/")
        return True
    except requests.ConnectionError:
        return False


def check_usis_connection(session: requests.sessions) -> bool:
    try:
        session.get("https://usis.bracu.ac.bd/")
        return True
    except requests.ConnectionError:
        return False


def login_to_usis(session: requests.sessions, email: str, password: str):
    try:
        response = session.post("https://usis.bracu.ac.bd/academia/j_spring_security_check",
                                data={'j_username': email.strip().lower(), 'j_password': password})
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        return f"USIS connection failed\nError: {e}"
