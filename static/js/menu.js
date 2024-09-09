document.addEventListener("DOMContentLoaded", function() {
    const nav = document.querySelector(".nav");
    const navBorder = document.querySelector(".nav__border");
    const searchLink = document.querySelector(".nav__link--search");
    const searchSidebar = document.getElementById("searchSidebar");
    const closeSidebar = document.getElementById("closeSidebar");
    const searchResults = document.getElementById('searchResults')
    const searchInput = document.getElementById('searchInput')
    const searchForm = document.getElementById("searchForm");
    const messagesSidebar = document.getElementById("messagesSidebar");
    const messagesUser = document.getElementById("messages-user");
    const closeMessages = document.getElementById("closeMessages");
    const messagesLink  =document.querySelector(".nav__link--messages");
    const pageContainer = document.getElementById("cont")


    function collapseNav() {
        if (!nav.classList.contains("nav--collapsed")) {
            nav.classList.add("nav--collapsed");
        }
    }

    function expandNav() {
        if (nav.classList.contains("nav--collapsed")) {
            nav.classList.remove("nav--collapsed");
        }
    }

    function areAllSidebarsClosed() {
        return !searchSidebar.classList.contains("search-sidebar--open") && 
               !messagesSidebar.classList.contains("messages-sidebar--open");
    }

    function closeAllSidebars() {
        searchSidebar.classList.remove("search-sidebar--open");
        messagesSidebar.classList.remove("messages-sidebar--open");
        updateNavState();
    }

    // Function to handle the navbar state based on sidebars
    function updateNavState() {
        if (areAllSidebarsClosed()) {
            expandNav(); // Expand the navbar if all sidebars are closed
        } else {
            collapseNav(); // Collapse the navbar if any sidebar is open
        }
    }

    // Event listener for search link

if (shouldOpenMessagesSidebar) {
messagesSidebar.classList.add("messages-sidebar--open");
pageContainer.classList.add("shift-right");
collapseNav(); // Ensure navbar is collapsed when the sidebar is open
}

if (searchLink) {
searchLink.addEventListener("click", (e) => {
    e.preventDefault();
    collapseNav(); // Ensure navbar is collapsed
    searchSidebar.classList.add("search-sidebar--open"); // Open the search sidebar
    messagesSidebar.classList.remove("messages-sidebar--open"); // Close the messages sidebar if open
    pageContainer.classList.add("shift-right");
});
}

// Event listener for messages link
if (messagesLink) {
messagesLink.addEventListener("click", (e) => {
    e.preventDefault();
    collapseNav(); // Ensure navbar is collapsed
    messagesSidebar.classList.add("messages-sidebar--open"); // Open the messages sidebar
    searchSidebar.classList.remove("search-sidebar--open"); // Close the search sidebar if open
    pageContainer.classList.add("shift-right");
});
}

// Event listener for close messages button
if (closeMessages) {
closeMessages.addEventListener("click", () => {
    messagesSidebar.classList.remove("messages-sidebar--open"); // Close the messages sidebar
    pageContainer.classList.remove("shift-right");
    updateNavState(); // Update the navbar state
});
}

// Event listener for close search button
if (closeSidebar) {
closeSidebar.addEventListener("click", () => {
    searchSidebar.classList.remove("search-sidebar--open"); // Close the search sidebar
    pageContainer.classList.remove("shift-right");
    updateNavState(); // Update the navbar state
});
}

// Event listener for navbar border click
if (navBorder) {
navBorder.addEventListener("click", () => {
    if (nav.classList.contains("nav--collapsed")) {
        expandNav(); // Expand the navbar
    } else {
        collapseNav(); // Collapse the navbar
    }
});
}

document.addEventListener("click", (e) => {
// Check if the click was outside the sidebar and the navigation bar
if (!searchSidebar.contains(e.target) &&
    !messagesSidebar.contains(e.target) &&
    !searchLink.contains(e.target) &&
    !messagesLink.contains(e.target) &&
    !nav.contains(e.target)) {
    closeAllSidebars(); // Close all sidebars and expand the navbar
}
});

// Handle AJAX search
searchForm.addEventListener("submit", function(e) {
    e.preventDefault(); // Prevent the default form submission

    // Fetch query from the input
    const query = searchInput.value.trim();

    if (query.length > 0) {
        fetch(`/search/?query=${encodeURIComponent(query)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', // Identify the request as AJAX
            },
        })
        .then(response => response.json())
        .then(data => {
            // Update the search results in the sidebar
            searchResults.innerHTML = '';

            if (data.results && data.results.length > 0) {
                data.results.forEach(result => {
                    const resultItem = document.createElement('div');
                    resultItem.className = 'search-result-item';
                    resultItem.innerHTML = `
                    <a href="/view_user/${result.id}/">
                    <div class="card" style="width: 100%">
                    <div class="card-body d-flex align-items-center">
                        <img src=${result.profile_pic} alt='profile picture'class="img-thumbnail" style="width: 2.5em; height: 2.5em; border-radius: 50%;">
                        <div class = "container">
                        <h5 class="card-title">${result.username}</h5> 
                        <p>${result.first_name} ${result.last_name}</p>
                        </div>
                    </div>
                    </div>
                    </a>`
                    searchResults.appendChild(resultItem);
                });
            } else {
                searchResults.innerHTML = '<p>No results found</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
    }
});
});