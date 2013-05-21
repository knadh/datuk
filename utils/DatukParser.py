#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	A simple parser for the Datuk text corpus.
	Reads the entire text corpus and returns an iterable
	to traverse through all dictionary entries.

	Example:

	# ===
	parser = DatukParser("../corpus/datuk.corpus")

	for entry in parser.iterate_all():
		print(entry.id + " = " + entry.word)
		quit()


	# ===
	# each individual entry is a namedtuple
	Entry(
		letter=u'അ',
		word=u'അകമ്പ',
		origin='സം. അ-കമ്പ < കമ്പ്',
		literal='',
		id=u'101',

		definitions = [
			Definition(type=u'വി.', definition=u'ഇളക്കമില്ലാത്ത, ഉറച്ച'),
			Definition(type=u'വി.', definition=u'കുലുക്കമില്ലാത്ത')
		]
	)

	License: GNU GPLv3

	Kailash Nadh, http://nadh.in
	May 2013
"""


import codecs
from collections import namedtuple

class DatukParser:
	data = None

	def __init__(self, filename):
		"""Intitialize by loading the corpus into the memory"""

		try:
			self.data = codecs.open(filename, encoding = 'utf-8', errors = 'ignore').read()
			self.data = self.data.strip().split("\n\n")
		except Exception as e:
			print("Can't read " + filename)
			raise


	def get_all(self):
		"""Get all entries as a list"""
		entries = []

		for entry in self.iterate_all():
			entries.append(entry)

		return entries

	def iterate_all(self):
		"""Compile the line-break and tab separated records into data structures"""

		entry_head = namedtuple("Entry", "letter word origin literal id definitions")
		entry_defition = namedtuple("Definition", "type definition")
		entry = None

		# single record
		for item in self.data:
			lines = item.strip().split("\n")

			head = lines[0].split("\t") # first line is the word, type, id etc.

			if len(head) != 5:
				continue

			head = [h if h != "_" else "" for h in head]
			
			# the rest of the lines are definitions
			defns = []
			for defn in lines[1:]:
				defns.append( entry_defition( *[h if h != "_" else "" for h in  defn.strip().split("\t")] ) )

			# put it all together
			head.append(defns)
			entry = entry_head(*head)

			yield entry
