from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")

head_marker = '  <meta name="description" content="Visualizador elegante de PDFs para cifras, partituras e repertórios.">\n'
head_insert = '''  <meta name="apple-mobile-web-app-capable" content="yes">\n  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n  <meta name="apple-mobile-web-app-title" content="CifraView">\n  <link rel="manifest" href="./manifest.webmanifest">\n  <link rel="apple-touch-icon" href="./icons/icon-192.svg">\n  <link rel="icon" type="image/svg+xml" href="./icons/icon-192.svg">\n'''

css_marker = '    /* Visualizador */\n'
css_insert = '''    .install-card {\n      position: relative;\n      margin-top: 15px;\n      display: grid;\n      grid-template-columns: auto minmax(0, 1fr) auto;\n      align-items: center;\n      gap: 12px;\n      padding: 13px 42px 13px 13px;\n      border: 1px solid rgba(91, 140, 255, 0.28);\n      border-radius: 17px;\n      background: linear-gradient(135deg, rgba(91, 140, 255, 0.13), rgba(17, 23, 34, 0.94));\n      text-align: left;\n      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.04);\n      animation: cardEnter 280ms ease-out both;\n    }\n\n    .install-card-icon {\n      width: 45px;\n      height: 45px;\n      display: grid;\n      place-items: center;\n      border-radius: 13px;\n      background: rgba(91, 140, 255, 0.16);\n      overflow: hidden;\n    }\n\n    .install-card-icon img { width: 100%; height: 100%; }\n    .install-card-content { min-width: 0; }\n    .install-card-content strong, .install-card-content span { display: block; }\n    .install-card-content strong { color: #f5f7fa; font-size: 0.9rem; }\n    .install-card-content span { margin-top: 3px; color: #93a4b7; font-size: 0.75rem; line-height: 1.4; }\n\n    .install-button {\n      min-height: 38px;\n      padding: 0 15px;\n      border: 1px solid rgba(121, 162, 255, 0.48);\n      border-radius: 11px;\n      background: linear-gradient(180deg, #79a2ff, #5b8cff);\n      color: #fff;\n      font-weight: 750;\n      cursor: pointer;\n    }\n\n    .install-close {\n      position: absolute;\n      top: 8px;\n      right: 9px;\n      width: 27px;\n      height: 27px;\n      border: 0;\n      background: transparent;\n      color: #8494a8;\n      font-size: 20px;\n      cursor: pointer;\n    }\n\n    .ios-install-steps {\n      grid-column: 1 / -1;\n      margin: 0;\n      padding: 8px 10px;\n      border-radius: 10px;\n      background: rgba(255, 255, 255, 0.035);\n      color: #b8c6d8;\n      font-size: 0.75rem;\n      line-height: 1.45;\n    }\n\n    @media (max-width: 520px) {\n      .install-card { grid-template-columns: auto minmax(0, 1fr); }\n      .install-button { grid-column: 1 / -1; width: 100%; }\n    }\n\n'''

html_marker = '      <p class="privacy-note">Seu arquivo é processado localmente e permanece no aparelho.</p>\n'
html_insert = '''      <aside id="install-card" class="install-card" hidden>\n        <div class="install-card-icon"><img src="./icons/icon-192.svg" alt=""></div>\n        <div class="install-card-content">\n          <strong>Instale o CifraView</strong>\n          <span id="install-description">Abra suas cifras como um aplicativo, direto da tela inicial.</span>\n        </div>\n        <button id="install-button" class="install-button" type="button">Instalar</button>\n        <button id="install-close" class="install-close" type="button" aria-label="Fechar sugestão de instalação">×</button>\n        <p id="ios-install-steps" class="ios-install-steps" hidden>Toque em <strong>Compartilhar</strong> e depois em <strong>Adicionar à Tela de Início</strong>.</p>\n      </aside>\n\n'''

js_marker = '    const MIN_ZOOM = 0.5;\n'
js_insert = '''    const installCard = document.getElementById("install-card");\n    const installButton = document.getElementById("install-button");\n    const installClose = document.getElementById("install-close");\n    const installDescription = document.getElementById("install-description");\n    const iosInstallSteps = document.getElementById("ios-install-steps");\n    let deferredInstallPrompt = null;\n\n'''

logic_marker = '    openPdfButton.addEventListener("click", (event) => {\n'
logic_insert = '''    const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);\n    const isInstalled = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;\n\n    function canShowInstallCard() {\n      return !isInstalled && sessionStorage.getItem("cifraview-install-dismissed") !== "true";\n    }\n\n    window.addEventListener("beforeinstallprompt", (event) => {\n      event.preventDefault();\n      deferredInstallPrompt = event;\n      if (canShowInstallCard()) installCard.hidden = false;\n    });\n\n    installButton.addEventListener("click", async () => {\n      if (!deferredInstallPrompt) return;\n      await deferredInstallPrompt.prompt();\n      const choice = await deferredInstallPrompt.userChoice;\n      if (choice.outcome === "accepted") installCard.hidden = true;\n      deferredInstallPrompt = null;\n    });\n\n    installClose.addEventListener("click", () => {\n      installCard.hidden = true;\n      sessionStorage.setItem("cifraview-install-dismissed", "true");\n    });\n\n    window.addEventListener("appinstalled", () => {\n      installCard.hidden = true;\n      deferredInstallPrompt = null;\n    });\n\n    if (isIOS && canShowInstallCard()) {\n      installCard.hidden = false;\n      installButton.hidden = true;\n      iosInstallSteps.hidden = false;\n      installDescription.textContent = "Adicione o CifraView à Tela de Início.";\n    }\n\n'''

sw_marker = '  </script>\n'
sw_insert = '''    if ("serviceWorker" in navigator) {\n      window.addEventListener("load", () => {\n        navigator.serviceWorker.register("./service-worker.js").catch((error) => {\n          console.error("Falha ao registrar o service worker:", error);\n        });\n      });\n    }\n\n'''

replacements = [
    (head_marker, head_marker + head_insert),
    (css_marker, css_insert + css_marker),
    (html_marker, html_insert + html_marker),
    (js_marker, js_insert + js_marker),
    (logic_marker, logic_insert + logic_marker),
    (sw_marker, sw_insert + sw_marker),
]

for marker, replacement in replacements:
    if replacement in text:
        continue
    if marker not in text:
        raise RuntimeError(f"Marcador não encontrado: {marker!r}")
    text = text.replace(marker, replacement, 1)

path.write_text(text, encoding="utf-8")
