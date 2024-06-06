class FormHelper {


    static getTooltipTemplate(tooltipText, width = 30) {
        return `
        <span class="tooltip-container mr-1">
            <svg style="width: ${width}px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle opacity="0.5" cx="12" cy="12" r="10" stroke="#C1002A" stroke-width="1.5"/>
                    <path d="M10.125 8.875C10.125 7.83947 10.9645 7 12 7C13.0355 7 13.875 7.83947 13.875 8.875C13.875 9.56245 13.505 10.1635 12.9534 10.4899C12.478 10.7711 12 11.1977 12 11.75V13" stroke="#C1002A" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="12" cy="16" r="1" fill="#C1002A"/>
            </svg>
            <span class="tooltip-text">${tooltipText}</span>
        </span>
        `;
    }

    static getInputWrapper(title, label_for = "", className = 'col-9') {
        let inputWrapperTemplate = `
            <div class="input-group mb-1">
                <label class="row col-12" for="${label_for}">
                    <div class="flex v-align-center space-between ${className}">${title}</div>
                </label>
            </div>
        `;
        let wrapper = document.createElement('div')
        wrapper.innerHTML = inputWrapperTemplate;
        return {
            inputWrapper: wrapper.firstElementChild,
            label: wrapper.firstElementChild.firstElementChild,
            labelTitle: wrapper.firstElementChild.firstElementChild.firstElementChild
        }
    }

     static getButtonsWrapper() {
        let inputWrapperTemplate = `
            <div class="input-group row mb-1" style="justify-content: flex-end; gap: 10px">
            </div>
        `;
        let wrapper = document.createElement('div')
        wrapper.innerHTML = inputWrapperTemplate;
        return {
            buttonsWrapper: wrapper.firstElementChild,
        }
    }


    static getCheckboxElement(name, checked=false, className = "") {
        let input = document.createElement('input')
        input.type = 'checkbox'
        input.name = name
        input.checked = checked
        input.className=className
        return input;
    }

    static getSelectElement(name, options, selected = null, className = "") {
        let selectElement = document.createElement('select')
        selectElement.name = name;
        selectElement.className = className;
        const columnValuesEntries = Object.entries(options.values);
        columnValuesEntries.sort((a, b) => a[1] - b[1]);
        columnValuesEntries.forEach(value => {
            let option = document.createElement('option')
            option.innerText = value[0]
            if (selected === value[0])
                option.selected = true;

            selectElement.append(option)
        })
        return selectElement;
    }

    static getSliderElement(name, min, max) {
        let sliderTemplate = `
            <div class="row col-3">
                <input class="col-12" type="range" name="${name}" step="1" min="${min}" max="${max}">
                <input class="mt-05 col-12" type="number" min="${parseInt(min)}" max="${parseInt(max)}">
            </div>
        `;
        let wrapper = document.createElement('div')
        wrapper.innerHTML = sliderTemplate;
        let rangeInput = wrapper.querySelector('input[type="range"]')
        let input = wrapper.querySelector('input[type="number"]')
        input.value = parseInt(rangeInput.value)
        rangeInput.oninput = (ev) => {
            input.value = parseInt(ev.target.value)
        }
        input.oninput = (ev) => {
            rangeInput.value = parseInt(ev.target.value)
        }
        return wrapper.firstElementChild
    }

    static buildUrlWithFormInputs(url, formId) {
        const jsUrl = new URL(url);
        const formEl = document.getElementById(formId)
        Array.from(formEl.elements).forEach((input) => {
            if (input.name.length > 0)
                jsUrl.searchParams.append(input.name, input.type === 'checkbox' ? input.checked : input.value)
        })
        return jsUrl.href

    }

    static getFormValues(formId) {
        const formValuesObject = {}
        const formEl = document.getElementById(formId)
        Array.from(formEl.elements).forEach((input) => {
            if (input.name.length > 0)
                formValuesObject[input.name] = input.type === 'checkbox' ? input.checked : input.value
        })
        return formValuesObject;
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
                    numberInput.value = randVal
                }
                if (input.type === 'checkbox') {
                    input.checked = Math.random() >= 0.5;
                }
            }
        })
    }
}