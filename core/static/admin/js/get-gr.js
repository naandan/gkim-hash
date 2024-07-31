function handleQr() {
    const url = new URL(window.location.href);
    const pathParts = url.pathname.split('/');
    const desiredValue = pathParts[pathParts.length - 3];

    document.body.addEventListener('htmx:configRequest', (event) => {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        event.detail.headers['X-CSRFToken'] = csrfToken;
    });
    
    let qrcodeContainer = document.getElementById("qrcode");
    const btnGenerate = document.getElementById('btnGenerate');

    if (qrcodeContainer && btnGenerate) {
        qrcodeContainer.setAttribute('hx-get', `/management/qr-code/${desiredValue}`);
        btnGenerate.setAttribute('hx-post', `/management/qr-code/${desiredValue}/regenerate`);
        
        document.addEventListener('htmx:afterRequest', (event) => {
            qrcodeContainer.innerHTML = "";
            const code = JSON.parse(event.detail.xhr.response).qrcode;
            new QRCode(qrcodeContainer, {
                text: code,
                width: 256,
                height: 256,
                colorDark: "#000",
                colorLight: "#fff",
                correctLevel: QRCode.CorrectLevel.H
            });
        });
    }
}

handleQr();

$('.field-qrcode').hide();
