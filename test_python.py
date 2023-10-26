class R:
    def __init__(self, r_attribute):
        self.r_attribute = r_attribute

class A(R):
    def __init__(self, r_attribute):
        super().__init__(r_attribute)

    def use_method_from_B(self):
        # Создайте экземпляр класса B
        b_instance = B(self.r_attribute)  # Передайте нужные атрибуты

        # Вызовите метод класса B
        result = b_instance.method_from_B()

        # Используйте результат
        print(result)

class B(R):
    def __init__(self, r_attribute):
        super().__init__(r_attribute)

    def method_from_B(self):
        # Выполняйте операции с атрибутами класса R
        print(self.r_attribute, type(self.r_attribute))
        return f"Method from B: {self.r_attribute}"

# Пример использования
b_instance = B(1111111)
a_instance = A(b_instance.r_attribute)

a_instance.use_method_from_B()