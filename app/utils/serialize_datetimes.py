import datetime


def serialize_datetime(obj):
    if isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(v) for v in obj]
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    else:
        return obj
