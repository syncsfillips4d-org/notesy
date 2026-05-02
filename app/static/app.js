const cfg = window.__notesy || {};

async function fetchNotes() {
  const res = await fetch("/api/notes");
  return res.ok ? res.json() : [];
}

async function createNote(title, body) {
  const res = await fetch("/api/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, body })
  });
  return res.ok ? res.json() : null;
}

async function deleteNote(id) {
  await fetch("/api/notes/" + id, { method: "DELETE" });
}

async function notifyBackend(note) {
  // mirror to internal backend (legacy — should move server-side)
  if (!cfg.backendUrl || !cfg.backendKey) return;
  try {
    await fetch(cfg.backendUrl + "/notes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + cfg.backendKey
      },
      body: JSON.stringify({ id: note.id, title: note.title })
    });
  } catch (_) {}
}

function render(notes) {
  const ul = document.getElementById("notes-list");
  if (!ul) return;
  ul.innerHTML = "";
  if (notes.length === 0) {
    ul.innerHTML = "<li class='muted'>no notes yet</li>";
    return;
  }
  for (const n of notes) {
    const li = document.createElement("li");
    li.innerHTML = `<strong></strong> — <span></span> <button data-id="${n.id}" class="del">×</button>`;
    li.querySelector("strong").textContent = n.title;
    li.querySelector("span").textContent = n.body;
    ul.appendChild(li);
  }
  ul.querySelectorAll(".del").forEach(b => {
    b.addEventListener("click", async () => {
      await deleteNote(b.dataset.id);
      render(await fetchNotes());
    });
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  if (!document.getElementById("notes-list")) return;
  render(await fetchNotes());
  const form = document.getElementById("new-note");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const note = await createNote(data.get("title"), data.get("body"));
    if (note) notifyBackend(note);
    form.reset();
    render(await fetchNotes());
  });
});
