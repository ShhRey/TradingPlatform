from jwt import encode, decode
import datetime as dt


def validate_jwt(jwt_token):
    decoded_payload = decode(jwt_token, "d0a7eef09820f71d9c14", algorithms=["HS256"])
    current_date = dt.datetime.now()
    jwt_date = dt.datetime.strptime(decoded_payload.get('Time'), "%d/%m/%Y %H:%M:%S")
    jwt_expiry = 60*60*2
    if (current_date-jwt_date).seconds > jwt_expiry:
        raise Exception('Session Expired! Kindly Login Again')
    return decoded_payload


def generate_user_token(userid, email):
    payload = {'UserID': userid, 'Email': email}
    payload['Time'] = dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    jwt_token = encode(payload, "d0a7eef09820f71d9c14", algorithm="HS256")
    return jwt_token


