function getMusic() {
    let city = document.getElementById("city").value;
    let mood = document.getElementById("mood").value;

    fetch("/get_music", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city: city, mood: mood })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML = 
            `Mood: ${data.mood} <br> Weather: ${data.weather} <br> 🎵 Playlist: ${data.playlist}`;
    })
    .catch(error => console.error("Error:", error));
}
