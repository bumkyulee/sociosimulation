# -*- coding: utf-8 -*-
from __future__ import division
from minWageSim.Economy import *
import matplotlib.pyplot as plt
import math

def normalizeConsume(totalConsumes):
	return ["%0.5f" % (x / totalConsumes[0]) for x in totalConsumes]

def runEconomy(minWageTarget, duration, tickLimit, loop):
	plt.title('Go '+ str(minWageTarget) + 'KRW in ' + str(duration) + 'weeks', fontsize=10, fontweight='bold')
	plt.ylabel('Effect', fontsize=10)
	plt.xlabel('Weeks', fontsize=10)
	plt.grid(True)

	for i in range(0,loop):
		e = Economy(minWageTarget,duration,tickLimit)
		e.run()
		ymax = math.ceil(float(max([max(normalizeConsume(e.totalConsumes)),max(e.employmentRates),max(e.openingRates)])))
		plt.axis([e.weeks[0],e.weeks[-1],0,ymax])
		plt.plot(e.weeks,normalizeConsume(e.totalConsumes), 'go-', label='Consume' if i==0 else '',alpha=0.7)
		plt.plot(e.weeks,normalizeConsume(e.minWages),'bo-', label='MinWage' if i==0 else '',alpha=0.7)
		plt.plot(e.weeks,e.employmentRates,'ro-', label='Employment' if i==0 else '',alpha=0.7)
		plt.plot(e.weeks,e.openingRates,'co-', label='Opening' if i==0 else '',alpha=0.7)


#with plt.style.context('fivethirtyeight'):
plt.subplot(221)
runEconomy(10000,5,30,2)
plt.subplot(222)
runEconomy(10000,10,30,2)
plt.subplot(223)
runEconomy(10000,15,30,2)
plt.subplot(224)
runEconomy(10000,20,30,2)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)

plt.show()