const downloadBtn = document.getElementById('downloadBtn');
const videoUrlInput = document.getElementById('urlInput');
const result = document.getElementById('result');
const pasteBtn = document.getElementById('pasteBtn');


// Platform selector
const platformBtns = document.querySelectorAll('.platform-btn');
platformBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        platformBtns.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        // Update placeholder based on selected platform
        videoUrlInput.placeholder = `Paste ${btn.textContent} video link here...`;
    });
});





// 📋 Paste / Clear toggle
let isPasted = false; // toggle state
pasteBtn.addEventListener('click', async () => {
    if (!isPasted) {
        // Paste from clipboard
        try {
            const text = await navigator.clipboard.readText();
            if (text) {
                videoUrlInput.value = text;
                isPasted = true;
                pasteBtn.src = "/static/img/x.svg"; // 🔄 change to X image
            } else {
                alert("Clipboard is empty.");
            }
        } catch (err) {
            alert("Failed to read clipboard. Please allow clipboard permissions.");
            console.error(err);
        }
    } else {
        // Clear input
        videoUrlInput.value = "";
        isPasted = false;
        pasteBtn.src = "/static/img/paste.png"; // 🔄 change back to paste icon
    }
});

// Download Logic
downloadBtn.addEventListener('click', () => {
    const url = videoUrlInput.value.trim();
    if (!url) {
        alert('Please enter a valid URL');
        return;
    }

    // Hide input + platform
    document.querySelector('.platform-selector').style.display = 'none';
    document.querySelector('.input-row').style.display = 'none';

    // Show loader inside result box
    result.style.display = 'block';
    result.innerHTML = `
        <center>
            <div class="loader"></div>
            <p>Processing your download...</p>
        </center>
    `;

    // Send request
    const formData = new FormData();
    formData.append("url", url);

    fetch("/download/", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error("Failed to download");
        return response.blob();
    })
    .then(blob => {
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "video.mp4";
        a.click();

        // Show success + "Download Another" button
        result.innerHTML = `
            <center>
                <p>✅ Video Downloaded!</p>
                <button class="btn" id="resetBtn">Download Another</button>
            </center>
        `;

        // Add event listener for reset
        document.getElementById('resetBtn').addEventListener('click', () => {
            resetDownloader();
        });
    })
    .catch(err => {
        result.innerHTML = `
            <center>
                <p style="color:red;">❌ Error: ${err.message}. Check Internet or Link</p>
                <button class="btn" id="resetBtn" style="width: 240px;">Try Again</button>
            </center>
        `;
        document.getElementById('resetBtn').addEventListener('click', () => {
            resetDownloader();
        });
    });
});

function resetDownloader() {
    // Show input + platform again
    document.querySelector('.platform-selector').style.display = 'flex';
    document.querySelector('.input-row').style.display = 'flex';

    // Hide result box
    result.style.display = 'none';

    // Clear input field
    videoUrlInput.value = "";
}


// downloadBtn.addEventListener('click', () => {
//     const url = videoUrlInput.value.trim();
//     if (!url) {
//         alert('Please enter a valid URL');
//         return;
//     }

//     // Hide input + platform
//     document.querySelector('.platform-selector').style.display = 'none';
//     document.querySelector('.input-row').style.display = 'none';

//     // Show loader inside result box
//     result.style.display = 'block';
//     result.innerHTML = `
//         <center>
//         <div class="loader"></div>
//         <p>Processing your download...</p>
//         </center>
//     `;

//     // Send request
//     const formData = new FormData();
//     formData.append("url", url);

//     fetch("/download/", {
//         method: "POST",
//         body: formData
//     })
//     .then(response => {
//         if (!response.ok) throw new Error("Failed to download");
//         return response.blob();
//     })
//     .then(blob => {
//         const a = document.createElement("a");
//         a.href = URL.createObjectURL(blob);
//         a.download = "video.mp4";
//         a.click();
//         result.innerHTML = "<p>✅ Video Downloaded!</p>";
//     })
//     .catch(err => {
//         result.innerHTML = `<p style="color:red;">❌ Error: ${err.message}. Check Internet or Link</p>`;
//     });
// });
