# -*- coding: utf-8 -*-
from __future__ import division
from Constants import *
from Person import *
from Company import *
import numpy as np
import random

class Economy:
	def __init__(self,minWageTarget,duration,lastTick):
		# 1. 모델마다 최저임금 / 달성시기가 다르다.
		self.minWageTarget = minWageTarget
		self.duration = duration
		self.minWage = minWageBegin
		self.industryAccount = dict()
		self.lastTick = lastTick

		# 2. 경제가 가질 Agent 모음
		self.people_employed = list()
		self.people_unemployed = list()
		self.companies = list()
		self.companies_bankrupted = list()

		# 3. 그래프 변수들 (주차, 소비총합, 고용률, 운영률)
		self.week = 0
		self.weeks = list()
		self.totalConsumes = list()
		self.employmentCount = list()
		self.openingCount = list()
		self.minWages = list()
		self.emergencyRate = dict()

	def run(self):
		# 1. 시뮬레이션 시작
		self.init()
		# 2. Tick
		for i in range(0, self.lastTick):
			print 'tick: ' + str(i)
			self.tick()
			# 3. Output 기록
			self.setOutputMeasures()

	def init(self):
		print 'init'
		# 1. 사람을 만든다. (분포 기준: 나이)
		for age, count in personAgeCount.items():
			for i in range(0,count):
				p = Person(age)
				self.people_unemployed.append(p)
		# 2. 회사를 만든다. (분포 기준: 산업)
		random.shuffle(self.people_unemployed)
		for industry, employmentRange in companyEmployeeCount.items():
			for employmentCount, companyCount in employmentRange.items():
				for i in range(0,companyCount):
					c = Company(industry)
					for j in range(0,employmentCount):
						p = self.people_unemployed.pop(0)
						c.hire(p)
					self.companies.append(c)

	# tick 한번
	def tick(self):
		# 0. 시간이 간다 & 최저임금이 오른다.
		self.week += 1
		self.setMinWage()
		weeklyWage = self.getWeeklyWage()

		# 1. 회사는 임금을 지불한다(행동주체) = 사람은 돈을 번다
		for company in self.companies:
			company.pay(weeklyWage)

		# 2. 사람은 물건을 산다(행동주체) = 회사는 돈을 번다
		# 1) 사람은 산업에 돈을 쓰고,
		self.people_employed = list()
		for company in self.companies:
			self.people_employed += company.employees

		self.industryAccount = dict.fromkeys(self.industryAccount.iterkeys(),0)
		self.emergencyNormalize()
		for person in self.people_employed:
			personConsume = person.buy(self.emergencyRate)
			self.industryAccount = { k: self.industryAccount.get(k, 0) + personConsume.get(k, 0) for k in set(self.industryAccount) | set(personConsume) }
		self.emergencyRateInit()

		'''
		# 2) 회사는 산업에 모인 돈을 고용인 수 순서대로, 파레토 비율대로 나눠갖는다.
		# 2-1) 산업별로 회사, 인원수를 정리한다.
		industryInfo = dict()
		for company in self.companies:
			if len(company.employees) > 0:
				if company.industry in industryInfo:
						industryInfo[company.industry]['employees'].append(len(company.employees))
						industryInfo[company.industry]['companies'].append(company)
				else:
					industryInfo[company.industry] = {'employees':[len(company.employees)],'companies':[company]}

		# 2-2) 산업별로 처리한다.
		for industry, info in industryInfo.items():
			# 2-3) 파레토 인원수 / 총 인원수를 정리한다.
			info['employees'].sort(reverse=True)
			paretoEmployeesPoint = int(len(info['employees'])/5)
			paretoEmployees = info['employees'][paretoEmployeesPoint]
			paretoEmployeesAbove = sum(info['employees'][:paretoEmployeesPoint])
			paretoEmployeesBelow = sum(info['employees'][paretoEmployeesPoint:])

			# 2-4) 기업이 파레토 Above / Below 중 어디있는지 판별하고 돈을 준다.
			paretoProfitAbove = self.industryAccount[industry]*0.8
			paretoProfitBelow = self.industryAccount[industry]*0.2
			for company in info['companies']:
				if len(company.employees) > paretoEmployees:
					profit = paretoProfitAbove*len(company.employees)/paretoEmployeesAbove
				else:
					profit = paretoProfitBelow*len(company.employees)/paretoEmployeesBelow
				company.earn(profit)

		# 2) 회사는 산업에 모인 돈을 고용인 수 비율로 나눠갖는다.
		industryEmployeeCount = dict()
		for company in self.companies:
			if company.industry in industryEmployeeCount:
				industryEmployeeCount[company.industry] += len(company.employees)
			else:
				industryEmployeeCount[company.industry] = len(company.employees)

		for company in self.companies:
			if industryEmployeeCount[company.industry] > 0:
				profit = self.industryAccount[company.industry]*len(company.employees)/industryEmployeeCount[company.industry]
				company.earn(profit)
		'''
		# 3) 회사는 산업에 모인 돈을 고용인 수 비율에 파레토 랜덤/미라클을 더해 나눠갖는다.
		industryInfo = dict()
		for company in self.companies:
			if len(company.employees) > 0:
				if company.industry not in industryInfo:
						industryInfo[company.industry] = dict()
				industryInfo[company.industry][company] = len(company.employees)

		for companies in industryInfo.values():
			paretoPortion = 0.01
			paretoMiracle = 0.3
			paretoValues = sorted(list(np.random.pareto(1,len(companies))),reverse=True if paretoMiracle < random.random() else False)
			paretoValues = [float(x)/sum(paretoValues) for x in paretoValues]
			industryEmployeeCount = sum(companies.values())
			for i,company in enumerate(sorted(companies, key=companies.get, reverse=True)):
				paretoProfit = self.industryAccount[company.industry]*paretoPortion*paretoValues[i]
				employeeProfit = self.industryAccount[company.industry]*(1-paretoPortion)*len(company.employees)/industryEmployeeCount
				company.earn(paretoProfit+employeeProfit)

		# 3. 회사는 사람을 자르거나 더 고용한다.
		# 3-1. bankruptNum 이하는 다짤리고 파산한다.
		bankruptNum = 0
		employmentPeriod = 4
		if self.week % employmentPeriod == 0:
			for company in self.companies:
				num = company.hrNum(weeklyWage)
				if num > 0:
					for i in range(0,num):
						if len(self.people_unemployed) > 0:
							p = self.people_unemployed.pop(0)
							company.hire(p)
				elif num < 0:
					for i in range(0,-num):
						if len(company.employees) > 0:
							self.fireOne(company)
						if len(company.employees) <= bankruptNum:
							for _ in range(len(company.employees)):
								self.fireOne(company)
							self.companies.remove(company)
							self.companies_bankrupted.append(company)
							break

	# setMinWage
	def setMinWage(self):
		raisePeriod = 26
		if self.duration >= self.week and self.week % raisePeriod == 0:
			wage = (self.minWageTarget-minWageBegin)/self.duration*self.week+minWageBegin
			self.minWage = int(wage)

	# getWeeklyWage
	def getWeeklyWage(self):
		# 하루 8시간 x 5일
		return self.minWage*8*5

	# graph - output 기록 - [필수] Tick 끝에서 실행된다
	def setOutputMeasures(self):
		# 0) 최저임금 기록
		self.minWages.append(self.minWage)
		# 1) week 기록
		self.weeks.append(self.week)
		# 2) 소비총합 기록
		self.totalConsumes.append(sum(self.industryAccount.values()))
		# 3) 고용률 기록
		self.employmentCount.append(len(self.people_employed))
		# 4) 운영률 기록
		self.openingCount.append(len(self.companies))

	# print
	def doPrint(self):
		print '[     '+ str(self.week) + ' th week'+'       ]'
		print 'Running Companies--'
		indus = ''
		emplo = 0
		for company in self.companies:
			if indus != company.industry or emplo != len(company.employees):
				print company.industry + ' : ' + str(len(company.employees)) + ' / ' + str(company.profit)
			indus = company.industry
			emplo = len(company.employees)
		print 'Bankrupted Companies--'
		for company in self.companies_bankrupted:
			if indus != company.industry or emplo != len(company.employees):
				print company.industry + ' : ' + str(len(company.employees)) + ' / ' + str(company.profit)
			indus = company.industry
			emplo = len(company.employees)

	# print dict
	def doPrintDict(self,d):
		for key, value in d.items():
			print key + ' : ' + str(value)

	# emergencyRate = 0으로 바꾼다.
	def emergencyRateInit(self):
		self.emergencyRate = dict.fromkeys(self.emergencyRate, 0)

	# emergencyRate를 노말라이즈한다.
	def emergencyNormalize(self):
		totalFireNum = sum(self.emergencyRate.values())
		if totalFireNum == 0: return
		for key, value in self.emergencyRate.items():
			self.emergencyRate[key] = float(value) / totalFireNum

	# 해고 룰
	def fireOne(self,company):
		p = company.fire()
		self.people_unemployed.append(p)
		if company.industry in self.emergencyRate:
			self.emergencyRate[company.industry] += 1
		else:
			self.emergencyRate[company.industry] = 1

