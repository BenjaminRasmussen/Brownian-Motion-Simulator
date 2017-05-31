import numpy as np
import matplotlib.pyplot as mp
import pandas as pd

mp.style.use("dark_background")
# Make like the one in the class
ParticleSize = 0.05

class Particle:
    PaticleSize = 0.5
    def __init__(self):
        self.x = 0
        self.y = 0
        self.curVel = 0
        self.oldx = 0
        self.oldy = 0
        self.particlesize = ParticleSize


    def apox(self, otherparticle):
        # |√(x2-x1)^2+(y2-y1)^2| < epsilon, then...
        if np.abs(np.sqrt((self.x+otherparticle.getx())**2 + (self.y+otherparticle.gety())**2)) <= self.particlesize:
            self.docolission(otherparticle, self.particlesize)

    def docolission(self, otherparticle, epsilon=ParticleSize):
        """Particle a has incident angle Theta and deflection angle Ø.
                Ø = π-2*Theta
        Particle b has deflection angle ß, ß Is a right angle to Ø which is normal to the incident.
                ß = Theta
                Theta = Tan^-1(dy/dx) of particle 1
                vel forboth: (initvel - travellength)/2,
                    this is since momentum is equal, shared equally and conserved.
            """
        # Find the distance to the other particle using pythagoras.

        dy = np.sqrt((self.y+otherparticle.gety())**2)
        dx = np.sqrt((self.x+otherparticle.getx())**2)
        # Find the incident angle
        Theta = np.arctan(dy/dx)
        # Find the deflection angle
        Deflection = (np.pi-(2*Theta))
        # find the velocity after collision
        vel = (self.curVel - np.sqrt(dy**2+dx**2))/2
        # Move the particles
        self.move(vel, Deflection)
        otherparticle.move(vel, Theta)

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getpos(self):
        return [self.x,self.y]

    def move(self, vel, deg):
        # Set a delimiting function such that a recursion cant go on forever. Note this in the IA.
        # Indefinite recursion (cascading collisions) dose not seem to be the case but i will be on the lookout for it.
        # dx = x+v*cos(Ø), x = x+dx
        # dy = y+v*sin(Ø), y = y+dy
        self.curVel = vel
        self.oldx = self.x
        self.oldy = self.y
        self.x = self.oldx + vel * np.math.cos(deg)
        self.y = self.oldy + vel * np.math.sin(deg)

    def getDistVel(self):
        # e^(-x^2/2) /(√(2*pi)
        # x is rand from -Ø to inf
        return abs(np.random.normal())

    def getRandDeg(self):
        # Random*π*2*(180/π)
        return (np.random.rand(1) * np.pi * 2) * (180 / np.pi)

    def update(self):
        # dx = x*v*cos(Ø) , = move(vel,deg) , vel=NDF , deg=rand
        # dy = y*v*sin(Ø) , = move(vel,deg) , vel=NDF , deg =rand
        self.move(self.getDistVel(), self.getRandDeg())



class Simulation:
    def __init__(self, size=1, dt=1):
        df = pd.DataFrame()
        arr = []
        for n in range(size):
            arr.append(Particle())
        for i in range(dt):
            for m in range(arr.__len__()):
                arr[m].update()
                # Check for collisions
                for j in range(arr.__len__()):
                    if not j==m:
                        arr[m].apox(arr[j])

class simulationWithPlot:
    #OLD!
    def __init__(self, size=1, dt=1):
        xcoor = []
        ycoor = []
        arr = []
        for n in range(size):
            arr.append(Particle())
        for i in range(dt):
            print("Step:    " + str(i+1) + " out of " + str(dt))
            for m in range(arr.__len__()):
                arr.__getitem__(m).update()
                #  print(arr.__getitem__(m).getpos())
                for j in range(arr.__len__()):
                    if not j==m:
                        arr[m].apox(arr[j])

        for i in arr:
            xcoor.append(i.getpos()[0])
            ycoor.append(i.getpos()[1])
        # Show line to every other particle from the 0th particle
        for z in range(len(arr)):
            mp.plot([arr.__getitem__(0).getx(),arr.__getitem__(z).getx()],
                    [arr.__getitem__(0).gety(),arr.__getitem__(z).gety()])

        mp.scatter(xcoor,ycoor, 0.5)
        mp.yscale('linear')
        mp.xscale('linear')
        mp.title("With: Collisions, SDF speed, and dt=1 and Pn=250")
        mp.show()

simulationWithPlot(250,100)