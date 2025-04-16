// Handle live updates from the server
document.getElementById("uploadForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent form submission

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Send the file to the server
    fetch("/process", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            // Display the result
            const resultDiv = document.getElementById("result");
            resultDiv.textContent = data.result || data.error;

            // Update the result style dynamically
            if (data.result === "MATCH!") {
                resultDiv.style.color = "green";
            } else if (data.result === "NO MATCH!") {
                resultDiv.style.color = "red";
            } else {
                resultDiv.style.color = "black";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});