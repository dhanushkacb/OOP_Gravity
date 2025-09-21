class Security:

    @staticmethod
    def hash(text):
        import hashlib
        return hashlib.sha256(text.encode()).hexdigest()
    
    @staticmethod
    def verify(text, hash_value):
        return Security.hash(text) == hash_value