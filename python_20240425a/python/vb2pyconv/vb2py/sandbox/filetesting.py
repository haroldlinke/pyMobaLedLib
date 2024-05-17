#@+leo-ver=5-thin
#@+node:pap.120703001453.922: * @file sandbox/filetesting.py



"""Some testing to see if we can clean up the file access"""


class Test(object):

	def __init__(self, dataset):
		self.data = dataset
		self._datastream = iter(self.data)
		self.input = self.__next__

	def __getattribute__(self, name):
		print(("Get", name))
		return super(Test, self).__getattribute__(name)

	def __iter__(self):
		print("Getting iterator")
		return self

	def __next__(self):
		print("In next")
		d = self._datastream[:]
		while d:
			print(("Yielding", d[0]))
			yield d.pop()

	def __getitem__(self, index):
		print(("Getting item", index))
		return self._datastream[index]

if __name__ == "__main__":
	f = Test(list(range(20)))
	a, b, c = f

#@-leo
