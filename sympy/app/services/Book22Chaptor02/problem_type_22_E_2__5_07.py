import random
import sympy as sp
import random
from fractions import Fraction
from typing import Any, Dict, List

import sympy as sp
from app.models.dataModels import LatexStringModel, LatexObject, ServiceResponce
from app.utils.helpers import  generate_general_constant_number,generate_general_constant_without_sqrt
from app.services.mcqRuleService import generateCustomeAnswerList, Rule



def generate_polynomial_or_combined_function(var):
        def generate_polynomial():
            degree = random.randint(1, 2)
            coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
            return sum(coeff * var**i for i, coeff in enumerate(coefficients))
        
        def generate_combined_function():
            components = [
                sp.Abs(var),
                sp.sin(random.randint(1, 3) * var),
                sp.cos(random.randint(1, 3) * var),
                sp.exp(var)
            ]
            return sum(random.choice(components) for _ in range(random.randint(1, 3)))
        
        return random.choice([generate_polynomial, generate_combined_function])()

def  generate_22_E_2__5_07_questions(difficulty: int, questions_count: int):
    def generate_question_and_answers(difficulty):
        variable_names = ['x', 'y', 't', 'u', 'v', 'z', ]
        function_names = ['f', 'g', 'h']
        
        var = sp.Symbol(random.choice(variable_names))
        func_name = random.choice(function_names)
        if difficulty == 1:
            
            sub_diff = random.choice([0, 1])
            if sub_diff == 0:
                degree = random.randint(2, 5)
                coefficients = [sp.Rational(random.randint(-10, 10), random.randint(1, 5)) for _ in range(degree + 1)]
                polynomial = sum(coeff * var**i for i, coeff in enumerate(coefficients))
                function =sp.Eq(sp.Function(func_name)(var),  polynomial) 
            elif sub_diff == 1:
                components = [
                    sp.Abs(var), 
                    sp.sin(2 * var), 
                    sp.exp(var),
                    sp.Rational(random.randint(-10, 10), random.randint(1, 3)) * var**random.randint(1, 3)
                ]
                function = sum(random.choice(components) for _ in range(random.randint(2, 4)))
                function = sp.Eq(sp.Function(func_name)(var), function) 
            
            a, b, c = random.sample(range(-20, 21), 3)
            other_solutions = [
                LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, c), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="None of the above. ",
                    placeholders=[]
                ).convert_to_latex()
            ]
            correct_answer = "Continuous on the entire real numbers."
            return function, other_solutions, correct_answer
        
        elif difficulty == 2:
            
            p, q, r = random.sample(range(-10, 11), 3)
            p = random.randint(1, 10)
            q = random.randint(1, 10)
            r = random.randint(-10, 10)
            c = random.randint(1, 5)
            d = random.randint(1, 5)
            
            function_type = random.choice([1, 2, 3, 4, 5])
            
            if function_type == 1:
                function = sp.Eq(sp.Function(func_name)(var) , (sp.sin(p * var + q)**d / (p * var + q)**c))
            elif function_type == 2:
                function = sp.Eq(sp.Function(func_name)(var), ((p * var + q)**d / sp.sin(p * var + q)**c))
            elif function_type == 3:
                function = sp.Eq(sp.Function(func_name)(var), ((1 - sp.cos(p * var + q)) / (p * var + q)**c))
            elif function_type == 4:
                function = sp.Eq(sp.Function(func_name)(var), ((p * var + q)**c / (1 - sp.cos(p * var + q))))
            elif function_type == 5:
                if c==d:
                    if c== 1:
                        c=2
                    elif c==5:
                        c=4
                function = sp.Eq(sp.Function(func_name)(var), ((var**d - r**d) / (var**c - r**c)))
            print(function_type,p,q)
            if function_type in [1, 2]:
                if d >= c:
                    correct_answer = LatexStringModel(
                        string_value="Has a removable discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                    ).convert_to_latex()
                else:
                    correct_answer = correct_answer = LatexStringModel(
                        string_value = "Has an asymptotic discontinuity at {}. ",
                        placeholders = [LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                    ).convert_to_latex()
            elif function_type == 3:
                if 2 >= c:
                    correct_answer = LatexStringModel(
                        string_value="Has a removable discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                    ).convert_to_latex()
                else:
                    correct_answer = LatexStringModel(
                        string_value="Has an asymptotic discontinuity at {}. ",
                        placeholders = [LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                    ).convert_to_latex()
            elif function_type == 4:
                if 2 <= c:
                    correct_answer = LatexStringModel(
                        string_value="Has a removable discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                    ).convert_to_latex()
                else:
                    correct_answer = LatexStringModel(
                        string_value="Has an asymptotic discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                    ).convert_to_latex()
            elif function_type == 5:
                correct_answer = LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
            other_solutions =  [
                LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                        string_value="None of the above. ",
                        placeholders=[]
                    ).convert_to_latex()
            ]
            if function_type == 5:
                correct_answer = LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, r), False, False)]
                ).convert_to_latex()
                other_solutions = [
                    LatexStringModel(
                        string_value="Has a jump discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, r), False, False)]
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="Has a removable discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, r), False, False)]
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="Has an asymptotic discontinuity at {}. ",
                        placeholders=[LatexObject(sp.Eq(var, r), False, False)]
                    ).convert_to_latex(),

                    LatexStringModel(
                        string_value="Continuous on the entire real numbers.",
                        placeholders=[]
                    ).convert_to_latex(),
                    LatexStringModel(
                        string_value="None of the above. ",
                        placeholders=[]
                    ).convert_to_latex()
                ]

            
            return function, other_solutions, correct_answer
        elif difficulty == 3:
            p = generate_polynomial_or_combined_function(var)
            q = generate_polynomial_or_combined_function(var)
                
            a = random.randint(-15, 15)
            condition_type = random.choice(['equal', 'not_equal'])
            
            if condition_type == 'equal':
                q = p.subs(var, a)
            
            conditions = [('<=', '>'), ('<', '>=')]
            cond = random.choice(conditions)
            
            piecewise_function = sp.Piecewise((p, eval(f"var {cond[0]} {a}")), (q, eval(f"var {cond[1]} {a}")))
            
            other_solutions =  [
                LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex(),
                
                LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                        string_value="None of the above. ",
                        placeholders=[]
                    ).convert_to_latex()
            ]
            
            if p.subs(var, a) == q.subs(var, a):
                correct_answer = LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex()
            else:
                correct_answer = LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False)]
                ).convert_to_latex()
            
            return sp.Eq(sp.Function(func_name)(var), piecewise_function), other_solutions, correct_answer
        elif difficulty == 4:
            a, b, c, d, p, q = [random.randint(-15, 15) for _ in range(6)]
            p = random.randint(1, 15)  # p > 0
            q = random.choice([i for i in range(-15, 16) if i != 0])  # q non-zero
            
            while c == 0 or (b == 0 and d == 0):
                a, b, c, d = [random.randint(-15, 15) for _ in range(4)]
            d = random.randint(1, 4)  # d < 5, positive integer
            
            type_choice = random.choice([1, 2, 3])
            
            if type_choice == 1:
                expression = sp.Abs(p * var + q) / (p * var + q)**d
                if d == 1:
                    correct_answer = LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
                else:
                    correct_answer = LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
                    
            elif type_choice == 2:
                expression = (p * var + q)**d / sp.Abs(p * var + q)
                if d % 2 == 1:
                    correct_answer = LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
                else:
                    correct_answer =LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
                    
            elif type_choice == 3:
                expression = (a * (p * var + q) + b * sp.Abs(p * var + q)) / (c * (p * var + q) + d * sp.Abs(p * var + q))
                if a * d == b * c:
                    correct_answer = LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
                else:
                    correct_answer = LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex()
            
            function = sp.Eq(sp.Function(func_name)(var), expression)
            
            other_solutions =  [
                LatexStringModel(
                    string_value="Has a jump discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {}. ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(-q,p)), False, False)]
                ).convert_to_latex(),
                
                LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                        string_value="None of the above. ",
                        placeholders=[]
                    ).convert_to_latex()
            ]
            
            return function, other_solutions, correct_answer
        elif difficulty == 5:
            def generate_polynomial(var, max_degree=3):
                degree = random.randint(1, max_degree)
                coeffs = [random.randint(-10, 10) for _ in range(degree + 1)]
                while coeffs[0] == 0:  # Ensure the leading coefficient is non-zero
                    coeffs[0] = random.randint(-10, 10)
                return sp.Poly(coeffs, var)
            a, b, c = (random.randint(-15, 15) for _ in range(3))
            while c == 0:
                c = random.randint(-15, 15)
            p = generate_polynomial(var)
            
            type_choice = random.choice([1, 2, 3])
            if type_choice == 1:
                root = sp.Rational(a, c)  
                p = generate_polynomial(var, 2)
                adjusted_poly = p * sp.Poly(var - root, var)
                p = random.choice([p, sp.Poly(sp.expand(adjusted_poly.as_expr()))])
                function = p / (c * var - a)
                correct_answer = LatexStringModel(
                    string_value="Has a removable discontinuity at {} .",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(a,c)), False, False)]
                ).convert_to_latex() if p.eval(a/c) == 0 else LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {} .",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(a,c)), False, False)]
                ).convert_to_latex()
                other_solutions =  [
                LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has removable discontinuities at {} . ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(a,c)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {} .",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(a,c)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {} . ",
                    placeholders=[LatexObject(sp.Eq(var, sp.Rational(a,c)), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="None of the above. ",
                    placeholders=[]
                ).convert_to_latex(),
                
            ]
            elif type_choice == 2:

                b = random.randint(-15, 15)
                while b == a:
                    b = random.randint(-15, 15)
                p = generate_polynomial(var)
                p_case_1 = generate_polynomial(var,2) * sp.Poly(var -a, var)
                p_case_2 = generate_polynomial(var,1) * sp.Poly(var -a, var)  * sp.Poly(var -b, var)
                p = random.choice([p, sp.Poly(sp.expand(p_case_1.as_expr())), sp.Poly(sp.expand(p_case_2.as_expr()))])
                function = p / sp.expand((c * var - a) * (c * var - b))
                if p(a) == 0 and p(b) == 0:
                    correct_answer = LatexStringModel(
                    string_value="Has removable discontinuities at {} and  {} .",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex()
                elif p(a) == 0 and p(b) != 0:
                    correct_answer = LatexStringModel(
                    string_value="Has a removable discontinuity at {} and an asymptotic discontinuity at {}.",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False), LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex()
                else:
                    correct_answer = LatexStringModel(
                    string_value="Has asymptotic discontinuities at {} and {} .",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex()

                other_solutions =  [
                LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has removable discontinuities at {} and  {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {} and an asymptotic discontinuity at {}.",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {} and {}. ",
                    placeholders=[LatexObject(sp.Eq(var, a), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="None of the above. ",
                    placeholders=[]
                ).convert_to_latex(),
                
            ]
            elif type_choice == 3:
                while b**2 - 4 * a * c >=0:
                    a, b, c = (random.randint(-15, 15) for _ in range(3))
                function = p / (a * var**2 + b * var + c)
                correct_answer = LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex()
                other_solutions =  [
                LatexStringModel(
                    string_value="Continuous on the entire real numbers.",
                    placeholders=[]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has removable discontinuities at {} and  {}. ",
                    placeholders=[LatexObject(sp.Eq(var, c), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has a removable discontinuity at {} and an asymptotic discontinuity at {}.",
                    placeholders=[LatexObject(sp.Eq(var, c), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="Has an asymptotic discontinuity at {} and {}. ",
                    placeholders=[LatexObject(sp.Eq(var, c), False, False),LatexObject(sp.Eq(var, b), False, False)]
                ).convert_to_latex(),
                LatexStringModel(
                    string_value="None of the above. ",
                    placeholders=[]
                ).convert_to_latex(),
                
            ]

            
            
            return sp.Eq(sp.Function(func_name)(var), function), other_solutions, correct_answer
                        
    output = []
    for _ in range(questions_count):
    
        function, other_solution, correct_answer = generate_question_and_answers(difficulty)
        
        output.append({
                'question': LatexStringModel(
                    string_value="What is true about the following function? {} ",
                    placeholders=[LatexObject(function, False, True)]
                ).convert_to_latex(),
                'solution': correct_answer,
                'other_solutions':other_solution
            }
            )
        questions_and_answers = list(map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],other_solutions=x['other_solutions']), output))
    

    return questions_and_answers

