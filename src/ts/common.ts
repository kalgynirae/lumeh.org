const menu = document.querySelector("#site-menu") as HTMLElement;
if (menu.scrollWidth > menu.clientWidth + 20) {
  menu.classList.add("truncated");
  function hideScrollGradient() {
    menu.classList.remove("truncated");
    menu.removeEventListener("scroll", hideScrollGradient);
  }
  menu.addEventListener("scroll", hideScrollGradient);
}

class LumehIcon extends HTMLElement {
  connectedCallback() {
    var name = this.getAttribute("name");
    var template = document.querySelector(`#icon-${name}`) as HTMLTemplateElement;
    var icon = template.content.querySelector("svg")!.cloneNode(true) as SVGSVGElement;
    icon.classList.add("icon");
    if (this.hasAttribute("right")) {
      icon.classList.add("right");
      this.appendChild(icon);
    } else {
      if (this.hasAttribute("standalone")) {
        icon.classList.add("standalone");
      }
      this.insertBefore(icon, this.firstChild);
    }
  }
}
customElements.define("l-icon", LumehIcon);

document.querySelectorAll(".anchor-button").forEach((e) => {
  e.addEventListener("click", (event) => {
    var currentHash = document.location.hash;
    if (currentHash && e.getAttribute("href")!.endsWith(currentHash)) {
      history.pushState(null, "", document.location.pathname + document.location.search)
      event.preventDefault();
      // Note: back and forward is needed to update :target selectors,
      // see https://stackoverflow.com/a/59013961
      const oldOnpopstate = window.onpopstate;
      window.onpopstate = () => {
        window.onpopstate = oldOnpopstate;
        history.forward();
      };
      history.back();
    }
  });
})

// Browsers on iOS don't handle the FRACTION SLASH character correctly,
// so we have to replace those with explicitly-styled fractions.
function replaceFractions(element: HTMLElement) {
  for (let node of element.childNodes) {
    switch (node.nodeType) {
      case Node.ELEMENT_NODE:
        if (node instanceof HTMLElement && !node.classList.contains("skip-fraction-replacement")) {
          replaceFractions(node);
        }
        break;
      case Node.TEXT_NODE:
        if (node.textContent && node.textContent.includes("\u2044")) {
          let span = document.createElement("span");
          span.innerHTML = node.textContent
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll(
              /(\d+)\u2044(\d+)/g,
              "<span class=replaced-fraction>" +
                "<span class=numerator>$1</span>" +
                "<span class=slash>\u2044</span>" +
                "<span class=denominator>$2</span>" +
              "</span>"
            );
          node.replaceWith(span);
        }
        break;
    }
  }
}
if (/^(ipad|iphone|ipod|mac)/i.test(navigator.platform)) {
  replaceFractions(document.body);
}

// Prefill current URL in the "Report a problem" link
const reportProblem = document.querySelector("#report-a-problem-link") as HTMLAnchorElement;
if (reportProblem.href!.endsWith("/form")) {
  // Note: encodeURIComponent() doesn't encode some of the characters
  // that should be encoded per RFC 3986, so do those additionally.
  const encodedURL = encodeURIComponent(document.location.toString())
    .replace("!", "%21")
    .replace("'", "%27")
    .replace("(", "%28")
    .replace(")", "%29")
    .replace("*", "%2A");
  reportProblem.href += `?prefill_URL=${encodedURL}`;
}
