function startConversion() {
    // Get the convert button and the input field for the YouTube link
    const button = document.getElementById('convertButton');
    const youtubeLinkInput = document.getElementById('youtube_link');

    // Change button text to 'Loading...' and disable it to prevent multiple clicks
    button.innerHTML = 'Loading...';
    button.disabled = true;

    // Retrieve the value from the input field
    const youtubeLink = youtubeLinkInput.value;

    // Regular expression to validate YouTube URL format
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})$/;

    // Check if the input is empty or does not match the valid YouTube URL format
    if (!youtubeLink || !youtubeRegex.test(youtubeLink)) {
        // Set error message in the input field if validation fails
        youtubeLinkInput.value = 'Please input a valid YouTube URL.';

        // Reset button text and enable it again for user interaction
        button.innerHTML = 'Convert & Download';
        button.disabled = false;
        return; // Exit the function early
    }

    // If the URL is valid, send a POST request to the Flask server
    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Set content type for form data
        },
        body: new URLSearchParams({ youtube_link: youtubeLink }), // Send the YouTube link
    })
    .then(response => {
        // Check if the response is okay; if not, throw an error
        if (!response.ok) throw new Error('Conversion failed');

        // Return both the blob of the response and the Content-Disposition header
        return Promise.all([response.blob(), response.headers.get('Content-Disposition')]);
    })
    .then(([blob, contentDisposition]) => {
        // Create a URL for the blob and a temporary link element for downloading
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        // Extract the filename from the Content-Disposition header or default to 'download.mp3'
        const filename = contentDisposition ? contentDisposition.split('filename=')[1].replace(/"/g, '') : 'download.mp3';
        a.download = filename; // Set the download attribute with the filename

        // Append the link to the body and programmatically click it to trigger download
        document.body.appendChild(a);
        a.click();
        a.remove(); // Clean up the DOM

        // Reset button text and enable it again for further interaction
        button.innerHTML = 'Convert & Download';
        button.disabled = false;
    })
    .catch(error => {
        // Log any errors that occur during the fetch process
        console.error('Error:', error);

        // Reset button text and enable it again
        button.innerHTML = 'Convert & Download';
        button.disabled = false;
    });
}
