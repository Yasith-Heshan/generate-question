import random
from fractions import Fraction
import sympy as sp
import re

# returns random nubmer between a and b (may be integer or float)
# c = number of decimal places for float
def generate_random_number(a,b,c):
    if random.choice([True, False]):
        return random.randint(a, b) 
    else:
        return round(random.uniform(float(a), float(b)),c)

def generate_random_proper_fraction(a, b):
    while True:
        numerator = random.randint(1, 9)
        denominator = random.randint(numerator + 1, 10)
        fraction = Fraction(numerator, denominator)
        if a < fraction < b:
            return fraction

def generate_random_improper_fraction(a, b):
    while True:
        denominator = random.randint(1, 9)
        numerator = random.randint(denominator + 1, 10)
        fraction = Fraction(numerator, denominator)
        if a < fraction < b:
            return fraction
        
def generate_non_integer_number(a, b,decimal_points):
    if random.choice([True, False]):
        return random.randint(a, b)
    elif random.choice([True, False]):
        return round(random.uniform(float(a), float(b)),decimal_points)
    else:
        return generate_random_proper_fraction(a, b)
    
def generate_fraction(a, b):
    if random.choice([True, False]):
        return generate_random_proper_fraction(a, b)
    else:
        return generate_random_improper_fraction(a, b)
    
def float_to_fraction(float_value, max_value=10, decimal_points=2):
    # Convert to fraction and limit denominator
    fraction_value = Fraction(float_value).limit_denominator(max_value)
    
    # Check if both numerator and denominator are within the desired range
    print(float_value,fraction_value.numerator,fraction_value.denominator,max_value)
    print(abs(fraction_value.numerator) < max_value, abs(fraction_value.denominator) < max_value)
    if (abs(fraction_value.numerator) < max_value) and (abs(fraction_value.denominator) < max_value):
        return fraction_value
    else:
        # Return rounded float if the condition is not met
        return round(float_value, decimal_points)
    
def simplify_equation(equation):
    """Simplify the equation of the line using sympy."""
    x, y, slope = sp.symbols('x y slope')
    # Convert the string equation to a sympy expression

    equation = equation.replace('- -', '+').replace('- +', '-').replace('+ -', '-').replace(' 1(', '(').replace('- 0', '').replace('-1x', '-x').replace('-1y', '-y').replace(' 1y', ' y').replace(' 1x', ' x').replace(' + 0', '')    # Adjust to match sympy format

    try:
        expr = sp.sympify(equation)
        simplified_expr = sp.simplify(expr)
        return str(simplified_expr)
    except Exception as e:

        
        return equation
    
def simplify_sqrt(n: int) -> str:
    """Simplify the square root of a number."""
    if n < 0:
        raise ValueError("Cannot compute the square root of a negative number")

    # Find the largest square factor of n
    largest_square_factor = 1
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % (i * i) == 0:
            largest_square_factor = i * i

    # Simplify
    sqrt_part = int(math.sqrt(largest_square_factor))
    remaining_part = n // largest_square_factor

    if remaining_part == 1:
        return f"{sqrt_part}"
    elif sqrt_part == 1:
        return f"√{remaining_part}"
    else:
        return f"{sqrt_part}√{remaining_part}"

def generate_integer_or_fraction(a, b):
    if random.choice([True, False]):
        return random.randint(a, b)
    else:
        return generate_fraction(a,b)

def generate_integer_or_fraction(a, b):
    if random.choice([True, False]):
        return random.randint(a, b)
    else:
        return generate_fraction(a,b)

def generate_general_constant_number(a,b):
    choice = random.choice(["integer", "integer_fraction", "other_fraction"])
    if choice == "integer":
        return random.choice([i for i in range(a,b) if i != 0])
    elif choice == "integer_fraction":
        return generate_fraction(a, b)
    else:
        a = random.choice([i for i in range(a,b) if i != 0])
        b = random.choice([i for i in range(a,b) if i != 0])
        c = random.choice([a,-sp.sqrt(sp.Abs(a)) if a<0 else sp.sqrt(a)])
        d = random.choice([b,-sp.sqrt(sp.Abs(b)) if b<0 else sp.sqrt(b)])
        if c==a and d==b:
            if a>0:
                return sp.simplify(sp.sqrt(sp.Abs(a))/b)
            else:
                return -sp.simplify(sp.sqrt(sp.Abs(a))/b)
        return sp.simplify(c/d)

def generate_general_constant_without_sqrt(a,b):
    choice = random.choice(["integer", "integer_fraction"])
    if choice == "integer":
        return random.choice([i for i in range(a,b) if i != 0])
    else:
        return generate_fraction(a, b)
        
def random_non_zero_real(weights, numerator_and_denominator_limit=None, power=None):
    # Choose type of number: integer, fraction, square root, cube root
    choice = random.choices(
        ['integer', 'fraction', 'square_root', 'cube_root'],
        weights=weights,
        k=1
    )[0]

    if choice == 'integer':
        value = random.choice([random.randint(-20, -1), random.randint(1, 20)])

        return value

    elif choice == 'fraction':
        if numerator_and_denominator_limit is not None:
            bound_num = int(sp.floor(sp.real_root(numerator_and_denominator_limit, power)))
            numerator = random.choice([random.randint(-bound_num, -1), random.randint(1, bound_num)])
            denominator = random.randint(1, bound_num)
        else:
            numerator = random.choice([random.randint(-20, -1), random.randint(1, 20)])
            denominator = random.randint(1, 20)
        fraction = sp.Rational(numerator, denominator)
        return fraction

    elif choice == 'square_root':
        base = random.randint(2, 400)
        square_root = sp.sqrt(base, evaluate=False)
        return square_root if random.choice([True, False]) else -square_root

    elif choice == 'cube_root':
        base = random.choice([random.randint(-20, -1), random.randint(2, 20)])

        cube_root = sp.cbrt(base, evaluate=False)
        return cube_root

# Random integer generator excluding
def randint_exclude_list(low, high, exclude_list = [0]):
    while True:
        num = random.randint(low, high)
        if num not in exclude_list:
            return num
def generate_general_constant_number(a,b):
    choice = random.choice(["integer", "integer_fraction", "other_fraction"])
    if choice == "integer":
        return random.choice([i for i in range(a,b) if i != 0])
    elif choice == "integer_fraction":
        return generate_fraction(a, b)
    else:
        a = random.choice([i for i in range(a,b) if i != 0])
        b = random.choice([i for i in range(a,b) if i != 0])
        c = random.choice([a,-sp.sqrt(sp.Abs(a)) if a<0 else sp.sqrt(a)])
        d = random.choice([b,-sp.sqrt(sp.Abs(b)) if b<0 else sp.sqrt(b)])
        if c==a and d==b:
            if a>0:
                return sp.simplify(sp.sqrt(sp.Abs(a))/b)
            else:
                return -sp.simplify(sp.sqrt(sp.Abs(a))/b)
        return sp.simplify(c/d)

def generate_general_constant_without_sqrt(a,b):
    choice = random.choice(["integer", "integer_fraction"])
    if choice == "integer":
        return random.choice([i for i in range(a,b) if i != 0])
    else:
        return generate_fraction(a, b)

exp_hack = lambda e: e.replace(
    lambda x: x.is_Pow and x.exp.is_Rational and x.exp<0,
    lambda x: x.base**sp.Symbol(str(x.exp)))