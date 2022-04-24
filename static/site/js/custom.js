setupNoSpamLinks();
setupExpoTabs();
setupGallery();

/**
 * Make text emails clickable
 */
function setupNoSpamLinks() {
  for (const span of document.querySelectorAll(".nospam")) {
    const email = span.textContent.trim().replace(" (arobase) ", "@");
    const link = document.createElement("a");
    link.textContent = email;
    link.setAttribute("href", "mailto:" + email);
    span.replaceWith(link);
  }
}

/**
 * Expo details tabs
 */
function setupExpoTabs() {
  const isLarge = window.matchMedia("(min-width: 800px)").matches;
  const container = document.querySelector(".expo-tabs");
  if (!container || !isLarge) return;
  const tabs = document.querySelectorAll(".expo-tab");
  const nav = document.createElement("ul");
  nav.className = "expo-tabs-nav";

  const onNavClick = (event) => {
    const link = event.target.closest("a");
    const id = link ? link.getAttribute("href").replace("#", "") : null;
    if (link && id) {
      event.preventDefault();
      selectExpoTab(id);
    }
  };

  const selectExpoTab = (id) => {
    const href = "#" + id;
    const links = document.querySelectorAll(".expo-tabs-nav a");
    for (const link of links) {
      link.parentElement.setAttribute(
        "aria-current",
        link.getAttribute("href") === href ? "true" : "false"
      );
    }
    for (const tab of tabs) {
      tab.hidden = tab.id !== id;
    }
  };

  // Find tab titles
  // Build nav
  nav.innerHTML = Array.from(tabs)
    .map((tab) => {
      const title = tab.querySelector("h2");
      const text = title ? title.textContent.trim() : tab.id;
      return `<li><a href="#${tab.id}">${text}</a></li>`;
    })
    .join("\n");
  nav.addEventListener("click", onNavClick);
  container.prepend(nav);

  // Select first tab
  selectExpoTab(tabs[0].id);
}

/**
 * Expo image gallery
 */
function setupGallery() {
  const galleryLinks = document.querySelector(".gallery-links");
  if (!galleryLinks) return;
  const pictureImg = document.querySelector(".gallery-display img");
  const figcaption = document.querySelector(".gallery-display figcaption");

  const showImage = (link) => {
    pictureImg.setAttribute("src", link.href);
    figcaption.textContent = link.querySelector("img").getAttribute("alt");
    const currentLink = galleryLinks.querySelector("a[aria-current=true]");
    if (currentLink) {
      currentLink.removeAttribute('aria-current');
    }
    link.setAttribute('aria-current', 'true');
  };

  galleryLinks.addEventListener("click", (event) => {
    const link = event.target.closest("a");
    if (link) {
      event.preventDefault();
      showImage(link);
    }
  });
}
