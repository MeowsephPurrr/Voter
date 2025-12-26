const btnConf = [
    {
        name: "BAD",
        value: "0",
        color: "red",
        group: 1
    },
    {
        name: "BAD",
        value: "0",
        color: "red",
        group: 1
    },
    {
        name: "BAD",
        value: "0",
        color: "red",
        group: 1
    },
    {
        name: "BAD",
        value: "0",
        color: "red",
        group: 1
    },
    {
        name: "GOOD",
        value: "1",
        color: "green",
        group: 1
    },
    {
        name: "?",
        value: "255",
        color: "blue",
        group: 2
    },
    {
        name: "!",
        value: "254",
        color: "yellow",
        group: 2
    },
];

const renderBtns = (containerId, callback) => {
    const container = document.getElementById(containerId);
    if (!container) return;

    const groups = btnConf.reduce((acc, btn) => {
        if (!acc[btn.group]) acc[btn.group] = [];
        acc[btn.group].push(btn);
        return acc;
    }, {});

    Object.keys(groups).forEach(groupNum => {
        const groupWrapper = document.createElement("div");
        groupWrapper.className = "group-wrapper";
        groupWrapper.setAttribute("data-group", groupNum);

        const buttonGrid = document.createElement("div");
        buttonGrid.className = "button-grid";

        groups[groupNum].forEach(btn => {
            const el = document.createElement("button");
            el.className = "btn";
            el.textContent = btn.name;
            el.style.backgroundColor = btn.color;
            buttonGrid.appendChild(el);
            el.addEventListener("click", () => {
                document.querySelectorAll('.btn').forEach(
                    b => {
                        b.classList.add('other-highlighted');
                        b.classList.remove('active-highlight');
                    });
                el.classList.add('active-highlight');
                el.classList.remove('other-highlighted');
                callback(btn.value)
            });
        });

        groupWrapper.appendChild(buttonGrid);
        container.appendChild(groupWrapper);
    });
}