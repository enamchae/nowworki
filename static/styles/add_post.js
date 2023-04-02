const qs = (selector, context=document) => context.querySelector(selector);
const qsa = (selector, context=document) => context.querySelectorAll(selector);

qs(".back-button").addEventListener("click", () => {
    history.back();
});

const logoutButton = qs(".logout-button");
logoutButton?.addEventListener("click", async () => {
    const response = await fetch("/logout", {method: "POST"});

    if (response.ok) {
        location.replace("/");
    }
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

const postButton = qs(".post-button")
postButton.addEventListener("click", async () => {
    const titleText = h2.textContent;
    if (!titleText) {
        statusIndicator.textContent = "Please enter a title!";
        return;
    }

    const bodyText = [...body.children]
            .map(paragraph => paragraph.textContent)
            .join("\n")
            || body.textContent;
    if (!bodyText) {
        statusIndicator.textContent = "Please enter text in the body of your post!";
        return;
    }

    const fulltimeRadio = qs("[name='fulltime']:checked");
    if (!replyTargetPid && !fulltimeRadio) {
        statusIndicator.textContent = "Please indicate whether your post is for internship or full-time jobs!";
        return;
    }

    postButton.classList.add("disabled");


    statusIndicator.textContent = "";
    statusIndicator.classList.add("loading");
    
    const response = await fetch("/api/post", {
        method: "POST",
        body: JSON.stringify({
            title: titleText,
            body: bodyText,
            topic,
            fulltime: Boolean(Number(fulltimeRadio?.value)),
            reply_target_pid: replyTargetPid,
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
    postButton.classList.remove("disabled");
});