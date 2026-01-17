export function openRegistrationModal(eventId, eventElement) {
    const modal = document.getElementById("registrationModal");
    const rollnoField = document.getElementById("rollno");

    // Pre-fill roll number with the logged-in student's username
    rollnoField.value = sessionStorage.getItem("username");
    rollnoField.readOnly = true; // Make it read-only to avoid garbage values

    modal.dataset.eventId = eventId; // Store event ID in modal

    // Close any other open modals
    closeAllModals();

    // Position the modal below the event card
    const rect = eventElement.getBoundingClientRect();
    modal.style.position = "absolute";
    modal.style.top = `${rect.bottom + window.scrollY + 10}px`; // Adjust for spacing
    modal.style.left = `${rect.left}px`;

    modal.style.display = "block";
    modal.classList.add("popup-animation"); // Add animation class
    // Ensure modal is on top and glassy
    modal.style.zIndex = 2000;
}

export function openEventDetails(eventId, eventElement) {
    console.log("Opening details for event ID:", eventId); // Debug log
    fetch(`http://127.0.0.1:5000/events`) // Fetch all events
        .then(response => response.json())
        .then(data => {
            const { upcoming, past } = data; // Destructure the response
            const events = [...upcoming, ...past]; // Combine upcoming and past events
            const event = events.find(e => e.id === eventId); // Find the specific event

            if (event) {
                console.log("Event details:", event); // Debug log
                const modal = document.getElementById("eventDetailsModal");

                // Populate modal fields
                modal.querySelector(".modal-title").innerText = event.title;
                modal.querySelector(".modal-tagline").innerText = event.tagline || "No tagline available.";
                modal.querySelector(".modal-date").innerText = `Date: ${event.date}`;
                modal.querySelector(".modal-poster").src = event.poster_path; // Set the poster image
                modal.querySelector(".modal-poster").alt = `${event.title} Poster`; // Set alt text

                // Position the modal near the clicked button
                const rect = eventElement.getBoundingClientRect();
                modal.style.position = "absolute";
                modal.style.top = `${rect.bottom + window.scrollY + 10}px`; // Adjust for spacing
                modal.style.left = `${rect.left}px`;

                // Show the modal
                modal.style.display = "block";
                modal.classList.add("popup-animation"); // Add animation class
                modal.style.zIndex = 2000;
            } else {
                console.error("Event not found for ID:", eventId);
                alert("Event not found. Please refresh the page and try again.");
            }
        })
        .catch(error => {
            console.error("Error fetching event details:", error.message);
            alert("Failed to fetch event details. Please try again.");
        });
}

export function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "none";
    modal.classList.remove("popup-animation");
}

function closeAllModals() {
    document.querySelectorAll(".modal").forEach(modal => {
        modal.style.display = "none";
        modal.classList.remove("popup-animation");
    });
}
