import datetime
import os
import random
import re

from twitter import OAuth, Twitter

EPOCH = 736925  # LOONA's birthday

auth = OAuth(
    os.environ["TWITTER_ACCESSTOKEN"],
    os.environ["TWITTER_ACCESSSECRET"],
    os.environ["TWITTER_CONSUMERKEY"],
    os.environ["TWITTER_CONSUMERSECRET"],
)
t = Twitter(auth=auth)


def get_loonaday(date: datetime.date = None):
    if date is None:
        date = datetime.date.today()
    return date.toordinal() - EPOCH


def get_byte(path, edit_file=True):
    today = get_loonaday()
    with open(path, "r+b") as f:
        stream = bytearray(f.read())
        byte = stream.pop(0)
        if today % 2 and edit_file:
            f.seek(0)
            f.write(stream)
            f.truncate(len(stream))
        return byte


def get_key(seed=None):
    if seed is None:
        seed = get_loonaday()
    random.seed(seed)
    return random.getrandbits(4)


class Nibble(int):
    _map = "🌕🐰🐱🕊🐸🌗🦌🦉🐟🦇🌚🦢🐧🦋🐺🌓"

    def __new__(cls, n: int):
        if n >= 16:
            raise ValueError("Must be less than 16")
        return super(Nibble, cls).__new__(cls, n)

    def cypher(self, key: int = None):
        if key is None:
            key = get_key()
        return Nibble(self ^ key)

    def __repr__(self):
        return f"Nibble({int(self)})"

    def __str__(self):
        return Nibble._map[self]


def get_nibble(byte: int):
    if get_loonaday() % 2:
        return Nibble(byte >> 4)
    else:
        return Nibble(byte & 0x0F)


def main():
    handle = t.account.verify_credentials()["name"]
    byte = get_byte(os.getenv("CYPHERSTREAM_PATH"))
    nibble = get_nibble(byte).cypher()
    new_handle = re.sub(
        r"^(loona the trends) .",
        r"\1 {}".format(nibble),
        handle,
    )
    t.account.update_profile(name=new_handle)


if __name__ == "__main__":
    main()
