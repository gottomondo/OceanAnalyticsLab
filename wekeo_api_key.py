import base64


def generate_api_key(username, password):
    """
    Generates a Base64-encoded api key, based on the WEkEO user
    credentials username:password.

    Parameters:
        username: WEkEO username
        password: WEkEO password

    Returns:
        Returns a string of the Base64-encoded api key
    """
    s = username + ':' + password
    return (base64.b64encode(str.encode(s), altchars=None)).decode()


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        raise Exception("Pass as arguments username and password of WEkEO")
    print("Your WEkEO api key is:")
    print(generate_api_key(sys.argv[1], sys.argv[2]))
