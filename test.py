from numpy import *
import numpy
from collections import deque


a0  = deque([])
lp  = []
# estimate percentile for each ensemble
for i in range(100):
    nsample = 10*365*4
    a       = numpy.random.weibull(0.5, nsample)
    p       = numpy.percentile(a, 99.99)

    a0.extend(a)
    lp.append(p)
    print i,a.min(),a.max(),"--99.99---",p
print " "*50
print "*"*50
a0      = asarray(a0)
p0      = percentile(a0, 99.99)
lp      = sorted(asarray(lp), reverse=True)
print "ALL",a0.min(),a0.max(),"--99.99--",p0



