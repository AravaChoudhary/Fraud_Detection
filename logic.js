async function fetchNews() {
    const apiKey = 'dd0ff48fddfa430c8e77e46151b39b99';
    const timestamp = Date.now();
    const apiUrl = `https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=${apiKey}&timestamp=${timestamp}`;

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        return data.articles;
    } catch (error) {
        console.error('Error fetching news:', error);
        return [];
    }
}

        
async function displayNews() {
    const articles = await fetchNews();
    const newsContainer = document.getElementById('news-container');

    articles.forEach(article => {
        const newsCard = document.createElement('div');
        newsCard.classList.add('news-card');

        const image = document.createElement('img');
        image.src = article.urlToImage;
        image.alt = 'News Image';
        image.style.width = '150px'; 
        image.style.height = '100px';

        const title = document.createElement('h2');
        title.textContent = article.title;

        const description = document.createElement('p');
        description.textContent = article.description;

        newsCard.appendChild(image);
        newsCard.appendChild(title);
        newsCard.appendChild(description);

        newsContainer.appendChild(newsCard);
    });
}

// Call the displayNews function to fetch and display news articles
displayNews();

        async function populateNewsSection() {
            const newsSlider = document.getElementById('newsSlider');
            const newsData = await fetchNews();
            if (newsData && newsData.length > 0) {
                newsData.forEach(article => {
                    const newsCard = document.createElement('div');
                    newsCard.classList.add('news-card');
                    newsCard.innerHTML = `
                        <img src="${article.urlToImage}" alt="${article.title}">
                        <h2>${article.title}</h2>
                        <p>${article.description}</p>
                    `;
                    newsSlider.appendChild(newsCard);
                });
            } else {
                const noNewsMessage = document.createElement('p');
                noNewsMessage.textContent = 'No news available.';
                newsSlider.appendChild(noNewsMessage);
            }
        }

        let slideIndex = 0;

        function slideNews(direction) {
            const newsSlider = document.querySelector('.news-slider');
            const newsCards = document.querySelectorAll('.news-card');
            const cardWidth = newsCards[0].offsetWidth + 20; // Width of card + margin-right

            slideIndex += direction * 2;
            if (slideIndex < 0) {
                slideIndex = 0;
            }
            if (slideIndex >= newsCards.length) {
                slideIndex = newsCards.length - 4; // Display 4 articles per slide
            }

            newsSlider.style.transform = `translateX(-${cardWidth * slideIndex}px)`;
        }

        function loadMore() {
            // This function can be used if you want to load more news articles dynamically
        }

        // Populate news section when the page loads
        window.addEventListener('DOMContentLoaded', populateNewsSection);