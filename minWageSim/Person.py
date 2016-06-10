# -*- coding: utf-8 -*-
from Constants import *

class Person:
	def __init__(self,age):
		self.consumeWeight = consumeWeight[age]
		self.consumeWeightSurplus = consumeWeightSurplus[age]
		self.cash = 0
		self.cashSurplus = 0
		self.company = None
		self.emergencyProportion = 0.5

	def earn(self,cash):
		self.cash += minWageWeekly
		self.cashSurplus += (cash-minWageWeekly)

	# 산업 별 얼마 쓰는지를 리턴
	def buy(self,emergencyRate):
		consume = dict()
		for key, value in self.consumeWeight.items():
			consume[key] = value*self.cash

		for key, value in self.consumeWeightSurplusTotal(emergencyRate).items():
			consume[key] += value*self.cashSurplus

		self.cash, self.cashSurplus = 0, 0
		return consume

	def consumeWeightSurplusTotal(self,emergencyRate):
		consumeRateTotal = dict()
		for key, value in self.consumeWeightSurplus.items():
			value *= (1-self.emergencyProportion)
			if key in emergencyRate:
				value += emergencyRate[key]*self.emergencyProportion
			consumeRateTotal[key] = value

		total = sum([x for x in consumeRateTotal.values()])
		if total == 0:
			print 'total is zero'
			return self.consumeWeight
		for key, value in consumeRateTotal.items():
			consumeRateTotal[key] = float(value) / total

		return consumeRateTotal

	def hired(self,company):
		self.company = company

	def fired(self):
		self.company = None