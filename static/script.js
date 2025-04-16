document.getElementById('startButton').addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.getElementById('video');
        video.srcObject = stream;
    } catch (err) {
        console.error('Error accessing the camera: ', err);
    }
});