import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import base64
from io import BytesIO

def is_constant_function(sympy_function):
    derivative = sp.diff(sympy_function, sp.symbols('x'))
    return derivative == 0

class FunctionInformation:
    def __init__(self, sympy_function, equal_points=None, inEqual_points=None, line_color='blue', point_color='red', edge_color='red', x_range=(-10, 10),is_infinity=False,y_limit=50):
        self.sympy_function = sympy_function
        self.equal_points = equal_points if equal_points is not None else []
        self.inEqual_points = inEqual_points if inEqual_points is not None else []
        self.line_color = line_color
        self.point_color = point_color
        self.edge_color = edge_color
        self.x_range = x_range
        self.y_limit =y_limit
        self.is_infinity = is_infinity



def generate_graph(functions, num_points= 1000,legend=False,is_infinity= False,  y_limit=20):
    x = sp.symbols('x')
    plt.figure(figsize=(10, 6))
    
    for function in functions:
        sympy_function = function.sympy_function
        equal_points = function.equal_points
        inEqual_points = function.inEqual_points
        line_color = function.line_color
        point_color = function.point_color
        edge_color = function.edge_color
        function_x_range = function.x_range
        
        f_lambdified = sp.lambdify(x, sympy_function, modules=['numpy'])
        x_vals = np.linspace(function_x_range[0], function_x_range[1], num_points)
        y_vals = f_lambdified(x_vals)
        if is_constant_function(sympy_function):
            y_vals = [f_lambdified(x_vals)]* len(x_vals)

        if function.is_infinity:
            y_vals[np.isnan(y_vals)] = np.nan  # Keep NaNs (won't plot them)
            y_vals[np.abs(y_vals) > y_limit] = np.nan  # Clip extreme values
        plt.plot(x_vals, y_vals, color=line_color, label=str(sympy_function))
        
        for point in equal_points:
            plt.plot(point[0], point[1], 'o', color=point_color)
        
        for point in inEqual_points:
            plt.scatter(point[0], point[1], s=50, marker='o', facecolors='none', edgecolors=edge_color)

        
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
  
    if legend:
        plt.legend()
    plt.grid(True)
    # plt.show()
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    
    return img_base64

# Test functions
# x = sp.symbols('x')
# f1 = x**2
# f2 = x**3
# functions_details = [
#     FunctionInformation(sympy_function=f1,
#                         equal_points=[(1, 1), (2, 4), (3, 9)],
#                         inEqual_points=[(4, 16), (5, 25), (6, 36)],
#                         line_color='green',
#                         point_color='blue', 
#                         edge_color='black',
#                         x_range=(-10, 10)),
#     # FunctionInformation(sympy_function=f2, equal_points=[(1, 1), (2, 8), (3, 27)], inEqual_points=[(4, 64), (5, 125), (6, 216)], line_color='red', point_color='yellow', edge_color='purple', x_range=(-5, 5)),
#     FunctionInformation(equal_points=[(4, 1), (3, 8), (2, 27)], inEqual_points=[(1, 64), (2, 125), (3, 216)], line_color='red', point_color='yellow', edge_color='purple', x_range=(-5, 5))
# ]
# print(generate_graph(functions_details))
