import hashlib, re
from cryptography.fernet import Fernet

class HashEncryption:
    def __init__(self):
        self.correct_password = "TeamA21"
        self.password_hash = self.hashcrypt(self.correct_password)

    def hashcrypt(self, user_input):
        h = hashlib.new("SHA256")
        h.update(user_input.encode())
        return h.hexdigest()

    def check_password(self, user_input):
        input_hash = self.hashcrypt(user_input)
        return self.password_hash == input_hash
    
    def get_key(self):
        return Fernet.generate_key()
    
    def encrypt(self, keyInput: bytes, data: str) -> bytes:
        return Fernet(keyInput).encrypt(data.encode())
    
    def decrypt(self, keyInput: bytes, data: bytes) -> str:
        return Fernet(keyInput).decrypt(data).decode()
    
    def CheckPasswordStrength(self, password: str)-> str:
        pattern = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
        if len(password) >= 8 and re.search("[A-Z]",password)  and re.search("[0-9]",password) and (pattern.search(password) != None):
            return 'strong'
            # print("\nYOUR PASSWORD IS STRONG\n")
        elif len(password) >= 8 and (re.search("[A-Z]",password) or re.search("[0-9]",password) or (pattern.search(password) != None)):
            return 'medium'
            # print("\nYOUR PASSWORD IS MEDUIM STRENGTH\n")
        else: 
            return 'weak'
            # print("\nYOUR PASSWORD IS WEAK\n")
       
if __name__=="__main__":
    password = input("enter a password : ")
    print(HashEncryption().CheckPasswordStrength(password))
