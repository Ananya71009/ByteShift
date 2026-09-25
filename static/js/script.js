const menuButton = document.getElementById("menuButton");
const navLinks = document.querySelector(".nav-links");

menuButton.addEventListener("click", () => {
navLinks.classList.toggle("mobile-menu");
});
