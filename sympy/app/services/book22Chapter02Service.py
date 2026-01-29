import random
from fractions import Fraction
from typing import Any, Dict, List

import sympy as sp

from app.models.dataModels import LatexStringModel, ServiceResponce, LatexObject
from app.services.base_quetion_generator_service import BaseQuestionGeneratorService
from app.services.mcqRuleService import generateCustomeAnswerList, Rule
from app.utils.helpers import random_non_zero_real, randint_exclude_list, generate_general_constant_number, generate_general_constant_without_sqrt
from app.services.Book22Chaptor02.problem_type_22_E_2__2__01 import generate_problem_22_E_2__2_01_questions
from app.services.Book22Chaptor02.problem_type_22_E_2__4_11 import generate_problem_22_E_2__4_11_questions

class RandomFactoredExpressionGenerator:
    def __init__(self, variable):
        self.variable = variable

    def generate_factor(self):
        a = randint_exclude_list(-5, 5)  # Coefficient of x
        b = random.randint(-5, 5)  # Constant term
        return a * self.variable + b

    def generate_fully_factorizable_expression(self, variable, constant, degree, avoid_double_root_at=None):
        if degree == 1:
            return variable - constant
        else:
            expression = variable - constant
            for _ in range(degree - 1):
                factor = self.generate_factor()
                while avoid_double_root_at is not None and factor == (variable - avoid_double_root_at):
                    factor = self.generate_factor()  # Regenerate to avoid double root
                expression *= factor
            return expression


class Book22Chapter02Service(BaseQuestionGeneratorService):

    def generate_answers(self) -> list:
        pass

    def format_questions(self):
        pass

    def generate_22_E_2__2_01_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_solutions = generate_problem_22_E_2__2_01_questions(difficulty, questions_count)
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']),
                questions_and_solutions))

        return questions_and_answers

    def generate_22_E_2__4_11_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_solutions = generate_problem_22_E_2__4_11_questions(difficulty, questions_count)
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],
                                          other_solutions=x["other_solutions"]), questions_and_solutions))

        return questions_and_answers

    def generate_22_E_2__3_21_questions(self, difficulty: int, questions_count: int):

        def generate_limit_question(difficulty: int) -> Dict[str, Any]:
            other_solutions = None
            a = random_non_zero_real([4, 1, 1, 0])
            b = random_non_zero_real([4, 1, 1, 0])

            symbol = random.choice(['x', 'y', 't', 'u', 'v', 'z', 'r', 's'])
            x = sp.symbols(symbol)
            question_expr = None

            if difficulty == 1:
                # Randomly select the form of the limit question
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin(ax) / (bx))

                    expr = sp.sin(a * x) / (b * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:
                    # Form: lim x -> 0 (bx / sin(ax))
                    expr = (b * x) / sp.sin(a * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 2:
                # Randomly select the form of the limit question
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                c = random.randint(1, 4)
                if c ==4:
                    c = 3
                    d = 4
                else:
                    d = random.choice([c, c, random.randint(c,4), random.randint(c,4), random.randint(c,4)])
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin^2(ax) / (bx^2))
                    expr = (sp.sin(a * x) ** d) / (b * x ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:
                    # Form: lim x -> 0 (bx^2 / sin^2(ax))
                    expr = (b * x ** d) / (sp.sin(a * x) ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 3:
                a = random.randint(1, 10)
                b = random.randint(11, 20)
                # Randomly select the form of the limit question
                if random.choice([True, False]):
                    # Form: lim x -> 0 (sin(ax) / sin(bx))
                    expr = sp.sin(a * x) / sp.sin(b * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:

                    expr = sp.sin(b * x) / sp.sin(a * x)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 4:

                choice = random.choice([1, 2,3,4])
                if choice == 1:
                    # Form: lim x -> 0 (1 - cos(ax) / bx^2)
                    c = random.choice([1,2,2,2,2])
                    expr = (1 - sp.cos(a * x)) / (b * x ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                elif choice==2:

                    c = random.choice([3,4,2,2,2,2])
                    expr = (b * x ** c)/ (1 - sp.cos(a * x))
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                elif choice ==3:
                    c = random.choice([1,2,2,2,2])
                    expr = (1 - sp.cos(a * x)) / (sp.sin(b * x) ** c)
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
                else:
                    c = random.choice([3,4,2,2,2,2])
                    if b**c>=200:
                        c = 2
                        b= random.choice([3,4,5,6,7,8])
                    expr = sp.sin(b * x) ** c/ (1 - sp.cos(a * x))
                    limit = sp.limit(expr, x, 0)
                    question_expr = sp.Limit(expr, x, 0, dir="+-")
            elif difficulty == 5:
                p = random.randint(1, 9)
                q = random.choice([i for i in range(-9, 10) if i != 0])
                a = b = 1
                transformed_x = p * x + q
                limit_value = sp.Rational(-q, p)
                sub_difficulty = random.choice([1, 2, 4])
                if sub_difficulty == 1:
                    if random.choice([True, False]):
                        expr = sp.sin(a * transformed_x) / (b * transformed_x)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    else:
                        expr = (b * transformed_x) / sp.sin(a * transformed_x)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                elif sub_difficulty == 2:
                    c = random.randint(1, 4)
                    if c == 4:
                        c = 3
                        d = 4
                    else:
                        d = random.choice([c, c, random.randint(c, 4), random.randint(c, 4), random.randint(c, 4)])
                    if random.choice([True, False]):
                        expr = (sp.sin(a * transformed_x) ** d) / (b * transformed_x ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    else:
                        expr = (b * transformed_x ** d) / (sp.sin(a * transformed_x) ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                elif sub_difficulty == 4:
                    choice = random.choice([1, 2, 3, 4])
                    if choice == 1:
                        c = random.choice([1, 2, 2, 2, 2])
                        expr = (1 - sp.cos(a * transformed_x)) / (b * transformed_x ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    elif choice == 2:
                        c = random.choice([3, 4, 2, 2, 2, 2])
                        expr = (b * transformed_x ** c) / (1 - sp.cos(a * transformed_x))
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    elif choice == 3:
                        c = random.choice([1, 2, 2, 2, 2])
                        expr = (1 - sp.cos(a * transformed_x)) / (sp.sin(b * transformed_x) ** c)
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                    else:
                        c = random.choice([3, 4, 2, 2, 2, 2])
                        if b ** c >= 200:
                            c = 2
                            b = random.choice([3, 4, 5, 6, 7, 8])
                        expr = sp.sin(b * transformed_x) ** c / (1 - sp.cos(a * transformed_x))
                        limit = sp.limit(expr, x, limit_value)
                        question_expr = sp.Limit(expr, x, limit_value, dir="+-")
                other_solutions = [0, 1, 2, sp.Rational(1, 2), random.randint(3, 9)]
                other_solutions.remove(limit)
            elif difficulty == 6:
                c = random.randint(-20, 20)
                if random.choice([True, False]):
                    d = random.randint(-20, 20)
                    # Form: lim x -> -d/c (sin(ax + b) / (cx + d))
                    expr = sp.sin(a * x + b) / (c * x + d)
                    limit = sp.limit(expr, x, -d / c, dir="+-")
                    question_expr = sp.Limit(expr, x, -d / c, dir="+-")
                else:
                    d = random.randint(-20, 20)
                    # Form: lim x -> d/c (sin^2(ax - b) / (1 - cos(cx - d)))
                    expr = sp.sin(a * x - b) ** 2 / (1 - sp.cos(c * x - d))
                    limit = sp.limit(expr, x, d / c, dir="+-")
                    question_expr = sp.Limit(expr, x, d / c, dir="+-")

            return expr, limit, question_expr, sp.latex(limit), other_solutions

        output = []
        for _ in range(questions_count):
            if difficulty != 5:
                q, a, question_exp, b, other_Solution = generate_limit_question(difficulty)

                output.append({

                    'question': LatexStringModel(
                        string_value="Evaluate the following limit (without using any derivatives). {} ",
                        placeholders=[LatexObject(question_exp, False, True)]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(a)]
                    ).convert_to_latex()
                }
                )

                questions_and_answers = list(
                    map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']), output))
            else:
                q, a, question_exp, b, other_Solution = generate_limit_question(difficulty)

                output.append({

                    'question': LatexStringModel(
                        string_value="Evaluate the following limit (without using any derivatives). {} ",
                        placeholders=[LatexObject(question_exp, False, True)]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(a)]
                    ).convert_to_latex(),
                    'other_solutions': [LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(a)]
                    ).convert_to_latex() for a in other_Solution]
                }
                )

                questions_and_answers = list(
                    map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'],
                                                  other_solutions=x['other_solutions']), output))

        return questions_and_answers

    # Question type: 22_E_2__3_25
    def generate_22_E_2__3_25_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_solutions = []
        q_no = 0

        while q_no < questions_count:
            symbol = random.choice(['x', 'y', 't', 'u', 'v', 'z', 'r', 's'])
            selected_var = sp.symbols(symbol)
            if difficulty == 1:
                # Form: lim x -> a (x^2 - a^2) / (x - a)
                a = random_non_zero_real([4, 1, 1, 0], 500, 2)
                expr = (selected_var ** 2 - a ** 2) / (selected_var - a)
            elif difficulty == 2:
                # Form: lim x -> a (x^d - a^d) / (x - a) where 3 <= d <= 5 and -500 < a^d < 500
                d = random.randint(3, 5)
                a = random_non_zero_real([4, 1, 1, 1], 500, d)

                while not (abs(a ** d) < 500):
                    d = random.randint(3, 5)
                    a = random_non_zero_real([4, 1, 1, 0], 500, d)

                expr = (selected_var ** d - a ** d) / (selected_var - a)
            elif difficulty == 3:
                # Form: lim x -> a (x^d - a^d) / (x^c - a^c) where 2 <= c, d <= 5 and -500 < a^c, a^d < 500
                powers = [2, 3, 4, 5]
                c = random.choice(powers)
                powers.remove(c)
                d = random.choice(powers)
                a = random_non_zero_real([4, 1, 1, 1], 500, max(c, d))

                while not (abs(a ** c) < 500) or not (abs(a ** d) < 500):
                    powers = [2, 3, 4, 5]
                    c = random.choice(powers)
                    powers.remove(c)
                    d = random.choice(powers)
                    a = random_non_zero_real([4, 1, 1, 1], 500, max(c, d))
                expr = (selected_var ** d - a ** d) / (selected_var ** c - a ** c)
            elif difficulty == 4:
                # Form: lim x -> a (x^(1/d) - a^(1/d)) / (x^(1/c) - a^(1/c)) where d, c = 1, 2, 3 and d not equal c. If d or c even a > 0
                value_list = [1, 2, 3]
                c = random.choice(value_list)
                value_list.remove(c)
                d = random.choice(value_list)
                a = random_non_zero_real([4, 0, 0, 0])
                if c % 2 == 0 or d % 2 == 0:
                    a = abs(a)
                expr = (selected_var ** (sp.Rational(1, d)) - a ** (sp.Rational(1, d))) / (
                            selected_var ** (sp.Rational(1, c)) - a ** (sp.Rational(1, c)))
            elif difficulty == 5:
                random_factored_expression_generator = RandomFactoredExpressionGenerator(selected_var)
                # Form: lim x -> a (polynomial of degree 1, 2, 3 with a factor (x - a)) / (polynomial of degree 1, 2, 3 with a factor (x - a))
                # where all the polynomial easily factorisable and make sure that the denominator does not have a double root at x = a. a can be integers (slightly higher probability), fractions.
                a = random_non_zero_real([4, 1, 0, 0])
                numerator_degree = random.randint(1, 3)
                if numerator_degree == 1:
                    denominator_degree = random.randint(2, 3)
                else:
                    denominator_degree = random.randint(1, 3)
                numerator = random_factored_expression_generator.generate_fully_factorizable_expression(selected_var, a,
                                                                                                        numerator_degree,
                                                                                                        avoid_double_root_at=None).expand()
                denominator = random_factored_expression_generator.generate_fully_factorizable_expression(selected_var,
                                                                                                          a,
                                                                                                          denominator_degree,
                                                                                                          avoid_double_root_at=a).expand()
                expr = numerator / denominator
            else:
                raise ValueError('Unsupported difficulty level')

            question_expr = sp.Limit(expr, selected_var, a, dir="+-")
            try:
                answer = sp.limit(expr, selected_var, a, dir="+-")
                q_no += 1
            except ValueError:
                continue
            questions_and_solutions.append(
                {
                    'question': LatexStringModel(
                        string_value="Evaluate the following limits (without using any derivatives). {}",
                        placeholders=[
                            LatexObject(value=question_expr, is_in_latex_format=False, is_double_dollar_required=True),
                        ]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[
                            LatexObject(value=answer, is_in_latex_format=False, is_double_dollar_required=False),
                        ]
                    ).convert_to_latex()
                }
            )
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution']),
                questions_and_solutions))
        return questions_and_answers

    # Question type: 22_E_2__4_07
    def generate_22_E_2__4_07_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_solutions = []
        question_no = 0

        while question_no < questions_count:
            symbol = random.choice(['x', 'y', 't', 'u', 'v', 'z', 'r', 's'])
            selected_var = sp.symbols(symbol)
            is_in_latex_format = False
            other_solutions = None
            if difficulty == 1:
                # Form: lim x -> (p/q) (qx - p)^(1/2) or lim x -> (-p/q) (p - qx)^(1/2) where p, q integers between -20
                # and 20, q > 0 , have a slightly higher probability for q = 1 (Single side limit)
                p = random.randint(-20, 20)
                q = random.choice([1, random.randint(1, 20)])
                if random.choice([True, False]):
                    expr = sp.sqrt(q * selected_var - p)
                    question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="+")
                    answer = sp.limit(expr, selected_var, Fraction(p, q), dir="+")
                else:
                    expr = sp.sqrt(p - q * selected_var)
                    question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="-")
                    answer = sp.limit(expr, selected_var, Fraction(p, q), dir="-")
                other_solutions = [1, -1, "Does not exist"]
                other_solutions_copy = other_solutions.copy()
                other_solutions_copy.append(answer)
                other_solutions.append(randint_exclude_list(-10, 10, other_solutions_copy))

            elif difficulty == 2:
                # Form: lim x -> (p/q)+ abs(qx - p)/(qx - p) or lim x -> (p/q)- abs(qx - p)/(qx - p) or
                # lim x -> (p/q)+ (qx - p)/abs(qx - p) or lim x -> (p/q)- (qx - p)/abs(qx - p) where p, q integers
                # between -20 and 20, q > 0 , have a slightly higher probability for q = 1, q not equal to 0.
                # Also, randomly choose to have p - qx instead of qx - p, in exactly one of numerator or denominator.
                # (Single side limit)
                p = random.randint(-20, 20)
                q = random.choice([1, random.randint(1, 20)])
                is_absolute_value_in_numerator = random.choice([True, False])
                qx_p_occurrence_type = random.choice([1, 2, 3])

                # Make expression
                if is_absolute_value_in_numerator:
                    if qx_p_occurrence_type == 1:
                        expr = sp.Abs(q * selected_var - p) / (q * selected_var - p)
                    elif qx_p_occurrence_type == 2:
                        expr = sp.Abs(p - q * selected_var) / (q * selected_var - p)
                    else:
                        expr = sp.Abs(q * selected_var - p) / (p - q * selected_var)
                else:
                    if qx_p_occurrence_type == 1:
                        expr = (q * selected_var - p) / sp.Abs(q * selected_var - p)
                    elif qx_p_occurrence_type == 2:
                        expr = (p - q * selected_var) / sp.Abs(q * selected_var - p)
                    else:
                        expr = (q * selected_var - p) / sp.Abs(p - q * selected_var)

                # Apply limit direction
                if random.choice([True, False]):
                    question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="+")
                    answer = sp.limit(expr, selected_var, Fraction(p, q), dir="+")
                else:
                    question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="-")
                    answer = sp.limit(expr, selected_var, Fraction(p, q), dir="-")
                other_solutions = [1, -1, "Does not exist", "Infinity", "-Infinity"]
                other_solutions.remove(answer)

            elif difficulty == 3:
                # lim x -> (p/q)+ abs(qx - p) - abs(x) or lim x -> (p/q)- (p - qx)^(1/2) where p, q integers between -20
                # and 20, q != 0 , have a slightly higher probability for q = 1.  Also, randomly choose to have
                # (p - qx) instead of (qx - p), in the expression. (Single side limit)
                p = random.randint(-20, 20)
                q = random.choice([random.randint(-20, -1), 1, 1, random.randint(1, 20)])
                is_qx_p_in_present = random.choice([True, False])
                if random.choice([True, False]):
                    if is_qx_p_in_present:
                        expr = sp.Abs(q * selected_var - p) - sp.Abs(selected_var)
                    else:
                        expr = sp.Abs(p - q * selected_var) - sp.Abs(selected_var)
                    question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="+")
                    answer = sp.limit(expr, selected_var, Fraction(p, q), dir="+")
                else:
                    if is_qx_p_in_present:
                        expr = sp.Abs(q * selected_var - p) - sp.Abs(selected_var)
                    else:
                        expr = sp.Abs(p - q * selected_var) - sp.Abs(selected_var)
                    question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="-")
                    answer = sp.limit(expr, selected_var, Fraction(p, q), dir="-")

            elif difficulty == 4:
                # lim x -> 0+ (ax + b*abs(x))/(cx + d*abs(x)) or lim x -> 0+ (ax + b*abs(x))/(cx + d*abs(x))
                # where a, b, c, d integers between -20 and 20. Also, randomly choose to have b|x| + ax instead of
                # ax + b |x|, in the numerator, and similarly for the denominator. (Single side limit)
                a = random.randint(-20, 20)
                b = random.randint(-20, 20)
                c = random.randint(-20, 20)
                d = random.randint(-20, 20)

                is_ax_babsx_in_numerator = random.choice([True, False])
                is_cx_dabsx_in_denominator = random.choice([True, False])

                # Make expression
                if is_ax_babsx_in_numerator:
                    numerator = a * selected_var + b * sp.Abs(selected_var)
                else:
                    numerator = b * sp.Abs(selected_var) + a * selected_var
                if is_cx_dabsx_in_denominator:
                    denominator = c * selected_var + d * sp.Abs(selected_var)
                else:
                    denominator = d * sp.Abs(selected_var) + c * selected_var
                expr = numerator / denominator

                # Apply limit direction
                if random.choice([True, False]):
                    question_expr = sp.Limit(expr, selected_var, 0, dir="+")
                    answer = sp.limit(expr, selected_var, 0, dir="+")
                else:
                    question_expr = sp.Limit(expr, selected_var, 0, dir="-")
                    answer = sp.limit(expr, selected_var, 0, dir="-")

            elif difficulty == 5:

                pre_difficulty_level = random.randint(2, 4) # Select question type for question generation from level 1 to 4

                try:
                    if pre_difficulty_level == 2:
                        # Form: lim x -> (p/q)+ abs(qx - p)/(qx - p) or lim x -> (p/q)- abs(qx - p)/(qx - p) or
                        # lim x -> (p/q)+ (qx - p)/abs(qx - p) or lim x -> (p/q)- (qx - p)/abs(qx - p) where p, q integers
                        # between -20 and 20, q > 0 , have a slightly higher probability for q = 1, q not equal to 0.
                        # Also, randomly choose to have p - qx instead of qx - p, in exactly one of numerator or denominator.
                        # (Dual side limit)
                        p = random.randint(-20, 20)
                        q = random.choice([1, random.randint(1, 20)])
                        is_absolute_value_in_numerator = random.choice([True, False])
                        qx_p_occurrence_type = random.choice([1, 2, 3])

                        # Make expression
                        if is_absolute_value_in_numerator:
                            if qx_p_occurrence_type == 1:
                                expr = sp.Abs(q * selected_var - p) / (q * selected_var - p)
                            elif qx_p_occurrence_type == 2:
                                expr = sp.Abs(p - q * selected_var) / (q * selected_var - p)
                            else:
                                expr = sp.Abs(q * selected_var - p) / (p - q * selected_var)
                        else:
                            if qx_p_occurrence_type == 1:
                                expr = (q * selected_var - p) / sp.Abs(q * selected_var - p)
                            elif qx_p_occurrence_type == 2:
                                expr = (p - q * selected_var) / sp.Abs(q * selected_var - p)
                            else:
                                expr = (q * selected_var - p) / sp.Abs(p - q * selected_var)

                        # Apply limit direction
                        question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="+-")
                        other_solutions = [1, -1, "Does not exist", "Infinity", "-Infinity"]
                        answer = sp.limit(expr, selected_var, Fraction(p, q), dir="+-")
                        other_solutions.remove(answer)

                    elif pre_difficulty_level == 3:
                        # lim x -> (p/q)+ abs(qx - p) - abs(x) or lim x -> (p/q)- (p - qx)^(1/2) where p, q integers between -20
                        # and 20, q != 0 , have a slightly higher probability for q = 1.  Also, randomly choose to have
                        # (p - qx) instead of (qx - p), in the expression. (Dual side limit)
                        p = random.randint(-20, 20)
                        q = random.choice([random.randint(-20, -1), 1, 1, random.randint(1, 20)])
                        is_qx_p_in_present = random.choice([True, False])
                        if is_qx_p_in_present:
                            expr = sp.Abs(q * selected_var - p) - sp.Abs(selected_var)
                        else:
                            expr = sp.Abs(p - q * selected_var) - sp.Abs(selected_var)
                        question_expr = sp.Limit(expr, selected_var, Fraction(p, q), dir="+-")
                        answer = sp.limit(expr, selected_var, Fraction(p, q), dir="+-")

                    else:
                        # lim x -> 0+ (ax + b*abs(x))/(cx + d*abs(x)) or lim x -> 0+ (ax + b*abs(x))/(cx + d*abs(x))
                        # where a, b, c, d integers between -20 and 20. Also, randomly choose to have b|x| + ax instead of
                        # ax + b |x|, in the numerator, and similarly for the denominator. (Single side limit)
                        a = random.randint(-20, 20)
                        b = random.randint(-20, 20)
                        c = random.randint(-20, 20)
                        d = random.randint(-20, 20)

                        is_ax_babsx_in_numerator = random.choice([True, False])
                        is_cx_dabsx_in_denominator = random.choice([True, False])

                        # Make expression
                        if is_ax_babsx_in_numerator:
                            numerator = a * selected_var + b * sp.Abs(selected_var)
                        else:
                            numerator = b * sp.Abs(selected_var) + a * selected_var
                        if is_cx_dabsx_in_denominator:
                            denominator = c * selected_var + d * sp.Abs(selected_var)
                        else:
                            denominator = d * sp.Abs(selected_var) + c * selected_var
                        expr = numerator / denominator

                        # Apply limit direction
                        question_expr = sp.Limit(expr, selected_var, 0, dir="+-")
                        answer = sp.limit(expr, selected_var, 0, dir="+-")
                except:
                    answer = "Does not exist"
                    is_in_latex_format = True
                    if other_solutions is not None and answer in other_solutions:
                        other_solutions.remove(answer)
            else:
                raise ValueError('Unsupported difficulty level')

            if difficulty != 5:
                question_str = "Determine the following one-sided limit. {}"
            else:
                question_str = "Determine the following limit. {}"

            questions_and_solutions.append(
                {
                    'question': LatexStringModel(
                        string_value=question_str,
                        placeholders=[
                            LatexObject(value=question_expr, is_in_latex_format=False, is_double_dollar_required=True),
                        ]
                    ).convert_to_latex(),
                    'solution': LatexStringModel(
                        string_value="{}",
                        placeholders=[
                            LatexObject(value=answer, is_in_latex_format=is_in_latex_format, is_double_dollar_required=False),
                        ]
                    ).convert_to_latex(),
                    'other_solutions': other_solutions
                }
            )
            question_no += 1
        questions_and_answers = list(
            map(lambda x: ServiceResponce(question=x['question'], correct_solution=x['solution'], other_solutions=x['other_solutions']),
                questions_and_solutions))
        return questions_and_answers
    def generate_polynomial_or_combined_function(self,var):
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
    def  generate_22_E_2__5_07_questions(self, difficulty: int, questions_count: int):
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
                p = self.generate_polynomial_or_combined_function(var)
                q = self.generate_polynomial_or_combined_function(var)

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


    # Question type: 22_E_2__4_35
    def generate_22_E_2__4_35_questions(self,
                                        difficulty: int,
                                        questions_count: int) -> List[ServiceResponce]:
        questions_and_answers = []
        x, k = sp.symbols('x k')

        for _ in range(questions_count):

            symbol = sp.Symbol(random.choice(['x', 'y', 't', 'u', 'v', 'z', 'r', 's']))
            limit_dir = random.choice(['+', '-'])
            # Choose question type based on the following randomly
            # Type:
            # 1 -> E_22_2.2_01
            # 2 -> E_22_2.3_21
            # 3 -> E_22_2.3_25
            question_type = random.randint(1, 3)
            piecewise_function = None
            print(question_type, len(questions_and_answers))

            if question_type == 1:

                if difficulty == 1:
                    expression = generate_general_constant_number(-10, 10)
                    constant = generate_general_constant_number(-10, 10)
                    limit = sp.Limit(expression, symbol, constant, dir=limit_dir)
                    solution = sp.limit(expression, symbol, constant, dir=limit_dir)
                elif difficulty == 2:
                    a = generate_general_constant_without_sqrt(-10, 10)
                    b = generate_general_constant_without_sqrt(-10, 10)
                    constant = generate_general_constant_without_sqrt(-10, 10)
                    print(a, b, symbol)
                    print(type(a), type(b), type(symbol))
                    expression = a * symbol + b
                    limit = sp.Limit(expression, symbol, constant, dir=limit_dir)
                    solution = sp.limit(expression, symbol, constant, dir=limit_dir)
                elif difficulty == 3:
                    degree = random.choice([2, 3, 4, 5, 6])
                    polynomial = 0
                    for i in range(degree):
                        if (degree == 2):
                            coefficient = generate_general_constant_without_sqrt(-10, 10)
                        else:
                            coefficient = random.choice([i for i in range(-10, 11) if i != 0])
                        polynomial += coefficient * symbol ** i
                    constant = generate_general_constant_without_sqrt(-10, 10)
                    limit = sp.Limit(polynomial, symbol, constant, dir=limit_dir)
                    solution = sp.limit(polynomial, symbol, constant, dir=limit_dir)
                elif difficulty == 4:
                    # Define possible limit numbers with higher probability for specific trigonometric values
                    trig_values = [0, sp.pi / 6, sp.pi / 4, sp.pi / 3, sp.pi / 2, 5 * sp.pi / 6, 3 * sp.pi / 4,
                                   2 * sp.pi / 3, sp.pi, 3 * sp.pi / 2, 2 * sp.pi]
                    # Define possible functions
                    functions = [
                        sp.Abs(symbol),
                        sp.sin(symbol),
                        sp.cos(symbol),
                        sp.tan(symbol),
                        sp.exp(symbol),
                        sp.log(symbol)
                    ]

                    # Randomly select a combination of functions
                    selected_functions = random.sample(functions, k=random.randint(2, 3))
                    if (sp.sin(symbol) in selected_functions or sp.cos(symbol) in selected_functions or sp.tan(
                            symbol) in selected_functions):
                        limit_number = random.choice(trig_values)
                    else:
                        limit_number = generate_general_constant_number(-10, 10)

                        # Create the expression by combining the selected functions
                    expression = selected_functions[0]
                    for func in selected_functions[1:]:
                        expression += func

                    # Create the limit and solution
                    limit = sp.Limit(expression, symbol, limit_number, dir=limit_dir)
                    solution = sp.limit(expression, symbol, limit_number, dir=limit_dir)

                elif difficulty == 5:
                    def generate_piece(degree):
                        if degree == 0:  # Constant
                            return generate_general_constant_without_sqrt(-10, 10)
                        elif degree == 1:  # Linear
                            a = generate_general_constant_without_sqrt(-10, 10)
                            b = generate_general_constant_without_sqrt(-10, 10)
                            return a * symbol + b
                        elif degree == 2:  # Quadratic
                            a = generate_general_constant_without_sqrt(-10, 10)
                            b = generate_general_constant_without_sqrt(-10, 10)
                            c = generate_general_constant_without_sqrt(-10, 10)
                            return a * symbol ** 2 + b * symbol + c

                    # Randomly choose breakpoints and corresponding pieces
                    breakpoint = generate_general_constant_without_sqrt(-10, 10)
                    left_piece = generate_piece(random.choice([0, 1, 2]))
                    right_piece = generate_piece(random.choice([0, 1, 2]))

                    # Define the piecewise function

                    # Define the limit at the breakpoint
                    limit = sp.Limit(k, symbol, breakpoint, dir=limit_dir)
                    piecewise_function = sp.Piecewise(
                        (left_piece, symbol <= breakpoint),
                        (right_piece, symbol > breakpoint), Evaluate=False
                    )
                    solution = sp.limit(piecewise_function, symbol, breakpoint, dir=limit_dir)
                else:
                    raise ValueError('Unsupported difficulty level')

                if (solution != sp.oo and solution != -sp.oo and solution != "no_solutions"):
                    other_solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, solution, 4)
                else:
                    other_solutions = generateCustomeAnswerList(Rule.MULTIPLY.value, random.randint(1, 10), 4)
                if (piecewise_function):
                    pf_str = LatexStringModel(
                        string_value="{}",
                        placeholders=[LatexObject(sp.Eq(sp.Function("f")(x), piecewise_function), False, True)],
                    ).convert_to_latex()
                    question = (LatexStringModel(
                        string_value="Evaluate the following one-sided limit. {}",
                        placeholders=[LatexObject(limit, False, True)],
                    ).convert_to_latex().replace("k", f"f({symbol})") + f" where " + pf_str)
                else:
                    question = LatexStringModel(
                        placeholders=[LatexObject(limit, False, True)],
                        string_value="Evaluate the following one-sided limit. {}",
                    ).convert_to_latex()
                other_solution_latex = [LatexStringModel(
                    placeholders=[LatexObject(x, False, False)],
                    string_value="{}"
                ).convert_to_latex() for x in other_solutions]
                if (difficulty == 5):
                    other_solution_latex = other_solution_latex + ["Do not exist."]
                questions_and_answers.append(ServiceResponce(
                    question=question,
                    correct_solution=LatexStringModel(
                        placeholders=[LatexObject(solution, False, False)],
                        string_value="{}").convert_to_latex() if solution != "no_solutions" else "Do not exist.",
                    other_solutions=other_solution_latex
                ))

            elif question_type == 2:
                def generate_limit_question(difficulty: int) -> Dict[str, Any]:
                    other_solutions = None
                    a = random_non_zero_real([4, 1, 1, 0])
                    b = random_non_zero_real([4, 1, 1, 0])

                    question_expr = None

                    if difficulty == 1:
                        # Randomly select the form of the limit question
                        if random.choice([True, False]):
                            # Form: lim x -> 0 (sin(ax) / (bx))

                            expr = sp.sin(a * x) / (b * x)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                        else:
                            # Form: lim x -> 0 (bx / sin(ax))
                            expr = (b * x) / sp.sin(a * x)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                    elif difficulty == 2:
                        # Randomly select the form of the limit question
                        a = random.randint(1, 20)
                        b = random.randint(1, 20)
                        c = random.randint(1, 4)
                        if c == 4:
                            c = 3
                            d = 4
                        else:
                            d = random.choice([c, c, random.randint(c, 4), random.randint(c, 4), random.randint(c, 4)])
                        if random.choice([True, False]):
                            # Form: lim x -> 0 (sin^2(ax) / (bx^2))
                            expr = (sp.sin(a * x) ** d) / (b * x ** c)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                        else:
                            # Form: lim x -> 0 (bx^2 / sin^2(ax))
                            expr = (b * x ** d) / (sp.sin(a * x) ** c)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                    elif difficulty == 3:
                        a = random.randint(1, 10)
                        b = random.randint(11, 20)
                        # Randomly select the form of the limit question
                        if random.choice([True, False]):
                            # Form: lim x -> 0 (sin(ax) / sin(bx))
                            expr = sp.sin(a * x) / sp.sin(b * x)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                        else:

                            expr = sp.sin(b * x) / sp.sin(a * x)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                    elif difficulty == 4:

                        choice = random.choice([1, 2, 3, 4])
                        if choice == 1:
                            # Form: lim x -> 0 (1 - cos(ax) / bx^2)
                            c = random.choice([1, 2, 2, 2, 2])
                            expr = (1 - sp.cos(a * x)) / (b * x ** c)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                        elif choice == 2:

                            c = random.choice([3, 4, 2, 2, 2, 2])
                            expr = (b * x ** c) / (1 - sp.cos(a * x))
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                        elif choice == 3:
                            c = random.choice([1, 2, 2, 2, 2])
                            expr = (1 - sp.cos(a * x)) / (sp.sin(b * x) ** c)
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                        else:
                            c = random.choice([3, 4, 2, 2, 2, 2])
                            if b ** c >= 200:
                                c = 2
                                b = random.choice([3, 4, 5, 6, 7, 8])
                            expr = sp.sin(b * x) ** c / (1 - sp.cos(a * x))
                            limit = sp.limit(expr, x, 0)
                            question_expr = sp.Limit(expr, x, 0, dir=limit_dir)
                    elif difficulty == 5:
                        p = random.randint(1, 9)
                        q = random.choice([i for i in range(-9, 10) if i != 0])
                        a = b = 1
                        transformed_x = p * x + q
                        limit_value = sp.Rational(-q, p)
                        sub_difficulty = random.choice([1, 2, 4])
                        if sub_difficulty == 1:
                            if random.choice([True, False]):
                                expr = sp.sin(a * transformed_x) / (b * transformed_x)
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                            else:
                                expr = (b * transformed_x) / sp.sin(a * transformed_x)
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                        elif sub_difficulty == 2:
                            c = random.randint(1, 4)
                            if c == 4:
                                c = 3
                                d = 4
                            else:
                                d = random.choice([c, c, random.randint(c, 4), random.randint(c, 4), random.randint(c, 4)])
                            if random.choice([True, False]):
                                expr = (sp.sin(a * transformed_x) ** d) / (b * transformed_x ** c)
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                            else:
                                expr = (b * transformed_x ** d) / (sp.sin(a * transformed_x) ** c)
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                        elif sub_difficulty == 4:
                            choice = random.choice([1, 2, 3, 4])
                            if choice == 1:
                                c = random.choice([1, 2, 2, 2, 2])
                                expr = (1 - sp.cos(a * transformed_x)) / (b * transformed_x ** c)
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                            elif choice == 2:
                                c = random.choice([3, 4, 2, 2, 2, 2])
                                expr = (b * transformed_x ** c) / (1 - sp.cos(a * transformed_x))
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                            elif choice == 3:
                                c = random.choice([1, 2, 2, 2, 2])
                                expr = (1 - sp.cos(a * transformed_x)) / (sp.sin(b * transformed_x) ** c)
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                            else:
                                c = random.choice([3, 4, 2, 2, 2, 2])
                                if b ** c >= 200:
                                    c = 2
                                    b = random.choice([3, 4, 5, 6, 7, 8])
                                expr = sp.sin(b * transformed_x) ** c / (1 - sp.cos(a * transformed_x))
                                limit = sp.limit(expr, x, limit_value)
                                question_expr = sp.Limit(expr, x, limit_value, dir=limit_dir)
                        other_solutions = [0, 1, 2, sp.Rational(1, 2), random.randint(3, 9)]
                        other_solutions.remove(limit)
                    elif difficulty == 6:
                        c = random.randint(-20, 20)
                        if random.choice([True, False]):
                            d = random.randint(-20, 20)
                            # Form: lim x -> -d/c (sin(ax + b) / (cx + d))
                            expr = sp.sin(a * x + b) / (c * x + d)
                            limit = sp.limit(expr, x, -d / c, dir=limit_dir)
                            question_expr = sp.Limit(expr, x, -d / c, dir=limit_dir)
                        else:
                            d = random.randint(-20, 20)
                            # Form: lim x -> d/c (sin^2(ax - b) / (1 - cos(cx - d)))
                            expr = sp.sin(a * x - b) ** 2 / (1 - sp.cos(c * x - d))
                            limit = sp.limit(expr, x, d / c, dir=limit_dir)
                            question_expr = sp.Limit(expr, x, d / c, dir=limit_dir)

                    return expr, limit, question_expr, sp.latex(limit), other_solutions

                if difficulty != 5:
                    q, a, question_exp, b, other_Solution = generate_limit_question(difficulty)

                    questions_and_answers.append(ServiceResponce(
                        question = LatexStringModel(
                            string_value="Evaluate the following one-sided limit. {} ",
                            placeholders=[LatexObject(question_exp, False, True)]
                        ).convert_to_latex(),
                        correct_solution = LatexStringModel(
                            string_value="{}",
                            placeholders=[LatexObject(a)]
                        ).convert_to_latex(),
                        other_solutions=[LatexStringModel(
                            string_value="{}",
                            placeholders=[LatexObject(a)]
                        ).convert_to_latex() for a in generateCustomeAnswerList(Rule.ADD.value, a, 4)]
                    ))
                else:
                    q, a, question_exp, b, other_Solution = generate_limit_question(difficulty)

                    questions_and_answers.append(ServiceResponce(
                        question = LatexStringModel(
                            string_value="Evaluate the following one-sided limit. {} ",
                            placeholders=[LatexObject(question_exp, False, True)]
                        ).convert_to_latex(),
                        correct_solution=LatexStringModel(
                            string_value="{}",
                            placeholders=[LatexObject(a)]
                        ).convert_to_latex(),
                        other_solutions=[LatexStringModel(
                            string_value="{}",
                            placeholders=[LatexObject(a)]
                        ).convert_to_latex() for a in other_Solution]
                    ))
            else:
                q_no = 0

                while q_no < 1:
                    if difficulty == 1:
                        # Form: lim x -> a (x^2 - a^2) / (x - a)
                        a = random_non_zero_real([4, 1, 1, 0], 500, 2)
                        expr = (symbol ** 2 - a ** 2) / (symbol - a)
                    elif difficulty == 2:
                        # Form: lim x -> a (x^d - a^d) / (x - a) where 3 <= d <= 5 and -500 < a^d < 500
                        d = random.randint(3, 5)
                        a = random_non_zero_real([4, 1, 1, 1], 500, d)

                        while not (abs(a ** d) < 500):
                            d = random.randint(3, 5)
                            a = random_non_zero_real([4, 1, 1, 0], 500, d)

                        expr = (symbol ** d - a ** d) / (symbol - a)
                    elif difficulty == 3:
                        # Form: lim x -> a (x^d - a^d) / (x^c - a^c) where 2 <= c, d <= 5 and -500 < a^c, a^d < 500
                        powers = [2, 3, 4, 5]
                        c = random.choice(powers)
                        powers.remove(c)
                        d = random.choice(powers)
                        a = random_non_zero_real([4, 1, 1, 1], 500, max(c, d))

                        while not (abs(a ** c) < 500) or not (abs(a ** d) < 500):
                            powers = [2, 3, 4, 5]
                            c = random.choice(powers)
                            powers.remove(c)
                            d = random.choice(powers)
                            a = random_non_zero_real([4, 1, 1, 1], 500, max(c, d))
                        expr = (symbol ** d - a ** d) / (symbol ** c - a ** c)
                    elif difficulty == 4:
                        # Form: lim x -> a (x^(1/d) - a^(1/d)) / (x^(1/c) - a^(1/c)) where d, c = 1, 2, 3 and d not equal c. If d or c even a > 0
                        value_list = [1, 2, 3]
                        c = random.choice(value_list)
                        value_list.remove(c)
                        d = random.choice(value_list)
                        a = random_non_zero_real([4, 0, 0, 0])
                        if c % 2 == 0 or d % 2 == 0:
                            a = abs(a)
                        expr = (symbol ** (sp.Rational(1, d)) - a ** (sp.Rational(1, d))) / (
                                symbol ** (sp.Rational(1, c)) - a ** (sp.Rational(1, c)))
                    elif difficulty == 5:
                        random_factored_expression_generator = RandomFactoredExpressionGenerator(symbol)
                        # Form: lim x -> a (polynomial of degree 1, 2, 3 with a factor (x - a)) / (polynomial of degree 1, 2, 3 with a factor (x - a))
                        # where all the polynomial easily factorisable and make sure that the denominator does not have a double root at x = a. a can be integers (slightly higher probability), fractions.
                        a = random_non_zero_real([4, 1, 0, 0])
                        numerator_degree = random.randint(1, 3)
                        if numerator_degree == 1:
                            denominator_degree = random.randint(2, 3)
                        else:
                            denominator_degree = random.randint(1, 3)
                        numerator = random_factored_expression_generator.generate_fully_factorizable_expression(
                            symbol, a,
                            numerator_degree,
                            avoid_double_root_at=None).expand()
                        denominator = random_factored_expression_generator.generate_fully_factorizable_expression(
                            symbol,
                            a,
                            denominator_degree,
                            avoid_double_root_at=a).expand()
                        expr = numerator / denominator
                    else:
                        raise ValueError('Unsupported difficulty level')

                    question_expr = sp.Limit(expr, symbol, a, dir=limit_dir)
                    try:
                        answer = sp.limit(expr, symbol, a, dir=limit_dir)
                        q_no += 1
                    except ValueError:
                        continue
                    questions_and_answers.append(ServiceResponce(
                        question=LatexStringModel(
                                string_value="Evaluate the following one-sided limit. {}",
                                placeholders=[
                                    LatexObject(value=question_expr, is_in_latex_format=False,
                                                is_double_dollar_required=True),
                                ]
                            ).convert_to_latex(),
                        correct_solution=LatexStringModel(
                                string_value="{}",
                                placeholders=[
                                    LatexObject(value=answer, is_in_latex_format=False, is_double_dollar_required=False),
                                ]
                            ).convert_to_latex(),
                        other_solutions=[LatexStringModel(
                            string_value="{}",
                            placeholders=[LatexObject(a)]
                        ).convert_to_latex() for a in generateCustomeAnswerList(Rule.MULTIPLY.value, answer, 4)]
                    ))
        return questions_and_answers

