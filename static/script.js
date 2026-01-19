function updateProgress() {
    fetch(PROGRESS_URL)
        .then(response => response.json())
        .then(data => {
            const progressBar = document.getElementById("session_bar");
            const progressText = document.getElementById("progress_text");

            progressBar.value = data.progress;
            progressBar.max = 100;
            progressText.textContent = `${data.progress}%`;
        })
        .catch(err => console.error("Error fetching progress:", err));
}


setInterval(updateProgress, 60000);


updateProgress();

