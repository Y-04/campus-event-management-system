export function addEvent() {
    const title = document.getElementById("event-title").value;
    const date = document.getElementById("event-date").value;
    const poster = document.getElementById("event-poster").files[0];

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

    fetch("http://127.0.0.1:5000/admin/add_event", {
        method: "POST",
        body: formData,
        credentials: "include",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to add event");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchAdminEvents(); // Refresh the admin event list
        fetchEvents(); // Refresh the public event list
    })
    .catch(error => {
        console.error("Error adding event:", error.message);
        alert("Failed to add event. Please try again.");
    });
}

// Ensure events are fetched when the admin panel is loaded
document.addEventListener("DOMContentLoaded", function() {
    fetchAdminEvents();
});

export function editEvent(eventId) {
    console.log("Editing event with ID:", eventId); // Debug log
    const modal = document.getElementById("editEventModal");
    const titleInput = document.getElementById("edit-event-title");
    const dateInput = document.getElementById("edit-event-date");
    const posterInput = document.getElementById("edit-event-poster");

    // Fetch the event details to pre-fill the form
    fetch(`http://127.0.0.1:5000/events`)
        .then(response => response.json())
        .then(data => {
            const { upcoming, past } = data; // Destructure the response
            const events = [...upcoming, ...past]; // Combine upcoming and past events
            const event = events.find(e => e.id === eventId); // Find the specific event

            if (event) {
                console.log("Event found:", event); // Debug log
                titleInput.value = event.title;
                dateInput.value = event.date;
                posterInput.value = ""; // Clear the file input
                modal.dataset.eventId = eventId; // Store event ID in the modal
                modal.style.display = "block"; // Show the modal
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

export function submitEditEvent() {
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
        closeModal("editEventModal");
        fetchAdminEvents(); // Refresh the admin event list
        fetchEvents(); // Refresh the public event list
    })
    .catch(error => {
        console.error("Error editing event:", error.message);
        alert("Failed to edit event. Please try again.");
    });
}

export function deleteEvent(eventId) {
    if (!confirm("Are you sure you want to delete this event?")) {
        return;
    }

    fetch(`http://127.0.0.1:5000/admin/delete_event/${eventId}`, {
        method: "DELETE",
        credentials: "include",
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to delete event");
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchAdminEvents(); // Refresh the admin event list
        fetchEvents(); // Refresh the public event list
    })
    .catch(error => {
        console.error("Error deleting event:", error.message);
        alert("Failed to delete event. Please try again.");
    });
}
