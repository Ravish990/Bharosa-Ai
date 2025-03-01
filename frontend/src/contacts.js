document.getElementById('contacts-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get the user input
    const contact1 = document.getElementById('contact1').value;
    const contact2 = document.getElementById('contact2').value;
    const contact3 = document.getElementById('contact3').value;
    const contact4 = document.getElementById('contact4').value;

    // Store the trusted contacts in localStorage
    const trustedContacts = {
        contact1,
        contact2,
        contact3,
        contact4
    };

    localStorage.setItem('trustedContacts', JSON.stringify(trustedContacts));

    // Display success message
    document.getElementById('message').innerHTML = "<p>Your trusted contacts have been saved successfully!</p>";
    
    // Redirect to the home page after saving contacts
    setTimeout(function() {
        window.location.href = "index.html";
    }, 2000);
});

// Check if the trusted contacts are already saved
window.onload = function() {
    const savedContacts = localStorage.getItem('trustedContacts');

    if (savedContacts) {
        const contacts = JSON.parse(savedContacts);
        document.getElementById('contact1').value = contacts.contact1;
        document.getElementById('contact2').value = contacts.contact2;
        document.getElementById('contact3').value = contacts.contact3;
        document.getElementById('contact4').value = contacts.contact4;
    }
};