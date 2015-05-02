from diethack import makeConverter, makeElements, makeProductUnits
import logging

def goal():
    mass = 89.0 # kg

    # There's no need to track what is referenced in DRI tables as "chloride".
    # It means only chloride part of NaCl, therefore it's tracked implicitly
    # by tracking sodium.
    # (Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate)

    # Dietary Reference Intake Tables (USDA)
    waterPerDay = 3.7 # kg (AI)
    sodiumPerDay = 1500.0 # mg (AI)
    sodiumMaxPerDay = 2300.0 # mg
    potassiumPerDay = 4700.0 # mg (AI)
    fiberPerDay = 38.0 # g (AI)
    sugarMaxEnergyPercent = 25.0 # %
    ironMaxPerDay = 45.0 # mg
    calciumPerDay = 1000.0 # mg (RDA)
    calciumMaxPerDay = 2500.0 # mg
    vitaminAPerDay = 900.0 # RAE (RDA)
    retinolMaxPerDay = 3000.0 # mcg
    vitaminCPerDay = 90.0 # mg (RDA)
    vitaminCMaxPerDay = 2000.0 # mg
    vitaminDPerDay = 15.0 # mcg (RDA)
    vitaminDMaxPerDay = 100.0 # mcg
    vitaminEPerDay = 15.0 # mg (RDA)
    vitaminESupMaxPerDay = 1000.0 # mg
    vitaminKPerDay = 120.0 # mcg (AI)
    thiaminPerDay = 1.2 # mg (RDA)
    riboflavinPerDay = 1.3 # mg (RDA)
    niacinPerDay = 16.0 # mg (RDA)
    niacinSupMaxPerDay = 35.0 # mg
    vitaminB6PerDay = 1.3 # mg (RDA)
    vitaminB6MaxPerDay = 100.0 # mg
    folatePerDay = 400.0 # DFE (RDA)
    folateSupMaxPerDay = 1000.0 # DFE
    vitaminB12PerDay = 2.4 # mcg (RDA)
    pantothenicAcidPerDay = 5.0 # mg (AI)
    biotinPerDay = 30.0 # mcg (AI)
    cholinePerDay = 550.0 # mg (AI)
    cholineMaxPerDay = 3500.0 # mg
    chromiumPerDay = 35.0 # mcg (AI)
    copperPerDay = 900.0 # mcg (RDA)
    copperMaxPerDay = 10000.0 # mcg
    fluoridePerDay = 4.0 # mg (AI)
    fluorideMaxPerDay = 10.0 # mg
    iodinePerDay = 150.0 # mcg (RDA)
    iodineMaxPerDay = 1100.0 # mcg
    magnesiumPerDay = 420.0 # mg (RDA)
    magnesiumSupMaxPerDay = 350.0 # mg
    manganesePerDay = 2.3 # mg (AI)
    manganeseMaxPerDay = 11.0 # mg
    molybdenumPerDay = 45.0 # mcg (RDA)
    molybdenumMaxPerDay = 2000.0 # mcg
    phosphorusPerDay = 700.0 # mg (RDA)
    phosphorusMaxPerDay = 4000.0 # mg
    seleniumPerDay = 55.0 # mcg (RDA)
    seleniumMaxPerDay = 400.0 # mcg
    zincPerDay = 11.0 # mg (RDA)
    zincMaxPerDay = 40.0 # mg
    boronMaxPerDay = 20.0 # mg
    nickelMaxPerDay = 1.0 # mg
    siliconMaxPerDay = 0
    vanadiumMaxPerDay = 1.8 # mg

    # Treating High Level Cholesterol (National Heart, Lung and Blood Institute)
    fatSatMaxEnergyPercent = 7.0 # %
    cholMaxPerDay = 200.0 # mg

    # Google
    fatEnergyPerGram = 9.0 # kcal
    carbEnergyPerGram = 4.0 # kcal

    # The Complete Guide to Food for Sports Performance (Burke, Cox)
    # pick products with low (GI < 55)-to-moderate (55 < GI < 70) sugar range
    # use www.glycemicindex.com to find product GI
    fatEnergyPercent = 25.0 # %
    carbScaleLow = 3.0 # g*kg-1 light training program
    carbScaleMed = 7.0 # g*kg-1 moderate excercise program
    proteinScale = 1.6 # g*kg-1 resistance training, weight gain
    ironPerDay = 17.5 # mg 
    bmr = 8.4 / 0.0042 # kcal (for 88 kg body mass, 30 years old)
    activity = 1.4 # sedatory lifestyle

    energyRateBig = 0.236 # kcal*kg-1*min-1 (in a 30 seconds) Energy Cost of Resistance Exercises: an Update (Reis, Junior, Zajac, Oliveira)
    energyRateMed = 0.101 # kcal*kg-1*min-1 Energy Cost of Moderate-Duration Resistance and Aerobic Excercise (Bloomer)
    energyRateLow = 0.06 # kcal*kg-1*min-1 (pull-ups, push-ups, curl-ups, lunges) Energy Expenditure of Resistance Training Activities in Young Men (Vezina)
    
    # my data
    # each set ~= 1 min
    timeWarmup = 5.0 # min
    timeDeadLift = 4.0 # min
    timeBenchPress = 4.0 # min
    timeBentOverRow = 3.0 # min
    timeBenchPressCloseGrip = 3.0 # min
    timeCurl = 2.0 # min
    timePinch = 5.0 # min
    timeCrunches = 3.0 # min
    timeBig = timeDeadLift + timeBenchPress # min
    timeMed = timeBentOverRow + timeBenchPressCloseGrip # min
    timeLow = timeCurl + timePinch + timeCrunches + timeWarmup # min
    timeTotal = timeLow + timeMed + timeBig # min
    timeReal = 120.0 # min
    timeScale = timeReal / timeTotal
    energyScale = timeBig*energyRateBig + timeMed*energyRateMed + timeLow*energyRateLow # kcal*kg-1
    energyScale *= timeScale
    energyWorkout = energyScale * mass # kcal

    logging.info('energy per workout: %i kcal' % energyWorkout)

    daysPerWeek = 7.0
    workoutsPerWeek = 1.0
    energyPerDay = (bmr*activity*daysPerWeek + energyWorkout*workoutsPerWeek) / daysPerWeek # kcal
    carbPerDay = mass * (carbScaleLow*(daysPerWeek - workoutsPerWeek) + carbScaleMed*workoutsPerWeek) / daysPerWeek # g
    proteinPerDay = mass * proteinScale # g
    fatPerDay = energyPerDay*fatEnergyPercent / (100.0 * fatEnergyPerGram)
    fatSatMaxPerDay = energyPerDay*fatSatMaxEnergyPercent / (100.0 * fatEnergyPerGram)
    sugarMaxPerDay = energyPerDay*sugarMaxEnergyPercent / (100.0 * carbEnergyPerGram)

    def relaxed(v):
        return [v*0.99, v*1.01]

    def unbound(v):
        return [v, v*100.0]

    def upper(v):
        return [0, max(v, 0.1)]

    return makeConverter().convertDict(makeElements(
        energy = (relaxed(energyPerDay), 'kcal'),
        water = (relaxed(waterPerDay), 'kg'),
        protein = (relaxed(proteinPerDay), 'g'),
        fat = (relaxed(fatPerDay), 'g'),
        fatSat = (upper(fatSatMaxPerDay), 'g'),
        carb = ([carbPerDay, carbPerDay*1.5], 'g'), # increased to meet energy needs
        sugar = (upper(sugarMaxPerDay), 'g'),
        sodium = ([sodiumPerDay, sodiumMaxPerDay], 'mg'),
        chol = (upper(cholMaxPerDay), 'mg'),
        fiber = (relaxed(fiberPerDay), 'g'),
        potassium = (unbound(potassiumPerDay), 'mg'),
        iron = ([ironPerDay, ironMaxPerDay], 'mg'),
        calcium = ([calciumPerDay, calciumMaxPerDay], 'mg'),
        vitaminA = (unbound(vitaminAPerDay), 'RAE'),
        retinol = (upper(retinolMaxPerDay), 'mcg'),
        vitaminC = ([vitaminCPerDay, vitaminCMaxPerDay], 'mg'),
        vitaminD = ([vitaminDPerDay, vitaminDMaxPerDay], 'mcg'),
        vitaminE = (unbound(vitaminEPerDay), 'mg'),
        vitaminESup = (upper(vitaminESupMaxPerDay), 'mg'),
        vitaminK = (relaxed(vitaminKPerDay), 'mcg'),
        thiamin = (relaxed(thiaminPerDay), 'mg'),
        riboflavin = (relaxed(riboflavinPerDay), 'mg'),
        niacin = (unbound(niacinPerDay), 'mg'),
        niacinSup = (upper(niacinSupMaxPerDay), 'mg'),
        vitaminB6 = ([vitaminB6PerDay, vitaminB6MaxPerDay], 'mg'),
        folate = (unbound(folatePerDay), 'DFE'),
        folateSup = (upper(folateSupMaxPerDay), 'DFE'),
        vitaminB12 = (relaxed(vitaminB12PerDay), 'mcg'),
        pantothenicAcid = (relaxed(pantothenicAcidPerDay), 'mg'),
        biotin = (relaxed(biotinPerDay), 'mcg'),
        choline = ([cholinePerDay, cholineMaxPerDay], 'mg'),
        chromium = (relaxed(chromiumPerDay), 'mcg'),
        copper = ([copperPerDay, copperMaxPerDay], 'mcg'),
        fluoride = ([fluoridePerDay, fluorideMaxPerDay], 'mg'),
        iodine = ([iodinePerDay, iodineMaxPerDay], 'mcg'),
        magnesium = (unbound(magnesiumPerDay), 'mg'),
        magnesiumSup = (upper(magnesiumSupMaxPerDay), 'mg'),
        manganese = ([manganesePerDay, manganeseMaxPerDay], 'mg'),
        molybdenum = ([molybdenumPerDay, molybdenumMaxPerDay], 'mcg'),
        phosphorus = ([phosphorusPerDay, phosphorusMaxPerDay], 'mg'),
        selenium = ([seleniumPerDay, seleniumMaxPerDay], 'mcg'),
        zinc = ([zincPerDay, zincMaxPerDay], 'mg'),
        boron = (upper(boronMaxPerDay), 'mg'),
        nickel = (upper(nickelMaxPerDay), 'mg'),
        silicon = (upper(siliconMaxPerDay), 'mg'),
        vanadium = (upper(vanadiumMaxPerDay), 'mg')
    ), makeProductUnits()['elements'])
