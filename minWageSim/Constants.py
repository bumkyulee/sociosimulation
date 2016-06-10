# -*- coding: utf-8 -*-
import xlrd

workbook = xlrd.open_workbook('C:\Users\Bumkyu Lee\Desktop\socio\data.xls')
sheetConsumeRatio = workbook.sheet_by_name('ConsumeRatio')
sheetConsumeRatioSurplus = workbook.sheet_by_name('ConsumeRatio_Surplus')
sheetEmployment = workbook.sheet_by_name('Employment')

# 연령대 별 인구수
personAgeCount = dict()
for i, age in enumerate(sheetConsumeRatio.row_values(0)[1:]):
	personAgeCount[int(age)] = int(sheetConsumeRatio.row_values(1)[1:][i])

# 연령대별 산업별 소비 비율
consumeWeight = dict()
for i, age in enumerate(sheetConsumeRatio.row_values(0)[1:]):
	consumeWeight[age] = dict()
	for row in range(2,21):
		consumeWeight[age][sheetConsumeRatio.row_values(row)[0]] = sheetConsumeRatio.row_values(row)[1:][i]

# 연령대별 산업별 추가 소비 비율
consumeWeightSurplus = dict()
for i, age in enumerate(sheetConsumeRatioSurplus.row_values(0)[1:]):
	consumeWeightSurplus[age] = dict()
	for row in range(2,21):
		consumeWeightSurplus[age][sheetConsumeRatioSurplus.row_values(row)[0]] = sheetConsumeRatioSurplus.row_values(row)[1:][i]

# 회사 별 초기 고용 인원 수
companyEmployeeCount = dict()

for row in range(1,20):
	employmentRange = dict()
	for v in sheetEmployment.row_values(row)[1:6]:
		companyCount = int(v.split('|')[0])
		employmentCount = int(v.split('|')[1])
		if employmentCount > 0:
			avgEmployment = employmentCount / companyCount
			employmentRange[avgEmployment] = (companyCount-employmentCount % companyCount)
			if employmentCount % companyCount > 0:
				employmentRange[avgEmployment+1] = (employmentCount % companyCount)
	companyEmployeeCount[sheetEmployment.row_values(row)[0]] = employmentRange

# 최저임금 시작
minWageBegin = 6000
minWageWeekly = minWageBegin*5*8
