const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
const PORT = 3000;

let posts = [];

app.use(bodyParser.json());
app.use(express.static('public'));

// Route to serve index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/posts', (req, res) => {
    res.json(posts);
});

app.post('/api/posts', (req, res) => {
    const { title, content } = req.body;
    const newPost = { title, content };
    posts.push(newPost);
    res.status(201).json(newPost);
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
