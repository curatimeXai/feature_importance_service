class IframeBuilder {
    constructor() {
        this.loaderTemplate = `
            <div class="loader-background" style="display: block">
                <div class="loader">
                    <svg height="200" width="200">
                        <circle id="circle" cx="100" cy="100" r="50" stroke="#C1002A" stroke-width="5" fill="transparent"></circle>
                    </svg>
                </div>
            </div>`
    }

    buildIframeWrapper() {
        const iframeWrapper=document.createElement('div')
        iframeWrapper.className='iframe-wrapper col-6'
        return iframeWrapper
    }

    buildIframe(iframeId,url,anchorEl) {
        const iframe=document.createElement('div')
        iframe.id=iframeId
        const iframeWrapper=this.buildIframeWrapper()
        iframeWrapper.append(iframe)
        anchorEl.append(iframeWrapper)
        this.loadIframe(iframeId,url)
    }

    loadIframe(id, url) {
        const iframeDiv = document.getElementById(id)
        iframeDiv.innerHTML = this.loaderTemplate
        const iframeElem = document.createElement('iframe');
        iframeElem.className = 'chart-iframe col-12'
        iframeElem.src = url
        iframeElem.addEventListener('load', () => {
            let chartLoader = iframeDiv.getElementsByClassName('loader-background')[0];
            chartLoader.style.display = 'none';
        });
        iframeDiv.append(iframeElem)

    }
}