// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', async () => {
    // Check if the Google Maps API is loaded
    if (typeof google === 'undefined') {
        console.error('Google Maps JavaScript API failed to load.');
        return;
    }

    // Initialize the map
    await initMap();
});


async function initMap() {
    console.log("initMap function called");

    const manhattanCenter = { lat: 40.7831, lng: -73.9712 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: manhattanCenter,
    });

    try {
        // Fetch cafes from the backend
        const response = await fetch("/api/cafes");
        const cafesData = await response.json();
        const cafes = cafesData.cafes || [];

        // Add a marker for each cafe
        cafes.forEach(cafe => {
            console.log(`Processing cafe: ${cafe.name}, Photo URL: ${cafe.photo_url}`);

            const marker = new google.maps.Marker({
                position: { lat: cafe.latitude, lng: cafe.longitude },
                map: map,
                title: cafe.name,
            });

            // Info window content
            const infoWindowContent = `
                ${cafe.photo_url
                        ? `<img src="${cafe.photo_url}" alt="${cafe.name}" style="max-width:200px; max-height:200px;">`
                        : '<p>No image available</p>'
                }
                <h3>${cafe.name}</h3>
                <p>${cafe.address}</p>
                <p>Rating: ${cafe.rating || 'N/A'}</p> 
            `;

            const infoWindow = new google.maps.InfoWindow({
                content: infoWindowContent,
            });

            marker.addListener("click", () => {
                infoWindow.open(map, marker);
            });
        });
    } catch (error) {
        console.error("Error fetching cafe data:", error);
    }
}