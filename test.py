import toga

class TestApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(self.name)
        box1 = toga.Box()

        box2 = toga.Box()

        input = toga.NumberInput()
        # input = toga.TextInput()

        box2.add(input)
        box1.add(box2)

        self.main_window.content = box1
        self.main_window.show()

if __name__ == '__main__':
    TestApp("test", "org.pybee.test").main_loop()