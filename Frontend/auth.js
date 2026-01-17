export function login() {
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
}

export function logout() {
    fetch('http://127.0.0.1:5000/logout')
        .then(() => {
            sessionStorage.clear(); // Clear sessionStorage
            window.location.href = 'index.html';
        })
        .catch(error => console.error('Error:', error));
}
