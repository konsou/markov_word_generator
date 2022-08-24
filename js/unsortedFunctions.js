const generateNames = async (numberOfNames, generatorInstructions) => {
    //tag = "finnish_names_female"
    const names = []
    let name = ""

    for (let i = 0; i < numberOfNames; i++) {
        console.log(i)
        name = await generateNameFromInstructions(generatorInstructions)
        console.log(name)
        names.push(name)
    }
    return names
}

const generateNameFromInstructions = async (instructions) => {
    console.log(instructions)
    let words = []
    let generatedWord, analysisData, instruction
    for (let index in instructions){
        instruction = instructions[index]
        console.log(instruction)
        analysisData = await getAnalysisData(instruction.chainLength, instruction.tag)
        generatedWord = await generateWord(analysisData, instruction.chainLength)
        if (instruction.capitalize){ generatedWord = capitalizeFirstLetter(generatedWord) }
        words.push(generatedWord)
    }
    return words.join(" ")
}


const generateWord = async (analysisData, chainLength) => {
    let previousLetter = ""
    let word = ""
    let nextLetterFrequencies = {}
    let letters, weights

    while (true){
        nextLetterFrequencies = analysisData[previousLetter]
        // console.log(nextLetterFrequencies)

        letters = []
        weights = []

        for (let letter in nextLetterFrequencies) {
            let weight = nextLetterFrequencies[letter]
            // console.log(`letter: ${letter}`)
            // console.log(`weight: ${weight}`)
            letters.push(letter)
            weights.push(weight)
        }
        // console.log(`letters: ${letters}`)
        // console.log(`weights: ${weights}`)

        const chosenLetter = weightedRandom(letters, weights).item
        // console.log(`chosenLetter: ${chosenLetter}`)

        word = `${word}${chosenLetter}`

        previousLetter += chosenLetter

        previousLetter = previousLetter.slice(-chainLength)

        if (chosenLetter === ""){
            break
        }
    }
    return word
}

const getAnalysisData = async (chainLength, tag) => {
    const analysisDataFilename = `data_processed/analysis_results_${tag}_${chainLength}.json`
    let analysisData
    // console.log(analysisDataFilename)

    try {
        analysisData = await getFromCache(analysisDataFilename)
        // console.log(`loaded ${analysisDataFilename} from cache`)
        return analysisData
    } catch {
        analysisData = await(await fetch(analysisDataFilename)).json()
        // console.log(`loaded ${analysisDataFilename} from file`)
    }
    await saveToCache(analysisDataFilename, analysisData)
    return analysisData
}

const getFromCache = async (name) => {
    // console.log(`getFromCache: ${name}`)
    const result = window.analysisCache[name]
    // console.log(result)
    if (!result) { throw "notFoundInCache" }
    return result
}

const saveToCache = async (name, data) => {
    window.analysisCache[name] = data
    // console.log(`saved ${name} to cache`)
}

const updateAdvancedOptionsContent = (generatorInstructions) => {
    const instructionsTextField = document.getElementById("generator-instructions")
    instructionsTextField.value = JSON.stringify(generatorInstructions, null, 2)
}

const updateRealismSliderValue = (value) => {
    const realismSlider = document.getElementById("realism-slider")
    realismSlider.value = value
    document.getElementById("realism-slider-value").innerHTML = value.toString()
}

const getUpdatedGeneratorInstructions = (realismValue, generatorInstructions) => {
    //console.log(generatorInstructions)
    const copiedInstructions = JSON.parse(JSON.stringify(generatorInstructions))
    copiedInstructions.forEach((item, index) => {
        console.log(item)
        console.log(index)
        item.chainLength = item.tag === "finnish_names_surnames"
            ? realismValue + 1
            : realismValue
    })
    //console.log(copiedInstructions)
    return copiedInstructions
}

