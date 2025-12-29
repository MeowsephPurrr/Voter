const createQRCode = async (selector) => {
    async function getUrl() {
        const res = await fetch("/api/data");
        const json = await res.json();

        return json.url
    }

    const url = await getUrl();
    const sessionId = window.location.pathname.split('/').pop();
    const mobileUrl = `${url}/mobile/${sessionId}`;

    new QRCode(selector, mobileUrl);
}