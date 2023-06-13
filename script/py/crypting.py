from cryptography.fernet import Fernet

class Crypting():
    def encrypt(path: str,
                fileToEncrypt: str,
                filekeyName: str):
        """
        encrypts the given file and creates a key with the given name
        """
        if not path.endswith("\\"):
            path = path + "\\"

        key = Fernet.generate_key()

        with open(path + filekeyName, "wb") as filekey:
            filekey.write(key)

        with open(path + filekeyName, "rb") as filekey:
            key = filekey.read()

        fernet = Fernet(key)

        with open(path + fileToEncrypt, "rb") as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(path + fileToEncrypt, "wb") as encrypted_file:
            encrypted_file.write(encrypted)

    # decrypting file
    def decrypt(path: str, fileToDecrypt: str, filekeyName: str):
        """
        decrypts the given file and uses the given key(file)
        """
        if not path.endswith("\\"):
            path = path + "\\"

        with open(path + filekeyName) as keyfile:
            key = keyfile.read()

        fernet = Fernet(key)

        with open(path + fileToDecrypt, "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(path + fileToDecrypt, "wb") as dec_file:
            dec_file.write(decrypted)
