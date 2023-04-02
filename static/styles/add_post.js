const qs = (selector, context=document) => context.querySelector(selector);
const qsa = (selector, context=document) => context.querySelectorAll(selector);

qs(".back-button").addEventListener("click", () => {
    history.back();
});

const topic = globalThis.topic;
const replyTargetPid = globalThis.replyTargetPid;


for (const element of qsa("[contenteditable]")) {
    element.addEventListener("input", event => {
        if (element.textContent !== "") return;
        // Without this, the element will contain a <br /> when emptied manually; thus,
        // it will not match the :empty rule
        element.innerHTML = "";
    });
}

const h2 = qs(".editor > h2");
const body = qs(".editor > div");
h2.addEventListener("keydown", event => {
    if (event.key !== "Enter") return;

    body.focus();

    event.preventDefault();
});

const statusIndicator = qs(".status-indicator");

qs(".post-button").addEventListener("click", async () => {
    statusIndicator.classList.add("loading");
    
    const response = await fetch("/api/post", {
        method: "POST",
        body: JSON.stringify({
            title: h2.textContent,
            body: [...body.children]
                    .map(paragraph => paragraph.textContent)
                    .join("\n"),
            topic,
        }),
    });

    if (response.ok) {
        const json = await response.json();

        statusIndicator.classList.remove("loading");
        location.replace(`/forum/${topic}?post=${json.new_post_id}`);
    } else {
        statusIndicator.classList.remove("loading");
        statusIndicator.textContent = "An error occurred!";
    }
});