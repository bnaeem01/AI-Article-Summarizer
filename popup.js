document.addEventListener('DOMContentLoaded', function () {
    // Attach event listener to the button
    var button = document.getElementById('summarizeButton');
    button.addEventListener('click', function () {
        summarizeArticle();
    });
});

function summarizeArticle() {
    var articleUrl = document.getElementById('articleUrl').value;

    fetch('http://localhost:5000/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: articleUrl })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('summary').innerText = data.summary;
        })
        .catch(error => console.error('Error:', error));
}