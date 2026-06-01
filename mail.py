# Mail module

class Classifier:
    def __init__(self):
        self.rules = {}
        self.make_rules()
        self.category_order = ["monitoring", "incident", "spam", "hr", "equipment", "request", "finance", "info"]