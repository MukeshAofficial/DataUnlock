# DataUnlock

**DataUnlock** is an innovative platform that allows users to create instant chatbots and voicebots for free. Simply provide a company website URL, and DataUnlock extracts data, builds a knowledge base, and generates a fully functional customer support bot in real-time. 🚀

---

## 🌟 Features
- **Instant Chatbots**: Paste a company URL and get a functional chatbot instantly.
- **Voicebot Support**: Advanced audio-based interactions powered by Gemini 2.0.
- **Data Extraction**: Automatically extracts and structures data from websites.
- **Embeddable Bots**: For businesses, embed your custom chatbot directly on your site.
- **Real-Time Responses**: Quick and intelligent answers based on company data.

---

## 🛠 How It Works
1. Enter a company website URL.
2. DataUnlock scrapes the site using **Beautiful Soup**.
3. A knowledge base is created using **Llama Index**.
4. The bot is powered by **Gemini embeddings** for precise answers.
5. For voice interactions, **Gemini 2.0** enables natural, conversational audio.

---

## 🚧 Challenges Solved
- Eliminates the high cost of custom chatbot development (usually $500+ per bot).
- Works seamlessly even with websites containing incomplete or variable data.

# 🛠 Setup

Step 1: Clone the Repository


Step 2: Install Requirements
pip install -r requirements.txt

Step 3: Run main.py to initialize the project
python main.py

Step 4: Start a Local HTTP Server in a new terminal
python -m http.server

Step 5: Run the Flask App in another terminal
python app.py

Step 6: Access the Application
Open your browser and go to:
http://localhost:5001
