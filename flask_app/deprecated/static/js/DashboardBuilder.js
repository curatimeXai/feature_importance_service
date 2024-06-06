class DashboardBuilder {
    constructor(dashboardId, formId, columns) {
        this.dashboardElement = document.getElementById(dashboardId)
        this.formId = formId
        this.sidebarBuilder = new SidebarBuilder(columns, 'sidebarForm')
        this.localChartsUris = ['/xdg/breakdown', '/xdg/shapley']
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


    buildGlobalForm() {
        this.localForm = this.sidebarBuilder.siderbarForm.innerHTML;
        this.sidebarBuilder.siderbarForm.innerHTML = ''
    }

    buildLocalDashboard() {
        this.buildLocalForm()
        this.buildLocalCharts()
    }

    buildLocalForm() {
        this.globalForm = this.sidebarBuilder.siderbarForm.innerHTML;
        this.sidebarBuilder.siderbarForm.innerHTML = ''
        this.sidebarBuilder.buildInput('BMI', 'Body Mass Index', 'Body Mass Index is an important measurement for checking whether someone is probably obese. (> 26)')
        this.sidebarBuilder.buildInput('PhysicalHealth', 'Physical Health', 'For how many days during the past 30 days was the physical health good?')
        this.sidebarBuilder.buildInput('MentalHealth', 'Mental Health', 'For how many days during the past 30 days was the physical health good?')
        this.sidebarBuilder.buildInput('SleepTime', 'Sleep Time', 'Amount of sleep time can have an significant effect on the probability of having heart disease.')
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
        let buttonsWrapper=this.sidebarBuilder.buildButtons([
            {
                type: 'button',
                text: 'Randomize',
                id: 'randomizer',
            },
            {
                 type: 'submit',
                text: 'Explain',
            }
        ])
        this.sidebarBuilder.siderbarForm.append(buttonsWrapper)
        let randomizer = document.getElementById('randomizer')
        randomizer.onclick = () => {
            FormHelper.randomizeFormInputs(this.formId)
        }
        document.getElementById(this.formId).addEventListener('submit', event => {
            event.preventDefault()
            this.buildLocalCharts()
        })
    }

    buildLocalCharts() {
        this.dashboardElement.innerHTML = ''
        let chartBuilder = new ChartBuilder()
        let params = FormHelper.getFormValues(this.formId);
        chartBuilder.loadChart('chart0',
            this.dashboardElement,
            Http.get('/xdg/breakdown', params));
        chartBuilder.loadChart('chart1',
            this.dashboardElement,
            Http.get('/xdg/shapley', params));
    }
}