class test:
    def __init__(self):
        self.hello = 1

    def test(self):
        print dir(self)


a = test()
a.test()
a.hello
