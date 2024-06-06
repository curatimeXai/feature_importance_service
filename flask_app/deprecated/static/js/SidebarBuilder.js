class SidebarBuilder {
    constructor(columns, sidebarId) {
        this.columns = columns
        this.siderbarForm = document.getElementById(sidebarId)
        this.sidebarSubmitButton = this.siderbarForm.querySelector('button');
        this.localFormButtons = `
        <div class="row">
            <button id="randomizer" type="button">Randomize</button>
            <button type="submit">Explain</button>
        </div>`
    }

    buildInput(key, title,tooltip='test') {
        let column = this.columns[key]
        if (column.type === 'boolean')
            this.buildCheckbox(key, title)
        if (column.type === 'category')
            this.buildSelect(column, key, title)
        if (column.type === 'numerical')
            this.buildSlider(column, key, title,tooltip)

    }

    buildInputWrapper() {
        let inputWrapper = document.createElement('div')
        inputWrapper.className = 'input-group'
        return inputWrapper
    }

    buildLabel(title, labelFor = 'text',tooltip) {
        let label = document.createElement('label')
        label.htmlFor = labelFor;
        let textDiv = document.createElement('div')
        let textNode = document.createTextNode(title);
        textDiv.append(textNode)
        // textDiv.insertAdjacentHTML('beforeend', this.getTooltipTemplate(tooltip))
        label.append(textDiv)
        return label;
    }

    buildCheckbox(key, title, checked = false) {
        let inputWrapper = FormHelper.getInputWrapper(title, 'checkbox')
        inputWrapper.label.classList.add('space-between')
        let input = FormHelper.getCheckboxElement(key,checked,'col-6')
        inputWrapper.label.append(input)
        this.siderbarForm.append(inputWrapper.inputWrapper);
    }

    buildSelect(column, key, title, selected = null,tooltip='') {
        let inputWrapperObj = FormHelper.getInputWrapper(title, 'select', 'col-6')
           if (tooltip) {
            inputWrapperObj.labelTitle.insertAdjacentHTML('beforeend', FormHelper.getTooltipTemplate(tooltip));
        }
        let selectElement = FormHelper.getSelectElement(key,column,selected,'col-6')
        inputWrapperObj.label.append(selectElement)
        this.siderbarForm.append(inputWrapperObj.inputWrapper);
    }

    buildSlider(column, key, title, tooltip = '') {
        let inputWrapperObj = FormHelper.getInputWrapper(title, 'range')
        if (tooltip)
            inputWrapperObj.labelTitle.insertAdjacentHTML('beforeend', FormHelper.getTooltipTemplate(tooltip));
        inputWrapperObj.label.append(FormHelper.getSliderElement(key, column.values[0], column.values[1]))
        this.siderbarForm.append(inputWrapperObj.inputWrapper);
    }

    buildButtons(buttonsCollection) {
        let buttonsWrapperObj = FormHelper.getButtonsWrapper()
        buttonsCollection.forEach(buttonObj => {
            buttonsWrapperObj.buttonsWrapper.append(this.buildButton(buttonObj.type, buttonObj.text, buttonObj.id))
        })
        return buttonsWrapperObj.buttonsWrapper;
    }
    buildButton(type, text, id = null) {
        let btn = document.createElement('button')
        btn.type = type
        btn.innerText = text
        if (id)
            btn.id = id
        this.siderbarForm.append(btn)
        return btn
    }



}