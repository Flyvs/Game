from cryptography.fernet import Fernet

class Crypting():
    def encrypt():
        key = Fernet.generate_key()

        with open("F:\\programming\\PYprojects\idkGame4\\filekey.key", "wb") as filekey:
            filekey.write(key)
        filekey.close()

        with open ("F:\\programming\\PYprojects\idkGame4\\filekey.key", "rb") as filekey:
            key = filekey.read()
        filekey.close()

        fernet = Fernet(key)

        with open("F:\\programming\\PYprojects\\idkGame4\\script\\data.json", "rb") as file:
            original = file.read()
        file.close()

        encrypted = fernet.encrypt(original)

        with open("F:\\programming\\PYprojects\\idkGame4\\script\\data.json", "wb") as encrypted_file:
            encrypted_file.write(encrypted)
        encrypted_file.close()

        return fernet
    

    def decrypt(fernet: Fernet):

        with open("F:\\programming\\PYprojects\\idkGame4\\script\\data.json", "rb") as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open("F:\\programming\\PYprojects\\idkGame4\\script\\data.json", "wb") as dec_file:
            dec_file.write(decrypted)

Crypting.encrypt()
