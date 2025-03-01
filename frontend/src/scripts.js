let loggedInUser = ""; // Variable to store logged in user's name
let userEmail = ""; // Variable to store user email
let userPhone = ""; // Variable to store user phone number

// Show the Login Modal
function showLoginModal() {
    document.getElementById("loginModal").style.display = "block";
}

// Close the Login Modal
function closeLoginModal() {
    document.getElementById("loginModal").style.display = "none";
}

// Show the Register Modal
function showRegisterModal() {
    document.getElementById("registerModal").style.display = "block";
}

// Close the Register Modal
function closeRegisterModal() {
    document.getElementById("registerModal").style.display = "none";
}

// Handle User Login
function loginUser(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const password = form.password.value;

    // Simulate fetching stored user data from localStorage
    const storedUser = JSON.parse(localStorage.getItem('user'));

    if (storedUser && storedUser.username === username && storedUser.password === password) {
        loggedInUser = username; // Save the username
        userEmail = storedUser.email; // Save email
        userPhone = storedUser.phone; // Save phone number

        document.getElementById("userDetails").innerText = loggedInUser; // Update the profile button text
        document.getElementById("loginButton").style.display = "none"; // Hide login button
        document.getElementById("registerButton").style.display = "none"; // Hide register button
        document.getElementById("logoutButton").style.display = "inline-block"; // Show logout button
        document.getElementById("profileButton").style.display = "inline-block"; // Show profile button
        document.getElementById("takeActionButton").style.display = "inline-block"; // Show take action button

        closeLoginModal(); // Close modal
        showProfile(); // Display user profile
        showSuccessPopup("Login Successful!"); // Show login successful popup
    } else {
        alert('Invalid credentials. Please try again.');
    }
}

// Handle User Registration
function registerUser(event) {
    event.preventDefault();
    const form = event.target;
    const username = form.username.value;
    const email = form.email.value;
    const phone = form.phone.value;
    const password = form.password.value;

    const existingUser = JSON.parse(localStorage.getItem('user'));

    if (existingUser && (existingUser.username === username || existingUser.email === email)) {
        alert('User already exists. Please try to login.');
        return; 
    }

    if (phone.length !== 10) {
        alert('Mobile number must be exactly 10 digits.');
        return;
    }

    const user = { username, email, phone, password };
    localStorage.setItem('user', JSON.stringify(user));

    alert('Registration successful! You can now log in.');
    closeRegisterModal();
}

// Show User Profile
function showProfile() {
    document.getElementById("profileUsername").innerText = loggedInUser; // Set username in profile
    document.getElementById("profileEmail").innerText = userEmail; // Set email in profile
    document.getElementById("profilePhone").innerText = userPhone; // Set phone in profile
    document.getElementById("profileSection").style.display = "block";
}

// Close the Profile Modal
function closeProfile() {
    document.getElementById("profileSection").style.display = "none";
}

// Logout function
function logout() {
    loggedInUser = ""; // Clear user
    userEmail = ""; // Clear email
    userPhone = ""; // Clear phone
    document.getElementById("userDetails").innerText = "Profile"; // Reset profile button
    document.getElementById("loginButton").style.display = "inline-block"; // Show login button
    document.getElementById("registerButton").style.display = "inline-block"; // Show register button
    document.getElementById("logoutButton").style.display = "none"; // Hide logout button
    document.getElementById("profileButton").style.display = "none"; // Hide profile button
    document.getElementById("takeActionButton").style.display = "none"; // Hide take action button
    alert('Logged out successfully!');
}

// Show success popup
function showSuccessPopup(message) {
    const popup = document.createElement("div");
    popup.className = "popup";
    popup.innerText = message;
    document.body.appendChild(popup);
    setTimeout(() => {
        popup.remove();
    }, 3000);
}

// JavaScript for handling Learn More button click
document.getElementById("learnMoreButton").onclick = function () {
    window.location.href = "learnMore.html"; // Redirect to learnMore.html
};

// Event listeners for dynamically hidden elements
document.getElementById("sosButton").onclick = function() {
    alert("SOS button clicked!");
};

document.getElementById("shareLocationButton").onclick = function() {
    alert("Share Location button clicked!");
};

// Assign login and registration event listeners
document.getElementById("loginForm").onsubmit = loginUser;
document.getElementById("registerForm").onsubmit = registerUser;