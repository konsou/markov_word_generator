const DOMLoaded = (event) => {
    console.log('dom ready')
    window.analysisCache = {}
    const tag = document.querySelector('input[name="tag"]:checked').value

    window.generatorInstructions = {
        "finnish_names_male": [{chainLength: 3, tag: "finnish_names_male", capitalize: true},
            {chainLength: 4, tag: "finnish_names_surnames", capitalize: true}],
        "finnish_names_female": [{chainLength: 3, tag: "finnish_names_female", capitalize: true},
            {chainLength: 4, tag: "finnish_names_surnames", capitalize: true}],
        "animal_scientific_names": [{chainLength: 3, tag: "animal_scientific_names_first_part", capitalize: true},
            {chainLength: 3, tag: "animal_scientific_names_second_part", capitalize: false}],
    }
    window.chosenInstructions = generatorInstructions[tag]
    window.defaultRealismValue = 3
    updateAdvancedOptionsContent(chosenInstructions)


    document.getElementById("button-generate").addEventListener("click", generateNamesClick)
    document.getElementById("generator-instructions").addEventListener("change", advancedOptionsContentChanged)
    document.getElementById("generator-instructions").addEventListener("keyup", advancedOptionsContentChanged)
    document.querySelectorAll('input[name="tag"]').forEach(element => {
        element.addEventListener("change", nameTypeChanged)
    })
    document.getElementById("toggle-advanced-options-visibility").addEventListener("click", toggleAdvancedOptionsVisibility)
    document.getElementById("generator-instructions-label").addEventListener("click", toggleAdvancedOptionsVisibility)
    document.getElementById("realism-slider").addEventListener("change", realismSliderChanged)

}

const generateNamesClick = async () => {
    console.log('yo')
    const tag = document.querySelector('input[name="tag"]:checked').value
    console.log(tag)
    //const chainLength = parseInt(document.getElementById("chain-length").value)
    const numberOfNames = parseInt(document.getElementById("names-to-generate").value)
    //console.log(chainLength)
    console.log(numberOfNames)

    const names = await generateNames(numberOfNames, window.chosenInstructions)
    console.log(names)

    document.getElementById("generated-names").textContent = names.join("\n")
}

const advancedOptionsContentChanged = (event) => {
    const instructionsTextField = document.getElementById("generator-instructions")
    try {
        //console.log(instructionsTextField.value)
        window.chosenInstructions = JSON.parse(instructionsTextField.value)
        console.log("valid json")
        //console.log(window.chosenInstructions)
        document.getElementById("instructions-valid-symbol").innerHTML = "✔️"
    } catch (e) {
        console.warn("invalid JSON")
        document.getElementById("instructions-valid-symbol").innerHTML = "❌"
    }
}

const nameTypeChanged = (event) => {
    const tag = document.querySelector('input[name="tag"]:checked').value
    window.chosenInstructions = window.generatorInstructions[tag]
    console.log(`tag changed to ${tag}`)
    updateAdvancedOptionsContent(window.chosenInstructions)
    updateRealismSliderValue(window.defaultRealismValue)
}

const toggleAdvancedOptionsVisibility = (event) => {
    event.preventDefault()
    const advancedOptionsContainer = document.getElementById("advanced-options-container")
    const currentVisibility = advancedOptionsContainer.style.display
    console.log(currentVisibility)
    const newVisibility = currentVisibility === "block" ? "none" : "block"
    advancedOptionsContainer.style.display = newVisibility
}

const realismSliderChanged = (event) => {
    const newValue = parseInt(event.target.value)
    console.log(newValue)
    window.chosenInstructions = getUpdatedGeneratorInstructions(newValue, window.chosenInstructions)
    updateAdvancedOptionsContent(window.chosenInstructions)
    document.getElementById("realism-slider-value").innerHTML = newValue.toString()
}
