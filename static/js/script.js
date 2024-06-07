document.addEventListener('DOMContentLoaded', function () {
    const video = document.createElement('video');
    video.style.display = 'none';  // Hide the video element as we only need it to capture frames

    document.body.appendChild(video);

    const img = document.querySelector('img');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
        })
        .catch(console.error);

    setInterval(() => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const data = canvas.toDataURL('image/jpeg');

        fetch('/process_frame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: data })
        })
        .then(response => response.json())
        .then(data => {
            img.src = 'data:image/jpeg;base64,' + data.image;
        })
        .catch(console.error);
    }, 120);  // Adjust as necessary for frame rate
});
