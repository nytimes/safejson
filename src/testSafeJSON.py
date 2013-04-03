import unittest, logging, safeJSON, json, os, pickle
from safeJSON import SafeNone


class TestSafeJSON(unittest.TestCase):
	
	def testSafeList(self):
		logger.info("Testing SafeList")
		l = safeJSON.SafeList()
		l.append('a')
		
		# test get
		self.assertTrue(l[0] == 'a', "Expected list to contain 'a' at position zero.")
		self.assertTrue(l[1] is SafeNone, "Expected list to return SafeNone")

		exceptionThrown = False
		try:
			l['not_a_key']
		except:
			exceptionThrown = True
		self.assertTrue(exceptionThrown, 'Expected access of non integer index to raise an exception.')

		# test delete
		del(l[0])
		self.assertTrue(l[0] is SafeNone, "Expected list to return SafeNone")		
		
		exceptionThrown = False
		try:
			del(l['not_a_key'])
		except:
			exceptionThrown = True
		self.assertTrue(exceptionThrown, 'Expected deletion of non integer index to raise an exception.')


	def testSafeDict(self):
		logger.info("Testing SafeDict")
		d = safeJSON.SafeDict()
		
		# test get
		d[0] = 'a'
		self.assertTrue(d[0] == 'a', "Expected dict to contain 'a' at for key 0.")
		self.assertTrue(d[1] is SafeNone, "Expected list to return SafeNone")		
		
		# test delete
		del(d[0])
		self.assertTrue(d[0] is SafeNone, "Expected list to return SafeNone")		
		del(d['not_a_key'])


	def testSafeNone(self):
		logger.info("Testing SafeNone")
		self.assertTrue(SafeNone == None, "Expected SafeNone to == None")
		self.assertTrue(SafeNone < 0, "Expected SafeNone to < 0")
		self.assertTrue(SafeNone <= 0, "Expected SafeNone to <= 0")
		self.assertFalse(SafeNone > 0, "Expected SafeNone to not be > 0")
		self.assertFalse(SafeNone >= 1, "Expected SafeNone to not be >= 1")
		self.assertTrue(SafeNone >= 0, "Expected SafeNone to be >= 0")
		self.assertFalse(SafeNone != SafeNone, "Expected SafeNone to == SafeNone")
		self.assertTrue(SafeNone != 1, "Expected SafeNone to != 1")
		self.assertTrue(False if SafeNone else True, "Expected SafeNone to evaluate to False")
		
		# test containment
		self.assertFalse('test' in SafeNone, "A SafeNone should never contain an object.")

		# test iteration
		for i in SafeNone:
			self.assertTrue(False ,"It should not be possible to iterate over a SafeNone object.")
		

		# test dict functions
		for i in SafeNone.iteritems():
			self.assertTrue(False ,"It should not be possible to iterate over the items of a SafeNone object.")	

		for i in SafeNone.iterkeys():
			self.assertTrue(False ,"It should not be possible to iterate over the keys of a SafeNone object.")	

		for i in SafeNone.itervalues():
			self.assertTrue(False ,"It should not be possible to iterate over the keys of a SafeNone object.")	

		for k,v in SafeNone.items():
			self.assertTrue(False ,"It should not be possible to iterate over a SafeNone object.")

		for k in SafeNone.keys():
		 	self.assertTrue(False ,"It should not be possible to iterate over the keys of a SafeDict object.")

		for k in SafeNone.values():
		 	self.assertTrue(False ,"It should not be possible to iterate over the values of a SafeDict object.")

	 	for k in SafeNone.viewitems():
		 	self.assertTrue(False ,"It should not be possible to iterate over the items of a SafeDict object.")

	 	for k in SafeNone.viewkeys():
		 	self.assertTrue(False ,"It should not be possible to iterate over the keys of a SafeDict object.")

		for k in SafeNone.viewvalues():
		 	self.assertTrue(False ,"It should not be possible to iterate over the values of a SafeDict object.")
		
 		self.assertTrue(SafeNone.copy() is SafeNone, "Expected SafeNone.copy() to be SafeNone.")
		self.assertTrue(SafeNone.get('any_key') is SafeNone, "Expected SafeNone.get() to be SafeNone.")
		self.assertTrue(SafeNone.has_key('any_key') is False, "Expected SafeNone.has_key('any_key') to be False.")
		self.assertTrue(SafeNone.clear() is None, "Expected dict-like behavior for SafeNone.clear().")
		self.assertTrue(SafeNone.pop() is SafeNone, "Expected SafeNone.pop() to be SafeNone.")
		
		exceptionRaisers = [SafeNone.popitem, SafeNone.setdefault, SafeNone.update, SafeNone.fromkeys]
		for exceptionRaiser in exceptionRaisers:
			exceptionRaised = False
			try:
				exceptionRaiser()
			except:
				exceptionRaised = True
			self.assertTrue(exceptionRaised, "Expected call to SafeNone.{0}() to raise an exception.".format(exceptionRaiser.__name__))

		del(SafeNone['fail'])

		# test list functions
		y = [1,2]
		self.assertTrue(SafeNone + y is y, "Expected SafeNone + y is y to be y.")
		del(SafeNone[1:5])
		self.assertTrue(SafeNone[1:5] is SafeNone, "Expected SafeNone[1:5] to be SafeNone.")
		self.assertTrue(SafeNone * y is SafeNone, "Expected SafeNone * y to be SafeNone.")
		self.assertTrue(y * SafeNone is SafeNone, "Expected y * SafeNone to be SafeNone.")
		self.assertTrue(SafeNone.__reversed__() is SafeNone, "Expected SafeNone.__reversed__() to be SafeNone.")
		self.assertTrue(SafeNone.count('a') == 0, "Expected SafeNone.count('a') to equal 0.")
		SafeNone.reverse()
		SafeNone.sort()

		exceptionRaisers = [
			"SafeNone *= 1", 
			"SafeNone += 1", 
			"SafeNone[1:5] = 10",
			"SafeNone.append('a')",
			"SafeNone.extend('a')",
			"SafeNone.insert('a')",
			"SafeNone.index('a')",
			"SafeNone.remove('a')",
		]
		for exceptionRaiser in exceptionRaisers:
			exceptionRaised = False
			try:
				eval(exceptionRaisers)
			except:
				exceptionRaised = True
			self.assertTrue(exceptionRaised, "Expected call to {0} to raise an exception.".format(exceptionRaiser))


		# test len
		self.assertTrue(len(SafeNone) == 0, "SafeNone must evaluate to having a length of 0.")
		

	def testLoads(self):
		logger.info("Testing loads")
		testObject = {
			'testInt' : 1,
			'testString' : 'String',
			'testArray' : ['item1','item2',3],
			'testDict' : {
				'dictKey1' : 'dictVal1',
				'dictKey2' : 'dictVal2'
			},
			'testNested1' : [{
				'dictKey3' : [1,2,3]
			}],
			'testNested2' : {
				'dictKey4' : [1,2,3]
			}
		}
		jsonString = json.dumps(testObject)
		safeJsonObject = safeJSON.loads(jsonString)
		self.doTestLoadLoads(testObject, safeJsonObject)

	def testLoad(self):
		logger.info("Testing load")
		testObject = json.load(open(os.sep.join(['testData','test.json'])))
		safeJsonObject = safeJSON.load(open(os.sep.join(['testData','test.json'])))
		self.doTestLoadLoads(testObject, safeJsonObject)

	def doTestLoadLoads(self, testObject, safeJsonObject):
		# Make sure the two objects are identical
		self.assertTrue(
			testObject == safeJsonObject, 
			"Expected parsed object to be the same as original object."
		)

		self.assertTrue(
			safeJsonObject['testMissing'] is SafeNone,
			"Expected to get a SafeNone object."
		)

		self.assertTrue(
			safeJsonObject['testArray'][3] is SafeNone,
			"Expected to get a SafeNone object."
		)

		self.assertTrue(
			safeJsonObject['testDict']['dictKey3'] is SafeNone,
			"Expected to get a SafeNone object."
		)
		
		self.assertTrue(
			safeJsonObject['testNested1'][0]['dictKey3'][3] is SafeNone,
			"Expected to get a SafeNone object."
		)

		self.assertTrue(
			safeJsonObject['testNested2']['dictKey4'][4] is SafeNone,
			"Expected to get a SafeNone object got {0}."
		)		

		self.assertTrue(
			safeJsonObject['notAKey'][0]['notAKeyAlso'][3]['stillNotAKey'] is SafeNone,
			"Expected to get a SafeNone object."
		)
		
	#def safeJSON

def configLogger():
	logger = logging.getLogger('test.safeJSON')
	logger.setLevel(logging.DEBUG)

	stderr_log_handler = logging.StreamHandler()
	logger.addHandler(stderr_log_handler)

	# nice output format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	stderr_log_handler.setFormatter(formatter)
	return logger

if __name__ == '__main__':
	logger = configLogger()
	unittest.TextTestRunner().run(unittest.makeSuite(TestSafeJSON,'test'))