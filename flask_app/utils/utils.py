import typing
from flask import jsonify
from datetime import datetime, timezone


def create_response(status = 200, *args: typing.Any, **kwargs: typing.Any):
    response = {
        "time": datetime.now(timezone.utc).isoformat(),
        "status": status
    }
    if len(kwargs) > 0:
        response.update(kwargs)
    return jsonify(response)