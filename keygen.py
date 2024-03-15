from Crypto.PublicKey import RSA
import os

"""
TODO: add checks to see if keys exist, create more robust key managment
"""
def gen_rsa(size : int=4096, location : str='.keychain/') -> None:
    print('Generating keys - this may take a couple seconds...')
    key = RSA.generate(4096)

    with open(location + 'rsa-publ-key.pem', 'w') as publ_key:
        publ_key.write(key.publickey().exportKey(format='PEM').decode('utf-8'))

    with open(location + 'rsa-priv-key.pem', 'w') as priv_key:
        priv_key.write(key.exportKey(format='PEM').decode('utf-8'))

    path = os.getcwd() + '/' + location
    print('Keys can be found at {}'.format(path))

if __name__ == '__main__':
    gen_rsa()
