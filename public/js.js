document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.getElementById('postForm');
    const postsDiv = document.getElementById('posts');

    const fetchPosts = async () => {
        const response = await fetch('/api/posts');
        const posts = await response.json();
        postsDiv.innerHTML = '';
        posts.forEach(post => {
            const postDiv = document.createElement('div');
            postDiv.classList.add('post');
            postDiv.innerHTML = `
                <h2>${post.title}</h2>
                <p>${post.content}</p>
            `;
            postsDiv.appendChild(postDiv);
        });
    };

    postForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;

        await fetch('/api/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, content }),
        });

        postForm.reset();
        fetchPosts();
    });

    fetchPosts();
});
