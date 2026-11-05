// mobile toggle
 
document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.getElementById("menuBtn");
  const mobileMenu = document.getElementById("mobileMenu");

  if (!menuBtn || !mobileMenu) {
    console.warn("Menu elements not found on this page.");
    return;
  }

  menuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("scale-y-100");
    mobileMenu.classList.toggle("opacity-100");
    mobileMenu.classList.toggle("pointer-events-auto");
  });

  document.querySelectorAll("#mobileMenu a").forEach(link => {
    link.addEventListener("click", () => {
      mobileMenu.classList.remove(
        "scale-y-100",
        "opacity-100",
        "pointer-events-auto"
      );
    });
  });
});





// counting of trusted users



    function rollDigit(el, target, speed, forceRoll) {
      let container = document.createElement("div");
      el.appendChild(container);

      // Create rolling numbers
      if (forceRoll) {
        // Roll 0 → 9 → final
        for (let i = 0; i <= 9; i++) {
          let d = document.createElement("span");
          d.textContent = i;
          container.appendChild(d);
        }
        let final = document.createElement("span");
        final.textContent = target;
        container.appendChild(final);
      } else {
        // Normal count
        for (let i = 0; i <= target; i++) {
          let d = document.createElement("span");
          d.textContent = i;
          container.appendChild(d);
        }
      }

      // Height of each number = 28px
      let numberHeight = 28;
      let stopIndex = forceRoll ? 10 : target;

      setTimeout(() => {
        container.style.transform = `translateY(-${stopIndex * numberHeight}px)`;
        container.style.transitionDuration = speed + "ms";
      }, 50);
    }

    window.onload = () => {
      const digits = document.querySelectorAll(".digit");

      rollDigit(digits[0], 7, 900, false);      // first digit (normal speed)
      rollDigit(digits[1], 2, 2000, false);     // second digit (slow)
      rollDigit(digits[2], 0, 900, true);       // 3rd digit rolls 0–9–0
      rollDigit(digits[3], 0, 900, true);       // 4th digit same timing
    };
 


// hero section text animation
const wordDelay = 400;
const afterWordsPause = 300;
const slideDuration = 600;
const pauseBetweenSlides = 1200;
const slideHeight = 70;

// 📱 mobile detection
const isMobile = window.matchMedia('(max-width: 768px)').matches;

// weights
const HEADING_WEIGHT = '500';                 // All Your Needs (always)
const CONTENT_WEIGHT = isMobile ? '600' : '500'; // Only solution lines

const line1 = document.getElementById('line1');
const scrollContent = document.getElementById('scrollContent');

/* ---------- Animate 'All Your Needs' (NO mobile change) ---------- */
const line1Words = ["All", "Your", "Needs"];
line1Words.forEach((w, i) => {
  const span = document.createElement('span');
  span.className = 'word';
  span.textContent = w;
  span.style.fontFamily = "'Poppins', sans-serif";
  span.style.fontWeight = HEADING_WEIGHT; // ✅ stays same
  line1.appendChild(span);

  setTimeout(() => {
    span.style.opacity = '1';
    span.style.transform = 'translateX(0)';
  }, i * wordDelay);
});

const allYourNeedsTotal = line1Words.length * wordDelay + afterWordsPause;

/* ---------- Animate words left -> right ---------- */
function animateWordsLeftToRight(text, onComplete) {
  const container = document.createElement('div');
  container.style.display = 'flex';
  container.style.alignItems = 'center';
  container.style.gap = '8px';
  container.style.fontFamily = "'Poppins', sans-serif";
  container.style.fontWeight = CONTENT_WEIGHT; // ✅ mobile 600
  scrollContent.appendChild(container);

  const words = text.split(' ');
  words.forEach((w, i) => {
    const span = document.createElement('span');
    span.className = 'word';
    span.textContent = w;
    span.style.fontFamily = "'Poppins', sans-serif";
    span.style.fontWeight = CONTENT_WEIGHT; // ✅
    container.appendChild(span);

    setTimeout(() => {
      span.style.opacity = '1';
      span.style.transform = 'translateX(0)';
    }, i * wordDelay);
  });

  const total = words.length * wordDelay + afterWordsPause;
  setTimeout(() => onComplete(container), total);
}

/* ---------- Animate letters inside words ---------- */
function animateLettersByWord(text, onComplete) {
  const container = document.createElement('div');
  container.style.display = 'flex';
  container.style.gap = '12px';
  container.style.fontFamily = "'Poppins', sans-serif";
  container.style.fontWeight = CONTENT_WEIGHT; // ✅
  scrollContent.appendChild(container);

  const words = text.split(' ');
  let totalDelay = 0;

  words.forEach((word) => {
    const wordSpan = document.createElement('span');
    wordSpan.style.display = 'flex';
    wordSpan.style.gap = '0px';
    wordSpan.style.fontFamily = "'Poppins', sans-serif";
    wordSpan.style.fontWeight = CONTENT_WEIGHT; // ✅
    container.appendChild(wordSpan);

    [...word].forEach((letter, i) => {
      const letterSpan = document.createElement('span');
      letterSpan.className = 'letter';
      letterSpan.textContent = letter;
      letterSpan.style.fontFamily = "'Poppins', sans-serif";
      letterSpan.style.fontWeight = CONTENT_WEIGHT; // ✅
      letterSpan.style.opacity = '0';
      letterSpan.style.transform = 'translateX(-20px)';
      letterSpan.style.display = 'inline-block';
      letterSpan.style.transition = 'all 0.4s ease';
      wordSpan.appendChild(letterSpan);

      setTimeout(() => {
        letterSpan.style.opacity = '1';
        letterSpan.style.transform = 'translateX(0)';
      }, totalDelay + i * 80);
    });

    totalDelay += word.length * 80 + 100;
  });

  setTimeout(() => onComplete(container), totalDelay + 300);
}

/* ---------- Sequence ---------- */
setTimeout(() => {

  // 1️⃣ One Strong Solution (mobile 600)
  animateLettersByWord("One Strong Solution", () => {

    // 2️⃣ One Smart Solution (mobile 600)
    const smartDiv = document.createElement('div');
    smartDiv.textContent = "One Smart Solution";
    smartDiv.style.fontFamily = "'Poppins', sans-serif";
    smartDiv.style.fontWeight = CONTENT_WEIGHT; // ✅
    scrollContent.appendChild(smartDiv);

    // 3️⃣ One Small Solution (mobile 600)
    animateWordsLeftToRight("One Small Solution", () => {

      let currentIndex = 0;
      const totalLines = scrollContent.children.length;

      function scrollNext() {
        if (currentIndex < totalLines - 1) {
          currentIndex++;
          scrollContent.style.transition = `transform ${slideDuration}ms ease`;
          scrollContent.style.transform = `translateY(-${slideHeight * currentIndex}px)`;
          setTimeout(scrollNext, slideDuration + pauseBetweenSlides);
        }
      }

      // setTimeout(scrollNext, pauseBetweenSlides);
      animateWordsLeftToRight("One Small Solution", () => {
          startScrolling();
      });
    });

  });

}, allYourNeedsTotal);



function startScrolling() {
    const totalLines = scrollContent.children.length;
    let currentIndex = 0;

    if (totalLines < 2) return;

    // Keep every phrase at the same height and alignment
    Array.from(scrollContent.children).forEach(line => {
        line.style.height = `${slideHeight}px`;
        line.style.minHeight = `${slideHeight}px`;
        line.style.flexShrink = '0';
        line.style.display = 'flex';
        line.style.alignItems = 'center';
        line.style.whiteSpace = 'nowrap';
        line.style.boxSizing = 'border-box';
    });

    scrollContent.style.display = 'flex';
    scrollContent.style.flexDirection = 'column';
    scrollContent.style.transform = 'translateY(0)';
    scrollContent.style.transition = 'none';

    function scrollNext() {
        currentIndex++;

        // Restart from the first phrase after the third
        if (currentIndex >= totalLines) {
            currentIndex = 0;
        }

        scrollContent.style.transition =
            `transform ${slideDuration}ms ease`;

        scrollContent.style.transform =
            `translateY(-${slideHeight * currentIndex}px)`;

        // Scroll to the next phrase after 1 second
        setTimeout(scrollNext, 1000);
    }

    // Show the first phrase in its original position
    setTimeout(scrollNext, 1000);
}



// phone animation of index page hero section



//     gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

// window.addEventListener("load", () => {

//   const phone = document.querySelector("#heroPhone");
//   const circleCenter = document.querySelector("#circleCenter");
//   const circleSection = document.querySelector("#circleSection");
//   const heroSection = document.querySelector("#heroSection");

//   // Clone phone
//   const clone = phone.cloneNode(true);
//   document.body.appendChild(clone);

//   const phoneRect = phone.getBoundingClientRect();
//   const circleRect = circleCenter.getBoundingClientRect();

//   const fixedX = phoneRect.left;
//   const startY = phoneRect.top + window.scrollY;

//   const targetY =
//     circleRect.top +
//     circleRect.height / 2 -
//     phoneRect.height / 2 +
//     window.scrollY;

//   gsap.set(clone, {
//     position: "absolute",
//     left: fixedX,
//     top: startY,
//     width: phoneRect.width,
//     height: phoneRect.height,
//     zIndex: 9999,
//     pointerEvents: "none",
//     visibility: "hidden"
//   });

// let heroLocked = false;

//   // 🔥 SINGLE SCROLL DOWN → SNAP TO CIRCLE
//   ScrollTrigger.create({
//     trigger: heroSection,
//     start: "top top",
//     end: "bottom top",
//     onLeave: () => {
//       if (heroLocked) return;
// heroLocked = true;

//       phone.style.opacity = "0";
//       clone.style.visibility = "visible";

//       // Force scroll
//       gsap.to(window, {
//         scrollTo: circleSection,
//         duration: 0.9,
//         ease: "power3.inOut"
//       });

//       // Move phone
//       gsap.to(clone, {
//         top: targetY,
//         duration: 0.9,
//         ease: "power3.out",
//         onComplete: () => heroLocked = false

//       });
//     },

//     // 🔥 SINGLE SCROLL UP → SNAP BACK TO HERO
//     onEnterBack: () => {
//       if (heroLocked) return;
//       heroLocked = true;

//       gsap.to(window, {
//         scrollTo: heroSection,
//         duration: 0.9,
//         ease: "power3.inOut"
//       });

//       gsap.to(clone, {
//         top: startY,
//         duration: 0.9,
//         ease: "power3.out",
//         onComplete: () => {
//           clone.style.visibility = "hidden";
//           phone.style.opacity = "1";
//           heroLocked = false;
//         }
//       });
//     }
//   });

// });

//  




gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

window.addEventListener("load", () => {

    const phone = document.querySelector("#heroPhone");
    const circleCenter = document.querySelector("#circleCenter");
    const circleSection = document.querySelector("#circleSection");
    const heroSection = document.querySelector("#heroSection");
    const targetCircle = document.querySelector("#targetCircle");

    if (
        !phone ||
        !circleCenter ||
        !circleSection ||
        !heroSection ||
        !targetCircle
    ) return;

    // Remove previous clones
    document.querySelectorAll(".hero-phone-clone").forEach(el => el.remove());

    // Create phone clone
    const clone = phone.cloneNode(true);

    clone.removeAttribute("id");
    clone.classList.add("hero-phone-clone");
    clone.setAttribute("aria-hidden", "true");

    clone.querySelectorAll("[id]").forEach(el => {
        el.removeAttribute("id");
    });

    Object.assign(clone.style, {
        position: "absolute",
        display: "block",
        margin: "0",
        padding: "0",
        pointerEvents: "none",
        visibility: "hidden",
        opacity: "1",
        transform: "none",
        transition: "none",
        boxSizing: "border-box"
    });

    // IMPORTANT:
    // Put clone inside circleSection, not document.body.
    // It will stay behind targetCircle and its contents.
    // circleSection.insertBefore(clone, circleSection.firstChild);
    circleSection.appendChild(clone);

    clone.style.setProperty("z-index", "9999", "important");

    let animating = false;
    let isInRing = false;

    let startPosition = null;

    // Get positions relative to circleSection
    function getPositions() {

        const phoneRect = phone.getBoundingClientRect();
        const ringRect = circleCenter.getBoundingClientRect();
        const sectionRect = circleSection.getBoundingClientRect();

        return {

            left: phoneRect.left - sectionRect.left,
            startY: phoneRect.top - sectionRect.top,

            width: phoneRect.width,
            height: phoneRect.height,

            targetY:
                ringRect.top -
                sectionRect.top +
                ringRect.height / 2 -
                phoneRect.height / 2

        };
    }

    // Set original phone dimensions and position
    function setClonePosition(position) {

        gsap.set(clone, {

            left: position.left,
            top: position.startY,

            width: position.width,
            height: position.height,

            minWidth: position.width,
            maxWidth: position.width,

            minHeight: position.height,
            maxHeight: position.height,

            scale: 1,
            x: 0,
            y: 0,

            visibility: "visible",
            zIndex: 1

        });

        clone.style.setProperty("z-index", "1", "important");
    }

    startPosition = getPositions();

    gsap.set(clone, {
        left: startPosition.left,
        top: startPosition.startY,
        width: startPosition.width,
        height: startPosition.height,
        visibility: "hidden"
    });

    // =====================================
    // PHONE MOVES DOWN INTO THE RING
    // =====================================

    function animatePhoneDown() {

        if (animating || isInRing) return;

        animating = true;

        startPosition = getPositions();

        setClonePosition(startPosition);

        // Hide original phone
        gsap.set(phone, {
            opacity: 0
        });

        // Scroll to circular section
        gsap.to(window, {

            scrollTo: {
                y: circleSection,
                autoKill: false
            },

            duration: 0.9,
            ease: "power3.inOut",
            overwrite: "auto"

        });

        // Move clone into center of ring
        gsap.to(clone, {

            top: startPosition.targetY,

            duration: 0.9,
            ease: "power3.inOut",
            overwrite: "auto",

            onComplete: () => {

                animating = false;
                isInRing = true;

            }

        });

    }

    // =====================================
    // PHONE RETURNS UP TO ORIGINAL POSITION
    // =====================================

    function animatePhoneUp() {

        if (animating || !isInRing) return;

        animating = true;

        // Keep phone behind ring contents
        clone.style.setProperty("z-index", "1", "important");

        gsap.set(clone, {
            visibility: "visible"
        });

        // Scroll back to hero
        gsap.to(window, {

            scrollTo: {
                y: heroSection,
                autoKill: false
            },

            duration: 0.9,
            ease: "power3.inOut",
            overwrite: "auto"

        });

        // Move phone back to original position
        gsap.to(clone, {

            top: startPosition.startY,

            duration: 0.9,
            ease: "power3.inOut",
            overwrite: "auto",

            onComplete: () => {

                gsap.set(clone, {
                    visibility: "hidden"
                });

                // Show original phone again
                gsap.set(phone, {
                    opacity: 1
                });

                animating = false;
                isInRing = false;

            }

        });

    }

    // =====================================
    // SCROLL TRIGGER
    // =====================================

    ScrollTrigger.create({

        trigger: heroSection,

        start: "top top",
        end: "bottom top",

        onLeave: animatePhoneDown,

        onEnterBack: animatePhoneUp

    });

    // =====================================
    // RESIZE
    // =====================================

    window.addEventListener("resize", () => {

        if (!animating && !isInRing) {

            startPosition = getPositions();

            gsap.set(clone, {

                left: startPosition.left,
                top: startPosition.startY,

                width: startPosition.width,
                height: startPosition.height

            });

        }

        ScrollTrigger.refresh();

    });

});


// Smart Features for a Smooth Experience section phone animation


    gsap.utils.toArray(".phone-anim").forEach((phone, index) => {

      const card = phone.closest(".relative");

      const moveDistance =
        card.offsetHeight +
        phone.offsetHeight +
        400; // buffer

      gsap.timeline({
        repeat: -1,
        delay: index * 0.3
      })

        // Pause at center
        .to(phone, { duration: 2 })

        // Move completely UP (fully hidden)
        .to(phone, {
          y: -moveDistance,
          duration: 1.2,
          ease: "power1.inOut"
        })

        // Jump to bottom (fully hidden)
        .set(phone, {
          y: moveDistance
        })

        // Move back to center
        .to(phone, {
          y: 0,
          duration: 1.2,
          ease: "power1.inOut"
        })

        // Pause again
        .to(phone, { duration: 2 });

    });
  



function setQR(type) {
  const qrImage = document.getElementById("qrImage");

  if (type === "apple") {
    qrImage.src = "/static/images/apple_qr.png";
  } else {
    qrImage.src = "/static/images/playstore_qr.png";
  }
}


/* ==========================================
   SINGLE HAMBURGER MENU CONTROLLER
   Mobile + Tablet
========================================== */

// (function () {

//     function initializeHamburger() {

//         const menuBtn = document.getElementById("menuBtn");
//         const mobileMenu = document.getElementById("mobileMenu");

//         if (!menuBtn || !mobileMenu) {
//             return;
//         }

//         // Prevent duplicate event listeners
//         if (menuBtn.dataset.menuInitialized === "true") {
//             return;
//         }

//         menuBtn.dataset.menuInitialized = "true";

//         const breakpoint = 1024;

//         menuBtn.setAttribute("type", "button");
//         menuBtn.setAttribute("aria-controls", "mobileMenu");
//         menuBtn.setAttribute("aria-expanded", "false");

//         mobileMenu.setAttribute("aria-hidden", "true");

//         function isMobileOrTablet() {
//             return window.innerWidth < breakpoint;
//         }

//         function openMenu() {

//             if (!isMobileOrTablet()) return;

//             mobileMenu.classList.add("menu-open");
//             menuBtn.classList.add("active");

//             menuBtn.setAttribute("aria-expanded", "true");
//             mobileMenu.setAttribute("aria-hidden", "false");
//         }

//         function closeMenu() {

//             mobileMenu.classList.remove("menu-open");
//             menuBtn.classList.remove("active");

//             menuBtn.setAttribute("aria-expanded", "false");
//             mobileMenu.setAttribute("aria-hidden", "true");
//         }

//         // Hamburger click
//         menuBtn.addEventListener("click", function (event) {

//             event.preventDefault();
//             event.stopPropagation();

//             if (!isMobileOrTablet()) return;

//             const isOpen = mobileMenu.classList.contains("menu-open");

//             if (isOpen) {
//                 closeMenu();
//             } else {
//                 openMenu();
//             }
//         });

//         // Close after selecting a navigation link
//         mobileMenu.querySelectorAll("a").forEach(function (link) {

//             link.addEventListener("click", function () {
//                 closeMenu();
//             });

//         });

//         // Close when clicking outside
//         document.addEventListener("click", function (event) {

//             if (!mobileMenu.classList.contains("menu-open")) {
//                 return;
//             }

//             if (
//                 !mobileMenu.contains(event.target) &&
//                 !menuBtn.contains(event.target)
//             ) {
//                 closeMenu();
//             }

//         });

//         // Close with Escape key
//         document.addEventListener("keydown", function (event) {

//             if (event.key === "Escape") {
//                 closeMenu();
//             }

//         });

//         // Handle screen resize
//         window.addEventListener("resize", function () {

//             if (!isMobileOrTablet()) {
//                 closeMenu();
//             }

//         });

//         // Initial state
//         closeMenu();

//     }

//     if (document.readyState === "loading") {

//         document.addEventListener(
//             "DOMContentLoaded",
//             initializeHamburger,
//             { once: true }
//         );

//     } else {

//         initializeHamburger();

//     }

// })();


(function () {
    const BREAKPOINT = 1024;
    const MENU_GAP = 10;
    const SCREEN_PADDING = 12;

    let isMenuOpen = false;

    function getElements() {
        return {
            btn: document.getElementById("menuBtn"),
            menu: document.getElementById("mobileMenu")
        };
    }

    function positionMenu() {
        const { btn, menu } = getElements();

        if (!btn || !menu || !isMenuOpen) return;

        const btnRect = btn.getBoundingClientRect();

        const menuWidth = menu.offsetWidth || 335;

        // Align the menu's right edge with the button's right edge.
        let left = btnRect.right - menuWidth;

        // Keep the complete menu inside the viewport.
        left = Math.max(
            SCREEN_PADDING,
            Math.min(
                left,
                window.innerWidth - menuWidth - SCREEN_PADDING
            )
        );

        menu.style.setProperty("position", "fixed", "important");
        menu.style.setProperty("top", (btnRect.bottom + MENU_GAP) + "px", "important");
        menu.style.setProperty("left", left + "px", "important");
        menu.style.setProperty("right", "auto", "important");
        menu.style.setProperty("bottom", "auto", "important");

        // Remove Tailwind's horizontal centering.
        menu.style.setProperty("translate", "none", "important");

        menu.style.setProperty(
            "transform",
            "translateY(0) scaleY(1)",
            "important"
        );
    }

    function setMenuState(open) {
        const { btn, menu } = getElements();

        if (!btn || !menu) return;

        isMenuOpen = open && window.innerWidth < BREAKPOINT;

        if (isMenuOpen) {
            // Move outside transformed parent containers.
            if (menu.parentElement !== document.body) {
                document.body.appendChild(menu);
            }

            menu.style.setProperty("display", "block", "important");
            menu.style.setProperty("visibility", "visible", "important");
            menu.style.setProperty("opacity", "1", "important");
            menu.style.setProperty("pointer-events", "auto", "important");
            menu.style.setProperty("z-index", "999999", "important");

            positionMenu();

        } else {
            menu.style.setProperty("visibility", "hidden", "important");
            menu.style.setProperty("opacity", "0", "important");
            menu.style.setProperty("pointer-events", "none", "important");

            menu.style.setProperty(
                "transform",
                "translateY(-8px) scaleY(0)",
                "important"
            );

            if (window.innerWidth >= BREAKPOINT) {
                menu.style.setProperty("display", "none", "important");
            }
        }

        btn.classList.toggle("active", isMenuOpen);
        menu.classList.toggle("menu-open", isMenuOpen);

        btn.setAttribute("type", "button");
        btn.setAttribute("aria-expanded", String(isMenuOpen));
        menu.setAttribute("aria-hidden", String(!isMenuOpen));
    }

    function initializeMenu() {
        isMenuOpen = false;
        setMenuState(false);
    }

    // Capture clicks before other event handlers.
    document.addEventListener("click", function (event) {

        const clickedButton = event.composedPath().some(function (element) {
            return element && element.id === "menuBtn";
        });

        const clickedMenuLink = event.composedPath().some(function (element) {
            return element &&
                element.tagName === "A" &&
                element.closest &&
                element.closest("#mobileMenu");
        });

        if (clickedButton) {
            event.preventDefault();
            event.stopImmediatePropagation();

            setMenuState(!isMenuOpen);

            return;
        }

        if (clickedMenuLink) {
            setMenuState(false);
            return;
        }

        if (isMenuOpen) {
            setMenuState(false);
        }

    }, true);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            setMenuState(false);
        }
    });

    // Keep menu aligned while scrolling or resizing.
    window.addEventListener("resize", function () {
        if (window.innerWidth >= BREAKPOINT) {
            setMenuState(false);
        } else {
            positionMenu();
        }
    });

    window.addEventListener("scroll", function () {
        positionMenu();
    }, true);

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializeMenu);
    } else {
        initializeMenu();
    }

    window.addEventListener("pageshow", initializeMenu);

})();


/* ==========================================
   FIXED MOBILE + TABLET HAMBURGER MENU
   HTML DOES NOT NEED TO CHANGE
========================================== */

// (function () {
//     function initHamburgerMenu() {
//         const menuBtn = document.getElementById("menuBtn");
//         const mobileMenu = document.getElementById("mobileMenu");

//         if (!menuBtn || !mobileMenu) {
//             console.error(
//                 "Hamburger menu: #menuBtn or #mobileMenu was not found."
//             );
//             return;
//         }

//         // Avoid registering this script more than once.
//         if (menuBtn.dataset.hamburgerReady === "true") return;
//         menuBtn.dataset.hamburgerReady = "true";

//         const tabletBreakpoint = 1024;

//         menuBtn.setAttribute("type", "button");
//         menuBtn.setAttribute("aria-controls", "mobileMenu");
//         menuBtn.setAttribute("aria-expanded", "false");

//         // Remember the original display value.
//         const originalDisplay = mobileMenu.style.display;

//         function isMobileOrTablet() {
//             return window.innerWidth < tabletBreakpoint;
//         }

//         function setMenuState(open) {
//             const canShowMenu = isMobileOrTablet();
//             const shouldOpen = open && canShowMenu;

//             mobileMenu.classList.toggle("menu-open", shouldOpen);

//             mobileMenu.classList.toggle("scale-y-0", !shouldOpen);
//             mobileMenu.classList.toggle("scale-y-100", shouldOpen);

//             mobileMenu.classList.toggle("opacity-0", !shouldOpen);
//             mobileMenu.classList.toggle("opacity-100", shouldOpen);

//             mobileMenu.classList.toggle(
//                 "pointer-events-none",
//                 !shouldOpen
//             );
//             mobileMenu.classList.toggle(
//                 "pointer-events-auto",
//                 shouldOpen
//             );

//             // Override the existing md:hidden class on tablets.
//             if (canShowMenu) {
//                 mobileMenu.style.setProperty("display", "block", "important");
//             } else {
//                 mobileMenu.style.removeProperty("display");
//             }

//             mobileMenu.setAttribute("aria-hidden", String(!shouldOpen));
//             menuBtn.setAttribute("aria-expanded", String(shouldOpen));
//         }

//         // Start with the menu closed.
//         setMenuState(false);

//         // Open or close on hamburger click.
//         menuBtn.addEventListener("click", function (event) {
//             event.preventDefault();
//             event.stopPropagation();

//             const currentlyOpen =
//                 mobileMenu.classList.contains("menu-open");

//             setMenuState(!currentlyOpen);
//         });

//         // Close when a navigation link is selected.
//         mobileMenu.querySelectorAll("a").forEach(function (link) {
//             link.addEventListener("click", function () {
//                 setMenuState(false);
//             });
//         });

//         // Close when clicking outside the menu.
//         document.addEventListener("click", function (event) {
//             if (
//                 mobileMenu.classList.contains("menu-open") &&
//                 !mobileMenu.contains(event.target) &&
//                 !menuBtn.contains(event.target)
//             ) {
//                 setMenuState(false);
//             }
//         });

//         // Close when Escape is pressed.
//         document.addEventListener("keydown", function (event) {
//             if (event.key === "Escape") {
//                 setMenuState(false);
//             }
//         });

//         // Recalculate on orientation change or resize.
//         window.addEventListener("resize", function () {
//             if (!isMobileOrTablet()) {
//                 setMenuState(false);
//             } else if (mobileMenu.classList.contains("menu-open")) {
//                 setMenuState(true);
//             } else {
//                 mobileMenu.style.setProperty("display", "block", "important");
//                 setMenuState(false);
//             }
//         });

//         console.log("Mobile/tablet hamburger menu initialized.");
//     }

//     if (document.readyState === "loading") {
//         document.addEventListener(
//             "DOMContentLoaded",
//             initHamburgerMenu,
//             { once: true }
//         );
//     } else {
//         initHamburgerMenu();
//     }
// })();



document.addEventListener("DOMContentLoaded", function () {

    const menuBtn = document.getElementById("menuBtn");
    const mobileMenu = document.getElementById("mobileMenu");

    if (!menuBtn || !mobileMenu) return;

    function openMenu() {
        mobileMenu.classList.add("menu-open");

        menuBtn.classList.add("active");
        menuBtn.setAttribute("aria-expanded", "true");

        mobileMenu.setAttribute("aria-hidden", "false");
    }

    function closeMenu() {
        mobileMenu.classList.remove("menu-open");

        menuBtn.classList.remove("active");
        menuBtn.setAttribute("aria-expanded", "false");

        mobileMenu.setAttribute("aria-hidden", "true");
    }

    menuBtn.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();

        if (mobileMenu.classList.contains("menu-open")) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    document.addEventListener("click", function (event) {

        if (
            !menuBtn.contains(event.target) &&
            !mobileMenu.contains(event.target)
        ) {
            closeMenu();
        }

    });

    mobileMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", closeMenu);
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth >= 1024) {
            closeMenu();
        }
    });

});
