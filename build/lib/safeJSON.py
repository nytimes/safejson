"""
safeJSON provides replacements for the 'load' and 'loads' methods in the
standard Python 'json' module.  These new methods return objects that will never
raise 'IndexError' or 'KeyError' exceptions for 'missing' values.  Instead a
special value 'SafeNone' is returned.  'SafeNone' can itself be subscripted with
any key or index.  Doing so will return another SafeNone object, so that
SafeNone[<key|index>] == SafeNone.  In practice, this should allow developers to
dramatically reduce the number of checks required to deal with JSON in the wild.

IMPORTANT NOTE:
Rather than raise exceptions for missing values, 'safeJSON' returns a special
value 'SafeNone' instead.  This value can be treated in code as identical to
'None' with one major exception.  The SafeNone object is not identical to None
object so checks of the following form will evaluate to False.

	if SafeNone is None:

SafeNone does have equality with None, however, so the following check will 
evaluate to True
	
	if SafeNone == None:
"""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import json, exceptions

# -----------------------------------------------------------------------------
# The Safe None Class
# -----------------------------------------------------------------------------
class SafeNoneClass(object):
	"""
	Since we can't subclass 'None' we create a new object that we use as None 
	in safeJSON.  This object behaves like None with several exceptions.  

	1) 	Attempting to get items on SafeNone (e.g. SafeNone['a'])  will return
	   	SafeNone.

	2)	Since we can't subclass or re-assign None the expression SafeNone is None
		will (unfortunatley) return false.  Accounting for this is the major 
		difference between using safeJSON and regular python.

	3)	This object writes itself out as 'SafeNone' not None.

	4)	len(SafeNone) evaluates to 0

	5)	'for i in SafeNone:' will not raise an exception

	6)	SafeNone.__hash__() always evaluates to 0

	7)	PyMongo will store SafeNone as 0

	8)	JSON.dumps(SafeNone) will yield 'SafeNone' not 'null'

	As a note this object will evaluate to 'False' in boolean expressions.
	"""
	 # Singleton instance

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(SafeNoneClass, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __getitem__(self, index):
		"""
		This method simulates array accesses.  Whenever this object is 
		subscripted, it returns itself.
		"""
		return self._instance

	def __ge__(self, o):
		if self.__eq__(o):
			return True
		return False

	def __gt__(self, o):
		return False

	def __le__(self, o):
		return True

	def __lt__(self, o):
		return True

	def __ne__(self, o):
		return not self.__eq__(o)

	def __str__(self):
		"""
		The printout of this object.
		"""
		return 'SafeNone'

	def __repr__(self):
		"""
		The printout of this object.
		"""
		return 'SafeNone'

	def __eq__(self, o):
		"""
		SafeNone is only equal to 0, None and itself.
		"""
		return o == 0 or o is self or o is None

	def __cmp__(self, o):
		"""
		Compares this object to another object.  Will always be 
		-1 except for objects that are __eq__ to this object.
		"""
		if self.__eq__(o):
			return 0
		return 1


	def __iter__(self):
		"""
		SafeNone implements the iterator interface, so it is returned for 
		iterator requests.
		"""
		return self

	def next(self):
		"""
		The iterator interface.  This object always raises a StopIteration
		exception on the first iterator access.
		"""
		raise StopIteration()

	def __len__(self):
		"""
		The length of this object is always zero.
		"""
		return 0

	def __hash__(self):
		"""
		The hash of this object is always zero.
		"""
		return 0

	def __delitem__(self, item):
		"""
		Implemented so that calls to del(SafeNone[k]) don't throw an
		exception.
		"""
		pass

	def items(self):
		"""
		items() method for when SafeNone is treated like a dictionary.
		"""
		return ()

	def keys(self):
		"""
		keys() method for when SafeNone is treated like a dictionary.
		"""
		return()

	def __contains__(self, x):
		"""
		contains() method for when SafeNone is treated like a dictionary.
		"""
		return False

	def __setitem__(self, *args, **kwargs):
		raise Exception("Cannot store values in SafeNone.")

	def fromkeys(self, *args, **kwargs):
		raise Exception("Cannot store values in SafeNone.")

	def update(self, *args, **kwargs):
		raise Exception("Cannot store values in SafeNone.")

	def setdefault(self, *args, **kwargs):
		raise Exception("Cannot store values in SafeNone.")

	def clear(self):
		return None;

	def copy(self):
		return SafeNone

	def get(self, *args, **kwargs):
		return SafeNone

	def has_key(self, *args, **kwargs):
		return False

	def iteritems(self):
		return ().__iter__()

	def iterkeys(self):
		return ().__iter__()

	def itervalues(self):
		return ().__iter__()

	def pop(self, *args, **kwargs):
		return SafeNone

	def popitem(self, *args, **kwargs):
		raise exceptions.KeyError()

	def values(self):
		return ()

	def viewitems(self):
		return ()

	def viewkeys(self):
		return ()
	
	def viewvalues(self):
		return ()

	# LIST METHODS

	def __add__(self, y):
		return y

	def __delslice__(self, *args, **kwargs):
		pass

	def __getslice__(self, i, j):
		return SafeNone

	def __iadd__(self, y):
		raise Exception("Cannot modify SafeNone.")

	def __imul__(self, y):
		raise Exception("Cannot modify SafeNone.")

	def __mul__(self, n):
		return SafeNone

	def __reversed__(self):
		return SafeNone

	def __rmul__(self, n):
		return SafeNone

	def __setslice__(self, i, j, y):
		raise Exception("Cannot store values in SafeNone.")

	def append(self, o):
		raise Exception("Cannot store values in SafeNone.")		
	
	def count(self, value):
		return 0

	def extend(self, iterable):
		raise Exception("Cannot store values in SafeNone.")

	def index(self, *args, **kwargs):
		raise exceptions.ValueError()

	def insert(self, o):
		raise Exception("Cannot store values in SafeNone.")

	def remove(self, value):
		raise exceptions.ValueError()

	def reverse(self):
		pass

	def sort(self):
		pass

# Our static reference to SafeNone - put it in the scope of the module
SafeNone = SafeNoneClass()

# -----------------------------------------------------------------------------
# The Safe list class
# -----------------------------------------------------------------------------
class SafeList(list):
	"""
	Class that behaves exactly like list except that accesses to items not in 
	the list will return SafeNone rather than raise an IndexError.
	"""
	def __getitem__(self, index):
		if index < len(self) or type(index) != type(0):
			return super(SafeList, self).__getitem__(index)
		return SafeNone

	def __delitem__(self, index):
		if index < len(self) or type(index) != type(0):
			return super(SafeList, self).__delitem__(index)

# -----------------------------------------------------------------------------
# The safe dict class
# -----------------------------------------------------------------------------
class SafeDict(dict):
	"""
	Class that behaves exactly like dict except that accesses to items not in 
	the dict will return SafeNone rather than raise a KeyError.
	"""
	def __getitem__(self, key):
		if key in self:
			return super(SafeDict, self).__getitem__(key)
		return SafeNone

	def __delitem__(self, key):
		if key in self:
			return super(SafeDict, self).__delitem__(key)

# -----------------------------------------------------------------------------
# The safeJSON parser class
# -----------------------------------------------------------------------------
class SafeJSONParser(object):
	"""
	Wrapper for json.load and json.loads that returns objets that have had 
	their dictionaries and lists replaced by their 'Safe' equivalents.
	"""
	def loads(self, s):
		o = json.loads(s)
		return self.transcode(o)

	def load(self, f):
		o = json.load(f)
		return self.transcode(o)

	def transcode(self, o):
		if type(o) == dict:
			safeO = SafeDict()
			for key, value in o.items():
				safeO[key] = self.transcode(value)
			return safeO
		elif type(o) == list:
			safeO = SafeList()
			for value in o:
				safeO.append(self.transcode(value))
			return safeO
		else:
			return o

# Put the load / loads module in the global scope
load  = SafeJSONParser().load
loads = SafeJSONParser().loads