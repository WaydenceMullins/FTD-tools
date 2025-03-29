#Made by Waydence. Inspired by Japanator's blockdata.py
#Creates or overwrites BlockInfoboxes.txt and BlockData.csv (" in description and name fields are replaced with ˝ for csv file)
#For game version 4.2.5
import json
import os
import re

blockFilesPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\From The Depths\\From_The_Depths_Data\\StreamingAssets\\Mods" # Path to block data files [normally to /From_The_Depths_Data/StreamingAssets/Mods]

def FindBlockFiles(path, extension):                        #Finds files with "extension" in "path"
    foundFiles = []                                         #Declare found files list
    for root, dirs, files in os.walk(path):                     #Looks through files? IDK found this on the internet
        for file in files:                                          #Checks every file name
            if file.endswith(extension):                                #if it has the extension
                foundFiles.append(os.path.join(root, file))                 #add it to found files list
    return foundFiles
def CategoryCheck(category):                #Corrects category
    if category in ["Water", "Air", "Land", "Resources", "Control", "AI", "Fuel Engines", "Steam Engines", "Simple weapons", "CRAM Cannons", "Advanced Cannons", 
                    "Missiles", "Laser Systems", "Particle Cannons", "Plasma Cannons", "Flamethrowers", "Defence", "Miscellaneous", "Decorations", "Subobjects", "New blueprints"]:
        return category                     #Changes nothing if category is correct
    elif category in ["Alloy 1m to 2m slope transition left", "Alloy Plate", "Applique Panel", "Blocks", "ERA Armour", "Glass block", "Glass 1m to 2m slope transition left", "Heavy Armour", 
                    "Heavy Armour 1m to 2m slope transition left", "Lead 1m to 2m slope transition left", "Lead Block", "Light-weight Alloy Block", "Metal 1m to 2m slope transition left", 
                    "Metal Block", "Metal Plate", "Reinforced Wood", "Rubber 1m to 2m slope transition left", "Rubber Block", "Stone 1m to 2m slope transition left", "Stone Block", 
                    "Surge Protector", "Truss 1m", "Wood 1m to 2m slope transition left", "Wood Block Variant", "Wood Block", ]:
        return "Building blocks"            #Changes to appropriate category
    elif category in ["Rudder Square"]:
        return "Water"
    elif category in ["Aileron", "ControlSurfaceComponent", "Duct (3x3)", "Jet controller", "Jet intake", "Small Jet Controller", "Small Jet Intake", "Wing middle", "Wing strut"]:
        return "Air"
    elif category in ["Fuel Refinery Pipe", "Material Gatherer", "Wooden Material Storage Small"]:
        return "Resources"
    elif category in ["Vehicle Controller"]:
        return "Control"        #evil space at the end v
    elif category in ["Behaviours & Additional Routines ", "Frontal hovercraft AI", "Local Weapon Controller", "Range Finder (5m)", "Wireless Snooper"]:
        return "AI"
    elif category in ["Exhaust", "Inline turbocharger (left)"]:
        return "Fuel Engines"
    elif category in ["Large shaft", "Large 5m propeller", "Large axis-shifting gears R", "Large gearbox", "Large turbine generator", "Medium Shaft", "Medium 3m propeller", 
                    "Medium gearbox", "Medium turbine generator", "Small 1m propeller", "Small gearbox", "Small shaft", "Small turbine generator", "Steam pipe 1m"]:
        return "Steam Engines"
    elif category in ["Drill", "Medium transmission"]:
        return "Simple weapons"
    elif category in ["Elevation barrel", "Heavy Barrel", "Motor Driven Barrel", "Recoil Suppression Barrel", "Six Way Connector"]:
        return "CRAM Cannons"
    elif category in ["Barrel", "Belt feed autoloader (1m shells)", "Hydraulic recoil absorber (1m)", "Omni Mantlet (1m)", "Railgun Magnet Attaching Fixture"]:
        return "Advanced Cannons"
    elif category in ["Huge Launcher", "Large Launcher", "Medium Launcher", "Missile wireless transmitter", "Small Launcher"]:
        return "Missiles"
    elif category in ["Countermeasure", "Anti Missile Cannon Controller", "Shield Generator"]:
        return "Defence"
    elif category in ["ScentedCandleHolder1Nice", "ScentedCandleHolder1", "Docking station"]:
        return "Miscellaneous"
    elif category in ["Door Bulkhead Metal", "Railing TA 1m M1", "Crystal growth farm", "Display", "Sign Post"]:
        return "Decorations"
    elif category in ["Helicopter blade", "Nuclear Engines"]:
        return "Discontinued blocks"
    else:
        return "Unset or unrecognized block category"
def DropTrailZero(number):                                  #Removes trailing .0 from integers
    return number if number % 1 != 0 else int(number)
def GetDimension(dimPositive, dimNegative):                 #Calculates block size
    return dimPositive + dimNegative + 1
def GetDragValue(values, position):                         #Extracts a single item from 3-item drag list
    valueList = values.split(",")
    return valueList[position]

blockDataDictionary = {}                                    #List of blocks in the UUID(name,value,value,uuid,etc) format
itemFileList = FindBlockFiles(blockFilesPath, ".item")      #List of .item files
itemDupModFileList = FindBlockFiles(blockFilesPath, ".itemduplicateandmodify")  #List of .itemduplicateandmodify files
blocksHandled = 0
for itemFile in itemFileList:                                       #Do with each .item file
    rawItemFile = open(itemFile, "r")                                   #Load a file as string
    itemData = json.load(rawItemFile)                                   #Turn string into Python dictionary
    itemGuid = itemData.get("ComponentId").get("Guid")
    blockDataDictionary[itemGuid] = [                                                       #Set GUID as key and list of block's properties as value
        re.sub("###.*?#?!", '',itemData.get("DisplayName")),                                    #0| title =         DisplayName is the one used in mimics and decos, and shown when you mouse over block in inventory
        re.sub("###.*?#?!", '',itemData.get("Description")),                                    #1| Description =   ###.*?#?! is a regex to remove translation strings
        re.sub("###.*?#?!", '',itemData.get("DisplayName")) + ".png",                           #2| image = 
        CategoryCheck(itemData.get("InventoryTabOrVariantId").get("Reference").get("Name")),    #3| category = 
        DropTrailZero(itemData.get("Health")),                                                  #4| Health = 
        DropTrailZero(itemData.get("ArmourClass")),                                             #5| Armour = 
        DropTrailZero(round(itemData.get("Weight") * 100, 1)),                                  #6| Weight = 
        DropTrailZero(itemData.get("Cost").get("Material")),                                    #7| Cost = 
        GetDimension(itemData.get("SizeInfo").get("SizePos").get("z"),itemData.get("SizeInfo").get("SizeNeg").get("z")),   #8| length = 
        GetDimension(itemData.get("SizeInfo").get("SizePos").get("x"),itemData.get("SizeInfo").get("SizeNeg").get("x")),   #9| width = 
        GetDimension(itemData.get("SizeInfo").get("SizePos").get("y"),itemData.get("SizeInfo").get("SizeNeg").get("y")),   #10| height = 
        DropTrailZero(round(10*((-9.81*(itemData.get("Weight")*100)/100)+3.75*(itemData.get("SizeInfo").get("ArrayPositionsUsed")*itemData.get("SizeInfo").get("VolumeFactor")*itemData.get("SizeInfo").get("VolumeBuoyancyExtraFactor")))+0.001, 1)),  #11| relativeBuoyancy =     Thanks to Hyperion_21! Formula:10*((-9.81*(Weight*100)/100)+3.75*(SizeInfo.ArrayPositionsUsed*SizeInfo.VolumeFactor*SizeInfo.VolumeBuoyancyExtraFactor)
        DropTrailZero(round(itemData.get("SizeInfo").get("ArrayPositionsUsed")*itemData.get("SizeInfo").get("VolumeFactor")*itemData.get("SizeInfo").get("VolumeBuoyancyExtraFactor")*37.5+0.001, 1)),   #12| emptySpaceBuoyancy =      +0.001 so it rounds like in the game
        DropTrailZero(itemData.get("ExtraSettings").get("EmpSusceptibility")*100),              #13| empSusceptibility =    Multiply by 100 to get percent value
        DropTrailZero(itemData.get("ExtraSettings").get("EmpDamageFactor")*100),                #14| empDamageTaken = 
        DropTrailZero(itemData.get("ExtraSettings").get("EmpResistivity")*100),                 #15| empDamageReduction = 
        DropTrailZero(itemData.get("ExtraSettings").get("Flammability")*100),                   #16| Flammability = 
        DropTrailZero(itemData.get("ExtraSettings").get("FireResistance")),                     #17| Fire Resistance = 
        DropTrailZero(round(itemData.get("ArmourClass")*0.2*itemData.get("ExtraSettings").get("StructuralComponent"), 1)), #18| maxStructuralArmourBoost = 
        "0",                                                                                    #19| extraLengthHealth =    Blocks here shouldn't have extraLengthHealth
        itemData.get("DragSettings").get("DragStopper"),                                        #20| dragStopper =
        GetDragValue(itemData.get("DragSettings").get("DragFactorPos"), 2),                     #21| dragFront = 
        GetDragValue(itemData.get("DragSettings").get("DragFactorNeg"), 2),                     #22| dragBack = 
        GetDragValue(itemData.get("DragSettings").get("DragFactorPos"), 1),                     #23| dragTop = 
        GetDragValue(itemData.get("DragSettings").get("DragFactorNeg"), 1),                     #24| dragBottom = 
        GetDragValue(itemData.get("DragSettings").get("DragFactorNeg"), 0),                     #25| dragLeft = 
        GetDragValue(itemData.get("DragSettings").get("DragFactorPos"), 0),                     #26| dragRight = 
        itemGuid,                                                                               #27| GUID = 
        DropTrailZero(itemData.get("RadarRelativeCrossSection")*10),                            #28| radarReturn =          Multiply by 10 to show how it is in mod menu
        DropTrailZero(itemData.get("SizeInfo").get("VolumeFactor")),                            #29| Volume Factor = 
        DropTrailZero(itemData.get("SizeInfo").get("VolumeBuoyancyExtraFactor")),               #30| Buoyancy Factor = 
        itemData.get("ExtraSettings").get("WaterTight"),                                        #31| waterTight = 
        itemData.get("ExtraSettings").get("ExplosionOnDeath"),                                  #32| explosionOnDeath = 
        itemData.get("ExtraSettings").get("PlaceableOnFortress"),                               #33| placeableOnFortress = 
        itemData.get("ExtraSettings").get("PlaceableOnStructure"),                              #34| placeableOnStructure = 
        itemData.get("ExtraSettings").get("PlaceableOnVehicle"),                                #35| placeableOnVehicle = 
        itemData.get("ExtraSettings").get("PlaceableInPrefab"),                                 #36| placeableInPrefab = 
        itemData.get("ExtraSettings").get("PlaceableOnSubConstructable"),                       #37| placeableOnSubConstructable = 
        itemData.get("ExtraSettings").get("AllowsExhaust"),                                     #38| allowsExhaust = 
        itemData.get("ExtraSettings").get("AllowsVisibleBandTransmission"),                     #39| allowsVisibleBandTransmission = 
        itemData.get("ExtraSettings").get("AllowsIrBandTransmission"),                          #40| allowsIrBandTransmission = 
        itemData.get("ExtraSettings").get("AllowsRadarBandTransmission"),                       #41| allowsRadarBandTransmission = 
        itemData.get("ExtraSettings").get("AllowsSonarBandTransmission")                        #42| allowsSonarBandTransmission = 
        ]
    subObjectList = itemData.get("SubObjects").get("SubObjects")                                #Gets a list of block subobjects ("extra meshes")
    if subObjectList != []:
        for subObject in subObjectList:
            blockDataDictionary[itemGuid].append(subObject.get("ObjectReference").get("Reference").get("Name"))
    blocksHandled = blocksHandled + 1
    print(f"{blocksHandled}. {blockDataDictionary[itemGuid][0]}")

for itemDupModFile in itemDupModFileList:                                       #Do with each .itemduplicateandmodify file
    rawItemDupModFile = open(itemDupModFile, "r")
    itemDataDM = json.load(rawItemDupModFile)
    idToDup = itemDataDM.get("IdToDuplicate").get("Reference").get("Guid")      #Preemptively get values to later test if they exist
    isSizeInfo = itemDataDM.get("SizeInfo")
    isDispName = itemDataDM.get("DisplayName")
    isDragSettings = itemDataDM.get("DragSettings")
    ownWeight = DropTrailZero(round(blockDataDictionary[idToDup][6]*itemDataDM.get("CostWeightHealthScaling")*itemDataDM.get("WeightScaling"), 1))
    itemDMGuid = itemDataDM.get("ComponentId").get("Guid")
    blockDataDictionary[itemDMGuid] = [
        itemDataDM.get("ComponentId").get("Name") if isDispName == None else re.sub("###.*?#?!", '',itemDataDM.get("DisplayName")),             #0| title =         If DisplayName doesn't exist use ComponentId.Name
        re.sub("###.*?#?!", '',itemDataDM.get("Description")),                                                                                  #1| Description = 
        itemDataDM.get("ComponentId").get("Name") + ".png" if isDispName == None else re.sub("###.*?#?!", '',itemDataDM.get("DisplayName")) + ".png",   #2| image =         If DisplayName doesn't exist use ComponentId.Name
        CategoryCheck(itemDataDM.get("InventoryTabOrVariantId").get("Reference").get("Name")),                                                  #3| category = 
        DropTrailZero(round(blockDataDictionary[idToDup][4]*itemDataDM.get("CostWeightHealthScaling")*itemDataDM.get("HealthScaling"), 1)),     #4| Health = 
        DropTrailZero(round(blockDataDictionary[idToDup][5]*itemDataDM.get("ArmourScaling"), 1)),                                               #5| Armour = 
        ownWeight,                                                                                                                              #6| Weight = 
        DropTrailZero(round(blockDataDictionary[idToDup][7]*itemDataDM.get("CostWeightHealthScaling")*itemDataDM.get("CostScaling"), 1)),       #7| Cost = 
        blockDataDictionary[idToDup][8] if isSizeInfo == None else GetDimension(itemDataDM.get("SizeInfo").get("SizePos").get("z"),itemDataDM.get("SizeInfo").get("SizeNeg").get("z")),     #8| length =    If no size info copy original size
        blockDataDictionary[idToDup][9] if isSizeInfo == None else GetDimension(itemDataDM.get("SizeInfo").get("SizePos").get("x"),itemDataDM.get("SizeInfo").get("SizeNeg").get("x")),     #9| width = 
        blockDataDictionary[idToDup][10] if isSizeInfo == None else GetDimension(itemDataDM.get("SizeInfo").get("SizePos").get("y"),itemDataDM.get("SizeInfo").get("SizeNeg").get("y")),    #10| height = 
        blockDataDictionary[idToDup][11] if isSizeInfo == None else DropTrailZero(round(10*((-9.81*ownWeight/100)+3.75*(itemDataDM.get("SizeInfo").get("ArrayPositionsUsed")*itemDataDM.get("SizeInfo").get("VolumeFactor")*itemDataDM.get("SizeInfo").get("VolumeBuoyancyExtraFactor")))+0.001, 1)),   #11| relativeBuoyancy =
        blockDataDictionary[idToDup][12] if isSizeInfo == None else DropTrailZero(round(itemDataDM.get("SizeInfo").get("ArrayPositionsUsed")*itemDataDM.get("SizeInfo").get("VolumeFactor")*itemDataDM.get("SizeInfo").get("VolumeBuoyancyExtraFactor")*37.5+0.001, 1)),   #12| emptySpaceBuoyancy = 
        blockDataDictionary[idToDup][13],                                                                                                       #13| empSusceptibility =        Copy original block
        blockDataDictionary[idToDup][14],                                                                                                       #14| empDamageTaken = 
        blockDataDictionary[idToDup][15],                                                                                                       #15| empDamageReduction = 
        blockDataDictionary[idToDup][16],                                                                                                       #16| Flammability = 
        blockDataDictionary[idToDup][17],                                                                                                       #17| Fire Resistance = 
        blockDataDictionary[idToDup][18],                                                                                                       #18| maxStructuralArmourBoost = 
        DropTrailZero(round(itemDataDM.get("HealthScaling")*100-100, 1)),                                                                       #19| extraLengthHealth =        Multiply by 100 and substract 10 to get percentage
        blockDataDictionary[idToDup][20] if isDragSettings == None else itemDataDM.get("DragSettings").get("DragStopper"),                      #20| dragStopper =          If doesn't exist copy original block value
        blockDataDictionary[idToDup][21] if isDragSettings == None else GetDragValue(itemDataDM.get("DragSettings").get("DragFactorPos"), 2),   #21| dragFront = 
        blockDataDictionary[idToDup][22] if isDragSettings == None else GetDragValue(itemDataDM.get("DragSettings").get("DragFactorNeg"), 2),   #22| dragBack = 
        blockDataDictionary[idToDup][23] if isDragSettings == None else GetDragValue(itemDataDM.get("DragSettings").get("DragFactorPos"), 1),   #23| dragTop = 
        blockDataDictionary[idToDup][24] if isDragSettings == None else GetDragValue(itemDataDM.get("DragSettings").get("DragFactorNeg"), 1),   #24| dragBottom = 
        blockDataDictionary[idToDup][25] if isDragSettings == None else GetDragValue(itemDataDM.get("DragSettings").get("DragFactorNeg"), 0),   #25| dragLeft = 
        blockDataDictionary[idToDup][26] if isDragSettings == None else GetDragValue(itemDataDM.get("DragSettings").get("DragFactorPos"), 0),   #26| dragRight = 
        itemDMGuid,                                                                                                                             #27| GUID = 
        blockDataDictionary[idToDup][28],                                                                                                       #28| radarReturn = 
        blockDataDictionary[idToDup][29] if isSizeInfo == None else DropTrailZero(itemDataDM.get("SizeInfo").get("VolumeFactor")),              #29| Volume Factor = 
        blockDataDictionary[idToDup][30] if isSizeInfo == None else DropTrailZero(itemDataDM.get("SizeInfo").get("VolumeBuoyancyExtraFactor")), #30| Buoyancy Factor = 
        blockDataDictionary[idToDup][31],                                                                                                       #31| waterTight = 
        blockDataDictionary[idToDup][32],                                                                                                       #32| explosionOnDeath = 
        blockDataDictionary[idToDup][33],                                                                                                       #33| placeableOnFortress = 
        blockDataDictionary[idToDup][34],                                                                                                       #34| placeableOnStructure = 
        blockDataDictionary[idToDup][35],                                                                                                       #35| placeableOnVehicle = 
        blockDataDictionary[idToDup][36],                                                                                                       #36| placeableInPrefab = 
        blockDataDictionary[idToDup][37],                                                                                                       #37| placeableOnSubConstructable = 
        blockDataDictionary[idToDup][38],                                                                                                       #38| allowsExhaust = 
        blockDataDictionary[idToDup][39],                                                                                                       #39| allowsVisibleBandTransmission = 
        blockDataDictionary[idToDup][40],                                                                                                       #40| allowsIrBandTransmission = 
        blockDataDictionary[idToDup][41],                                                                                                       #41| allowsRadarBandTransmission = 
        blockDataDictionary[idToDup][42]                                                                                                        #42| allowsSonarBandTransmission = 
        ]
    blocksHandled = blocksHandled + 1
    print(f"{blocksHandled}. {blockDataDictionary[itemDMGuid][0]}")

#List of infobox fields. Needs to be equal or bigger than number of blockDataDictionary keys for script to work
wikiTextFields = ["| title = ", "| Description = ", "| image = ", "| category = ", "| Health = ", "| Armour = ", "| Weight = ", "| Cost = ", "| length = ", "| width = ", "| height = ",
                "| relativeBuoyancy = ", "| emptySpaceBuoyancy = ", "| empSusceptibility = ", "| empDamageTaken = ", "| empDamageReduction = ", "| Flammability = ", "| Fire Resistance = ",
                "| maxStructuralArmourBoost = ", "| extraLengthHealth = ", "| dragStopper = ", "| dragFront = ", "| dragBack = ", "| dragTop = ", "| dragBottom = ", "| dragLeft = ",
                "| dragRight = ", "| GUID = ", "| radarReturn = ", "| Volume Factor = ", "| Buoyancy Factor = ", "| waterTight = ", "| explosionOnDeath = ", "| placeableOnFortress = ",
                "| placeableOnStructure = ", "| placeableOnVehicle = ", "| placeableInPrefab = ", "| placeableOnSubConstructable = ", "| allowsExhaust = ", "| allowsVisibleBandTransmission = ",
                "| allowsIrBandTransmission = ", "| allowsRadarBandTransmission = ", "| allowsSonarBandTransmission = ", "| mesh1 = ", "| mesh2 = ", "| mesh3 = ", "| mesh4 = ", "| mesh5 = ",
                "| mesh6 = ", "| mesh7 = ", "| mesh8 = ", "| mesh9 = ", "| mesh10 = ", "| mesh11 = ", "| mesh12 = ", "| mesh13 = ", "| mesh14 = ", "| mesh15 = ", "| mesh16 = ", "| mesh17 = ",
                "| mesh18 = ", "| mesh19 = ", "| mesh20 = ", "| mesh21 = ", "| mesh22 = ", "| mesh23 = ", "| mesh24 = ", "| mesh25 = ", "| mesh26 = ", "| mesh27 = ", "| mesh28 = "]

with open("BlockInfoboxes.txt", "w") as wikiFile:
    wikiFile.write("")                                    #Wipe the output file
    for blockDictCount in blockDataDictionary:                          #For every block in blockDataDictionary
        wikiFile.write("<pre>\n{{Block Infobox\n")
        for propertyCount in range(len(blockDataDictionary[blockDictCount])):                #Write values from wikiTextFields next to each value from each block in blockDataDictionary
            wikiFile.write(wikiTextFields[propertyCount] + str(blockDataDictionary[blockDictCount][propertyCount]) + "\n")
        wikiFile.write("}}\n</pre>\n")

with open("BlockData.csv", "w", encoding="utf-8") as csvFile:
    csvFile.write("")                                               #Wipe the output file
    for header in range(len(wikiTextFields)-1):                     #Write all headers except last
        csvFile.write('"' + wikiTextFields[header][2:-3] + '",')        #while slicing off | and =
    csvFile.write('"' + wikiTextFields[-1][2:-3] + '"\n')           #Last header
    for blockDictCount in blockDataDictionary:                          #For every block in blockDataDictionary
        for propertyCount in range(len(blockDataDictionary[blockDictCount])-1):                #Write values from wikiTextFields next to values from each block in blockDataDictionary
            csvFile.write('"' + str(blockDataDictionary[blockDictCount][propertyCount]).replace('"', "˝") + '",')
        csvFile.write('"' + str(blockDataDictionary[blockDictCount][-1]) + '"\n')
#The end
