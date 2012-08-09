import matplotlib.pyplot as plot
import random
import math
from numpy import *

def easing1(index):
    #if(thisX > 10.0 and prevX < 10.0):
    #    return 10.0*(10.0-prevX)-(thixX-10.0)
    #el
    thisX = x[index+1]
    prevX = x[index]
    if(thisX < 5.0 or thisX > 45.0):
        v.append(v[index] + 4.0*(thisX-prevX))
    else:
        v.append(v[index] - 1.0*(thisX-prevX))
    return v[index+1]*(thisX-prevX)

def easing2(index):
    if(x[index+1] < 25.0):
        return x[index+1]-x[index]
    else:
        return x[index]-x[index+1]
velocity = 0.0
def easing3(index):
    max = 100.0
    retVal = 0.0
    if(y[index] < max*0.1 and y[index-1] <= y[index]):
        retVal = y[index]+max*((x[index+1]-x[index])*0.0001*pow(x[index+1],1))
    elif(y[index] < max-max/4000.0 and y[index-1] <= y[index]):
#        retVal = y[index]+((x[index+1]-x[index])*(max-y[index])/0.03)
        retVal = y[index]+((x[index+1]-x[index])*(max-y[index])/30.0)
    else:
        retVal = y[index]-((x[index+1]-x[index])*(y[index]-0.0)/200.0)
#    else:
#        retVal = y[index]
    if(retVal > max):
        return max
    return retVal



x = [0.0]
#x = range(0,100)
y = [0.0]
v = [0.0]
index = 0
while(x[index]<2000.0):
    timePassed = random.random()*000.2#about 10 frames/sec
    timePassed = random.random()*20.0#about 100 frames/sec
    x.append(x[index]+timePassed)
#    y.append(x[index+1])
#    y[index]=y[index-1]+easing1(x[index],x[index-1])
#    y.append(y[index]+easing2(index))
    y.append(easing3(index))    
#    y.append(exp(-0.5*pow(log(x[index+1]),2)))
#    v.append(.001/pow(x[index+1],2))
    index=index+1
#plot.plot(x,v)
#plot.plot(x,v)
#for data in y[:30]:
#    print data
plot.plot(x,y)
plot.show()
#plt.plot([1,2,3,4])
#plt.ylabel('some numbers')
#plt.show()
