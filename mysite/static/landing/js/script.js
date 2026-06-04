const menuBtn = document.getElementById("menuBtn");
const nav = document.querySelector(".nav");

menuBtn.addEventListener("click", () => {
  nav.classList.toggle("open");
});

document.querySelectorAll(".nav a").forEach(link => {
  link.addEventListener("click", () => nav.classList.remove("open"));
});

const revealElements = document.querySelectorAll(".reveal");
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
    }
  });
}, { threshold: 0.12 });

revealElements.forEach(el => revealObserver.observe(el));

const counters = document.querySelectorAll("[data-counter]");
let countersStarted = false;

function startCounters() {
  if (countersStarted) return;
  countersStarted = true;

  counters.forEach(counter => {
    const target = Number(counter.dataset.counter);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 45));

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      counter.textContent = current + (target === 24 ? "/7" : "+");
    }, 35);
  });
}

const statsObserver = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) startCounters();
}, { threshold: 0.4 });

const stats = document.querySelector(".stats");
if (stats) statsObserver.observe(stats);

const reviews = document.querySelectorAll(".review");
const prevReview = document.getElementById("prevReview");
const nextReview = document.getElementById("nextReview");
let reviewIndex = 0;

function showReview(index) {
  reviews.forEach(review => review.classList.remove("active"));
  reviews[index].classList.add("active");
}

function next() {
  reviewIndex = (reviewIndex + 1) % reviews.length;
  showReview(reviewIndex);
}

function prev() {
  reviewIndex = (reviewIndex - 1 + reviews.length) % reviews.length;
  showReview(reviewIndex);
}

nextReview.addEventListener("click", next);
prevReview.addEventListener("click", prev);
setInterval(next, 6000);

document.querySelector(".contact-form").addEventListener("submit", (event) => {
  event.preventDefault();
  alert("Заявка отправлена! Здесь можно подключить отправку в Telegram, email или Django backend.");
});
