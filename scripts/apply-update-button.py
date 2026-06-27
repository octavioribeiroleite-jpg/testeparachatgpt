from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

css_marker = "    /* Visualizador */\n"
css_insert = '''    .update-fab {
      position: fixed;
      right: max(14px, env(safe-area-inset-right));
      bottom: max(14px, env(safe-area-inset-bottom));
      z-index: 9999;
      width: 46px;
      height: 46px;
      display: grid;
      place-items: center;
      border: 1px solid rgba(121, 162, 255, 0.38);
      border-radius: 15px;
      background: linear-gradient(145deg, rgba(32, 48, 72, 0.96), rgba(15, 23, 35, 0.98));
      color: #cfe0ff;
      box-shadow:
        0 12px 34px rgba(0, 0, 0, 0.34),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
      cursor: pointer;
      backdrop-filter: blur(14px);
      transition: transform 140ms ease, border-color 160ms ease, background 160ms ease;
    }

    .update-fab:hover {
      border-color: rgba(121, 162, 255, 0.76);
      background: linear-gradient(145deg, rgba(44, 68, 104, 0.98), rgba(19, 30, 46, 0.98));
      transform: translateY(-2px);
    }

    .update-fab:active {
      transform: scale(0.94);
    }

    .update-fab-icon {
      display: block;
      font-size: 1.42rem;
      line-height: 1;
    }

    .update-fab.refreshing .update-fab-icon {
      animation: updateSpin 850ms linear infinite;
    }

    .update-fab:disabled {
      cursor: wait;
      opacity: 0.78;
    }

    .update-toast {
      position: fixed;
      right: max(14px, env(safe-area-inset-right));
      bottom: calc(max(14px, env(safe-area-inset-bottom)) + 56px);
      z-index: 9999;
      max-width: min(84vw, 320px);
      padding: 9px 12px;
      border: 1px solid rgba(121, 162, 255, 0.26);
      border-radius: 12px;
      background: rgba(12, 18, 27, 0.94);
      color: #d8e3f1;
      font-size: 0.75rem;
      font-weight: 650;
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.34);
      backdrop-filter: blur(16px);
      opacity: 0;
      transform: translateY(7px);
      pointer-events: none;
      transition: opacity 170ms ease, transform 170ms ease;
    }

    .update-toast.visible {
      opacity: 1;
      transform: translateY(0);
    }

    @keyframes updateSpin {
      to { transform: rotate(360deg); }
    }

    @media (max-width: 640px) {
      .update-fab {
        right: max(9px, env(safe-area-inset-right));
        bottom: max(9px, env(safe-area-inset-bottom));
        width: 43px;
        height: 43px;
        border-radius: 14px;
      }

      .update-toast {
        right: max(9px, env(safe-area-inset-right));
        bottom: calc(max(9px, env(safe-area-inset-bottom)) + 52px);
      }
    }

'''

body_marker = "<body>\n"
body_insert = '''<body>
  <button id="update-app-button" class="update-fab" type="button" aria-label="Buscar atualização" title="Buscar atualização">
    <span class="update-fab-icon" aria-hidden="true">↻</span>
  </button>
  <div id="update-toast" class="update-toast" role="status" aria-live="polite"></div>
'''

const_marker = '    const pdfViewer = document.getElementById("pdf-viewer");\n'
const_insert = '''    const updateAppButton = document.getElementById("update-app-button");
    const updateToast = document.getElementById("update-toast");
    let updateToastTimer = null;
    let isUpdatingApp = false;
'''

logic_marker = '    const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);\n'
logic_insert = '''    function showUpdateToast(message, keepVisible = false) {
      clearTimeout(updateToastTimer);
      updateToast.textContent = message;
      updateToast.classList.add("visible");

      if (!keepVisible) {
        updateToastTimer = setTimeout(() => updateToast.classList.remove("visible"), 2600);
      }
    }

    async function refreshCifraView() {
      if (isUpdatingApp) return;

      isUpdatingApp = true;
      updateAppButton.disabled = true;
      updateAppButton.classList.add("refreshing");
      showUpdateToast("Buscando a versão mais recente…", true);

      try {
        if ("serviceWorker" in navigator) {
          const registrations = await navigator.serviceWorker.getRegistrations();
          await Promise.all(registrations.map((registration) => registration.update().catch(() => null)));

          registrations.forEach((registration) => {
            if (registration.waiting) {
              registration.waiting.postMessage({ type: "SKIP_WAITING" });
            }
          });
        }

        if ("caches" in window) {
          const cacheNames = await caches.keys();
          const oldCifraViewCaches = cacheNames.filter((name) => name.startsWith("cifraview-"));
          await Promise.all(oldCifraViewCaches.map((name) => caches.delete(name)));
        }

        await fetch(window.location.href, { cache: "no-store" });
        showUpdateToast("Atualização carregada. Reiniciando…", true);
        setTimeout(() => window.location.reload(), 650);
      } catch (error) {
        console.error("Falha ao atualizar o CifraView:", error);
        showUpdateToast("Não foi possível atualizar. Verifique sua conexão.");
        isUpdatingApp = false;
        updateAppButton.disabled = false;
        updateAppButton.classList.remove("refreshing");
      }
    }

    updateAppButton.addEventListener("click", refreshCifraView);

    document.addEventListener("fullscreenchange", () => {
      const destination = document.fullscreenElement ? app : document.body;
      destination.appendChild(updateAppButton);
      destination.appendChild(updateToast);
    });

'''

replacements = [
    (css_marker, css_insert + css_marker),
    (body_marker, body_insert),
    (const_marker, const_marker + const_insert),
    (logic_marker, logic_insert + logic_marker),
]

for marker, replacement in replacements:
    if replacement in text:
        continue
    if marker not in text:
        raise RuntimeError(f"Marcador não encontrado: {marker!r}")
    text = text.replace(marker, replacement, 1)

path.write_text(text, encoding="utf-8")
