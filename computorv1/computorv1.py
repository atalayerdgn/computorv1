import sys
import re
import math

class ComputorV1:
    def __init__(self, value):
        self.before_arr = dict()
        self.after_arr = dict()
        self.value = str(value)
        self.power = 0
        self.a = 0
        self.b = 0
        self.c = 0
    
    def parse_terms(self, side: str) -> dict:
        terms = {}
        parts = self.value.split('=') if side == 'before' else self.value.split('=')[1:]
        newstr = parts[0].split(' ')

        term = ""
        for i in range(len(newstr)):
            if re.match(r'X\^\d+', newstr[i]):
                power = re.match(r'X\^(\d+)', newstr[i]).group(1)
                if int(power) > self.power:
                    self.power = int(power)
                if term == '':
                    terms[f'X^{power}'] = '1'
                else:
                    terms[f'X^{power}'] = term
                term = ""
            elif newstr[i] in ['+', '-']:
                if term:
                    terms[f'X^{self.power}'] = term
                term = newstr[i]
            elif re.match(r'\d+', newstr[i]):
                if term:
                    term += newstr[i]
                else:
                    term = newstr[i]
        
        if term:
            terms[f'X^{self.power}'] = term
        
        return terms

    def parse_before(self) -> None:
        self.before_arr = self.parse_terms('before')
    
    def parse_after(self) -> None:
        self.after_arr = self.parse_terms('after')

    def reduce(self):
        for key in self.before_arr:
            if key in self.after_arr:
                self.after_arr[key] = str(int(self.before_arr[key]) - int(self.after_arr[key]))
            else:
                self.after_arr[key] = self.before_arr[key]
        print("Reduced form:",dict((k,v) for v,k in self.after_arr.items()) , flush=True, file=sys.stdout)

    def discriminant(self):
        if self.power > 2:
            print(f"Polynomial degree: {self.power}")
            print("The polynomial degree is strictly greater than 2, I can't solve.")
            return
        self.a = float(self.after_arr.get('X^2', 0))
        self.b = float(self.after_arr.get('X^1', 0))
        self.c = float(self.after_arr.get('X^0', 0))
        if self.a == 0:
            print(f"Polynomial degree: {self.power}")
            print(f"The solution is:")
            print(-self.c / self.b)
            return
        discriminant = pow(self.b, 2) - (4 * self.a * self.c)
        print(f"Polynomial degree: {self.power}")
        print("Discriminant:", discriminant)
        if discriminant > 0 :
            print("Discriminant is strictly positive, the two solutions are:")
            print("{:.6f}".format((-self.b - math.sqrt(discriminant)) / (2 * self.a)))
            print("{:.6f}".format((-self.b + math.sqrt(discriminant)) / (2 * self.a)))
        elif discriminant == 0:
            print("Discriminant is zero, the solution is:")
            print(-self.b / (2 * self.a))
        else:
            print("Discriminant is strictly negative, no real solutions.")

def main():
    input_str = " ".join(sys.argv[1:])
    val = ComputorV1(input_str)
    val.parse_before()
    val.parse_after()
    val.reduce()
    val.discriminant()

if __name__ == '__main__':
    main()
