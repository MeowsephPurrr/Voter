async function getTickets() {
    const res = await fetch("/api/tickets");
    const json = await res.json();

    console.log(json)
    return json
}

getTickets();