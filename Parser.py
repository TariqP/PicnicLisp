from pyparsing import nestedExpr

class Parser:
	def parse(self, input):
		# Split based on parentheses.
		try:
			tokenized = self.tokenize(input)

			# Convert ints to ints. Keep other atoms as strings
			return self.convertInts(tokenized)
		except Exception as e:
			raise e

	def convertInts(self, tokenized):
		return tokenized

	def tokenize(self, input):
		""" Split into nest arrays of tokens (not yet atoms, lists) """

		# # If we have just one element, don't pass to the parser
		# token = input.strip().split()
		# if (len(token) == 1): return token

		# If we don't have a list, but just a symbol
		if input.find('(') == -1:
			return input 

		# Otherwise pass to parser and error check
		try:
			parsedExp = nestedExpr('(',')').parseString(input).asList()
			# Return first element b/c of unnecessary wrapping w/ 
			# list done by library
			return parsedExp[0]
		except:
			raise Exception("Invalid Lisp expression")


		""" NON Py Parsing version - Implementation incomplete""" 
		# # Init our recursive breakdown to the first open parantheses
		# toTokenize = input
		# openInd = toTokenize.find("(")

		# # If there were no open parantheses...
		# if openInd == -1 return input
		
		# while openInd != -1:

		# 	# Grab the inside and outside paranthesis
		# 	openInd = toTokenize.find("(")
			
		
		# return input