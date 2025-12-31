const createQRCode = async (selector, sessionId) => {
    async function getUrl() {
        const res = await fetch("/api/data");
        const json = await res.json();

        return json.url
    }

    const url = await getUrl();
    const mobileUrl = `${url}/mobile/${sessionId}`;

    new QRCode(selector, mobileUrl);
}