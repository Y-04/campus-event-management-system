export function fetchEvents() {
    if (window.fetchEventsInProgress) {
        console.warn("fetchEvents is already in progress. Skipping this call.");
        return;
    }
    window.fetchEventsInProgress = true; // Set a flag to prevent overlapping calls

    console.log("Fetching events..."); // Debug log
    fetch("http://127.0.0.1:5000/events")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const { upcoming, past } = data;

            // Render upcoming events
            const eventList = document.getElementById("event-list");
            if (eventList) {
                eventList.innerHTML = ""; // Clear previous data
                upcoming.forEach(event => {
                    const eventItem = document.createElement("div");
                    eventItem.classList.add("event-card");
                    if (isUpcomingGlow(event.date)) {
                        eventItem.classList.add("upcoming-glow");
                    }
                    eventItem.innerHTML = `
                        <h3>${event.title}</h3>
                        <p>Date: ${event.date}</p>
                        <button onclick="openEventDetails(${event.id}, this)">Details</button>
                        ${
                            sessionStorage.getItem("role") === "student"
                                ? `<button onclick="openRegistrationModal(${event.id}, this)">Register</button>`
                                : ""
                        }
                    `;
                    eventList.appendChild(eventItem);
                });
            }

            // Render past events
            const pastEventList = document.getElementById("past-event-list");
            if (pastEventList) {
                pastEventList.innerHTML = "<h2>Past Events</h2>";
                past.forEach(event => {
                    const eventItem = document.createElement("div");
                    eventItem.classList.add("event-card");
                    eventItem.innerHTML = `
                        <h3>${event.title}</h3>
                        <p>Date: ${event.date}</p>
                        <button onclick="openEventDetails(${event.id}, this)">Details</button>
                    `;
                    pastEventList.appendChild(eventItem);
                });
            }
        })
        .catch(error => console.error("Error fetching events:", error.message))
        .finally(() => {
            window.fetchEventsInProgress = false; // Reset the flag
        });
}

export function fetchRegisteredEvents(username) {
    if (!username) {
        console.error("fetchRegisteredEvents: username is missing!");
        return;
    }
    console.log("Fetching registered events for username:", username); // Debug log
    fetch(`http://127.0.0.1:5000/student_events/${username}`)
        .then(response => {
            if (!response.ok) {
                console.error("Backend returned status:", response.status, "for username:", username);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const { upcoming, past } = data;
            if (!upcoming && !past) {
                console.warn("No registered events returned from backend.");
            }
            renderRegisteredEvents(upcoming, past);
        })
        .catch(error => console.error("Error fetching registered events:", error.message));
}

export function renderRegisteredEvents(upcoming, past) {
    const upcomingEventsList = document.getElementById("upcoming-events");
    const pastEventsList = document.getElementById("past-events");

    if (upcomingEventsList) {
        upcomingEventsList.innerHTML = ""; // Clear previous data
        upcoming.forEach(event => {
            const eventCard = document.createElement("div");
            eventCard.classList.add("event-card");
            if (isUpcomingGlow(event.date)) {
                eventCard.classList.add("upcoming-glow");
            }
            eventCard.innerHTML = `
                <h3>${event.title}</h3>
                <p>Date: ${event.date}</p>
                <button onclick="openEventDetails(${event.id}, this)">Details</button>
            `;
            upcomingEventsList.appendChild(eventCard);
        });
    }

    if (pastEventsList) {
        pastEventsList.innerHTML = ""; // Clear previous data
        past.forEach(event => {
            const eventCard = document.createElement("div");
            eventCard.classList.add("event-card");
            eventCard.innerHTML = `
                <h3>${event.title}</h3>
                <p>Date: ${event.date}</p>
                <button onclick="openEventDetails(${event.id}, this)">Details</button>
            `;
            pastEventsList.appendChild(eventCard);
        });
    }
}

export function fetchAdminEvents() {
    console.log("Fetching admin events...");
    fetch("http://127.0.0.1:5000/events")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const { upcoming, past } = data;
            const adminEventList = document.getElementById("admin-event-list");

            if (adminEventList) {
                adminEventList.innerHTML = ""; // Clear previous data
                [...upcoming, ...past].forEach(event => {
                    const eventItem = document.createElement("div");
                    eventItem.classList.add("event-card");
                    eventItem.innerHTML = `
                        <h3>${event.title}</h3>
                        <p>Date: ${event.date}</p>
                        <button onclick="editEvent(${event.id})">Edit</button>
                        <button onclick="deleteEvent(${event.id})">Delete</button>
                    `;
                    adminEventList.appendChild(eventItem);
                });
            }
        })
        .catch(error => console.error("Error fetching admin events:", error.message));
}

function isUpcomingGlow(eventDateStr) {
    // eventDateStr is in 'YYYY-MM-DD' format
    const eventDate = new Date(eventDateStr);
    const today = new Date();
    const diff = (eventDate - today) / (1000 * 60 * 60 * 24);
    return diff >= 0 && diff <= 3; // within next 3 days
}
