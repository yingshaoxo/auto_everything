from sympy import *

class Calculator():
    def __init__(self):
        # init_printing(use_unicode=True)
        pass

    def symbol(self, symbol_string):
        return Symbol(symbol_string)

    def simplify(self, expression, use_latex=True):
        r = simplify(expression)
        if use_latex == False:
            return str(r)
        else:
            r = latex(r)
            return r

    def differential(self, expression, variable, times=1, use_latex=True):
        r = diff(expression, variable, times)
        if use_latex == False:
            return str(r)
        else:
            r = latex(r)
            return r
    
    def integral(self, expression, variable, use_latex=True):
        r = integrate(expression, variable)
        if use_latex == False:
            return str(r)
        else:
            r = latex(r)
            return r
        

class Drawer():
    def __init__(self, func):
        import numpy as np
        import pylab
        from scipy.misc import derivative

        self.f = func
        self.vf = np.vectorize(func)
        self.derivative = np.vectorize((lambda x, h=0.0001, f=self.f, level=1:derivative(f, x, dx=1e-6, n=level)))

        self.pylab = pylab

    def draw(self, x_start=-5.0, y_end=5.0, level=0, color=None, label=r''):
        unit = 0.1
        x = np.arange(x_start, y_end + unit, unit)
        if level == 0:
            y = self.vf(x)
        else:
            y = self.derivative(x, level=level)
        if color == None:
            pylab.plot(x, y, label=label)
        else:
            pylab.plot(x, y, color, label=label)

    def point(self, x):
        pylab.plot(x, self.f(x), 'or')

    def draw_tangent(self, *args, width=1, color='--r', auto_adjust=False, left_zero=False, right_zero=False):
        f = self.f
        xlist = args
        width = width / 2
        x_min = min(xlist)
        x_max = max(xlist)

        for x in xlist:
            unit = 0.1
            if auto_adjust == False:
                tangent_x = np.arange(x-width, x+width+unit, unit)
            else:
                if left_zero == False and right_zero == False:
                    tangent_x = np.arange(x_min-width, x_max+width+unit, unit)
                elif left_zero == True and right_zero == True:
                    tangent_x = np.arange(x, x, unit)
                elif left_zero == True:
                    tangent_x = np.arange(x, x_max+width+unit, unit)
                elif right_zero == True:
                    tangent_x = np.arange(x_min-width, x+unit, unit)

            h = 0.01 # the micro difference in x
            f_prime = (f(x+h) - f(x)) / h # derivative
            tangent_y = f_prime * (tangent_x - x) + f(x) # tangent

            # plot of the point and the tangent
            pylab.plot(x, f(x), 'om', tangent_x, tangent_y, color)

    def find_derivetive_points(self, x_min, x_max, derivetive):
            f = self.f

            unit = 0.001
            x = np.arange(x_min, x_max+unit, unit)
            d = self.derivative(x)

            measure = 0.1
            zero_prime = np.absolute(np.array(d) - derivetive)
            zero_prime = np.where(zero_prime < measure)[0]

            result = []
            previous = 0
            for anyx in zero_prime:
                if (anyx - previous) != 1:
                    result.append(anyx)
                previous = anyx

            zero_prime = np.array(result)
            # print(zero_prime)

            result = x[zero_prime].tolist()
            rr = []
            for x in result:
                rr.append(self.find_exact_derivetive_point(x, derivetive))
            return rr

    def find_exact_derivetive_point(self, x_start, derivetive, x_width=1):
            f = self.f
            x_width = x_width / 2

            unit = 0.01
            x = np.arange(x_start - x_width, x_start + x_width + unit, unit)
            d = self.derivative(x)

            dd = np.absolute(d-derivetive)

            return x[np.argmin(dd)].tolist()

    def show(self):
        pylab.legend(loc='lower right')
        pylab.show()



# c = Calculator()
# c.simplify("(x**2/(2/2)) * a")
