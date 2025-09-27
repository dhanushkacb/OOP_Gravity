class Validate:
    @staticmethod
    def validate_contact(new_value):
        if new_value == "":
            return True
        if new_value.isdigit() and len(new_value) <= 10:
            return True
        return False

    @staticmethod
    def validate_email(email):
        if email == "":
            return True
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None