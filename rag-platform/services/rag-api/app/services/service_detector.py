SERVICES = [
    "redis",
    "kafka",
    "terraform",
    "postgres"
]


def detect_service(question):

    q = question.lower()

    for service in SERVICES:

        if service in q:
            return service

    return None