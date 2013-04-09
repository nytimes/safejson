---------------------------
SafeJSON version 0.9 beta
---------------------------
(c)	2013 The New York Times Company

Created by Evan Sandhaus

---------
Overview:
---------
SafeJSON provides replacements for the 'load' and 'loads' methods in the standard Python 'json' module.  These new methods return objects that will never raise 'IndexError' or 'KeyError' exceptions for 'missing' values.  Instead a special value 'SafeNone' is returned.  'SafeNone' can itself be subscripted with any key or index.  Doing so will return another SafeNone object, so that SafeNone[<key|index>] == SafeNone.  In practice, this should allow developers to dramatically reduce the number of checks required to deal with JSON in the wild.

--------------
Important Note
--------------
Rather than raise exceptions for missing values, 'safeJSON' returns a special value 'SafeNone' instead.  This value can be treated in code as identical to 'None' with one major exception.  The SafeNone object is not identical to None object so checks of the following form will evaluate to False.

	if SafeNone is None:

SafeNone does have equality with None, however, so the following check will evaluate to True
	
	if SafeNone == None:

Additionally SafeNone implements all methods in the interface for python lists and dicts EXCEPT methods that attempt to store or modify the SafeNone object.  These methods will raise an Exception.

So you may make statements like this:

	x = SafeNone['some_key']

But statements like this will raise exeptions:
	
	SafeNone['some_key'] = x

The following methods will raise exceptions when invoked on SafeNone
	
	*	__setitem__
	*	__imul__
	*	__setslice__
	*	__setitem__
	*	append
	*	extend
	*	fromkeys
	*	insert
	*	setdefault
	*	update

------------
Installation
------------
To install safeJSON simply change into the directory containing this README and type the following command

	python setup.py install

----------------------
Rationale and Example:
----------------------
The standard approach to parsing JSON in python involves importing the 'json' module and using the 'load' or 'loads' method to parse a python object out of a JSON source.  For example:

	import json

	JSON_STRING = """
		{"results": [{
	        "child_items": [{
	            "name": "child item 1"
	        }], 
	        "name": "result 1"
	    }]}
	"""
	o = json.loads(JSON_STRING)

Now suppose we want to print out the value for the 'name' attribute of the first 'child_item' for the first 'result'.  We could simply write:

	print o['results'][0]['child_items'][0]['name']

But this is risky.  In the wild it is generally not advisable to access fields in a JSON object without first verifying that such fields exist.  After all, accessing a field that does not exist will raise an 'IndexError' or 'KeyError'. As such, we should modify our code to look something like this.

	if 'results' in o and len(o['results']) > 0:
		result = o['results'][0]
		if 'child_items' in result and len(result['child_items']) > 0:
			childItem = result['child_items'][0]
			if 'name' in childItem:
				print childItem['name']

This code is cumbersome to type and easy to mess up.  Moreover the tediousness of coding these kinds of checks likely leads some developers to omit them altogether, resulting in brittle code that makes dangerously narrow assumptions about the kind of input it's likely to encounter.

safeJSON solves this problem by introducing 'loads' and 'load' methods that return objects that will never raise 'IndexError' or 'KeyError' exceptions. As such we can write the above code as
	
	import safeJSON
	o = safeJson.loads(JSON_STRING)
	print o['results'][0]['child_items'][0]['name']

If we want to suppress output in the event that a specified value does not exist, we can introduce a simple check that will always evaluate to False if the value does not exist.
	
	if o['results'][0]['child_items'][0]['name']:
		print o['results'][0]['child_items'][0]['name']

We can even iterate over missing items without raising an exception.  Suppose, for the above example, we wanted to iterate over all the 'child_items' of the second result (which does not exist).  We could write:

	for childItem in o['results'][1]['child_items']:
		#this code will never be reached
		pass 

If we wanted to iterate over the key/value pairs in the first child_item of the second result (which again does not exist), we could write

	for key, value in o['results'][1]['child_items'][0].items():
		#this code will never be reached
		pass 

We can even check the length of a 'missing' list or dictionary.  
	
	x = len(o['results'][1]['child_items'])
	print x # will print 0

In this case the length will always be zero.


