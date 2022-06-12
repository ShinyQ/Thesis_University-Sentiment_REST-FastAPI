def builder(data, code):
    message = "Success"

    if not code:
        code = 200
    elif code == 500 or code == 400:
        message = "Error"
    elif code == 404:
        message = "Not Found"
    elif code == 405:
        message = "Method Not Allowed"

    return {'code': code, 'message': message, 'data': data}
