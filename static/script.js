function validateForm() {
    const email = document.querySelector("input[name='email']").value;
    const message = document.querySelector("textarea").value;

    if (!email.includes("@")) {
        alert("Enter a valid email");
        return false;
    }

    if (message.length < 10) {
        alert("Message must be at least 10 characters");
        return false;
    }

    return true;
}
