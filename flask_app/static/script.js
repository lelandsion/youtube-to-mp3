function startConversion() {
    const button = document.getElementById('convertButton');
    const youtubeLinkInput = document.getElementById('youtube_link');
    button.innerHTML = 'Loading...';  // Change text to loading
    button.disabled = true;  // Disable the button to prevent multiple clicks

    const youtubeLink = youtubeLinkInput.value; // Get the input value

    // Check for empty link or invalid YouTube URL format
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})$/;
    if (!youtubeLink || !youtubeRegex.test(youtubeLink)) {
        youtubeLinkInput.value = 'Please input a valid YouTube URL.'; // Set error message
        button.innerHTML = 'Convert & Download'; // Reset button text
        button.disabled = false; // Re-enable the button
        return; // Exit the function
    }

    // If the URL is valid, make a fetch request to the Flask endpoint
    fetch('/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ youtube_link: youtubeLink }), // Send the YouTube link
    })
    .then(response => {
        if (!response.ok) throw new Error('Conversion failed');

        // Return both the blob and the response object for later use
        return Promise.all([response.blob(), response.headers.get('Content-Disposition')]);
    })
    .then(([blob, contentDisposition]) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        // Extract the filename from the Content-Disposition header
        const filename = contentDisposition ? contentDisposition.split('filename=')[1].replace(/"/g, '') : 'download.mp3';
        a.download = filename; // Use the filename extracted from the header

        document.body.appendChild(a);
        a.click();
        a.remove();
        button.innerHTML = 'Convert & Download';  // Reset button text
        button.disabled = false;  // Re-enable the button
    })
    .catch(error => {
        console.error('Error:', error);
        button.innerHTML = 'Convert & Download';  // Reset button text
        button.disabled = false;  // Re-enable the button
    });
}
