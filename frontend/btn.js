const btnConf = [
    {
        name: "1",
        value: "1",
        color: "blue",
        img: "1.png",
        trivia: ["A 'mew-tual' understanding.", "Easy as knocking a glass off a table."],
        group: 1
    },
    {
        name: "2",
        value: "2",
        color: "blue",
        img: "2.png",
        trivia: ["Totally 'paws-ible' to finish today.", "Just a small 'zoomie' of effort required."],
        group: 1
    },
    {
        name: "3",
        value: "3",
        color: "blue",
        img: "3.png",
        trivia: ["Feeling 'fur-tunate' about this one.", "A bit of a scratcher, but nothing we can't lick."],
        group: 1
    },
    {
        name: "5",
        value: "5",
        color: "blue",
        img: "5.png",
        trivia: ["Entering 'cat-astrophic' territory if we rush.", "Requires 'purr-cision' and focus."],
        group: 1
    },
    {
        name: "8",
        value: "8",
        color: "blue",
        img: "8.png",
        trivia: ["This looks like a 'hairy' situation.", "Don't have a 'hissy' fit, it's just a big task."],
        group: 1
    },
    {
        name: "13",
        value: "13",
        color: "blue",
        img: "13.png",
        trivia: ["The 'tail' of a very long sprint.", "Are you 'kitten' me? This is a lot of work."],
        group: 1
    },
    {
        name: "21",
        value: "21",
        color: "blue",
        img: "21.png",
        trivia: ["Call in the 'cat-alyst', we're stuck.", "Absolute 'meow-ntain' of a task."],
        group: 1
    },
    {
        name: "?",
        value: "?",
        color: "yellow",
        img: "question.png",
        trivia: ["Is it a red laser dot? Nobody knows.", "Pure 'meow-stery'?"],
        group: 2
    },
    {
        name: "!",
        value: "!",
        color: "red",
        img: "bang.png",
        trivia: ["CAT-CON 1: Immediate 'purr-gent' action required.", "Abandon ship! Use one of your 9 lives."],
        group: 2
    },
];

const btnEl = [];

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
            btnEl.push(el);
        });

        groupWrapper.appendChild(buttonGrid);
        container.appendChild(groupWrapper);
    });
}

const getBtn = (value) => {
    return btnConf.find(item => item.value === value);
}

const getTrivia = (btn) => {
    const numbersOfTrivia = btn.trivia.length;
    const randomNumber = (Math.random() * numbersOfTrivia) << 0;

    return btn.trivia[randomNumber] || "";
}

const resetState = () => {
    btnEl.forEach(el => {
        el.classList.remove('other-highlighted');
        el.classList.remove('active-highlight');
    });
}