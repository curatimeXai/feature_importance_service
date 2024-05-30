class Loader {
    static getLoaderTemplate(id = null) {
        return `<div ${id ? `id=${id}` : ''} class="loader-background">
            <div class="loader">
                <svg height="200" width="200">
                    <circle id="circle" cx="100" cy="100" r="50" stroke="#C1002A" stroke-width="5" fill="transparent"></circle>
                </svg>
            </div>
        </div>`
    }


    static start(anchorElement, id) {
        let wrap=document.createElement('div')
        wrap.innerHTML = Loader.getLoaderTemplate(id);
        let loader=wrap.firstElementChild
        loader.id=id
        anchorElement.append(loader)
    }

    static stop(id) {
        document.getElementById(id).remove()
    }

    static waitOnElement(selector) {
        return new Promise((resolve, reject) => {
            const interval = setInterval(() => {
                if (document.querySelector(selector)) {
                    clearInterval(interval);
                    resolve();
                }
            }, 100);

            setTimeout(() => {
                clearInterval(interval);
                reject(new Error('Element not found within timeout'));
            }, 10000);
        });
    }
}