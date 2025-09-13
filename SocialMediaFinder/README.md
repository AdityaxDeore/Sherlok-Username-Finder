# 🕵️ Sherlock Finds - Social Media Username Finder

A powerful web application for finding social media profiles across 80+ platforms in real-time. Built with Flask and featuring live streaming search results.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3.3-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 🔄 **Real-Time Streaming Search**
- **Live Progress Updates**: See which platform is currently being searched
- **Progressive Results**: Results appear instantly as each website is checked
- **Real-Time Progress Bar**: Visual progress indicator with percentage
- **Current Platform Display**: Shows exactly which social media platform is being searched

### 📊 **Enhanced User Experience**
- **Smart Result Prioritization**: Found profiles appear at the top with special highlighting
- **Live Counter Updates**: Found count updates in real-time as profiles are discovered
- **Progress Tracking**: Shows "X% complete (processed/total platforms)"
- **Smooth Animations**: Found results have pulse animations and auto-scroll into view

### 🌐 **Platform Coverage**
Searches across 80+ social media platforms including:
- Facebook, Instagram, Twitter/X
- LinkedIn, GitHub, YouTube
- TikTok, Snapchat, Pinterest
- Reddit, Discord, Telegram
- And many more...

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/zadahmed/SocialMediaFinder.git
cd SocialMediaFinder
```

2. **Create a virtual environment**
```bash
python -m venv .venv
```

3. **Activate the virtual environment**

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
Navigate to `http://localhost:5000`

## 🎯 How to Use

1. **Enter Username**: Type the username you want to search for
2. **Start Search**: Click the search button or press Enter
3. **Watch Live Results**: See real-time progress as each platform is checked
4. **View Results**: Found profiles appear at the top with direct links

## 🔧 Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla JavaScript with Server-Sent Events (SSE)
- **Streaming**: Real-time data streaming using EventSource API
- **Styling**: Modern CSS with responsive design

### API Endpoints
- `GET /` - Main application interface
- `POST /search` - Batch search (legacy)
- `GET /search-stream/<username>` - Real-time streaming search
- `GET /about` - About page
- `GET /api/health` - Health check endpoint

### Key Files
- `app.py` - Main Flask application
- `sherlock.py` - Core search logic (command-line interface)
- `data.json` - Platform configuration and URLs
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies

## 📦 Dependencies

```
Flask==2.3.3
requests==2.31.0
gunicorn==21.2.0
Werkzeug==2.3.7
```

## 🌟 Features in Detail

### Real-Time Streaming
The application uses Server-Sent Events (SSE) to provide real-time updates:

```javascript
// Frontend connects to streaming endpoint
eventSource = new EventSource(`/search-stream/${username}`);

// Handles different types of stream events
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    handleStreamEvent(data);
};
```

### Smart Result Display
- **Priority Sorting**: Found profiles appear first
- **Live Animation**: New found results have special highlighting
- **Progress Tracking**: Real-time percentage and platform count
- **Auto-Scroll**: Automatically scrolls to new found results

## 🚀 Deployment

### Heroku Deployment
The application is ready for Heroku deployment with included `Procfile`:

```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
```

### Local Production
```bash
# Using gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Command Line Usage

You can also use the command-line interface:

```bash
python sherlock.py username
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Aditya Deore**
- GitHub: [@zadahmed](https://github.com/zadahmed)
- Project: [SocialMediaFinder](https://github.com/zadahmed/SocialMediaFinder)

## 🙏 Acknowledgments

- Inspired by the original Sherlock project
- Built with modern web technologies for enhanced user experience
- Special thanks to the open-source community

## 📸 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x400?text=Social+Media+Finder+Interface)

### Real-Time Search
![Real-Time Search](https://via.placeholder.com/800x400?text=Live+Search+Results)

### Results Display
![Results Display](https://via.placeholder.com/800x400?text=Search+Results+Display)

---

⭐ **Star this repository if you found it helpful!**