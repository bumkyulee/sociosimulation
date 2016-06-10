# -*- coding: utf-8 -*-
from __future__ import division
from minWageSim.Economy import *
import matplotlib.pyplot as plt
import math

def normalizeConsume(l):
	v = l[0]
	return ["%0.5f" % (x / v) for x in l]

def runEconomy(minWageTarget, duration, tickLimit, loop):

	fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,sharex=True)

	for i in range(0,loop):
		e = Economy(minWageTarget,duration,tickLimit)
		e.run()
		ax1.plot(e.weeks,e.totalConsumes, 'go-',alpha=0.7)
		ax2.plot(e.weeks,e.minWages,'bo-',alpha=0.7)
		ax3.plot(e.weeks,e.employmentCount,'ro-',alpha=0.7)
		ax4.plot(e.weeks,e.openingCount,'co-',alpha=0.7)

	plt.xlabel('Weeks',fontsize=10,style='italic', fontweight='bold')
	ax1.set_ylabel('TotalConsume',fontsize=10,style='italic', fontweight='bold')
	ax2.set_ylabel('Wage',fontsize=10,style='italic', fontweight='bold')
	ax3.set_ylabel('EmployementCount',fontsize=10,style='italic', fontweight='bold')
	ax4.set_ylabel('OpeningCount',fontsize=10,style='italic', fontweight='bold')

	plt.xlim(0,e.weeks[-1])
	ax1.set_ylim(0)
	ax2.set_ylim(0)
	ax3.set_ylim(0)
	ax4.set_ylim(0)

	fig.suptitle('Go '+ str(minWageTarget) + 'KRW in ' + str(duration) + 'weeks', fontsize=13, fontweight='bold')
	plt.show()

runEconomy(8000,52,300,1)