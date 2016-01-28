import operator as op
from parsimonious.grammar import Grammar

class Mini(object):

	def __init__(self, env={}):
		env.update({'sum': lambda *args: sum(args)})
		self.env = env

	def parse(self,source):
		grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
							if not k.startswith('__') and hasattr(v, '__doc__')
													  and getattr(v, '__doc__'))
		return Grammar(grammar)['program'].parse(source)

	def eval(self, source):
		node = self.parse(source) if isinstance(source, str) else source
		method = getattr(self, node.expr_name, lambda *a: 'error')
		return method(node, [self.eval(n) for n in node])

	def program(self, node, children):
		'program = expr*'
		return children

	def expr(self, node, children):
		'expr = call / infix / assignment / number / name'
		return children[0]

	def call(self, node, children):
		'call = name "(" arguments ")"'
		name, _, arguments, _ = children
		return name(*arguments)

	def arguments(self, node, children):
		'arguments = argument*'
		return children

	def argument(self, node, children):
		'argument = expr _'
		return children[0]

	def infix(self, node, children):
		'infix = "(" _ expr _ operator _ expr _ ")" '
		_, _, expr1, _, operator, _, expr2, _, _ = children
		return operator(expr1, expr2)

	def operator(self, node, children):
		'operator = "+" / "-" / "*" / "/"'
		operators = {
			'+': op.add,
			'-': op.sub,
			'*': op.mul,
			'/': op.div
		}
		return operators[node.text]

	def assignment(self, node, children):
		'assignment = lvalue _ "=" _ expr'
		lvalue, _, _, _, expr = children
		self.env[lvalue] = expr 
		return expr

	def lvalue(self, node, children):
		'lvalue = ~"[a-z]+" _'
		return node.text.strip()

	def name(self, node , children):
		'name = ~"[a-z]+" _'
		return self.env.get(node.text.strip(), -1)

	def number(self, node, children):
		'number = ~"[0-9]+" _'
		return int(node.text)

	def _(self, node, children):
		'_ = ~"\s*"'