# -*- coding: utf-8 -*-
import random

class Company:
	def __init__(self,industry):
		self.industry = industry
		self.profit = 0
		self.employees = list()

	def hrNum(self,wage):
		if self.profit < 0:
			return int(self.profit / wage)
		else:
			return int(self.profit / wage)

	def hire(self,person):
		self.employees.append(person)
		person.hired(self)

	def fire(self):
		person = self.employees.pop(0)
		person.fired()
		return person

	def earn(self,profit):
		self.profit += profit

	def pay(self,wage):
		for person in self.employees:
			person.earn(wage)
		self.profit -= wage*len(self.employees)

	def initProfit(self):
		self.profit = 0