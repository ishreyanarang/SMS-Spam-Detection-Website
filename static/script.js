function analyzeMessage() {
    const message = document.getElementById("message").value;

    // Ensure the message is not empty
    if (!message.trim()) {
        alert("Please enter a message to analyze.");
        return;
    }

    // Send the message to the backend
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById("result");
        
        // Clear previous styles and content
        resultDiv.className = ''; 
        resultDiv.style.display = 'none'; // Hide initially

        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        } else {
            const { result, confidence } = data;
            resultDiv.innerHTML = `<p>${result.toUpperCase()}<br>(Confidence: ${confidence}%)</p>`;
            resultDiv.style.display = 'block'; // Show result box
            
            // Apply the appropriate animation class
            if (result.toLowerCase() === 'spam') {
                resultDiv.classList.add('spam-blink');
            } else if (result.toLowerCase() === 'ham') {
                resultDiv.classList.add('ham-blink');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}
