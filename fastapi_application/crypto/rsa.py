import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization,  hashes

from cryptography.hazmat.primitives.asymmetric import padding


def create_keys(key_size: int = 2048) -> tuple[str, str]:
    private_key = rsa.generate_private_key(65537, key_size)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem.decode(), public_pem.decode()


def encrypt(text: str, public_pem: str) -> str:
    public_key = serialization.load_pem_public_key(
        public_pem.encode(),
    )
    ciphertext = public_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt(encoded_text: str, private_pem: str) -> str:
    private_key = serialization.load_pem_private_key(
        private_pem.encode(),
        password=None,
    )

    ciphertext_bytes = base64.b64decode(encoded_text)
    plaintext = private_key.decrypt(
        ciphertext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()
