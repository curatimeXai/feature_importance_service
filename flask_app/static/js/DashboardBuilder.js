class DashboardBuilder {
    constructor(dashboardId, formId, columns) {
        this.dashboardElement = document.getElementById(dashboardId)
        this.formId = formId
        this.sidebarBuilder = new SidebarBuilder(columns, 'sidebarForm')
        this.globalDashboard = null
        this.globalForm = null
        this.localDashboard = null
        this.localForm = null
    }


    buildGlobalDashboard() {
        this.buildGlobalForm()
        var url1 = 'http://127.0.0.1:5000/xdg/vip'
        var url2 = 'http://127.0.0.1:5000/xdg/pdp'
        var url3 = 'http://127.0.0.1:5000/xdg/modelperformance'
        const iframeBuilder = new IframeBuilder()
        this.dashboardElement.innerHTML = ''
        iframeBuilder.buildIframe('iframe1', url1, this.dashboardElement)
        iframeBuilder.buildIframe('iframe2', url2, this.dashboardElement)
        iframeBuilder.buildIframe('iframe3', url3, this.dashboardElement)
        this.globalDashboard = this.dashboardElement.innerHTML
    }

    buildLocalDashboard() {
        this.buildLocalForm()
        var url1 = 'http://127.0.0.1:5000/xdg/breakdown'
        url1 = FormHelper.buildUrlWithFormInputs(url1, this.formId)
        var url2 = 'http://127.0.0.1:5000/xdg/shapley'
        url2 = FormHelper.buildUrlWithFormInputs(url2, this.formId)
        var url3 = 'http://127.0.0.1:5000/xdg/ceterisparabus'
        url3 = FormHelper.buildUrlWithFormInputs(url3, this.formId)
        const iframeBuilder = new IframeBuilder()
        this.dashboardElement.innerHTML = ''
        iframeBuilder.buildIframe('iframe1', url1, this.dashboardElement)
        iframeBuilder.buildIframe('iframe2', url2, this.dashboardElement)
        iframeBuilder.buildIframe('iframe3', url3, this.dashboardElement)
        this.localDashboard = this.dashboardElement.innerHTML

    }

    buildGlobalForm() {
        this.localForm = this.sidebarBuilder.siderbarForm.innerHTML;
        this.sidebarBuilder.siderbarForm.innerHTML = ''
    }

    buildLocalForm() {
        this.globalForm = this.sidebarBuilder.siderbarForm.innerHTML;
        this.sidebarBuilder.siderbarForm.innerHTML = ''
        this.sidebarBuilder.buildInput('BMI', 'Body Mass Index')
        this.sidebarBuilder.buildInput('PhysicalHealth', 'For how many days during the past 30 days was your physical health not good?')
        this.sidebarBuilder.buildInput('MentalHealth', 'For how many days during the past 30 days was your mental health not good?')
        this.sidebarBuilder.buildInput('SleepTime', 'Sleep Time')
        this.sidebarBuilder.buildInput('AgeCategory', 'Age Category')
        this.sidebarBuilder.buildInput('Sex', 'Sex')
        this.sidebarBuilder.buildInput('Race', 'Race')
        this.sidebarBuilder.buildInput('Diabetic', 'Is Diabetic')
        this.sidebarBuilder.buildInput('GenHealth', 'General Health')
        this.sidebarBuilder.buildInput('Smoking', 'Is Smoking')
        this.sidebarBuilder.buildInput('AlcoholDrinking', 'Drinks alcohol')
        this.sidebarBuilder.buildInput('Stroke', 'Had Stroke')
        this.sidebarBuilder.buildInput('DiffWalking', 'Has Difficulties Walking')
        this.sidebarBuilder.buildInput('PhysicalActivity', 'Has Physical Activity')
        this.sidebarBuilder.buildInput('Asthma', 'Has Asthma')
        this.sidebarBuilder.buildInput('KidneyDisease', 'Has Kidney Disease')
        this.sidebarBuilder.buildInput('SkinCancer', 'Has Skin Cancer')
        let randomizer=this.sidebarBuilder.buildButton('button', 'Randomize', 'randomizer')
        randomizer.onclick = () => {
            FormHelper.randomizeFormInputs(this.formId)
        }
        this.sidebarBuilder.buildButton('submit', 'Explain', 'randomizer')
        document.getElementById(this.formId).addEventListener('submit', event => {
            event.preventDefault()
            this.buildLocalForm()
        })
    }
}