import string
import argparse

ACCEPTED_CHARS = set(string.ascii_uppercase)
ALPHABET_LENGTH = len(ACCEPTED_CHARS)
EXTRA_ASCII = 65 #min ASCII code of the alphabet


DEFAULT_KEY = "GRUPOALEX"





def encrypt(plaintext, key):
    key_length = len(key)
    key_as_int = [ord(i) - EXTRA_ASCII for i in key]
    plaintext_int = [ord(i) - EXTRA_ASCII for i in plaintext]
    ciphertext = ''

    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
        ciphertext += chr(value + EXTRA_ASCII)

    return ciphertext


def decrypt(ciphertext, key):

    key_length = len(key)
    key_as_int = [ord(i) - EXTRA_ASCII for i in key]
    ciphertext_int = [ord(i) - EXTRA_ASCII for i in ciphertext]
    plaintext = ''

    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        plaintext += chr(value + EXTRA_ASCII)

    return plaintext

def check_string(str_to_check):
        for ch in str_to_check:
            if ch not in ACCEPTED_CHARS:
                raise Exception('CHARACTER "' + ch + '" NOT IN ACCEPTED CHARS(' + ACCEPTED_CHARS + ")")

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="Text to be ciphered/deciphered")
    parser.add_argument("-d", "--decipher", help="decipher the input text", action="store_true")
    parser.add_argument("-k", "--key", help="key used to cipher/decipher input text, must be a text using this characters: " + str(ACCEPTED_CHARS))
    return parser.parse_args()

def main():

    args = get_arguments()

    check_string(args.text)

    if args.key:
        check_string(args.key)
        key = args.key
    else:
        key = DEFAULT_KEY

    if args.decipher:
        print(decrypt(args.text, key))
    else:
        print(encrypt(args.text, key))


if __name__ == '__main__':
    main()

