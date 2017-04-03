import cmd
from Parser import Parser
from Evaluator import Evaluator

class PicnicLisp(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)

		""" Setup attributes of the command line prompt """
		self.prompt = 'PicnicLisp$ '
		self.parser = Parser()
		self.evaluator = Evaluator()

	def emptyline(self):
		""" On empty line, do nothing. Default impl repeats previous command """
		pass

	def processLine(self, line):
		""" Parses and evaluates a line. Separate function for testing
		purposes """
		try:
			tokenized = self.parser.parse(line)
			value = self.evaluator.eval(tokenized)
			return value
		except Exception as e:
			print e.message

	def default(self, line):
		""" Accepts all atoms and lists """
		interpreted = self.processLine(line)
		if interpreted != None: print interpreted
		else: print "Ok"


def main():
	""" Welcome user and allow to enter command line of interpreter """
	print "Welcome, welcome, welcome to PincicLisp. You can use basic Lisp"\
	+ " forms here. Have fun!"

	PicnicLisp().cmdloop()

if __name__ == "__main__":
    main()