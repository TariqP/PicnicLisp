import Constants

class Evaluator:

	def __init__(self):
		# Define the map of defined symbols to values
		self.symbols = {}

		# Define the map of string to Form pointers
		self.forms = {'+': lambda x,y: x+y,
							'/': lambda x,y: x/y,
							'*': lambda x,y: x*y,
							'-': lambda x,y: x-y,
							Constants.EQ_FORM: lambda x,y: x == y,
							Constants.DEF_FORM: self.defineForm,
							Constants.QUOTE_FORM: self.quoteForm,
							Constants.CONS_FORM: self.consForm,
							Constants.CAR_FORM: self.carForm,
							Constants.CDR_FORM: self.cdrForm
							}

	def eval(self, tokenized):
		""" A recursive function that evaluates the nested, tokenized input """
		# ------- Symbol processing --------- #

		# Base case: if not a non-defined list, return the symbol
		if not isinstance(tokenized, list):
			# Call recursive print of symbol for nice printing of lists
			return self.getSymbolValue(tokenized)

		# ------- List processing ----------- #

		# Error check: if list and first element is not a Form
		form = tokenized[0]
		if form not in self.forms.keys():
			return tokenized
			# raise Exception("Invalid Lisp form: " + str(form))

		# Check that the number of arguments is correct
		self.checkArguments(form, tokenized)

		return self.execForm(form, tokenized)

	def checkArguments(self, form, tokenized):
		""" Ensures arguments are properly formatted """

		# Error checking for atom form
		if (form == Constants.ATOM_FORM or
				form == Constants.QUOTE_FORM or
				form == Constants.CAR_FORM) and len(tokenized) != 2:
			raise Exception(str(form) + " form accepts only 1 argument")

		# Error checking for eq form
		if (form == Constants.EQ_FORM or
			form == Constants.CONS_FORM) and len(tokenized) != 3:
			raise Exception(str(form) + " form accepts only 2 arguments")

		# Ensures the first arg to the define form is a definable symbol
		if (form == Constants.DEF_FORM):
			if len(tokenized) == 4 and tokenized[2] == "'":
				# We may have a " ' " to indicate a symbol
				pass
			elif len(tokenized) != 3:
				raise Exception(str(form) + " form accepts only 2 arguments") 

			if isinstance(tokenized[1], list) or tokenized[1].isdigit():
				raise Exception("First argument to define is not definable")

		# Car and cdr forms needs a list as its argument
		if (form == Constants.CAR_FORM or form == Constants.CDR_FORM) \
			and not isinstance(self.getSymbolValue(tokenized[1]), list):
			raise Exception(str(form) + " form accepts only a list" + \
				" as its arg")


	def execForm(self, form, tokenized):
		""" Executes the correct (special or normal) form based on input """

		# ------ Special Forms ---------- #
		if form == Constants.DEF_FORM:
			if tokenized[2]== "'":
				# What follows is a symbol so don't evaluate it
				self.forms[form](tokenized[1], tokenized[3])
			else:
				# It's ok to evaluate
				self.forms[form](tokenized[1], self.eval(tokenized[2]))
			return None

		elif form == Constants.QUOTE_FORM:
			(form, rest) = tokenized
			return self.forms[form](rest)

		elif form == Constants.CONS_FORM:
			return self.forms[form](tokenized[1], tokenized[2])

		elif form == Constants.CAR_FORM or form == Constants.CDR_FORM:
			return self.forms[form](self.eval(tokenized[1]))

		# ------ Normal Forms ----------- #

		# Apply this Form to the first symbol with the rest of symbols rec
		runningVal = self.eval(tokenized[1])

		for symbol in tokenized[2:]:
			runningVal = self.forms[form](runningVal, self.eval(symbol))

		return runningVal

	def getSymbolValue(self, symbol):
		""" If symbol is defined symbol or int, returns appropriate value.
		If not, just return the symbol as passed in"""
		
		# Check if this is an int
		try:
		    return int(symbol)
		except Exception:
		    pass

		# Otherwise check if it's a defined symbol
		if symbol in self.symbols.keys():
			return self.symbols[symbol]
		else:
			return symbol

	def defineForm(self, x, y):
		""" Defines the "define" Form. That's meta... """
		self.symbols[x] = y

	def quoteForm(self, tokenized):
		""" Wrapper fucntion for getPrintableForm """
		return self.getPrintableForm("", tokenized)

	def getPrintableForm(self, exp, tokenized):
		""" Returns the expression in neatly formatted form """
		# base case, just an atom
		if not isinstance(tokenized, list):
			return tokenized

		# otherwise loop through list and recurse
		else:
			exp += "("
			for token in tokenized:
				exp += self.getPrintableForm("", token) + " "
			exp = exp[:-1]				
			exp += ")"
			return exp

	def consForm(self, x, y):
		""" Takes in 2 symbols and sticks them together as a list """
		return [x,y]

	def carForm(self, x):
		""" Takes in a list or symbol defined as list 
			and returns the first arg """
		return self.getSymbolValue(x[0])

	def cdrForm(self, x):
		""" Takes in a list or symbol defined as list 
			and returns everything but the first """
		return x[1:]
		