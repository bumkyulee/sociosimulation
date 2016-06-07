# -*- coding: utf-8 -*-
from __future__ import division
from minWageSim.Economy import *
import matplotlib.pyplot as plt
import math

def normalizeConsume(l):
	v = l[0]
	return ["%0.5f" % (x / v) for x in l]

def runEconomy(minWageTarget, duration, tickLimit, loop):
	plt.title('Go '+ str(minWageTarget) + 'KRW in ' + str(duration) + 'weeks', fontsize=10, fontweight='bold')
	plt.ylabel('Effect', fontsize=10)
	plt.xlabel('Weeks', fontsize=10)
	plt.grid(True)

	for i in range(0,loop):
		e = Economy(minWageTarget,duration,tickLimit)
		e.run()
		e. totalConsumes = normalizeConsume(e.totalConsumes)
		e. minWages = normalizeConsume(e.minWages)
		e. employmentCount = normalizeConsume(e.employmentCount)
		e. openingCount = normalizeConsume(e.openingCount)

		ymax = math.ceil(float(max([max(e.totalConsumes),max(e.minWages),max(e.employmentCount),max(e.openingCount)])))
		plt.axis([e.weeks[0],e.weeks[-1],0,ymax*1.2])
		plt.plot(e.weeks,e.totalConsumes, 'go-', label='Consume' if i==0 else '',alpha=0.7)
		plt.plot(e.weeks,e.minWages,'bo-', label='MinWage' if i==0 else '',alpha=0.7)
		plt.plot(e.weeks,e.employmentCount,'ro-', label='Employment' if i==0 else '',alpha=0.7)
		plt.plot(e.weeks,e.openingCount,'co-', label='Opening' if i==0 else '',alpha=0.7)


#with plt.style.context('fivethirtyeight'):
'''
plt.subplot(221)
runEconomy(10000,52,50,1)
plt.subplot(222)
runEconomy(10000,52*2,50,1)
plt.subplot(223)
runEconomy(10000,52*3,50,1)
plt.subplot(224)
'''
runEconomy(10000,104,104,1)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)

plt.show()