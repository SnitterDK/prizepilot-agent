const queue = document.querySelector("#queue");
const run = document.querySelector("#run");

const labels = {
  ready: "Ready for review",
  needs_owner: "Evidence needed",
  blocked: "Blocked safely",
  approved: "Approved",
};

run.addEventListener("click", async () => {
  run.disabled = true;
  run.textContent = "Evaluating…";
  try {
    const response = await fetch("/api/queue", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        country: "Denmark",
        is_adult: true,
        works_solo: true,
        internet_access: true,
        verified_student: false,
      }),
    });
    const data = await response.json();
    queue.innerHTML = data.items
      .map(
        (item) => `
          <article class="item ${item.state}">
            <div>
              <p class="state">${labels[item.state]}</p>
              <h3>${item.opportunity}</h3>
              <p>${item.rationale}</p>
            </div>
            <div class="action">
              <span>${item.destination}</span>
              <strong>${item.action}</strong>
            </div>
          </article>`,
      )
      .join("");
  } catch (error) {
    queue.innerHTML = `<p class="error">Could not run the queue: ${error.message}</p>`;
  } finally {
    run.disabled = false;
    run.textContent = "Run again";
  }
});

