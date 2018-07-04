import base64
import datetime
import hashlib
import random
import string

import Crypto.Random
import M2Crypto.EVP
from Crypto.PublicKey import RSA
from dateutil import relativedelta

SALTLEN = 8
KEYLEN = 32
IVLEN = 16
ITERATIONS = 10000
ENCRYPT = 1
DECRYPT = 0
RSA_KEY_LEN = 2048


def util_encrypt(text, password):
    text = text.encode()
    password = password.encode()
    salt = Crypto.Random.get_random_bytes(SALTLEN)
    dk = hashlib.pbkdf2_hmac("md5", password, salt, ITERATIONS, IVLEN + KEYLEN)
    key = dk[:KEYLEN]
    iv = dk[KEYLEN:]
    cipher = M2Crypto.EVP.Cipher('aes_256_cfb', key, iv, ENCRYPT)
    encrypted = cipher.update(text) + cipher.final()
    return base64.b64encode(salt + iv + encrypted).decode()


def util_generate_key_pair():
    key_pair = RSA.generate(RSA_KEY_LEN)
    private_key = key_pair.export_key("PEM")
    public_key = key_pair.publickey().export_key()
    return public_key.decode(), private_key.decode()


def user_util_generate_file_encryption_key(password):
    def random_string(length=32):
        return ''.join(random.choice(string.ascii_letters) for m in range(length))

    key = random_string(32)
    encrypted_key = util_encrypt(key, password)
    return encrypted_key


def user_util_generate_encrypted_key_pair(password):
    public_key, private_key = util_generate_key_pair()
    encrypted_private_key = util_encrypt(private_key, password)
    return public_key, encrypted_private_key


def last_updated_calculator(updated_at):
    nowtime = datetime.datetime.now()
    difference = relativedelta.relativedelta(nowtime, updated_at)
    if difference.years > 0:
        return '{} years ago'.format(difference.years)
    if difference.months > 0:
        return '{} months ago'.format(difference.months)
    if difference.weeks > 0:
        return '{} weeks ago'.format(difference.weeks)
    if difference.days > 0:
        return '{} days ago'.format(difference.days)
    if difference.hours > 0:
        return '{} hours ago'.format(difference.hours)
    if difference.minutes > 0:
        return '{} minutes ago'.format(difference.minutes)
    if difference.seconds > 0:
        return '{} seconds ago'.format(difference.seconds)
    else:
        return 'Just now'
