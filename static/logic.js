document.getElementById('newIdea').addEventListener('click', function() {
    const keywords = document.getElementById('keywordInput').value.trim();

    if (!keywords) {
        document.getElementById('ideaBox').innerText = 'Please enter some keywords.';
        return;
    }

    document.getElementById('ideaBox').innerText = 'Generating ideas...';

    fetch('/generate_idea', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keywords: keywords }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('ideaBox').innerText = data.idea;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('ideaBox').innerText = 'Failed to generate ideas. Please try again.';
    });
});
