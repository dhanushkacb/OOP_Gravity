from Src.db.Schema import Students

class DiscountHandler:
    def __init__(self):
        self.students = Students()

    def calculate_discount(self, student_id, class_fee):
        student = self.students.select_by_id(student_id)
        if not student:
            return 0.00

        discount_percent = float(student.get("discount_percent", 0.0) or 0.0)
        discount_value = round((class_fee * discount_percent) / 100, 2)
        return discount_value
