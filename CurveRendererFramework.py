import math

from tkinter import *
window = Tk()
canv = Canvas(window, width = 1200, height = 700, background = "black")
canv.pack()

class curveRenderer():
    def __init__(self, point, vertex, colour, curveType):
        self.point = point
        self.vertex = vertex
        self.colour = colour

        vertex = self.adjustfNotValid(point, vertex)

        if curveType == "half-curve":
            canv.after(250, self.drawHalfCurve(point, vertex, colour))

        elif curveType == "chain":
            canv.after(250, self.drawChainLink(point, vertex, colour))

    def adjustfNotValid(self, point, vertex):
        increase = 100
        if point == vertex:
            vertex = [vertex[0] + increase, vertex[1] + increase]
        return vertex

    def calcRise(self, point, vertex):
        return point[1] - vertex[1]

    def calcRun(self, point, vertex):
        return point[0] - vertex[0]

    def calcGradient(self, rise, run):
        return rise / run #Use formula gradient = rise / run

    def createLines(self, p0, p1, colour, linesInCurve):
         line = canv.create_line(p0[0], p0[1], p1[0], p1[1], fill = colour)
         linesInCurve.append(line)
         window.update()
    
    def checkNegativeGradient(self, point, vertex, gradient):
        #If a point is to the right of the vertex, the gradient is positive. If not, it is negative.
        if point[0] < vertex[0]:
            gradient *= -1
        return gradient 

    def simplifyFraction(self, numerator, denominator):
        i = 2
        maxValue = numerator #The maximum value by which we can divide is the lowest number of either the numerator or the denominator.
        if denominator > numerator:
            maxValue = denominator

        while i <= maxValue:
            if numerator % i == 0 and denominator % i == 0:
                numerator = int(numerator / i)
                denominator = int(denominator / i)

            i += 1

        count = 1 #This count variable counts the number of times we increment i. It ensures that if a fraction cannot be further simplified, we do not end up with an uneding loop.

        return numerator, denominator

    def getIntoFraction(self, rise, run, gradient):
        fractionFound = False

        #find a whole number fraction equivalent to the gradient
        idx = 1
        numerator = gradient
        denominator = 1

        lim = rise
        if run > rise:
            lim = run

        while idx <= lim and fractionFound is False:
            numerator = gradient * idx
            numerator1DP = round(numerator, 1)
            if numerator1DP == int(numerator) + 0.0:
                denominator = idx
                fractionFound = True
            idx += 1

        numerator = int(numerator)

        numerator,denominator = self.simplifyFraction(numerator, denominator)

        print("{} / {}".format(numerator, denominator)) #DEBUGGING OUTPUT STATEMENT
        return numerator, denominator

    def drawHalfCurve(self, point, vertex, colour):
        linesInCurve = [] #This list tracks the .Canvas number of every line we draw

        #self.createLines(vertex, point, "white", linesInCurve) #THIS IS A OUTPUT STATEMENT TO ENSURE THE NORMALISED GRADIENT AND FINAL POINT MATCH UP

        rise = self.calcRise(point, vertex)
        run = self.calcRun(point, vertex)

        #Assume point = +-1 deviation from the vertex. With this assumption, the gradient of the curve equals the coefficient,'a' of the equation y = ax^2. 
        gradient =  self.calcGradient(rise, run) 
        gradient = self.checkNegativeGradient(point, vertex, gradient)

        xIncrement = 1
        if run > 0:
            xIncrement = math.sqrt(run)
        elif run < 0:
            run *= -1 
            xIncrement = math.sqrt(run) * -1

        else:
            run = 100
            xIncrement = math.sqrt(run)

        x = vertex[0]
        y = vertex[1]
        finishedDrawing = False

        count = 1 #This is the normalised x and y distance from the origin to point(1,1)
        p0 = vertex

        endValue = point[0] - xIncrement

        if vertex[0] < point[0]:
            
            while x <= endValue and count <= 100:
                val = count * count * gradient
                x += xIncrement
                y = vertex[1] + val
                p1 = [x,y]
                #print(p1)
                self.createLines(p0, p1, colour, linesInCurve)

                p0 = p1
                count += 1

            #drawing the final line 
            self.createLines(p1, point, colour, linesInCurve)

        else:

            while x >= endValue and count <= 100:
                val = count * count * gradient
                x += xIncrement
                y = vertex[1] + val
                p1 = [x,y]
                #print(p1)
                self.createLines(p0, p1, colour, linesInCurve)

                p0 = p1
                count += 1

            #drawing the final line 
            self.createLines(p1, point, colour, linesInCurve)
     
    def getMidPoint(self, p0, p1, makeLower):
        mid_x = int((p0[0] + p1[0]) / 2)
        mid_y = 0
        
        if makeLower is True:
            const = 100 #adjusting y-coordinate by a constant to make the midpoint below the lowest value
            if p0[1] < p1[1]:
                mid_y = p1[1] + const
            else:
                mid_y = p0[1] + const
        else:
            mid_y = int((p0[1] + p1[1])/2)

        return [mid_x, mid_y]

    def drawChainLink(self, startPoint, endPoint, colour):
        #This uses the cosh formula: y = (e^x + e^-x)/2
        linesInCurve = [] #This list tracks the .Canvas number of every line we draw
        makeLower = True
        midPoint = self.getMidPoint(startPoint, endPoint, makeLower)

        ePos = math.e

        rise1 = self.calcRise(startPoint, midPoint)
        run1 = self.calcRun(startPoint, midPoint)

        #Assume point = +-1 deviation from the vertex. With this assumption, the gradient of the curve equals the coefficient,'a' of the equation y = ax^2. 
        downSlope =  self.calcGradient(rise1, run1)

        rise2 = self.calcRise(midPoint, endPoint)
        run2 = self.calcRun(midPoint, endPoint)
        upSlope = self.calcGradient(rise2, run2)

        count = 1

        xIncrement = 1

        if run1 <= 0:
            run1 = ePos

        if run2 <= 0:
            run2 = ePos

        xIncrement = math.log(run1, ePos)
        
        count = 1 #normalised distance between start and end points
        endValue = 0

        if startPoint[0] < midPoint[0]:
            xIncrement *= -1
            endValue = midPoint[0] - xIncrement
        else:
            endValue = startPoint[0] - xIncrement
            startPoint, midPoint = midPoint, startPoint #swapping values

        p0 = startPoint
        x = startPoint[0]

        while x <= endValue and count <= 100:
            val = ( (math.pow(ePos,count) + math.pow(ePos, -count)) / 2 )
            print(val)
            x += xIncrement
            y = startPoint[1] + val
            p1 = [x,y]
            self.createLines(p0, p1, colour, linesInCurve)
            p0 = p1
            count += 1

        #drawing the final line
        self.createLines(p0, endPoint, colour, linesInCurve)

vertex = [100, 100]
point = [250, 220]
colour = "red"

#curve = curveRenderer(point, vertex, colour, "half-curve")

# xIncrease = 100
# yIncrease = 100
# colour = "red"
# for i in range(0, 5):
#     point = [200 + xIncrease * i, 200 + yIncrease * i]
#     curveRenderer(point, vertex, colour, "half-curve")
#     vertex = point

# x = point[0]
# y = point[1]
# colour = "blue"
# for i in range(1, 6):
#     point = [x - xIncrease * i, y - yIncrease * i]
#     curveRenderer(point, vertex, colour, "half-curve")
#     vertex = point

cosh = curveRenderer(point, vertex, colour, "chain")

window.title('RedHam Industries')
window.geometry("500x500+100+200")
window.mainloop()
