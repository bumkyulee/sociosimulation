# -*- coding: utf-8 -*-
from Constants import *

class Person:
	def __init__(self,age):
		self.consumeWeight = consumeWeight[age]
		self.consumeWeightSurplus = consumeWeightSurplus[age]
		self.cash = 0
		self.cashSurplus = 0
		self.company = None

	def earn(self,cash):
		self.cash += minWageWeekly
		self.cashSurplus += (cash-minWageWeekly)

	# 산업 별 얼마 쓰는지를 리턴
	def buy(self):
		consume = dict()
		for key, value in self.consumeWeight.items():
			consume[key] = value*self.cash
		for key, value in self.consumeWeightSurplus.items():
			consume[key] += value*self.cashSurplus
		self.cash, self.cashSurplus = 0, 0
		return consume

	def hired(self,company):
		self.company = company

	def fired(self):
		self.company = None