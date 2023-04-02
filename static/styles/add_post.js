document.querySelector(".back-button").addEventListener("click", () => {
    history.back();
});


for (const element of document.querySelectorAll("[contenteditable]")) {
    element.addEventListener("input", event => {
        if (element.textContent !== "") return;
        // Without this, the element will contain a <br /> when emptied manually; thus,
        // it will not match the :empty rule
        element.innerHTML = "";
    });
}

const h2 = document.querySelector(".editor > h2");
const body = document.querySelector(".editor > div");
h2.addEventListener("keydown", event => {
    if (event.key !== "Enter") return;

    body.focus();

    event.preventDefault();
});


document.querySelector(".post-button").addEventListener("click", () => {
    // fetch("/api/");
});