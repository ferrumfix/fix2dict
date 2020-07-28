import datetime


def iso8601_utc():
    # <https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset>
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
