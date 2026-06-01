# Mail module

class Classifier:
    def __init__(self):
        self.rules = {}
        self.make_rules()
        self.category_order = ["monitoring", "incident", "spam", "hr", "equipment", "request", "finance", "info"]
    def make_rules(self):
        self.rules["monitoring"] = ["мониторинг", "cpu usage", "disk usage", "healthcheck", "uptime"]
        self.rules["incident"]   = ["ошибка 500", "сбой", "не отвечает", "критический инцидент", "не могу войти"]
        self.rules["spam"]       = ["выиграли приз", "нажмите на ссылку", "подтвердите личность", "скидка 90%","аккаунт заблокирован", "аккаунт будет заблокирован", "перейдите по ссылке","верификация аккаунта", "победителем розыгрыша"]
        self.rules["hr"]         = ["отпуск", "больничн", "новый сотрудник", "рабочее место", "график работы"]
        self.rules["equipment"]  = ["ремонт", "не включается", "сломался", "замен", "оборудован"]
        self.rules["request"]    = ["доступ", "нужна помощь", "не работает", "запрос", "клиент"]
        self.rules["finance"]    = ["счёт", "счет", "оплат", "акт", "бухгалтер"]
        self.rules["info"]       = ["дайджест", "инструкц", "созвон", "демо", "техническое задание"]
    def choose_category(self, message):
        if message.error != '':
            return 'uncategorized'
        full_text = (message.subject.lower() + ' ' + message.body.lower())
        if len(full_text) < 5:
            return 'uncategorized'
        for category in self.category_order:
            words = self.rules.get(category, [])
            for word in words:
                if word in full_text:
                    return category
        return 'uncategorized'