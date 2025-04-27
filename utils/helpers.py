# utils/helpers.py

def greet_user(name: str) -> str:
    """
    Gibt einen Begrüßungstext für den angegebenen Namen zurück.
    """
    return f"Hallo {name}, willkommen in der traceability_app!"

def greet_user_extended(name: str, time_of_day: str) -> str:
    """
    Gibt eine Begrüßung basierend auf dem Tagesabschnitt zurück.
    """
    greetings = {
        "morning": "Guten Morgen",
        "afternoon": "Guten Tag",
        "evening": "Guten Abend",
        "night": "Gute Nacht"
    }
    greeting = greetings.get(time_of_day.lower(), "Hallo")
    return f"{greeting} {name}, willkommen in der traceability_app!"
