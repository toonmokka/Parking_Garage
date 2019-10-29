############################################################################################################################################
# Programmer: Pachara Harnirattisai
# Project: Parking Garage OOP Design (Also Energy Challenge)
# Language: Python 3.7
# Date: 10/29/2019
############################################################################################################################################
# INSTRUCTIONS: Due to not using any GUI or DB, you can view 
# all the visual and input command through the terminal. 
# This program will create a parking garage with customized
# numbers of spots for each floor. This will be visualized.
# You can then customized a list of vehicles in main using
# the preset for loops and the program will try to fit
# them in to the garage.
############################################################################################################################################
# Note 1: For simplicity sake, I've decided to design this lot
# with the assumption that all spots created are grouped into
# one row each. Example: if 3 motorcycle spots are created 
# they are all grouped next to each other in that floor.
# This solves the buses occupying 5 Large spots problem
# If there are more than 5 large spots other vehicle can
# be parked in it. 
#
# Note 2: I decided to skip the DB part due to time constraints. 
# I am going to learn building a GUI DB and continue to improve 
# this project To make up for this fact, I've decided to included 
# some visuals and data output in the terminal as it takes up less
# time. I've done my best as I can during the free time I had. 
############################################################################################################################################
# TEST CASES:
# 1) For One Floor: 
#                      # of Floors: 1
#                      # of Motorcycle Spots: 5
#                      # of Compact Spots: 5
#                      # of Large Spots: 10
#                      # of Motorcycles: 5
#                      # of Compact Cars: 5
#                      # of Buses: 2
# 2) For Multiple Floors: 
#                      # of Floors: 2
#                      # of Motorcycle Spots: 5 (Both Floors)
#                      # of Compact Spots: 5 (Both Floors)
#                      # of Large Spots: 10 (Both Floors)
#                      # of Motorcycles: 8
#                      # of Compact Cars: 7
#                      # of Buses: 3 or 4
############################################################################################################################################# 
from random import shuffle
############################################################## VEHICLES #####################################################################

#Oversees each vehicle type as the master class
class Vehicles:

    #Constructors consists of vehicle type and the parking spaces they take up
    def __init__(self, vtype, size):
        self.vList = [ ]
        self._vtype = vtype
        self._vSize = size

    #Getters
    def getVType(self):
        return  self._vtype
    def getVSize(self):
        return self._vSize
    
#Sub class of Vehicles, with each its own contructors 
# and characteristics
class Motorcycle(Vehicles):
    
    def __init__(self):
        self._vtype = "Motorcycle"
        self._vSize = .5

class Car(Vehicles):

    def __init__(self):
        self._vtype = "Car"
        self._vSize = 1 

class Bus(Vehicles):
    def __init__(self):
        self._vtype = "Bus"
        self._vSize = 5

################################################### GARAGE / FLOORS / SPOTS ################################################################

#Handle Parking Mechanics and Overall Garage 
class Garage:

    #initializes the parking lot creating empty levels, and populating the first level
    def __init__(self):
        # Declares the garage level
        self._numFloors = input("Please input the number of floors on your garage: ")
        #This list is the garage data structure itself
        self._lvl = [ ] * int(self._numFloors)
        #lists car in garage
        self._inGarage = [ ]
        # Initializes the first floor of garage
        print("Initializing the number of spots in the 1st floor")
        moSpot = input("Input the # of Motorcycle Spots: ")
        comSpot = input("Input the # of Compact Spots: ")
        larSpot = input("Input the # of Large Spots: ")
        self._totalSpot = self.buildLot(moSpot, comSpot, larSpot)

    #called to populate the first level, and further when called
    def buildLot(self, moSpot, comSpot, larSpot):
        
        self._totalSpot = [ ]
        for i in range(int(moSpot)):
            self._totalSpot.append(MotorcycleSpot())
        for i in range(int(comSpot)):
            self._totalSpot.append(CompactSpot())
        for i in range(int(larSpot)):
            self._totalSpot.append(LargeSpot())
        
        self._lvl.append(self._totalSpot)
        return self._totalSpot

    #Populates the rest of the parking garage floors
    # i + 1 as the first floor has been added
    def populateFloors(self):     
        for i in range(1, int(self._numFloors)):
            motorSpot = input("Input the # of Motorcycle spots for floor " + str(i + 1) + ": ")
            comSpot = input("Input the # of Compact spots for floor " + str(i + 1) + ": ")
            larSpot = input("Input the # of Large spots for floor " + str(i + 1) + ": ")
            self.buildLot(motorSpot, comSpot, larSpot)

    # Design to automatically park vehicles
    def parkVehicles(self, vecList):
        print("Parking. . .")
        print("Number of spots: " + str(len(self._lvl[0])))
        
        # Iterates through levels
        for i, levels in enumerate(self._lvl):
            #iterates through all the vehicles 
            for k, vec in enumerate(vecList):
                #Iterates through all the spots in a level
                for j, spots in enumerate(self._lvl[i]):
                    # If vehicle not parked already and the spot is open
                    if vec not in self._inGarage and spots._inSpot == False:
                            # This makes sure smaller vehicles canpark in larger spots
                            if vec.getVSize() <= spots.getSpotSize():
                                spots._inSpot = True
                                self._inGarage.append(vec)
                                print(str(vec.getVType()) + " is now parked in a " 
                                + spots.getSpotType() + " on level: " + str(i + 1))

                            #Park buses mechanics as its meant to take up 5 large spots
                            elif spots.getSpotSize() == 2 and vec.getVSize() > spots.getSpotSize():
                                for l in range(0, 5):
                                    #print("inner j: " + str(j + l))
                                    self._lvl[i][j + l]._inSpot = True
                                    self._inGarage.append(vec)
                                    print(str(vec.getVType()) + " is now parked in a "
                                    + spots.getSpotType() + " on level: " + str(i + 1))
                                  
    #Get number of levels in the garage
    def getLevel(self):
        return self._numFloors

    #Get the total spots of garage
    def getLevelSize(self, lvl):
        return len(self._lvl[int(lvl)])

    #Get total number of spots in the garage
    def getGarageSize(self):
        totalSpots = 0
        for i in range(int(self._numFloors)):
            totalSpots += self.getLevelSize(i)
        print("Total # of spots in garage: " + str(totalSpots))

    # Print a visual of the garage for every floor
    def printGarage(self):
        print("\n")
        print("Here are the layout of the garage \n")
        print("There are " + str(self._numFloors) + " floors \n")

        # for i in range(int(self._numFloors)):
        #     print("Floor " + str(i + 1) + ": " + str(self._lvl[i]) + "\n")

        for i , floor in enumerate(self._lvl):
            print("Floor: " + str(i + 1) + "\n")
            print("*" * (self.getLevelSize(i) + 2))
            for j, spot in enumerate(floor):
                if spot._spotSize == .5:
                    if spot._inSpot == True:
                        print("|x" + " " * (self.getLevelSize(i) - 1) + "*")
                    else: 
                        print("|" + " " * self.getLevelSize(i) + "*")
                elif spot._spotSize == 1:
                    if spot._inSpot == True:
                        print("||x" + " " * (self.getLevelSize(i) - 2) + "*")
                    else:
                        print("||" + " " * (self.getLevelSize(i) - 1) + "*")
                elif spot._spotSize == 2:
                    if spot._inSpot == True:
                        print("|x|" + " " * (self.getLevelSize(i) - 2) + "*")
                    else:
                        print("| |" + " " * (self.getLevelSize(i) - 2) + "*")
                else:
                    print("*" + " " * self.getLevelSize(i) + "*")
            print("*" * (self.getLevelSize(i) + 2))
            print("\n")
    
        self.getGarageSize()

    def getVecList(self):
        return self._inGarage
    
    def getOpenSpots(self):
        return self.getGarageSize() - len(self.getVecList())
    
#A class to handle a specific spot
class Spot(Garage):
    
    #This constructor sets the spot size and boolean for if spot is occupied
    def __init__(self, spotSize):
        self._spotType = None
        self._spotSize = spotSize
        self._inSpot = False
    
    #getters
    def getSpotSize(self):
        return self._spotSize
    
    def getInSpot(self):
        return self._inSpot

    def getSpotType(self):
        return self._spotType

#Numerical size is .5 because it has to be smaller that compact spot
class MotorcycleSpot(Spot):

    def __init__(self):
        self._spotType = "Motorcycle Spot"
        self._spotSize = .5 
        self._inSpot = False
        
#Numerical size will be just one
class CompactSpot(Spot):

    def __init__(self):
        self._spotType = "Compact Spot"
        self._spotSize = 1
        self._inSpot = False
    
#Numerical size will be double of compact spot 
class LargeSpot(Spot):

    def __init__(self):
        self._spotType = "Large Spot"
        self._spotSize = 2
        self._inSpot = False

##############################################################  MAIN  #######################################################################

if __name__ == "__main__":
    print("Garage Program Start")

    ##### Build a initital first floor of the garage
    PG = Garage()

    ##### Populate the rest of the garage
    PG.populateFloors()

    ### Show the built parking garage
    PG.printGarage()

    # Generate Vehicles to park in spot 
    vehiclesList = []

    # Input number of Motorcycles
    for i in range(int(input("Please Enter the # of MotorCycles: "))):
        vehiclesList.append(Motorcycle())
    # Input number of Compact Cars
    for i in range(int(input("Please Enter the # of Cars: "))):
        vehiclesList.append(Car())
    # Input number of Buses
    for i in range(int(input("Please Enter the # of Buses: "))):
        vehiclesList.append(Bus())

    shuffle(vehiclesList)
    print(str(vehiclesList))
    print("\n")
    PG.getGarageSize()

    #populate vehicles
    PG.parkVehicles(vehiclesList)

    PG.printGarage()