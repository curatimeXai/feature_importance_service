class ChartBuilder {
    getLoaderTemplate(id) {
         return `
            <div id="${id}" class="loader-background" style="display: block; height: 400px;">
                <div class="loader">
                    <svg height="200" width="200">
                        <circle id="circle" cx="100" cy="100" r="50" stroke="#C1002A" stroke-width="5" fill="transparent"></circle>
                    </svg>
                </div>
            </div>`
    }

    startLoading(chartId) {
        let chartWrapperTemplate = `
            <div id="${chartId}" class="col-8" style="position: relative; height: 0;">
            </div>
        `;
        let wrapper = document.createElement('div')
        wrapper.innerHTML = chartWrapperTemplate;
        wrapper.firstElementChild
        wrapper.firstElementChild.innerHTML = this.getLoaderTemplate(chartId + '-loader')
        return wrapper.firstElementChild
    }

    stopLoading(chartId) {
        let chartLoader = document.getElementById(chartId + '-loader');
        chartLoader.style.display = 'none';
    }

    buildChart(chartId, chartData) {
        Plotly.newPlot(chartId, chartData.data, chartData.layout)
    }

    loadChart(chartId,anchor, promise) {
        let chartElement = this.startLoading(chartId)
        anchor.append(chartElement)
        promise.then(async response => {
            this.buildChart(chartId, await response.json())
            this.stopLoading(chartId)
        });
    }
}