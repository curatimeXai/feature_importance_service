class FormHelper {
    static buildUrlWithFormInputs(url, formId) {
        const jsUrl = new URL(url);
        const formEl = document.getElementById(formId)
        Array.from(formEl.elements).forEach((input) => {
            if (input.name.length > 0)
                jsUrl.searchParams.append(input.name, input.value)
        })
        return jsUrl.href

    }

    static randomizeFormInputs(formId) {
        const formEl = document.getElementById(formId)
        Array.from(formEl.elements).forEach((input) => {
            if (input.name.length > 0) {
                if (input.tagName === 'SELECT') {
                    const optionsNr = input.options.length
                    input.selectedIndex = Math.floor(Math.random() * optionsNr);
                }
                if (input.type === 'range') {
                    let randVal = parseInt(Math.random() * (input.max - input.min) + input.min)
                    let numberInput = input.parentElement.querySelector('input[type="number"]')
                    input.value = randVal;
                    numberInput.value=randVal
                }
                if (input.type === 'checkbox') {
                    input.checked = Math.random() >= 0.5;
                }
            }
        })
    }
}