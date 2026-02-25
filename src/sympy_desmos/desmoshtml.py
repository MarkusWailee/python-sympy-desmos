import sympy as sp
import re
import webbrowser as web
from io import StringIO



class DesmosHtml:
    def __init__(self, path = "desmos.html", api_src="https://www.desmos.com/api/v1.11/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"):
        """
        Uses a StringIO in the backend. File writing does not happen until calling save_file()
        """

        self.buffer = StringIO()
        self.path = path
        self.api_src = api_src

    def write(self, left, right=None):
        """
        Writes a Desmos expression.

        Parameters
        ----------
        left : str or sympy expression
            Left-hand side of the expression.
        right : str or sympy expression, optional
            Right-hand side. If None, only left is written.

        Examples
        --------
        >>> import sympy
        >>> x, y, z = sympy.symbols("x y z")
        >>> f = sympy.Function("F")
        >>> desmos.write("F(x)", "x^2") # F(x) = x^2
        >>> desmos.write(f(x), x ** 2) # F(x) = x^2
        >>> desmos.write(x**2) # x^2
        >>> desmos.write(sympy.Matrix([x, y, z])) # (x,y,z)
        >>> desmos.write(sympy.Eq(x, 5)) # x = 5 with slider
        """
        left = left if isinstance(left, str) else sp.latex(left)
        right = right if isinstance(right, str) or right == None else sp.latex(right)
        expr = left if right == None else f"{left} = {right}"
        text = f"calculator.setExpression({{ latex: \"{expr}\" }});\n"
        self.buffer.write(text)

    def get_javasript(self):
        """
        Returns generated javascript based on Desmos api
        """


        text_s = """
var elt = document.getElementById(\"calculator\");
var calculator = Desmos.GraphingCalculator(elt);
        """
        text = self.buffer.getvalue()
        # match all vectors and replaces with '(group)'. group should not contain matrices
        pattern = re.compile(r"\\left\[\\begin\{matrix\}(((?!(begin|matrix)).)*)\\end\{matrix\}\\right\]")
        for match in pattern.finditer(text):
            text = text.replace(match.group(), '(' + match.group(1).replace(r"\\", ", ") + ')')
        text = text_s + text.replace("\\", "\\\\")

        return text

    def get_html(self):
        """
        Returns generated html/javascript based on Desmos api
        """

        text_s = f"""
<head><meta charset="UTF-8"></head>
<body style="background-color:#2A2A2A;" marginwidth="0px" marginheight="0px">
<script src="{self.api_src}"></script>
<div id="calculator"></div>
<script>
"""
        text_e = "\n</script>"
        return text_s + self.get_javasript() + text_e

    def save(self, path=None):
        """
        Saves generated html/javascript code to a file
        """
        self.path = path if path else self.path
        # write to the file
        text = self.get_html()
        if text:
            self.file = open(self.path, 'w')
            self.file.write(text)
            self.file.close()
            return True
        return False

    # saves html and opens in browswer
    def open_browser(self, new_window = True):
        """
        Saves generated html/javascript code and opens in browser.
        """
        if self.save():
            if new_window:
                web.open_new(self.path)
            else:
                web.open_new_tab(self.path)
        else:
            raise RuntimeError("Nothing to write to desmos")




class Desmos2D(DesmosHtml):
    def __init__(self, path="desmos2d.html", api_src="https://www.desmos.com/api/v1.11/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"):
        super().__init__(path, api_src)


class Desmos3D(DesmosHtml):
    def __init__(self, path="desmos3d.html", api_src="https://www.desmos.com/api/v1.12/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"):
        super().__init__(path, api_src)

