class SidebarBuilder {
    constructor(columns, sidebarId) {
        this.columns = columns
        this.siderbarForm = document.getElementById(sidebarId)
        this.sidebarSubmitButton = this.siderbarForm.querySelector('button');
        this.localFormButtons = `
            <button id="randomizer" type="button">Randomize</button>
            <button type="submit">Explain</button>`
    }

    buildInput(key, title) {
        let column = this.columns[key]
        if (column.type === 'boolean')
            this.buildCheckbox(key, title)
        if (column.type === 'category')
            this.buildSelect(column, key, title)
        if (column.type === 'numerical')
            this.buildSlider(column, key, title)

    }

    buildInputWrapper() {
        let inputWrapper = document.createElement('div')
        inputWrapper.className = 'input-group'
        return inputWrapper
    }

    buildLabel(title, labelFor = 'text') {
        let label = document.createElement('label')
        label.htmlFor = labelFor;
        let textDiv = document.createElement('div')
        let textNode = document.createTextNode(title);
        textDiv.append(textNode)
        label.append(textDiv)
        return label;
    }

    buildCheckbox(key, title, checked = false) {
        let inputWrapper = this.buildInputWrapper()
        let label = this.buildLabel(title, 'checkbox')
        let input = document.createElement('input')
        input.type = 'checkbox'
        input.name = key
        input.checked = checked
        label.append(input)
        label.className = 'flex'
        inputWrapper.append(label)
        this.siderbarForm.append(inputWrapper);
    }

    buildSelect(column, key, title, selected = null) {
        let inputWrapper = this.buildInputWrapper()
        let label = this.buildLabel(title, 'select')
        let selectElement = document.createElement('select')
        selectElement.name = key;
        const columnValuesEntries = Object.entries(column.values);

        columnValuesEntries.sort((a, b) => a[1] - b[1]);
        columnValuesEntries.forEach(value => {
            let option = document.createElement('option')
            option.innerText = value[0]
            if (selected === value[0])
                option.selected = true;

            selectElement.append(option)
        })
        label.append(selectElement)
        inputWrapper.append(label)
        this.siderbarForm.append(inputWrapper);
    }

    buildSlider(column, key, title) {
        let inputWrapper = this.buildInputWrapper();
        let label = this.buildLabel(title, 'range');
        let rangeInput = document.createElement('input');
        rangeInput.type = 'range';
        rangeInput.name = key
        rangeInput.min = column.values[0];
        rangeInput.max = column.values[1];
        rangeInput.step = 1;
        let input = document.createElement('input')
        input.type = 'number'
        input.value = parseInt(rangeInput.value)
        rangeInput.oninput = (ev) => {
            input.value = parseInt(ev.target.value)
        }
        input.oninput = (ev) => {
            rangeInput.value = parseInt(ev.target.value)
        }
        label.append(rangeInput);
        label.append(input);
        inputWrapper.append(label);
        this.siderbarForm.append(inputWrapper);
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