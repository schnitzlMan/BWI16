FillSequence = []  # Sequence read from input file

NumSlots = 10 # 10 # Number of Slots of the machine (10) by default
FillVal = 20  # Goal of how many balloons in a bag

Slots = []    # current state of the slots

Ausgabefach = []

#######################################################################
# this function is only called when you have no exact match
# and it was already checked that there is no value larger than FillVal

# given inList, find a value that is smaller or equal to goalVal
def getClosestInList(goalVal, inList):
    #print("getClosestInList")
    #print(goalVal, inList)
    outVal = 0
    outIndex = -1
    for curIndex, curVal in enumerate(inList):
        if (curVal <= goalVal) and (curVal > outVal):
            outVal = curVal
            outIndex = curIndex
    if outIndex == -1:
        print(goalVal, inList)
        print("ALARM - could not find a value goalVal or smaller in List")
        input("press a key")
        #TODO - either accept next best fill, or remove one of the list of possibilities        
    #print(outIndex, outVal)
    return outIndex, outVal   

def fillWithWhatYouGot():
    print("fillWithWhatYouGot")
    #TODO: Exit strategy for when Ausgabefach cannot be filled anymore because list is empty
    outIndex = 0
    while (sum(Ausgabefach) < FillVal) and (outIndex >= 0):
        outIndex, outVal = getClosestInList(FillVal-sum(Ausgabefach), Slots)
        print(outIndex, outVal)
        FACH(outIndex)
    if outIndex >= 0:
        VERPACKEN()
    return outIndex

def readFromFile():
    # Read from file
    fuellfolgefile = open("luftballonsTest.txt", 'r')
    for line in fuellfolgefile:
        FillSequence.append(int(line.rstrip('\r\n')))
    print(FillSequence)
    #input("readFromFile: fuellfolge - press key")

def fillEmptySlots():
    for curIndex, curVal in enumerate(Slots):
        if curVal == 0:
            #TODO Check if FillSequence still large enough to pop values
            while Slots[curIndex] == 0:
                Slots[curIndex] = FillSequence.pop(0)
    #print(Slots)
    #print(FillSequence)
    #input("fillEmptySlots: Slots refilled")

# mindlessly check all combinations if a combination is exactly the fillVal
def checkAllCombinations():
    returnList = []
    #TODO sum up and if smaller than target val return immediately
    #TODO check that NumSlots is not too large
    for i in range (1,2**NumSlots):   # goes to 2^N-1 hence all 1s in bin
        binString = bin(i)[2:].zfill(NumSlots) # [2:] removes the 0d in front
        currentSum = 0
        for j in range (NumSlots):
            if binString[j] == "1":
                currentSum += Slots[j]
        if currentSum == 20:
            returnList.append(binString)
    #print(returnList)
    #input("checkAllCombinations: combinations found")
    return returnList

# in: List of strings that contain the binary information which of the NumSlots
#     fullfill the requirement that exactly the value FillVal resutls
# out: one sequence that has the least number of entries
def findSmallestCombo(inList):
    mySum = NumSlots
    outIndex = -1
    for index, thisSeq in enumerate(inList):
        thisSum = 0
        for j in range(0,NumSlots):
            if thisSeq[j] == '1':
                thisSum += 1
        if thisSum < NumSlots:
            mySum = thisSum
            outIndex = index
    return inList[outIndex]   

def checkForTooLargeVal():
    outIndex = -1
    for index, curVal in enumerate(Slots):
        if curVal >= FillVal:
            outIndex = index
            break
    return outIndex

def emptySlots(inSlots):
    for j in range(0,NumSlots):
        if inSlots[j] == '1':
            FACH(j)

def FACH(i):
    Ausgabefach.append(Slots[i])
    Slots[i]=0
    while (len(FillSequence) > 0 and Slots[i] == 0):
        Slots[i]=FillSequence.pop(0)
    
def VERPACKEN():
    print("Ballons verpackt: Anzahl: ", Ausgabefach, " ", sum(Ausgabefach))
    del Ausgabefach [:]

#########################

def main():
    readFromFile()
    
    #initialize slots and refill them if empty
    for i in range (NumSlots):
        #TODO check if Fillsequence is actually long enough
        Slots.append(FillSequence.pop(0))
    
    # make sure that there are no slots without values for higher flexibility
    #refillSlots(speicherfaecher, fuellfolge, index)
    fillEmptySlots()
    # SETUP IS COMPLETE - SLOTS ARE FILLED FOR THE FIRST TIME

    # FILL SLOTS UNTIL THE LIST IS EMPTY AND NO MORE SLOTS CAN BE FILLED
    FillNextBag = True
    while FillNextBag:
        print("Slots: ", Slots)
        #TODO check all combinations only if sum is larger than FillVal

        # CHECK IF THERE IS ONE SINGLE SLOT THAT BLOCKS THE SYSTEM AND GET IT OUT
        tooLargeValInSlot = checkForTooLargeVal()
        if (tooLargeValInSlot >= 0):
            FACH(tooLargeValInSlot)
            VERPACKEN()
        else:
            
        # CHECK IF EXACT MATCH IS FOUND
            possibleList = checkAllCombinations()

            if possibleList:
                outSlots = findSmallestCombo(possibleList)
                emptySlots(outSlots)
                VERPACKEN()
            else:
                # No single slot is greater than 21 FillVal
                # there is no exact solution
                # start filling the bag starting with the largest slot
                # and keep refilling right away for best chances.
                #TODO: React on No Combo found
                print("could not find exact match - need to do something else")
                print("for the moment, just jump out of the eternal loop")

                # this could work right away, but think about it again
                outIndex = fillWithWhatYouGot()
                
                if (len(FillSequence) == 0 and sum(Slots) < FillVal) or outIndex < 0:
                    FillNextBag = False

        input("wait")
    print("done with it, left with Ausgabefach ", Ausgabefach)

    input("wait")
      
    #sum(speicher)
    #print(sum(speicherfaecher))
    #print(sum(speicherfaecher)%20)  # Modulo
    #print(sum(speicherfaecher)//20) # Teilen Integer
    #print(sum(speicherfaecher)/20)  # Teilen Dezimal

    
if __name__ == '__main__':
    main()
