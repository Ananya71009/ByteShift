// =========================================
// MOBILE NAVIGATION
// =========================================

const menuButton = document.getElementById("menuButton");
const navLinks = document.querySelector(".nav-links");

if (menuButton && navLinks) {

    menuButton.addEventListener("click", () => {

        navLinks.classList.toggle("mobile-menu");

    });

}


// =========================================
// ARTICLE SEARCH
// =========================================

const searchInput =
    document.getElementById("articleSearch");

const searchButton =
    document.getElementById("searchButton");

const articleCards =
    document.querySelectorAll(".article-card");


function searchArticles() {

    if (!searchInput) {
        return;
    }

    const searchTerm =
        searchInput.value.toLowerCase().trim();


    articleCards.forEach(card => {

        const articleText =
            card.innerText.toLowerCase();


        if (articleText.includes(searchTerm)) {

            card.style.display = "";

        } else {

            card.style.display = "none";

        }

    });

}


// SEARCH BUTTON

if (searchButton) {

    searchButton.addEventListener(
        "click",
        searchArticles
    );

}


// ENTER KEY

if (searchInput) {

    searchInput.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Enter") {

                searchArticles();

            }

        }
    );

}s