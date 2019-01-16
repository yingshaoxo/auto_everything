class Password():
    """
    This is for hash password generation
    """
    def __init__(self, base_string):
        """
        base_string: a base_string for PassWord generation
        """
        import hashlib
        self.hashlib = hashlib
        self.__base_data = base_string.encode("utf-8")

    def update(self, *args, length=12):
        """
        return a hashed string based on the text you were given
        you can use the returned string as your password

        Parameters
        ----------
        *args: 
            any string

        length: int
            password length
        """
        data_list = [string.encode("utf-8") for string in args]

        m = self.hashlib.sha512()
        m.update(self.__base_data)

        for data in data_list:
            m.update(data)

        result = m.hexdigest()
        result = result[:length-1]
        result = "A" + result
        return result


class Calculator():
    """
    A class for advanced mathematics
    """
    def __init__(self):
        import sympy
        self.sympy = sympy
        self.sympy.init_printing(use_unicode=True)

    def symbol(self, symbol_string):
        """
        define a unknown variable

        Parameters
        ----------
        symbol_string: string
            for example, `x`
        """
        return self.sympy.Symbol(symbol_string)

    def simplify(self, expression, use_latex=True):
        """
        simplify an expression

        Parameters
        ----------
        expression: string
            for example, `(x^2)^2`
        """
        r = self.sympy.simplify(expression)
        if use_latex == False:
            return str(r)
        else:
            r = self.sympy.latex(r)
            return r

    def differential(self, expression, variable, times=1, use_latex=True):
        """
        get derivative of an expression

        Parameters
        ----------
        expression: string
            for example, `(x^2)^2`

        variable: string or symbol
            for example, `x` or symbol('x')

        times: int
            if you want to get second derivative of an expression, you should set it to `2`
        """
        r = self.sympy.diff(expression, variable, times)
        if use_latex == False:
            return str(r)
        else:
            r = self.sympy.latex(r)
            return r

    def integral(self, expression, variable, use_latex=True):
        """
        get integration of an expression

        Parameters
        ----------
        expression: string
            for example, `(x^2)^2`

        variable: string or symbol
            for example, `x` or symbol('x')
        """
        r = self.sympy.integrate(expression, variable)
        if use_latex == False:
            return str(r)
        else:
            r = self.sympy.latex(r)
            return r


if __name__ == "__main__":
    pass
