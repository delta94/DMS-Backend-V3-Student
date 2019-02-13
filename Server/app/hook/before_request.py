from datetime import timedelta, datetime
from dateutil.parser import parse
from hashlib import sha3_512
from base64 import b64encode

from flask import request, abort


def check_secret_header():
    date = request.headers.get('X-Date')
    user_agent = request.headers.get('User-Agent')
    secret = request.headers.get('User-Data')

    if None in (date, user_agent, secret):
        abort(418)

    key = (user_agent + date).encode()
    h = sha3_512(b64encode(key)).hexdigest()
    request_date = parse(date)

    if not (request_date <= datetime.now() <= request_date + timedelta(seconds=10) and h == secret):
        abort(418)