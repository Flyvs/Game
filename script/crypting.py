from cryptography.fernet import Fernet

class Crypting():
    # encrypting file
    def encrypt(path: str):
        if not path.endswith("\\"):
            path = path + "\\"

        key = Fernet.generate_key()

        with open(path + "filekey.key", "wb") as filekey:
            filekey.write(key)
        filekey.close()

        with open (path + "filekey.key", "rb") as filekey:
            key = filekey.read()
        filekey.close()

        fernet = Fernet(key)

        with open(path + "data.json", "rb") as file:
            original = file.read()
        file.close()

        encrypted = fernet.encrypt(original)

        with open(path + "data.json", "wb") as encrypted_file:
            encrypted_file.write(encrypted)
        encrypted_file.close()
    
    # decypting file
    def decrypt(path: str):
        if not path.endswith("\\"):
            path = path + "\\"

        with open(path + "filekey.key") as keyfile:
            key = keyfile.read()

        fernet = Fernet(key)

        with open(path + "data.json", "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(path + "data.json", "wb") as dec_file:
            dec_file.write(decrypted)