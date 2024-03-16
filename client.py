import socket
import os

from typing import Final
from base64 import b64encode, b64decode

from dotenv import load_dotenv
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256, HMAC
from Crypto.Util import Padding

class Client:

    def __init__(self) -> None:
        self.sequence_no = Random.get_random_bytes(4)
        self.client_id = Random.get_random_bytes(2)

    def secret_exchange(self) -> str:
        """
        SCHEMA:
            payload = header + length + enc_secret + signature

            header = payload[:10] <= client_id + sequence_no
            length = int.from_bytes(header[6:10], byteorder='big')
            enc_secret = payload[10:length + 4] # 4 is the extra byte
            signature = payload[length + 4:]

        """
        header : bytes = self.client_id + self.sequence_no
        enc_secret : bytes = publ_key_encr(new_symmetric_key(), import_key())
        length : bytes = len(header + enc_secret).to_bytes(4, byteorder='big')

        signature : bytes = sign_data(
                header + length + enc_secret, 
                import_key('.keychain/rsa-priv-key.pem')
        )
        
        payload = header + length + enc_secret + signature
        return payload 

def connect(host_ip : str, port : int) -> None:
    try:
        with socket.create_connection((host_ip, port)) as tcp_service:
            while True:
                user_input = input('To quit, type QUIT\n')
                if user_input == 'QUIT':
                    break

                # add stuff here
                if user_input == 'START':
                    tcp_service.send(Client().secret_exchange())
                    response = tcp_service.recv(1024)
                    continue

                tcp_service.send(user_input.encode())
                response = tcp_service.recv(1024)
                print('Server@{}: {}'.format(host_ip, response.decode()))

    except KeyboardInterrupt:
        print('Shutting down.')

def import_key(path : str='.keychain/rsa-publ-key.pem'):
    """
        Ideally store passkeys and session keys, etc in some kind of
        password manager or session manager
    """
    with open(path, 'r') as key_file:
        return RSA.import_key(key_file.read())

def new_symmetric_key(key_size : int=256) -> bytes:
    return Random.get_random_bytes(key_size)

# should these go into the object?
def publ_key_encr(payload : str, publ_key : str) -> bytes:
    return PKCS1_OAEP.new(publ_key).encrypt(payload)

def sign_data(data : str, priv_key : str) -> bytes:
    hashed = SHA256.new(data)
    return PKCS1_PSS.new(priv_key).sign(hashed)

"""

if __name__ == '__main__':

"""
