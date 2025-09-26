import hashlib
class Security:

    @staticmethod
    def hash(text):        
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def verify(text, hash_value):
        return Security.hash(text) == hash_value