import unittest
from main import PicnicLisp

class Tests(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(Tests, self).__init__(*args, **kwargs)
		self.lisper = PicnicLisp()		

	def testAddSimple(self):
		self.assertEquals(12, self.lisper.processLine("(+ 2 10)"))

	def testAddAdvanced(self):
		self.assertEquals(-8, self.lisper.processLine("(+ -2 10 (+ 2 3) -21)"))

	def testEq(self):
		self.assertEquals(True, self.lisper.processLine("(eq? (+ 3 2) (+ 2 3) )"))

	def testDefineSimple(self):
		self.lisper.processLine("(define bob (+ 2 3))")
		self.assertEquals(5, self.lisper.processLine("bob"))

	def testDefineAdvanced(self):
		self.lisper.processLine("(define a (+ 5 3))")
		self.lisper.processLine("(define b (+ 5 a))")
		self.assertEquals(21, self.lisper.processLine("(+ a b)"))

	def testCons(self):
		self.lisper.processLine("(define bob (cons 1 2))")
		self.assertEquals(['1', '2'], self.lisper.processLine("bob"))

	def testCarSimple(self):
		self.assertEquals(1, self.lisper.processLine("(car (1 2))"))

	def testCarAdvanced(self):
		self.lisper.processLine("(define bob '(1 2 3))")
		self.assertEquals(1, self.lisper.processLine("(car bob)"))
		self.assertEquals(1, self.lisper.processLine("(car (cons 1 2))"))

	def testCdrSimple(self):
		self.assertEquals(['2', '3'], self.lisper.processLine("(cdr (1 2 3))"))

	def testCdrAdvanced(self):
		self.lisper.processLine("(define bob '(1 2 3))")
		self.assertEquals(['3'], self.lisper.processLine("(cdr (cdr bob))"))
		self.assertEquals([], self.lisper.processLine("(cdr (cdr (cdr bob)))"))

if __name__ == '__main__':
    unittest.main()