// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Smooth scroll to internal anchors (better mobile UX) and ensure behavior attaches after DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.header');
  const getHeaderHeight = () => (header ? header.getBoundingClientRect().height : 0);
  const scrollToId = (id) => {
    const el = document.getElementById(id);
    if (!el) return;
    const top = el.getBoundingClientRect().top + window.pageYOffset - getHeaderHeight() - 8;
    window.scrollTo({ top, behavior: 'smooth' });
  };

  // Attach to all in-page anchors (mobile only) - support click and touch
  const mobileQuery = window.matchMedia('(max-width: 900px)');
  function isMobile() { return mobileQuery.matches; }

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    ['click', 'touchstart'].forEach(evt => {
      link.addEventListener(evt, (e) => {
        if (!isMobile()) return; // desktop: use default
        const targetId = link.getAttribute('href').slice(1);
        if (!targetId) return;
        e.preventDefault();
        console.debug('mobile anchor tapped:', targetId);
        scrollToId(targetId);
      });
    });
  });

  // Delegate mobile menu taps to handle anchors reliably (also support touchstart)
  const mobileMenu = document.querySelector('.mobile-menu');
  if (mobileMenu) {
    ['click', 'touchstart'].forEach(evt => {
      mobileMenu.addEventListener(evt, (e) => {
        const a = e.target.closest('a[href^="#"]');
        if (!a) return;
        if (!isMobile()) return;
        e.preventDefault();
        const id = a.getAttribute('href').slice(1);
        console.debug('mobile menu tapped:', id);
        scrollToId(id);
      });
    });
  }

  // Topics "More" behavior: on mobile, expand inline instead of navigating away
  const topicsMore = document.querySelector('.topics-more');
  if (topicsMore) {
    ['click', 'touchstart'].forEach(evt => {
      topicsMore.addEventListener(evt, (e) => {
        if (!isMobile()) return; // on desktop, follow the link to full topics page
        e.preventDefault();
        const topicsCard = topicsMore.closest('.topics');
        if (!topicsCard) return;
        const expanded = topicsCard.classList.toggle('expanded');
        const moreText = topicsMore.querySelector('.topics-more-text');
        const allList = topicsCard.querySelector('.topics__all');
        if (moreText) moreText.textContent = expanded ? 'Less' : 'More';
        if (allList) allList.style.display = expanded ? 'block' : 'none';
        console.debug('topics expanded:', expanded);
        // Scroll into view so the newly expanded items are visible
        if (expanded) scrollToId('topics-section');
      });
    });
  }
});

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;
