import json

def readJson(filename):
	try:
		with open(filename, "r") as fp:
			data = json.load(fp)
		return data
	except:
		with open(filename, "r") as fp:
			data = fp.read().split("\n")
			new_data = []
			for item in data:
				try:
					new_data.append(json.loads(item))
				except:
					print(type(item))
					a = input("Enter: ")
		return new_data
def writeJson(filename, data):
	with open(filename, "w") as fp:
		json.dump(data, fp,indent=4)
