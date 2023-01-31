class a:
    def __init__(self, b, c):
        print(b + c)

class b(a):
    def __init__(self, c, d):
        super().__init__(c, d)

b(2, 5)
