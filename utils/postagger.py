#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from collections import defaultdict, OrderedDict

WORDS = defaultdict(lambda: None)

for pair in open('./utils/dic/tag').read().split("\n"):
	if ":" in pair:
		WORDS[pair[:pair.find(":")]] = pair[pair.find(":")+1:]

def tag(list):
	tagged = OrderedDict()
	for w in list:
		tagged[w] = WORDS[w] if not re.match("[0-9]{8}", w) else "dt"
	return tagged