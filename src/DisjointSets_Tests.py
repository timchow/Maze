from DisjointSets import DisjointSets
import unittest
import numpy as np


class MyTest(unittest.TestCase):
	def test_AddElements(self):
		numElements = 5
		test = DisjointSets(numElements)
		
		self.assertEqual(test.uptrees, list(np.repeat(-1,numElements)))
		
	def test_FindRoot(self):
		numElements = 5
		test = DisjointSets(numElements)
		test.uptrees = [2,2,-4,-1,2]
		
		self.assertEqual(test.FindRoot(2), 2)
		self.assertEqual(test.FindRoot(0), 2)
		self.assertEqual(test.FindRoot(-1), -1)
	
	def test_SetUnion(self):
		numElements = 5
		test = DisjointSets(numElements)
		
		self.assertEqual(test.SetUnion(0,2), True)
		self.assertEqual(test.uptrees, [2,-1,-2,-1,-1])
		
		self.assertEqual(test.SetUnion(0,2), False)
		self.assertEqual(test.uptrees, [2,-1,-2,-1,-1])
		
		self.assertEqual(test.SetUnion(1,2), True)
		self.assertEqual(test.uptrees, [2,2,-3,-1,-1])
		
		self.assertEqual(test.SetUnion(4,4),False)
		self.assertEqual(test.uptrees, [2,2,-3,-1,-1])
		
		self.assertEqual(test.SetUnion(5,5),False)
		self.assertEqual(test.uptrees, [2,2,-3,-1,-1])
		
		self.assertEqual(test.SetUnion(3,4),True)
		self.assertEqual(test.uptrees, [2,2,-3,4,-2])
		
		self.assertEqual(test.SetUnion(0,3),True)
		self.assertEqual(test.uptrees, [2,2,-5,4,2])
		
		self.assertEqual(test.SetUnion(-1,-2),False)
		self.assertEqual(test.uptrees, [2,2,-5,4,2])
		
if __name__ == '__main__':
	unittest.main()
