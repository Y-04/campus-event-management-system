import { login, logout } from './auth.js';
import { fetchEvents, fetchRegisteredEvents, fetchAdminEvents } from './events.js';
import { openRegistrationModal, openEventDetails, closeModal } from './modals.js';
import { addEvent, editEvent, deleteEvent } from './admin.js';

// Expose functions to the global scope
window.login = login;
window.logout = logout;
window.fetchEvents = fetchEvents;
window.fetchRegisteredEvents = fetchRegisteredEvents;
window.fetchAdminEvents = fetchAdminEvents;
window.openRegistrationModal = openRegistrationModal;
window.openEventDetails = openEventDetails;
window.closeModal = closeModal;
window.addEvent = addEvent;
window.editEvent = editEvent;
window.deleteEvent = deleteEvent;
window.submitRegistration = function submitRegistration() {
    const modal = document.getElementById("registrationModal");
    const eventId = modal.dataset.eventId;
    const year = document.getElementById("year").value;

    // Debug log to verify data being sent
    console.log("Submitting registration with eventId:", eventId, "year:", year);

    // Validate input fields
    if (!eventId || !year) {
        alert("Please select a valid event and year.");
        return;
    }

    // Send registration request to the backend
    fetch("http://127.0.0.1:5000/register_event", {
        method: "POST",
        body: JSON.stringify({ event_id: eventId, year }),
        headers: { "Content-Type": "application/json" },
        credentials: "include" // Include session cookies
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.message); });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message); // Show success message
        closeModal("registrationModal");
        fetchRegisteredEvents(sessionStorage.getItem("username")); // Refresh registered events
    })
    .catch(error => {
        console.error("Error registering for event:", error.message);
        alert("Failed to register for the event. Please try again.");
    });
};

window.login = function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value; // Get the selected role

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, role }),
        credentials: "include" // Include session cookies
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Invalid credentials");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        sessionStorage.setItem("username", username); // Save username in sessionStorage
        sessionStorage.setItem("role", role); // Save the role in sessionStorage
        window.location.href = data.redirect; // Redirect to the appropriate dashboard
    })
    .catch(error => {
        console.error("Login error:", error.message);
        alert("Login failed. Please check your credentials.");
    });
};

document.addEventListener("DOMContentLoaded", function () {
    const role = sessionStorage.getItem('role');
    const username = sessionStorage.getItem('username');
    console.log("Role:", role, "Username:", username); // Debug log

    const adminPanelLink = document.getElementById('adminPanelLink');
    const studentDashboardLink = document.getElementById('studentDashboardLink');

    if (!role || !username) {
        console.error("Role or username not set in sessionStorage. Redirecting to login page.");
        if (window.location.pathname !== "/index.html") {
            window.location.href = "index.html"; // Redirect to login page
        }
        return;
    }

    if (role === 'admin') {
        if (adminPanelLink) adminPanelLink.style.display = 'block'; // Show Admin Panel link
        if (studentDashboardLink) studentDashboardLink.style.display = 'none'; // Hide My Events link
    } else if (role === 'student') {
        if (studentDashboardLink) studentDashboardLink.style.display = 'block'; // Show My Events link
        if (adminPanelLink) adminPanelLink.style.display = 'none'; // Hide Admin Panel link
    }

    // Highlight the active nav link (robust for all cases)
    const navLinks = document.querySelectorAll('nav ul li a');
    const current = window.location.pathname.split('/').pop().split('?')[0] || "index.html";
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        if (!linkHref) return;
        const target = linkHref.split('/').pop().split('?')[0];
        if (current === target) {
            link.classList.add('active');
        }
    });

    // Ensure fetchEvents is called only once
    if (!window.eventsFetched) {
        window.eventsFetched = true; // Set a flag to prevent multiple calls
        console.log("Calling fetchEvents...");
        fetchEvents(); // Fetch events for the homepage
    }

    // Ensure fetchRegisteredEvents is called only once for students
    if (!window.registeredEventsFetched && role === 'student') {
        window.registeredEventsFetched = true; // Set a flag to prevent multiple calls
        console.log("Calling fetchRegisteredEvents...");
        fetchRegisteredEvents(username);
    }
});

// Function to open the Edit Event modal
window.openEditEventModal = function openEditEventModal(eventId, buttonElement) {
    const modal = document.getElementById("editEventModal");
    const rect = buttonElement.getBoundingClientRect(); // Get the position of the clicked button

    modal.style.position = "absolute";
    modal.style.top = `${rect.bottom + window.scrollY + 10}px`; // Position below the button
    modal.style.left = `${rect.left}px`;
    modal.style.display = "block";

    const eventCard = buttonElement.closest('.event-card');
    const title = eventCard.querySelector('h3').textContent;
    const date = eventCard.querySelector('p').textContent.replace('Date: ', '');

    document.getElementById("edit-event-title").value = title;
    document.getElementById("edit-event-date").value = date;

    // Store the event ID in the modal for later use
    modal.dataset.eventId = eventId;
};

// Function to close the Edit Event modal
window.closeModal = function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = "none";
};

// Function to submit the Edit Event form
window.submitEditEvent = function submitEditEvent() {
    const modal = document.getElementById("editEventModal");
    const eventId = modal.dataset.eventId;

    const title = document.getElementById("edit-event-title").value;
    const date = document.getElementById("edit-event-date").value;
    const poster = document.getElementById("edit-event-poster").files[0];

    if (!title || !date) {
        alert("Please fill in all fields.");
        return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("date", date);
    if (poster) {
        formData.append("poster", poster);
    }

    fetch(`http://127.0.0.1:5000/admin/edit_event/${eventId}`, {
        method: "POST",
        body: formData,
        credentials: "include",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to edit event");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        window.location.reload(); // Reload the page to reflect changes
    })
    .catch(error => {
        console.error("Error editing event:", error.message);
        alert("Failed to edit event. Please try again.");
    });
};
