import json
import safeJSON
from safeJSON import SafeNone

SAMPLE_JSON_1 = """
	{"results": [{
        "child_items": [{
            "name": "child item 1"
        }], 
        "name": "result 1"
    }]}
	"""

SAMPLE_JSON_2 = """
	{	
	    "results": [{
            "name": "result 1"
        }]
	}
	"""

SAMPLE_JSON_3 = """
	{}
"""

def parseWithJSON():
	count = 0
	for jsonString in [SAMPLE_JSON_1, SAMPLE_JSON_2, SAMPLE_JSON_3]:
		count += 1
		print 'Object {0}:'.format(count)

		o1 = json.loads(jsonString)

		# print first result name
		if 'results' in o1 and len(o1['results']) > 0:
			result = o1['results'][0]
			if 'name' in result:
				print "Name: {0}".format(result['name'])

		# print first child name
		if 'results' in o1 and len(o1['results']) > 0:
			result = o1['results'][0]
			if 'child_items' in result and len(result['child_items']) > 0:
				childItem = result['child_items'][0]
				if 'name' in childItem:
					print "Child Name: {0}".format(childItem['name'])


def parseWithSafeJSON():
	count = 0
	for jsonString in [SAMPLE_JSON_1, SAMPLE_JSON_2, SAMPLE_JSON_3]:
		count += 1
		print 'Object {0}:'.format(count)
		o1 = safeJSON.loads(jsonString)

		# print first result name
		if o1['results'][0]['name']:
			print "Name: {0}".format(o1['results'][0]['name'])

		# print first child name
		if o1['results'][0]['child_items'][0]['name']:
			print o1['results'][0]['child_items'][0]['name']

		
if __name__ == '__main__':
	parseWithJSON()
	print ""
	parseWithSafeJSON()