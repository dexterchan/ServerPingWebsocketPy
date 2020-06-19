from datetime import datetime, timedelta, timezone


# Load a RSA key from a JWK dict. (hardcode for testing)
with open('/Users/dexter/.ssh/aws_humble_pig', 'rb') as fh:
    signing_key = (fh.read())


def encodeKey(submessage, orgURL ):

    compact_jws = "abcd"

    return compact_jws