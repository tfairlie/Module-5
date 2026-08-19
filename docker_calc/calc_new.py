class calculator:
    def __init__(self, a,b):
        self.a =a
        self.b =b

    def get_sum(self):
        return self.a + self.b
        
    def get_diff(self):
        return self.a - self.b
        
    def get_prod(self):
        return self.a * self.b
        
    def get_div(self):
        return self.a / self.b
        
if __name__ == "__main__":
    myCalc = calculator(a=245, b=12)
    print(myCalc.get_div())