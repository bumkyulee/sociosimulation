# -*- coding: utf-8 -*-
from Constants import *

class Person:
	def __init__(self,age):
		self.consumeWeight = consumeWeight[age]
		self.cash = 0
		self.company = None

	def earn(self,cash):
		self.cash += cash

	# 산업 별 얼마 쓰는지를 리턴
	def buy(self):
		consume = dict()
		total = sum(self.consumeWeight.values())
		for key, value in self.consumeWeight.items():
			consume[key] = value*self.cash/total
		self.cash = 0
		return consume

	def hired(self,company):
		self.company = company

	def fired(self):
		self.company = None