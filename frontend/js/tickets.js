class Ticket {
    id;
    title;
    description;

    constructor(id, title, description) {
        this.id = id;
        this.title = title;
        this.description = description;
    }
}

const getTickets = async () => {
    const res = await fetch("/api/tickets");
    const json = await res.json();

    const tickets = [];
    json.forEach(el => {
        tickets.push(new Ticket(el.id, el.title, el.description));
    });

    return tickets
}

const loadTemplateDom = async () => {
    const response = await fetch('/static/ticket.html');
    const text = await response.text();
    const parser = new DOMParser();
    return parser.parseFromString(text, 'text/html')
}

const renderTickets = async () => {
    const tickets = await getTickets();
    const ticketTemplateDom = await loadTemplateDom();
    const targetElement = document.querySelector(".ticket-container");

    const template = buildTickets(ticketTemplateDom, tickets);
    targetElement.appendChild(template);
}

const buildTickets = (dom, tickets) => {
    const ticketTemplate = dom.querySelector(".ticket-template").content;
    const ticketContainer = document.createElement("template").content;
    tickets.forEach(ticket => {
        const cpTicketTemplate = ticketTemplate.cloneNode(true).querySelector(".ticket");
        cpTicketTemplate.querySelector(".ticket-title").innerText = ticket.title;
        cpTicketTemplate.querySelector(".ticket-description").innerText = ticket.description;

        ticketContainer.appendChild(cpTicketTemplate);
    });

    return ticketContainer;
}