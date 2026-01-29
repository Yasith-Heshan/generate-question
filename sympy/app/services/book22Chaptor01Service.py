import math
import random
from fractions import Fraction
import re
import sympy as sp
from sympy import oo
from app.models.dataModels import LatexStringModel, ServiceResponce, LatexObject, LatexConverter, DualInequalityParams
from app.services.base_quetion_generator_service import BaseQuestionGeneratorService
from app.utils.helpers import generate_integer_or_fraction

# from app.utils.helpers import  generate_fraction
from typing import List, Dict, Any,Tuple
from app.services.Book22Chaptor01.problem_type_22_E_1__2__27 import generate_problem_22_E_1__2_27_questions
from app.utils.helpers import float_to_fraction, generate_non_integer_number, generate_random_number, generate_random_proper_fraction, simplify_equation, simplify_sqrt, random_non_zero_real

# Random integer generator excluding zero
def randint_exclude_zero(low, high):
    while True:
        num = random.randint(low, high)
        if num != 0:
            return num

class RandomQuadraticExpression:
    def __init__(self, variable):
        self.variable = variable

    def generate_expression(self, max_power=2):
        coefficients = [random.randint(-10, 10) for _ in range(max_power + 1)]
        expression = sum(coeff * self.variable**power for power, coeff in enumerate(coefficients))
        return expression

    # This method only support for power 2 expressions only
    def generate_unfactorable_expression(self):
        a = randint_exclude_zero(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(1, 10)
        return sp.expand((a * self.variable + b)**2 + c)

    def generate_quadratic_expression_with_max_power_and_limited_terms(self, max_power=10, min_terms=3, max_terms=4):
        num_terms = random.randint(min_terms, max_terms) - 1
        power = random.randint(num_terms, max_power)
        terms = []
        for term_index in range(num_terms, -1, -1):
            coefficient = randint_exclude_zero(-10, 10)
            terms.append(coefficient * self.variable**power)
            power = random.randint(term_index-1, power - 1)
        return sp.Add(*terms)

class RandomFactoredExpression:
    def __init__(self, variable, max_power=2):
        self.variable = variable
        self.max_power = max_power

    def generate_factor(self):
        a = random.randint(1, 5)  # Coefficient of x
        b = random.randint(-5, 5)  # Constant term
        power = int(random.triangular(1, 2.5, 1)) # Generate factors with higher probability of 1
        return (a * self.variable + b) ** power

    def generate_factored_expression(self, min_factors=2, max_factors=4):
        if max_factors == 0:
            return random.randint(1, 10)
        num_factors = random.randint(min_factors, max_factors)  # Number of factors
        expression = 1
        for _ in range(num_factors):
            expression *= self.generate_factor()
        return expression

    def generate_expression_with_lower_coefficient(self, min_factors=2, max_factors=4):
        num_factors = random.randint(min_factors, max_factors)
        expression = 1
        if num_factors > 2:
            expression *= randint_exclude_zero(-3, 3) * (self.variable ** (num_factors - 2))
            num_factors = 2
        for _ in range(num_factors):
            expression *= self.generate_factor()
        return expression

    def generate_linear_expression(self):
        a = randint_exclude_zero(-5, 5)
        b = random.randint(-5, 5)
        return a * self.variable + b

    def generate_quadratic_expression(self):
        return self.generate_linear_expression() * self.generate_linear_expression()

class Book22Chaptor01Service(BaseQuestionGeneratorService):

    def generate_answers(self) -> list:
        pass

    def format_questions(self):
        pass

    # Question type: 22_E_1.1_09
    def generate_22_E_1__1_09_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:

        latex_converter = LatexConverter()
        x = sp.symbols('x')
        inequalities_and_solutions = []

        for _ in range(questions_count):

            if difficulty == 1:
                # ax + b <op> c
                a = randint_exclude_zero(-10, 10)
                b = randint_exclude_zero(-10, 10)
                c = randint_exclude_zero(-10, 10)
                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.StrictLessThan(a * x + b, c)
                elif op == '>':
                    inequality = sp.StrictGreaterThan(a * x + b, c)
                elif op == '<=':
                    inequality = sp.LessThan(a * x + b, c)
                elif op == '>=':
                    inequality = sp.GreaterThan(a * x + b, c)
                solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))
            elif difficulty == 2:
                # a <op1> bx + c <op2> d
                a = randint_exclude_zero(-10, 10)
                b = randint_exclude_zero(-10, 10)
                c = randint_exclude_zero(-10, 10)
                d = randint_exclude_zero(a + 1, a + 20)
                op1 = random.choice(['<', '<='])
                op2 = random.choice(['<', '<='])
                inequality = latex_converter.convert_double_inequality_in_latex(DualInequalityParams(a, op1, b * x + c, op2, d), True)
                inequality1 = (
                    sp.Lt(a, b * x + c) if op1 == '<' else
                    sp.Le(a, b * x + c)
                )
                inequality2 = (
                    sp.Lt(b * x + c, d) if op2 == '<' else
                    sp.Le(b * x + c, d)
                )
                solution1 = sp.solve_univariate_inequality(inequality1, x, relational=False)
                solution2 = sp.solve_univariate_inequality(inequality2, x, relational=False)
                solution = sp.Intersection(solution1, solution2)
            elif difficulty == 3:
                # (a/d)x + (b/e) <op> (c/f)
                a = randint_exclude_zero(-10, 10)
                b = randint_exclude_zero(-10, 10)
                c = randint_exclude_zero(-10, 10)
                d = random.randint(2,5)
                e = random.randint(2, 5)
                f = random.randint(2, 5)
                coefficient = Fraction(a,d)
                constant = Fraction(b, e)
                rhs = Fraction(c, f)
                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.Lt(coefficient * x + constant, rhs)
                elif op == '>':
                    inequality = sp.Gt(coefficient * x + constant, rhs)
                elif op == '<=':
                    inequality = sp.Le(coefficient * x + constant, rhs)
                elif op == '>=':
                    inequality = sp.Ge(coefficient * x + constant, rhs)
                solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))
            elif difficulty <= 5:
                # a/e <op1> (b/f)x + c/g <op2> d/h
                a = randint_exclude_zero(-10, 10)
                e = random.randint(2, 10)
                b = randint_exclude_zero(-10, 10)
                f = random.randint(1, 10)
                c = randint_exclude_zero(-10, 10)
                g = random.randint(1, 10)
                d = randint_exclude_zero(a+1, 15)
                h = random.randint(2, e+1)
                op1 = random.choice(['<', '<='])
                op2 = random.choice(['<', '<='])
                lhs = Fraction(a, e)
                rhs = Fraction(d, h)
                coefficient = Fraction(b, f)
                constant_fraction = Fraction(c, g)
                inequality = latex_converter.convert_double_inequality_in_latex(DualInequalityParams(lhs, op1, coefficient * x + constant_fraction, op2, rhs), True)
                inequality1 = (
                    sp.Lt(lhs, coefficient * x + constant_fraction) if op1 == '<' else
                    sp.Le(lhs, coefficient * x + constant_fraction)
                )
                inequality2 = (
                    sp.Lt(coefficient * x + constant_fraction, rhs) if op2 == '<' else
                    sp.Le(coefficient * x + constant_fraction, rhs)
                )
                solution1 = sp.solve_univariate_inequality(inequality1, x, relational=False)
                solution2 = sp.solve_univariate_inequality(inequality2, x, relational=False)
                solution = sp.Intersection(sp.Intersection(solution1, solution2))
            else:
                raise ValueError('Unsupported difficulty level')

            if difficulty == 2 or difficulty == 4 or difficulty == 5:
                latex_obj = LatexObject(inequality, True)
            else:
                latex_obj = LatexObject(inequality, False, True)

            inequalities_and_solutions.append(
                {
                    'question': LatexStringModel(
                        string_value="Solve the following inequality. {}",
                        placeholders=[latex_obj]
                        ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(solution, False, False)]
                    ).convert_to_latex()
                }
            )
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']), inequalities_and_solutions))
        return questions_and_answers

    # Question type: 22_E_1.1_47 by Yasith Heshan
    def generate_22_E_1__1_47_questions(self,
                                        difficulty: int,
                                        questions_count: int):

        # Define the variable
        x = sp.symbols('x')
        equations_and_solutions = []


        if difficulty == 1:
            def generate_equation_and_solution():
                a = random.choice([i for i in range(-10, 10) if i != 0])
                b = generate_integer_or_fraction(-10, 10)
                c = generate_integer_or_fraction(-10, 10)

                equation1 = a * x + b - c
                equation2 = a * x + b + c
                solutions1 = sp.solve(equation1, x)
                solutions2 = sp.solve(equation2, x)
                solutions = solutions1 + solutions2
                return a,b,c,solutions

            for _ in range(questions_count):
                a,b,c,solutions = generate_equation_and_solution()
                lhs = sp.Abs(a * x + b, evaluate=False)

                equations_and_solutions.append({
                    'equation': LatexStringModel(
                        string_value="Find all solutions for x: {}",
                        placeholders=[LatexObject(sp.Eq(lhs,c,evaluate=False), False, True)]
                    ).convert_to_latex(),
                    'solutions': [LatexStringModel(
                        placeholders=[LatexObject(sol, False, False)],
                        string_value="{}"
                    ).convert_to_latex() for sol in solutions]
                })

        elif difficulty == 2:
            def generate_equation_and_solution():
                while True:
                    # create a random variable a which either takes 1 or -1
                    a = random.choice([1, -1])
                    b = random.choice([1, -1])
                    c = random.randint(-10, 10)
                    d = random.randint(-10, 10)
                    solutions = []
                    # Case 1: a*x + c >= 0 and b*x + d >= 0
                    case1 = sp.solve((a * x + c) - (b * x + d), x)
                    solutions.extend(case1)

                    # Case 2: a*x + c >= 0 and b*x + d < 0
                    case2 = sp.solve((a * x + c) + (b * x + d), x)
                    solutions.extend(case2)

                    if (c!=d) and all(sol.is_real for sol in solutions):
                        break
                # solutions = list(set(solutions))
                return a,b,c,d,solutions

            for _ in range(questions_count):
                a,b,c,d,solutions = generate_equation_and_solution()
                lhs = sp.Abs(a * x + c,evaluate=False)
                rhs = sp.Abs(b * x + d,evaluate=False)
                equations_and_solutions.append({
                    'equation': LatexStringModel(
                        placeholders=[LatexObject(sp.Eq(lhs,rhs,evaluate=False), False, True)],
                        string_value="Find all solutions for x: {}"
                    ).convert_to_latex(),
                    'solutions': [LatexStringModel(
                        placeholders=[LatexObject(sol, False, False)],
                        string_value="{}"
                    ).convert_to_latex() for sol in solutions]
                })


        elif difficulty == 3:
            def generate_equation_and_solution():
                a = random.randint(-10, 10)
                b = random.randint(-10, 10)
                c = random.randint(-10, 10)
                d = random.randint(-10, 10)
                equation1 = (a * x + b) - (c * x + d)
                equation2 = (a * x + b) + (c * x + d)
                equation3 = -(a * x + b) - (c * x + d)
                equation4 = -(a * x + b) + (c * x + d)
                solutions1 = sp.solve(equation1, x)
                solutions2 = sp.solve(equation2, x)
                solutions3 = sp.solve(equation3, x)
                solutions4 = sp.solve(equation4, x)
                solutions = list(set(solutions1 + solutions2+ solutions3 + solutions4))
                return a,b,c,d,solutions

            for _ in range(questions_count):
                a,b,c,d,solutions = generate_equation_and_solution()
                lhs = sp.Abs(a*x+b,evaluate=False)
                rhs = sp.Abs(c*x+d,evaluate=False)
                equations_and_solutions.append({
                    'equation': LatexStringModel(
                        string_value="Find all solutions for x: {}",
                        placeholders=[LatexObject(sp.Eq(lhs,rhs,evaluate=False), False, True)]
                    ).convert_to_latex(),
                    'solutions': [LatexStringModel(
                        placeholders=[LatexObject(sol, False, False)],
                        string_value="{}"
                    ).convert_to_latex() for sol in solutions]
                })

        elif difficulty == 4:
            def generate_equation_and_solution():
                solution = []
                # t = |x + c|
                c = random.choice([i for i in range(-10, 10) if i != 0])
                t = random.choice([i for i in range(-10, 10) if i != 0])
                t_ = random.choice([i for i in range(-10, 10) if i != 0])
                
                # find the values of a and b for equation t**2-at+b=0
                if(t>0):
                    solution.extend(sp.solve(x+c-t, x)+ sp.solve(x+c+t, x))
                if(t_>0):
                    solution.extend(sp.solve(x+c-t_, x)+ sp.solve(x+c+t_, x))
                solution = list(set(solution))

                return c,t,t_,solution

            for _ in range(questions_count):
                c,t,t_,solutions = generate_equation_and_solution()
                d = sp.Abs(x+c,evaluate=False)
                a = -(t+t_)
                b = t*t_

                equation = sp.Eq(sp.Pow(d,2)+a*d+b,0,evaluate=False)
                equations_and_solutions.append({
                    'equation': LatexStringModel(
                        placeholders=[LatexObject(equation, False, True)],
                        string_value="Find all real solutions for x: {}"
                    ).convert_to_latex(),
                    'solutions': [LatexStringModel(
                        placeholders=[LatexObject(sol, False, False)],
                        string_value="{}"
                    ).convert_to_latex() for sol in solutions]
                })
            

        elif difficulty == 5:
            def generate_equation_and_solution():
                b=random.choice([i for i in range(-10, 10) if i != 0])
                case = random.choice([1, 2])
                # choose a random int m such that m**2 > 2*p**2
                if(case==1):
                    p = random.choice([i for i in range(-10, 10) if i != 0])
                    m = random.choice([i for i in range(1, 30) if i**2 > 2*p**2 and p%2==i%2])
                else:
                    # choose two random integers r and s such that r>s and r and s are prime numbers
                    r = random.choice([i for i in sp.primerange(1, 30)])
                    s = random.choice([i for i in sp.primerange(1, 30) if r!=i])
                    p=r**2+s**2
                    u = r**2-s**2
                    v = 2*r*s
                    m=sp.Abs(u+v)
                l=(p**2-m**2)/4
                d=b*p-l
                equation = sp.Eq(sp.Abs(x+b)**2,sp.Abs(p*x+d),evaluate=False)
                solutions = []
                solutions.extend(sp.solve(sp.Eq((x+b)**2,p*x+d), x))
                solutions.extend(sp.solve(sp.Eq((x+b)**2,-p*x-d), x))
                solutions = [sol for sol in solutions if sol.is_real]
                return equation,solutions     
                
                

            for _ in range(questions_count):
                equation,solutions = generate_equation_and_solution()

                equations_and_solutions.append({
                    'equation': LatexStringModel(
                        placeholders=[LatexObject(equation, False, True)],
                        string_value="Find all solutions for x: {}"
                    ).convert_to_latex(),
                    'solutions': [LatexStringModel(
                        placeholders=[LatexObject(sol, False, False)],
                        string_value="{}"
                    ).convert_to_latex() for sol in solutions]
                })

        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['equation'], correct_solution=x['solutions']), equations_and_solutions))
        return questions_and_answers

    # Question type: 22_E_1__1_59
    def generate_22_E_1__1_59_questions(self,
                                        difficulty: int,
                                        questions_count: int)->List[ServiceResponce]:
        # Define the variable
        latex_converter = LatexConverter()
        x = sp.symbols('x')
        inequalities_and_solutions = []

        for _ in range(questions_count):
            if difficulty == 1:
                # |x + b| <op> c

                # Function to generate a random inequality of the form |x + b| < c, |x + b| > c, |x + b| <= c, |x + b| >= c
                def generate_random_inequality():
                    b = randint_exclude_zero(-10, 10)
                    c = random.randint(1, 10)
                    inequality_type = random.choice(['<', '>', '<=', '>='])
                    return b, c, inequality_type

                # Function to solve the inequality |x + b| < c, |x + b| > c, |x + b| <= c, |x + b| >= c
                def solve_inequality(b, c, inequality_type):
                    if inequality_type == '<':
                        inequality1 = sp.Lt(x + b, c)
                        inequality2 = sp.Gt(x + b, -c)
                    elif inequality_type == '>':
                        inequality1 = sp.Gt(x + b, c)
                        inequality2 = sp.Lt(x + b, -c)
                    elif inequality_type == '<=':
                        inequality1 = sp.Le(x + b, c)
                        inequality2 = sp.Ge(x + b, -c)
                    elif inequality_type == '>=':
                        inequality1 = sp.Ge(x + b, c)
                        inequality2 = sp.Le(x + b, -c)

                    # For '<' and '<=', it's an AND condition (intersection)
                    # For '>' and '>=', it's an OR condition (union)
                    if inequality_type in ['<', '<=']:
                        solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                        solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                        # Intersection of both solutions
                        common_solution = sp.Intersection(solution1, solution2)
                    elif inequality_type in ['>', '>=']:
                        solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                        solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                        # Union of both solutions
                        common_solution = sp.Union(solution1, solution2)

                    return common_solution

                # Generate and solve a set of random inequalities
                def generate_and_solve_inequalities():
                    b, c, inequality_type = generate_random_inequality()
                    solution = solve_inequality(b, c, inequality_type)

                    if inequality_type == '<':
                        inequality = sp.Abs(x + b) < c
                    elif inequality_type == '>':
                        inequality = sp.Abs(x + b) > c
                    elif inequality_type == '<=':
                        inequality = sp.Abs(x + b) <= c
                    else:
                        inequality = sp.Abs(x + b) >= c

                    return inequality, solution

                inequality, solution = generate_and_solve_inequalities()

            elif difficulty == 2:
                # |ax + b| <op> c

                def generate_random_inequality():
                    a = random.randint(1, 10)
                    b = randint_exclude_zero(-10, 10)
                    c = random.randint(1, 20)
                    inequality_type = random.choice(['<', '>', '<=', '>='])
                    return a, b, c, inequality_type

                def solve_inequality(a, b, c, inequality_type):
                    if inequality_type == '<':
                        inequality1 = sp.Lt(a * x + b, c)
                        inequality2 = sp.Gt(a * x + b, -c)
                    elif inequality_type == '>':
                        inequality1 = sp.Gt(a * x + b, c)
                        inequality2 = sp.Lt(a * x + b, -c)
                    elif inequality_type == '<=':
                        inequality1 = sp.Le(a * x + b, c)
                        inequality2 = sp.Ge(a * x + b, -c)
                    elif inequality_type == '>=':
                        inequality1 = sp.Ge(a * x + b, c)
                        inequality2 = sp.Le(a * x + b, -c)

                    # For '<' and '<=', it's an AND condition (intersection)
                    # For '>' and '>=', it's an OR condition (union)
                    if inequality_type in ['<', '<=']:
                        solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                        solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                        # Intersection of both solutions
                        common_solution = sp.Intersection(solution1, solution2)
                    elif inequality_type in ['>', '>=']:
                        solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                        solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                        # Union of both solutions
                        common_solution = sp.Union(solution1, solution2)

                    return common_solution

                def generate_and_solve_inequalities():
                    a, b, c, inequality_type = generate_random_inequality()
                    solution = solve_inequality(a, b, c, inequality_type)

                    if inequality_type == '<':
                        inequality = sp.Abs(a * x + b) < c
                    elif inequality_type == '>':
                        inequality = sp.Abs(a * x + b) > c
                    elif inequality_type == '<=':
                        inequality = sp.Abs(a * x + b) <= c
                    else:
                        inequality = sp.Abs(a * x + b) >= c

                    return (inequality, solution)

                inequality, solution = generate_and_solve_inequalities()

            elif difficulty == 3:
                # |ax + b/d| <op> c/e
                def generate_random_inequality():
                    a = random.randint(1, 15)
                    b = randint_exclude_zero(-15, 15)
                    d = random.randint(1, 5)  # Keep denominator small to avoid complex fractions
                    c = randint_exclude_zero(-15, 15)
                    e = random.randint(1, 5)
                    inequality_type = random.choice(['<', '>', '<=', '>='])
                    return a, b, d, c, e, inequality_type

                def solve_inequality(a, b, d, c, e, inequality_type):
                    expr = a * x + sp.Rational(b, d)
                    rhs = sp.Rational(c, e)

                    if inequality_type == '<':
                        inequality1 = sp.Lt(expr, rhs)
                        inequality2 = sp.Gt(expr, -rhs)
                    elif inequality_type == '>':
                        inequality1 = sp.Gt(expr, rhs)
                        inequality2 = sp.Lt(expr, -rhs)
                    elif inequality_type == '<=':
                        inequality1 = sp.Le(expr, rhs)
                        inequality2 = sp.Ge(expr, -rhs)
                    elif inequality_type == '>=':
                        inequality1 = sp.Ge(expr, rhs)
                        inequality2 = sp.Le(expr, -rhs)

                    # For '<' and '<=', it's an AND condition (intersection)
                    # For '>' and '>=', it's an OR condition (union)
                    if inequality_type in ['<', '<=']:
                        solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                        solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                        # Intersection of both solutions
                        common_solution = sp.Intersection(solution1, solution2)
                    elif inequality_type in ['>', '>=']:
                        solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                        solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                        # Union of both solutions
                        common_solution = sp.Union(solution1, solution2)

                    return common_solution

                def generate_and_solve_inequalities():
                    a, b, d, c, e, inequality_type = generate_random_inequality()
                    solution = solve_inequality(a, b, d, c, e, inequality_type)
                    if inequality_type == '<':
                        inequality = sp.Abs(a * x + sp.Rational(b, d)) < sp.Rational(c, e)
                    elif inequality_type == '>':
                        inequality = sp.Abs(a * x + sp.Rational(b, d)) > sp.Rational(c, e)
                    elif inequality_type == '<=':
                        inequality = sp.Abs(a * x + sp.Rational(b, d)) <= sp.Rational(c, e)
                    else:
                        inequality = sp.Abs(a * x + sp.Rational(b, d)) >= sp.Rational(c, e)

                    return (inequality, solution)

                inequality, solution = generate_and_solve_inequalities()

            elif difficulty == 4:
                # a <op> | bx + c/d | <op> e
                def generate_random_inequality():
                    a = random.randint(0, 15)
                    b = randint_exclude_zero(-15, 15)
                    c = randint_exclude_zero(-15, 15)
                    d = random.randint(2, 5)  # Keep denominator small to avoid complex fractions
                    while c%d == 0:
                        d = random.randint(1, 9)
                    e = random.randint(a + 1, 20)
                    inequality_type1 = random.choice(['<', '<='])
                    if inequality_type1 == '<=':
                        inequality_type2 = '<'
                    else:
                        inequality_type2 = random.choice(['<', '<='])
                    return a, b, c, d, e, inequality_type1, inequality_type2

                def solve_inequality(a, b, c, d, e, inequality_type1, inequality_type2):
                    expr = b * x + sp.Rational(c, d)
                    lhs = a
                    rhs = e

                    if inequality_type1 == '<':
                        inequality1 = sp.Gt(expr, lhs)
                        inequality2 = sp.Lt(expr, -lhs)
                    elif inequality_type1 == '<=':
                        inequality1 = sp.Ge(expr, lhs)
                        inequality2 = sp.Le(expr, -lhs)

                    if inequality_type2 == '<':
                        inequality3 = sp.Lt(expr, rhs)
                        inequality4 = sp.Gt(expr, -rhs)
                    elif inequality_type2 == '<=':
                        inequality3 = sp.Le(expr, rhs)
                        inequality4 = sp.Ge(expr, -rhs)

                    # OR condition (union)
                    solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                    solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                    common_solution_1 = sp.Union(solution1, solution2)
                    # AND condition (intersection)
                    solution3 = sp.solveset(inequality3, x, domain=sp.S.Reals)
                    solution4 = sp.solveset(inequality4, x, domain=sp.S.Reals)
                    common_solution_2 = sp.Intersection(solution3, solution4)

                    # Union of both solutions
                    common_solution = sp.Intersection(common_solution_1, common_solution_2)

                    return common_solution

                def generate_and_solve_inequalities():
                    a, b, c, d, e, inequality_type1, inequality_type2 = generate_random_inequality()
                    solution = solve_inequality(a, b, c, d, e, inequality_type1, inequality_type2)

                    # inequality = f"{a} {inequality_type1} |{b if abs(b)!=1 else ''}x {'+' if c >= 0 else '-'} {Fraction(abs(c), d)}| {inequality_type2} {e}"
                    inequality = latex_converter.convert_double_inequality_in_latex(DualInequalityParams(a, inequality_type1, sp.Abs(b * x + sp.Rational(c, d)), inequality_type2, e), True)
                    return (inequality, solution)

                inequality, solution = generate_and_solve_inequalities()

            elif difficulty == 5:
                # a/f <op> | bx + c/d | <op> e/g with non-zero b
                def generate_random_inequality():
                    a = random.randint(1, 15)
                    b = randint_exclude_zero(-15, 15)
                    c = randint_exclude_zero(-15, 15)
                    d = random.randint(2, 5)
                    e = random.randint(a, 15)
                    f = random.randint(2, 5)
                    g = random.randint(2, f)

                    inequality_type1 = random.choice(['<', '<='])
                    if inequality_type1 == '<=':
                        inequality_type2 = '<'
                    else:
                        inequality_type2 = random.choice(['<', '<='])
                    return a, b, c, d, e, f, g, inequality_type1, inequality_type2

                def solve_inequality(a, b, c, d, e, f, g, inequality_type1, inequality_type2):
                    expr = b * x + sp.Rational(c, d)
                    lhs = sp.Rational(a, f)
                    rhs = sp.Rational(e, g)

                    if inequality_type1 == '<':
                        inequality1 = sp.Gt(expr, lhs)
                        inequality2 = sp.Lt(expr, -lhs)
                    elif inequality_type1 == '<=':
                        inequality1 = sp.Ge(expr, lhs)
                        inequality2 = sp.Le(expr, -lhs)

                    if inequality_type2 == '<':
                        inequality3 = sp.Lt(expr, rhs)
                        inequality4 = sp.Gt(expr, -rhs)
                    elif inequality_type2 == '<=':
                        inequality3 = sp.Le(expr, rhs)
                        inequality4 = sp.Ge(expr, -rhs)

                    # OR condition (union)
                    solution1 = sp.solveset(inequality1, x, domain=sp.S.Reals)
                    solution2 = sp.solveset(inequality2, x, domain=sp.S.Reals)
                    common_solution_1 = sp.Union(solution1, solution2)
                    # AND condition (intersection)
                    solution3 = sp.solveset(inequality3, x, domain=sp.S.Reals)
                    solution4 = sp.solveset(inequality4, x, domain=sp.S.Reals)
                    common_solution_2 = sp.Intersection(solution3, solution4)

                    # Union of both solutions
                    common_solution = sp.Intersection(common_solution_1, common_solution_2)

                    return common_solution

                def generate_and_solve_inequalities():
                    a, b, c, d, e, f, g, inequality_type1, inequality_type2 = generate_random_inequality()
                    solution = solve_inequality(a, b, c, d, e, f, g, inequality_type1, inequality_type2)

                    inequality = latex_converter.convert_double_inequality_in_latex(DualInequalityParams(Fraction(a, f), inequality_type1, sp.Abs(b * x + sp.Rational(c, d)), inequality_type2, Fraction(e, g)), True)

                    return (inequality, solution)

                inequality, solution = generate_and_solve_inequalities()
            else:
                raise ValueError('Unsupported difficulty level')

            if difficulty == 4 or difficulty == 5:
                latex_obj = LatexObject(inequality, True)
            else:
                latex_obj = LatexObject(inequality, False, True)

            inequalities_and_solutions.append(
                {
                    'question': LatexStringModel(
                        string_value="Solve the following inequality. {}",
                        placeholders=[latex_obj]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(solution, False, False)]
                    ).convert_to_latex()
                }
            )
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']), inequalities_and_solutions))

        return questions_and_answers

    # Question type: 22_E_1__2_37
    def generate_22_E_1__2_37_questions(
            self,
            difficulty: int,
            questions_count: int):

        global user_line_eq, user_point, parallel_line_equation
        output = []

        # Define variables
        x, y = sp.symbols('x y')

        def find_parallel_line(m, x1, y1):
            constant_term = -m * x1 + y1
            return sp.Eq(y, m * x + constant_term)

        for _ in range(questions_count):
            if difficulty == 1:
                m_num = randint_exclude_zero(-10, 10)  # slope(numerator) of the given line
                m_den = randint_exclude_zero(2, 10)  # slope(denominator) of the given line
                c = randint_exclude_zero(-10, 10)  # y-intercept of the given line
                x1 = randint_exclude_zero(-10, 10)  # x-coordinate of point P
                y1 = randint_exclude_zero(-10, 10)  # y-coordinate of point P

                if random.randint(0,1) == 1:
                    m = m_num
                else:
                    m = Fraction(m_num, m_den)

                user_line_eq = sp.Eq(y, m * x + c)
                user_point = sp.Point(x1, y1)
                parallel_line_equation = find_parallel_line(m, x1, y1)
            elif difficulty == 2:
                selected_axis = random.choice(["x", "y"])
                c = randint_exclude_zero(-10, 10)
                if selected_axis == "x":
                    user_line_eq = sp.Eq(x, c)
                else:
                    user_line_eq = sp.Eq(y, c)
                x1 = randint_exclude_zero(-10, 10)  # x-coordinate of point P
                y1 = randint_exclude_zero(-10, 10)  # y-coordinate of point P
                user_point = sp.Point(x1, y1)

                if selected_axis == "x":
                    while x1 == c:
                        x1 = randint_exclude_zero(-10, 10)
                    parallel_line_equation = sp.Eq(x, x1)
                else:
                    while y1 == c:
                        y1 = randint_exclude_zero(-10, 10)
                    parallel_line_equation = sp.Eq(y, y1)
            elif difficulty == 3:
                #  l: ax + by = c
                a = randint_exclude_zero(-10, 10)
                b = randint_exclude_zero(-10, 10)
                c = randint_exclude_zero(-10, 10)
                x1 = randint_exclude_zero(-10, 10)  # x-coordinate of point P
                y1 = randint_exclude_zero(-10, 10) # y-coordinate of point P

                user_line_eq = sp.Eq(a * x + b * y, c)
                user_point = sp.Point(x1, y1)
                m = -Fraction(a, b)
                parallel_line_equation = find_parallel_line(m, x1, y1)
            elif difficulty == 4 or difficulty == 5:
                # l: a(x+d) + b(y + e) = c
                a = randint_exclude_zero(-10, 10)
                b = randint_exclude_zero(-10, 10)
                c = randint_exclude_zero(-10, 10)
                d = randint_exclude_zero(-10, 10)
                e = randint_exclude_zero(-10, 10)
                x1 = randint_exclude_zero(-10, 10)  # x-coordinate of point P
                y1 = randint_exclude_zero(-10, 10) # y-coordinate of point P
                user_line_eq = f"${a}(x{'+' if d >= 0 else ''}{d}) {'-' if b < 0 else '+'} {abs(b)}(y{'+' if e >= 0 else ''}{e}) = {c}$"
                user_point = sp.Point(x1, y1)
                m = -Fraction(a, b)
                parallel_line_equation = find_parallel_line(m, x1, y1)
                pass
            else:
                raise ValueError("Unsupported difficulty level")

            if difficulty >= 4:
                user_line_eq = LatexObject(user_line_eq, True)
            else:
                user_line_eq = LatexObject(user_line_eq, False, False)

            question_string = "Find the equation of the line parallel to the line " + "{}" + f" and passing through the point $({user_point.x}, {user_point.y})$."
            output.append(
                {
                    'question': LatexStringModel(
                        string_value=question_string,
                        placeholders=[user_line_eq]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(parallel_line_equation, False, False)]
                    ).convert_to_latex()
                }
            )
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']),
                output))
        return questions_and_answers


    # Question type: 22_E_1__1_23
    def generate_22_E_1__1_23_questions(
            self,
            difficulty: int,
            questions_count: int):

        # Define the variable
        x = sp.symbols('x')
        factored_expression_generator = RandomFactoredExpression(x)
        quadratic_expression_generator = RandomQuadraticExpression(x)
        inequalities_and_solutions = []

        turn = 0

        while turn < questions_count:
            turn += 1
            if difficulty == 1:
                expression = factored_expression_generator.generate_factored_expression()
                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.StrictLessThan(expression, 0)
                elif op == '>':
                    inequality = sp.StrictGreaterThan(expression, 0)
                elif op == '<=':
                    inequality = sp.LessThan(expression, 0)
                elif op == '>=':
                    inequality = sp.GreaterThan(expression, 0)
                solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))

            elif difficulty == 2:
                factor_count = random.randint(3, 4)
                num_factors_in_numerator = random.randint(1, factor_count)
                num_factors_in_denominator = factor_count - num_factors_in_numerator
                expression = factored_expression_generator.generate_factored_expression(num_factors_in_numerator, num_factors_in_numerator) / factored_expression_generator.generate_factored_expression(num_factors_in_denominator, num_factors_in_denominator)
                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.StrictLessThan(expression, 0)
                elif op == '>':
                    inequality = sp.StrictGreaterThan(expression, 0)
                elif op == '<=':
                    inequality = sp.LessThan(expression, 0)
                elif op == '>=':
                    inequality = sp.GreaterThan(expression, 0)
                solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))

            elif difficulty == 3:
                expression = sp.expand(RandomFactoredExpression(x, 1).generate_expression_with_lower_coefficient(2, 4))
                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.StrictLessThan(expression, 0)
                elif op == '>':
                    inequality = sp.StrictGreaterThan(expression, 0)
                elif op == '<=':
                    inequality = sp.LessThan(expression, 0)
                elif op == '>=':
                    inequality = sp.GreaterThan(expression, 0)
                try:
                    solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))
                except:
                    turn = turn - 1
                    continue

            elif difficulty == 4:
                is_numerator_unfactored = random.randint(0, 1)
                is_numerator_factored = random.randint(1, 2) - is_numerator_unfactored
                is_denominator_unfactored = random.randint(0, 1)
                is_denominator_factored = random.randint(1, 2) - is_denominator_unfactored

                numerator = 1
                denominator = 1
                if is_numerator_factored:
                    numerator = factored_expression_generator.generate_factored_expression(is_numerator_factored, is_numerator_factored)
                if is_denominator_factored:
                    denominator = factored_expression_generator.generate_factored_expression(is_denominator_factored, is_denominator_factored)
                if is_numerator_unfactored:
                    numerator *= quadratic_expression_generator.generate_unfactorable_expression()
                if is_denominator_unfactored:
                    denominator *= quadratic_expression_generator.generate_unfactorable_expression()
                expression = numerator / denominator

                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.StrictLessThan(expression, 0)
                elif op == '>':
                    inequality = sp.StrictGreaterThan(expression, 0)
                elif op == '<=':
                    inequality = sp.LessThan(expression, 0)
                elif op == '>=':
                    inequality = sp.GreaterThan(expression, 0)
                solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))

            elif difficulty == 5:
                factored_expression_generator_temp = RandomFactoredExpression(x, 1)
                is_numerator_unfactored = random.randint(0, 1)
                is_numerator_factored = random.randint(1, 2) - is_numerator_unfactored
                is_denominator_unfactored = max(random.randint(0, 1), 1 - is_numerator_unfactored)
                is_denominator_factored = random.randint(1, 2) - is_denominator_unfactored
                sqrt_applied = False

                numerator = 1
                denominator = 1
                if is_numerator_factored:
                    numerator = factored_expression_generator_temp.generate_factored_expression(1, is_numerator_factored)
                if is_denominator_factored:
                    denominator = factored_expression_generator_temp.generate_factored_expression(1, is_denominator_factored)
                if is_numerator_unfactored:
                    if not sqrt_applied:
                        numerator *= sp.sqrt(quadratic_expression_generator.generate_unfactorable_expression())
                        sqrt_applied = True
                    else:
                        numerator *= quadratic_expression_generator.generate_unfactorable_expression()
                if is_denominator_unfactored:
                    if not sqrt_applied:
                        denominator *= sp.sqrt(quadratic_expression_generator.generate_unfactorable_expression())
                    else:
                        denominator *= quadratic_expression_generator.generate_unfactorable_expression()
                expression = numerator / denominator

                op = random.choice(['<', '>', '<=', '>='])
                if op == '<':
                    inequality = sp.StrictLessThan(expression, 0)
                elif op == '>':
                    inequality = sp.StrictGreaterThan(expression, 0)
                elif op == '<=':
                    inequality = sp.LessThan(expression, 0)
                elif op == '>=':
                    inequality = sp.GreaterThan(expression, 0)
                try:
                    solution = sp.Intersection(sp.solve_univariate_inequality(inequality, x, relational=False))
                except:
                    turn = turn - 1
                    continue
            else:
                raise ValueError("Unsupported difficulty level")

            inequalities_and_solutions.append(
                {
                    'question': LatexStringModel(
                        string_value="Find all solutions to the following inequality in interval notation. {}",
                        placeholders=[LatexObject(inequality, False, True)]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(solution, False, False)]
                    ).convert_to_latex()
                }
            )
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']), inequalities_and_solutions))
        return questions_and_answers

    # Question type: 22_E_1.3_15
    def generate_22_E_1__3_15_questions(self, difficulty: int, questions_count: int):
        # Define the variable
        x = sp.symbols('x')
        f = sp.Function('f')(x)
        quadratic_expression_generator = RandomQuadraticExpression(x)
        factored_expression_generator = RandomFactoredExpression(x, 1)
        inequalities_and_solutions = []

        for _ in range(questions_count):
            if difficulty == 1:
                equation = quadratic_expression_generator.generate_quadratic_expression_with_max_power_and_limited_terms(10, 3, 4)
                # Find domain for the above equation
                domain = sp.calculus.util.continuous_domain(equation, x, sp.S.Reals)
            elif difficulty == 2:
                equation = sp.sqrt(factored_expression_generator.generate_linear_expression())
                domain = sp.calculus.util.continuous_domain(equation, x, sp.S.Reals)
            elif difficulty == 3:
                equation = factored_expression_generator.generate_quadratic_expression()
                if random.randint(0, 1) == 1:
                    equation = sp.expand(equation)
                equation = sp.sqrt(equation)
                domain = sp.calculus.util.continuous_domain(equation, x, sp.S.Reals)
            elif difficulty == 4:
                numerator_max_power = int(random.triangular(0.7, 1.7, 2.7))
                denominator_max_power = random.randint(1, 2)
                numerator = factored_expression_generator.generate_factored_expression(numerator_max_power, numerator_max_power)
                if random.randint(0, 1):
                    numerator = sp.expand(numerator)
                denominator = factored_expression_generator.generate_factored_expression(denominator_max_power, denominator_max_power)
                if random.randint(0, 1):
                    denominator = sp.expand(denominator)
                equation = numerator / denominator
                domain = sp.calculus.util.continuous_domain(equation, x, sp.S.Reals)
            elif difficulty == 5:
                numerator_max_power = int(random.triangular(0.7, 1.7, 2.7))
                denominator_max_power = random.randint(1, 2)
                numerator = factored_expression_generator.generate_factored_expression(numerator_max_power,
                                                                                       numerator_max_power)
                if random.randint(0, 1):
                    numerator = sp.expand(numerator)
                denominator = factored_expression_generator.generate_factored_expression(denominator_max_power,
                                                                                         denominator_max_power)
                if random.randint(0, 1):
                    denominator = sp.expand(denominator)
                sqrt_type = random.randint(1, 3)
                if sqrt_type == 1:
                    equation = sp.sqrt(numerator / denominator)
                elif sqrt_type == 2:
                    equation = sp.sqrt(numerator) / denominator
                else :
                    equation = numerator / sp.sqrt(denominator)
                domain = sp.calculus.util.continuous_domain(equation, x, sp.S.Reals)
            else:
                raise ValueError("Unsupported difficulty level")
            inequalities_and_solutions.append(
                {
                    'question': LatexStringModel(
                        string_value="Find the domain of the given function. {}",
                        placeholders=[LatexObject(sp.Eq(f, equation), False, True)]
                    ).convert_to_latex(),
                    'correct_solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(domain, False, False)]
                    ).convert_to_latex()
                }
            )
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['correct_solution']),
                inequalities_and_solutions))
        return questions_and_answers


    # Question type: 22_E_1__2_50 by Yasith Heshan
    def generate_22_E_1__2_50_questions(self,
                                     difficulty: int,
                                     questions_count: int):

        questions_and_answers = []
        x = sp.symbols('x')


        def generate_for_difficulty_2():
            for _ in range(questions_count):
                while True:
                    # select suitable m and c
                    m = generate_integer_or_fraction(-10, 10)
                    c = generate_integer_or_fraction(-10, 10)

                    # select x value
                    x1 = generate_integer_or_fraction(-10, 10)
                    # calculate y value
                    y1= m*x1 + c

                    x2 = generate_integer_or_fraction(-10, 10)
                    y2 = m*x2 + c

                    if(x1 != x2 and y1 != y2):
                        break
                
                question = LatexStringModel(
                    string_value='Find the equation of the line passing through the points {} and {}',
                    placeholders=[LatexObject(sp.simplify((x1,y1)), False, False),
                                  LatexObject(sp.simplify((x2,y2)), False, False)]
                ).convert_to_latex()
                answer = LatexStringModel(
                    placeholders=[LatexObject(sp.Eq(sp.symbols('y'), m*x+c), False, False)],
                    string_value="{}"
                ).convert_to_latex()
                questions_and_answers.append({
                    'question': question,
                    'answer': answer
                })
        
        if(difficulty == 1):
            for _ in range(questions_count):
                while True:
                # select suitable m and c
                    m = random.choice([i for i in range(-10, 10) if i != 0])
                    c = random.randint(-10, 10)

                    # select y value
                    x1 = random.randint(-10, 10)
                    # calculate x value
                    y1= m*x1 + c

                    x2 = random.randint(-10, 10)
                    y2 = m*x2 + c

                    if(x1 != x2 and y1 != y2):
                        break
                
                question = LatexStringModel(
                    string_value='Find the equation of the line passing through the points {} and {}',
                    placeholders=[LatexObject(sp.simplify((x1,y1)), False, False),
                                  LatexObject(sp.simplify((x2,y2)), False, False)]
                ).convert_to_latex()
                answer = LatexStringModel(
                    placeholders=[LatexObject(sp.Eq(sp.symbols('y'), m*x + c), False, False)],
                    string_value="{}"
                ).convert_to_latex()
                questions_and_answers.append({
                    'question': question,
                    'answer': answer
                })

        elif(difficulty == 2):
            generate_for_difficulty_2()
        elif(difficulty == 3):
            generate_for_difficulty_2()
        elif(difficulty == 4):
            generate_for_difficulty_2()
        elif(difficulty == 5):
            generate_for_difficulty_2()

        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['answer']), questions_and_answers))

        return questions_and_answers

    # done latex Question type: 22_E_1__2_03 by Harshani -done latex
    def generate_22_E_1__2_03_questions(self, difficulty: int, questions_count: int):

        def generate_points(difficulty):
            if difficulty == 1:
                # Numeric points with integer coordinates
                x1, y1 = random.randint(-9, 9), random.randint(-9, 9)
                x2, y2 = random.randint(-9, 9), random.randint(-9, 9)
                return (x1, y1), (x2, y2)

            elif difficulty == 2:
                def format_sqrt_or_int(value):
                    if isinstance(value, float):
                        if float(int(math.sqrt(value**2))**2)==value**2:
                            return str(int(math.sqrt(value**2)))
                        return sp.sqrt(int(value ** 2),evaluate=False)
                        return f"√{int(value ** 2)}"
                    return value
                    return str(value)

                x1 = random.choice([random.randint(2, 9), random.randint(5, 9)])
                y1 = random.choice([random.randint(2, 9), random.randint(5, 9)])

                # Format the points
                x1, y1 =sp.sqrt(x1,evaluate=False), sp.sqrt(y1,evaluate=False)
                x2, y2 = random.randint(2, 3)*x1,random.randint(2, 3)*y1

                return (x1, y1), (x2, y2)

            elif difficulty == 3:
                a, b = sp.symbols('a b')
                return (random.choice([a,2*a,3*a,4*a]), random.choice([a,2*a,3*a,4*a,b,2*b,3*b,10*b])), (b, a)

            elif difficulty == 4:
                a, b, c, d, e ,f,g= sp.symbols('a b c d e f g')
                return (a + random.choice([b,c,d,e,f,g]), b +  random.choice([a,c,d,e,f,g])), (c +  random.choice([b,a,d,e,f,g]), d +  random.choice([b,c,d,a,f,g]))


            else:
                a, b, c, d, e, f, g= sp.symbols('a b c d e f g')
                return (a + random.choice([b,c,d,e,f,g]), b +  random.choice([a,c,d,e,f,g])), (c +  random.choice([b,a,d,e,f,g]), d +  random.choice([b,c,d,a,f,g]))

        def convert_sqrt_to_int(value):
            # if '√' in value:
            #     return math.sqrt(int(value[1:]))
            # return int(value)
            match = re.match(r"(\d*)√(\d+)", value)
            if match:
                coefficient = int(match.group(1)) if match.group(1) else 1
                root_value = int(match.group(2)) if match.group(2) else 1
                return coefficient * math.sqrt(root_value)
            else:
                return float(value)

        def calculate_distance(point1, point2, difficulty):
            if difficulty in [1]:
                # Numeric distance calculation
                return (point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2

            if difficulty in [2]:
                x1, y1 = point1[0], point1[1]
                x2, y2 = point2[0], point2[1]
                return int((x2 - x1) ** 2 + (y2 - y1) ** 2)

            elif difficulty in [3, 4, 5]:
                # Symbolic distance calculation
                return sp.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

        def generate_mcq_answers(correct_answer, difficulty):
            if difficulty in [1, 2]:
                # Numeric incorrect answers

                incorrect_answers = [f'√{round((correct_answer + _ + 1),2)}'if float(int(math.sqrt(correct_answer + _ + 1))**2)!=(correct_answer + _ + 1) else (correct_answer + _ + 1) for _ in range(3)]
            else:
                # Symbolic incorrect answers
                a, b, c, d, e = sp.symbols('a b c d e')
                incorrect_answers = [
                    sp.sqrt((point2[0] - 3*point1[0]) ** 2 + (point2[1] - point1[1]) ** 2),
                    sp.sqrt((5*point2[0] - point1[0]) ** 2 + (point2[1] - 2*point1[1]) ** 2),
                    sp.sqrt((point2[0] - 3*point1[0]) ** 2 + (2*point2[1] - point1[1]) ** 2),
                ]

            if difficulty in [1, 2]:
                answers = incorrect_answers
            else:
                answers = incorrect_answers

            random.shuffle(answers)
            return answers

        def convert_to_serializable(obj):
            if isinstance(obj, sp.Basic):
                return str(obj)  # Convert sympy objects to string
            if isinstance(obj, tuple):
                return tuple(convert_to_serializable(x) for x in obj)  # Handle tuple
            return obj

        questions = []
        for _ in range(questions_count):
            point1, point2 = generate_points(difficulty)
            if point1 is None or point2 is None:
                continue

            correct_answer = calculate_distance(point1, point2, difficulty)

            if difficulty in [1, 2]:
                # correct_answer_output=f'√{round(correct_answer,2)}' if float(int(math.sqrt(correct_answer))**2)!=(correct_answer ) else str(int(math.sqrt(correct_answer)))
                correct_answer_output = sp.sqrt(correct_answer)
            else:
                correct_answer_output = correct_answer

            answers = generate_mcq_answers(correct_answer, difficulty)

            answers.append(correct_answer_output)

            # Convert the points, correct answer, and answers to serializable forms
            question = {
                # 'question': f"Determine the distance between the given points.{convert_to_serializable(point1), convert_to_serializable(point2)}",
                # 'correct_answer': convert_to_serializable(correct_answer_output),
                # 'answers': [convert_to_serializable(answer) for answer in answers]

                'question':LatexStringModel(
                    string_value="Determine the distance between the given points.{},{}",
                    placeholders=[LatexObject(point1, False, False),
                                  LatexObject(point2, False, False)]
                ).convert_to_latex(),
                'correct_answer':LatexStringModel(
                    string_value="{}",
                    placeholders=[LatexObject(correct_answer_output, False, False)]
                ).convert_to_latex()
            }
            questions.append(question)

        # response = {"difficulty": difficulty, "questions_count": questions_count, "questions": questions}
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['correct_answer']), questions))

        return questions_and_answers
    # done latex harshani 
    def generate_22_E_1__2_43_questions(self, difficulty: int, questions_count: int) -> List[Dict[str, Any]]:

        def generate_line(difficulty: int) -> str:
            x, y = sp.symbols('x y')
            if difficulty == 1:
                m = random.choice([random.randint(-5, -1),random.randint(1, 5)])
                c = random.choice([random.randint(-10, -1),random.randint(1, 10)])
                line=sp.Eq(y,m*x+c)
                # line = f"y = {m}x + {c}"
            elif difficulty == 2:
                if random.choice([True, False]):
                    a = random.randint(-10, 10)
                    line=sp.Eq(x,a)
                    # line = f"x = {a}"
                else:
                    b = random.randint(-10, 10)
                    line = sp.Eq(y,b)
                    # line = f"y = {b}"
            else:
                a = random.choice([random.randint(-10, -1),random.randint(1, 10)])
                b = random.choice([random.randint(-10, -1),random.randint(1, 10)])
                c = random.choice([random.randint(-10, -1),random.randint(1, 10)])

                line = f" {a}x + {b}y + {c} = 0"
                line = sp.Eq(a*x+b*y+c,0)

            return line

        def generate_point() -> Tuple[int, int]:
            x = random.choice([random.randint(1, 10)])
            y = random.choice([random.randint(1, 10)])
            return x, y

        def find_perpendicular_slope(line: sp.Eq, difficulty: int) -> float:
            x, y = sp.symbols('x y')
            if difficulty == 1:
                # y = mx + c
                m = sp.simplify(line.rhs.coeff(x))
                return -1 / m  # Perpendicular slope is -1/m
            elif difficulty == 2:
                if line.lhs == x:
                    return 0  # Line perpendicular to vertical is horizontal (slope = 0)
                elif line.lhs == y:
                    return float('inf')  # Line perpendicular to horizontal is vertical (undefined slope)
            elif difficulty >= 3:
                # ax + by + c = 0 form
                a = line.lhs.coeff(x)
                b = line.lhs.coeff(y)
                return Fraction(b, a)  # Perpendicular slope is b/a
            else:
                raise ValueError("Invalid difficulty level")

        def generate_perpendicular_line(m, point: Tuple[int, int]) -> str:
            """Generate the equation of the line with slope m passing through point."""
            x1, y1 = point
            x, y =sp.symbols('x y')
            if m == float('inf'):
                return sp.Eq(x,x1)
                return f"x = {x1}"
            elif m==0:
                return sp.Eq(y,y1)
                return f"y = {y1}"
            else:
                c = Fraction(y1) - (m)*Fraction(x1)
                return sp.Eq(y, m * x + c)
                return f"y = {m}x + {c}"



        def generate_perpendicular_question(difficulty: int) -> Dict[str, Any]:
            line = generate_line(difficulty)
            point = generate_point()
            m_perpendicular = find_perpendicular_slope(line, difficulty)
            correct_answer = generate_perpendicular_line(m_perpendicular, point)

            question = {
                'question': LatexStringModel(
                    string_value="Find an equation of the line that is perpendicular to the line {} and passes through the given point {}.",
                    placeholders=[LatexObject(line, False, False),
                                  LatexObject(sp.Eq(sp.symbols('p'),point), False, False)]
                ).convert_to_latex(),
                'correct_answer':LatexStringModel(
                    string_value="{}",
                    placeholders= [LatexObject(correct_answer, False, False)]
                ).convert_to_latex(),
                # 'question': f"Find an equation of the line that is perpendicular to the line {simplify_equation(line)} and passes through the given point P = {point}.",
                # 'correct_answer': simplify_equation(correct_answer),
            }

            return question

        questions = []
        for _ in range(questions_count):
            questions.append(generate_perpendicular_question(difficulty))
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['correct_answer']), questions))

        return questions_and_answers

    # Question type: 22_E_1__2_27
    def generate_22_E_1__2_27_questions(self,
                                        difficulty: int,
                                        questions_count: int):
        # Define the variable
        x, y = sp.symbols('x y')
        equations_and_solutions = generate_problem_22_E_1__2_27_questions(difficulty, questions_count)

        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x['other_solutions']), equations_and_solutions))

        return questions_and_answers
    
    def generate_22_E_1__2_13_questions(self, difficulty, questions_count):
        def to_rational(value):
            """Convert Python Fraction to SymPy Rational if necessary."""
            if isinstance(value, Fraction):
                return sp.Rational(value.numerator, value.denominator)
            return value
        def generate_line_equation(x1, y1, slope):
            """Generate the equation of a line in point-slope form given a point and slope."""
            x, y = sp.symbols('x y')
            x1, y1 = to_rational(x1), to_rational(y1)
            if slope == sp.oo:
                return sp.Eq(x, x1)
            elif slope == 0:
                return sp.Eq(y, y1)
            elif isinstance(slope, str):  
                return sp.Eq(y, slope * x + y1 - slope *x1)
            else:
                return sp.Eq(y, slope * x + to_rational(y1 - slope * x1))


        def generate_incorrect_answers(correct_answer, x, y, slope):
            """Generate incorrect answers by slightly modifying the correct answer."""
            incorrect_answers = set()

            if isinstance(x, str) or isinstance(y, str) or isinstance(slope, str):
                if slope == sp.oo:
                    slope = random.randint(-5, 5)
                # For difficulty 5, create plausible incorrect symbolic expressions
                while len(incorrect_answers) < 3:
                    incorrect_forms = [
                        f"y - {y} = {slope} * (x - {x})",  # Slightly different form
                        f"y = {slope}x + {y}",             # Incorrect y-intercept form
                        f"{slope}y = x - {x}",             # Incorrect manipulation
                        f"x - {x} = {slope}(y - {y})",     # Reversed point-slope form
                    ]
                    incorrect = random.choice(incorrect_forms)
                    if incorrect != correct_answer and incorrect not in incorrect_answers:
                        # Ensure the incorrect answer is simplified
                        incorrect = simplify_equation(incorrect)
                        incorrect_answers.add(incorrect)
            else:
                # For other difficulties, generate numeric incorrect answers
                while len(incorrect_answers) < 3:
                    modified_x = Fraction(random.randint(-20, 20), random.randint(1, 20))
                    modified_y = Fraction(random.randint(-20, 20), random.randint(1, 20))
                    modified_slope = slope

                    if slope != sp.oo and slope != 0:
                        modified_slope = Fraction(random.randint(-20, 20), random.randint(1, 20))

                    incorrect = generate_line_equation(modified_x, modified_y, modified_slope)

                    if incorrect != correct_answer:
                        incorrect_answers.add(simplify_equation(incorrect))

            return list(incorrect_answers)

        """Generate a list of questions based on difficulty and count."""
        questions = []
        for _ in range(questions_count):
            if difficulty == 1:
                x, y = random.randint(-15, 15), random.randint(-15, 15)
                slope = random.randint(-15, 15)
            elif difficulty == 2:
                x, y = random.choice([random.randint(-15, 15), sp.Rational(random.randint(-10, 10), random.randint(11, 20))]), \
                    random.choice([random.randint(-15, 15), sp.Rational(random.randint(-10, 10), random.randint(11, 20))])
                slope = random.choice([random.randint(-15, -1), random.randint(1, 15)])
            elif difficulty == 3:
                x, y = sp.Rational(random.randint(-20, 20), random.randint(1, 20)), random.randint(-15, 15)
                slope = sp.Rational(random.randint(-20, 20), random.randint(1, 20))
            elif difficulty == 4:
                x, y = random.choice([0, sp.Rational(random.randint(-20, 20), random.randint(1, 20))]), \
                    random.choice([0, sp.Rational(random.randint(-20, 20), random.randint(1, 20))])
                slope = random.choice([0, sp.oo])
            else:  # difficulty 5
                m, y1, x1 = sp.symbols('m y0 x0')
                x, y = random.randint(-20, 20)*x1, random.randint(-20, 20)*y1
                slope = random.randint(-20, 20)*m
            
            # correct_answer = simplify_equation(generate_line_equation(x, y, slope))
            correct_answer = generate_line_equation(x, y, slope)
            # incorrect_answers = generate_incorrect_answers(correct_answer, x, y, slope)
            
            question_text = f"The line through ({x}, {y}) with slope {slope}"
            print(x,y,slope,correct_answer)
            questions.append({
                'question': LatexStringModel(
                        string_value="The line through {} with slope {}",
                        placeholders=[
                            LatexObject(tuple((x, y)), False, False),
                            LatexObject(slope, False, False)]
                    ).convert_to_latex(),
                "correct_answer": LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(correct_answer, False, False)]
                    ).convert_to_latex(),
                # "answers": [correct_answer] + incorrect_answers
            })
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['correct_answer']), questions))

        return questions_and_answers
    