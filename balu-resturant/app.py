from flask import Flask, render_template_string, jsonify, request
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    html = """
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Balu - Premium Dining Experience</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #1a1a1a;
            --secondary: #c9a145;
            --accent: #d4af37;
            --light: #f8f5f0;
            --dark: #0d0d0d;
            --gray: #333333;
            --success: #4CAF50;
            --warning: #FF9800;
            --error: #f44336;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: var(--primary);
            color: var(--light);
            overflow-x: hidden;
        }
        
        /* Header Styles */
        header {
            position: fixed;
            top: 0;
            width: 100%;
            padding: 20px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
            background: rgba(10, 10, 10, 0.95);
            backdrop-filter: blur(10px);
            transition: 0.3s;
        }
        
        .logo {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            font-weight: 700;
            color: var(--secondary);
            letter-spacing: 1px;
        }
        
        .logo span {
            color: var(--accent);
        }
        
        nav ul {
            display: flex;
            list-style: none;
        }
        
        nav ul li {
            margin: 0 15px;
        }
        
        nav ul li a {
            color: var(--light);
            text-decoration: none;
            font-size: 16px;
            font-weight: 500;
            transition: 0.3s;
            position: relative;
        }
        
        nav ul li a:after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background: var(--accent);
            transition: 0.3s;
        }
        
        nav ul li a:hover:after {
            width: 100%;
        }
        
        nav ul li a:hover {
            color: var(--accent);
        }
        
        .nav-buttons {
            display: flex;
            gap: 15px;
        }
        
        .btn {
            padding: 12px 25px;
            border-radius: 30px;
            font-weight: 500;
            cursor: pointer;
            transition: 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: var(--accent);
            color: var(--dark);
            border: 2px solid var(--accent);
        }
        
        .btn-outline {
            background: transparent;
            color: var(--accent);
            border: 2px solid var(--accent);
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        /* Hero Section */
        .hero {
            height: 100vh;
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3') center/cover no-repeat;
            display: flex;
            align-items: center;
            padding: 0 50px;
            position: relative;
        }
        
        .hero-content {
            max-width: 650px;
        }
        
        .hero h1 {
            font-family: 'Playfair Display', serif;
            font-size: 64px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 20px;
            color: var(--light);
        }
        
        .hero h1 span {
            color: var(--accent);
        }
        
        .hero p {
            font-size: 18px;
            margin-bottom: 30px;
            line-height: 1.7;
            max-width: 600px;
        }
        
        /* Dishes Section */
        .dishes-section {
            padding: 100px 50px;
            background: var(--dark);
        }
        
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            text-align: center;
            margin-bottom: 60px;
            position: relative;
        }
        
        .section-title:after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 3px;
            background: var(--accent);
        }
        
        .dishes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 35px;
            margin-top: 50px;
        }
        
        .dish-card {
            background: var(--gray);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .dish-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        
        .dish-image {
            height: 220px;
            width: 100%;
            background-size: cover;
            background-position: center;
        }
        
        .dish-info {
            padding: 25px;
        }
        
        .dish-title {
            font-size: 22px;
            margin-bottom: 10px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
        }
        
        .dish-title span:last-child {
            color: var(--accent);
            font-weight: 700;
        }
        
        .dish-description {
            color: #bbb;
            margin-bottom: 15px;
            font-size: 15px;
            line-height: 1.6;
        }
        
        .protein-info {
            display: flex;
            align-items: center;
            color: var(--accent);
            font-weight: 500;
        }
        
        .protein-info i {
            margin-right: 8px;
            font-size: 18px;
        }
        
        /* Chatbot */
        .chatbot-container {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
        }
        
        .chatbot-btn {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--accent);
            color: var(--dark);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            transition: 0.3s;
        }
        
        .chatbot-btn:hover {
            transform: scale(1.1);
        }
        
        .chatbot-btn i {
            font-size: 24px;
        }
        
        .chat-window {
            position: absolute;
            bottom: 70px;
            right: 0;
            width: 350px;
            height: 450px;
            background: var(--light);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: none;
            flex-direction: column;
        }
        
        .chat-header {
            background: var(--accent);
            color: var(--dark);
            padding: 15px 20px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .close-chat {
            cursor: pointer;
            font-size: 20px;
        }
        
        .chat-body {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f0f0f0;
        }
        
        .chat-message {
            margin-bottom: 15px;
            max-width: 80%;
            padding: 12px 15px;
            border-radius: 15px;
            position: relative;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .bot-message {
            background: #fff;
            border-bottom-left-radius: 0;
            align-self: flex-start;
        }
        
        .user-message {
            background: var(--accent);
            color: var(--dark);
            border-bottom-right-radius: 0;
            margin-left: auto;
        }
        
        .chat-footer {
            padding: 15px;
            background: #fff;
            display: flex;
        }
        
        .chat-footer input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 30px;
            outline: none;
        }
        
        .chat-footer button {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--accent);
            color: var(--dark);
            border: none;
            margin-left: 10px;
            cursor: pointer;
        }
        
        /* Special Features */
        .features {
            padding: 100px 50px;
            background: linear-gradient(to right, var(--primary), var(--dark));
            text-align: center;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-top: 50px;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.05);
            padding: 40px 25px;
            border-radius: 10px;
            transition: 0.3s;
            backdrop-filter: blur(10px);
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            background: rgba(255,255,255,0.1);
        }
        
        .feature-icon {
            width: 70px;
            height: 70px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 28px;
            color: var(--dark);
        }
        
        .feature-card h3 {
            font-size: 22px;
            margin-bottom: 15px;
            color: var(--accent);
        }
        
        .feature-card p {
            color: #bbb;
            line-height: 1.7;
        }
        
        /* Footer */
        footer {
            background: var(--dark);
            padding: 70px 50px 30px;
            text-align: center;
        }
        
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }
        
        .social-icons a {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: var(--gray);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--light);
            transition: 0.3s;
            text-decoration: none;
        }
        
        .social-icons a:hover {
            background: var(--accent);
            color: var(--dark);
            transform: translateY(-5px);
        }
        
        .copyright {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid var(--gray);
            color: #777;
            font-size: 14px;
        }
        
        /* Responsive */
        @media (max-width: 992px) {
            header {
                padding: 20px 30px;
            }
            
            .hero h1 {
                font-size: 48px;
            }
        }
        
        @media (max-width: 768px) {
            nav ul {
                display: none;
            }
            
            .hero {
                padding: 0 30px;
            }
            
            .hero h1 {
                font-size: 36px;
            }
            
            .dishes-section, .features {
                padding: 80px 30px;
            }
            
            .chat-window {
                width: 300px;
                height: 400px;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="logo">Balu<span>.</span></div>
        <nav>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">Menu</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Reservations</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
        <div class="nav-buttons">
            <a href="#" class="btn btn-outline">Login</a>
            <a href="#" class="btn btn-primary">Reserve Table</a>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>Exquisite Flavors <br><span>Crafted to Perfection</span></h1>
            <p>Experience culinary artistry with our premium dishes crafted by world-class chefs using the finest ingredients sourced from around the globe.</p>
            <a href="#" class="btn btn-primary">Explore Menu</a>
        </div>
    </section>

    <!-- Dishes Section -->
    <section class="dishes-section">
        <h2 class="section-title">Our Signature Dishes</h2>
        <div class="dishes-grid">
            <!-- Dish 1 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Truffle Mushroom Risotto</span>
                        <span>$28</span>
                    </div>
                    <p class="dish-description">Creamy Arborio rice with wild mushrooms, white truffle oil, and Parmesan.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 18g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 2 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1550547660-d9450f859349?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Grilled Salmon</span>
                        <span>$32</span>
                    </div>
                    <p class="dish-description">Atlantic salmon with lemon-dill sauce, seasonal vegetables, and quinoa.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 34g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 3 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1606755962773-d324e7a7a7d6?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Beef Wellington</span>
                        <span>$42</span>
                    </div>
                    <p class="dish-description">Prime beef tenderloin wrapped in puff pastry with mushroom duxelles.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 38g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 4 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Lobster Thermidor</span>
                        <span>$48</span>
                    </div>
                    <p class="dish-description">Fresh lobster meat in a creamy brandy sauce, topped with Gruyère cheese.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 36g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 5 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1606491956689-2ea866880c84?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Herb-Crusted Lamb</span>
                        <span>$38</span>
                    </div>
                    <p class="dish-description">Rack of lamb with rosemary crust, mint jus, and roasted vegetables.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 40g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 6 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1555939594-58d7cb561ad1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Seafood Paella</span>
                        <span>$36</span>
                    </div>
                    <p class="dish-description">Spanish saffron rice with shrimp, mussels, clams, and chorizo.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 32g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 7 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1603360946369-dc9bbf814493?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Duck Confit</span>
                        <span>$34</span>
                    </div>
                    <p class="dish-description">Slow-cooked duck leg with cherry sauce, potato gratin, and greens.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 35g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 8 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1544025162-d76694265947?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Vegetable Wellington</span>
                        <span>$28</span>
                    </div>
                    <p class="dish-description">Roasted vegetables and goat cheese wrapped in puff pastry.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 15g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 9 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1603105037880-8802c0a85d9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Black Cod Miso</span>
                        <span>$36</span>
                    </div>
                    <p class="dish-description">Marinated black cod with miso glaze, served with bok choy.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 30g per serving</span>
                    </div>
                </div>
            </div>
            
            <!-- Dish 10 -->
            <div class="dish-card">
                <div class="dish-image" style="background-image: url('https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80');"></div>
                <div class="dish-info">
                    <div class="dish-title">
                        <span>Filet Mignon</span>
                        <span>$44</span>
                    </div>
                    <p class="dish-description">8oz prime beef with truffle mashed potatoes and asparagus.</p>
                    <div class="protein-info">
                        <i class="fas fa-dumbbell"></i>
                        <span>Protein: 42g per serving</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features">
        <h2 class="section-title">Premium Experience</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <h3>Easy Reservations</h3>
                <p>Book your table in seconds with our seamless online reservation system.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-wine-glass-alt"></i>
                </div>
                <h3>Wine Pairing</h3>
                <p>Expertly curated wine selections to complement each dish.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-leaf"></i>
                </div>
                <h3>Farm to Table</h3>
                <p>Fresh ingredients sourced daily from local organic farms.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-utensils"></i>
                </div>
                <h3>Private Dining</h3>
                <p>Exclusive spaces for special events and private celebrations.</p>
            </div>
        </div>
    </section>

    <!-- Chatbot -->
    <div class="chatbot-container">
        <div class="chatbot-btn">
            <i class="fas fa-comments"></i>
        </div>
        <div class="chat-window">
            <div class="chat-header">
                <span>Balu Concierge</span>
                <span class="close-chat"><i class="fas fa-times"></i></span>
            </div>
            <div class="chat-body" id="chat-body">
                <div class="chat-message bot-message">
                    Hello! I'm Balu, your dining assistant. How can I help you today?
                </div>
            </div>
            <div class="chat-footer">
                <input type="text" id="user-input" placeholder="Type your message...">
                <button id="send-btn"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="logo">Balu<span>.</span></div>
            <p>Premium dining experience since 2008</p>
            <div class="social-icons">
                <a href="#"><i class="fab fa-facebook-f"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-tripadvisor"></i></a>
            </div>
            <p>123 Gourmet Avenue, Culinary District</p>
            <p>Reservations: (555) 123-4567</p>
            <div class="copyright">
                &copy; 2023 Balu Restaurant. All rights reserved.
            </div>
        </div>
    </footer>

    <script>
        // Chatbot functionality
        const chatbotBtn = document.querySelector('.chatbot-btn');
        const chatWindow = document.querySelector('.chat-window');
        const closeChat = document.querySelector('.close-chat');
        const chatBody = document.getElementById('chat-body');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        
        // Toggle chat window
        chatbotBtn.addEventListener('click', () => {
            chatWindow.style.display = 'flex';
        });
        
        closeChat.addEventListener('click', () => {
            chatWindow.style.display = 'none';
        });
        
        // Send message function
        function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;
            
            // Add user message
            addMessage(message, 'user');
            userInput.value = '';
            
            // Simulate bot response after delay
            setTimeout(() => {
                generateBotResponse(message);
            }, 1000);
        }
        
        // Add message to chat
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('chat-message');
            messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');
            messageDiv.textContent = text;
            chatBody.appendChild(messageDiv);
            
            // Scroll to bottom
            chatBody.scrollTop = chatBody.scrollHeight;
        }
        
        // Generate bot response
        function generateBotResponse(userMessage) {
            userMessage = userMessage.toLowerCase();
            let response;
            
            if (userMessage.includes('menu') || userMessage.includes('dish')) {
                response = "We offer a variety of premium dishes. Our signature items include Truffle Mushroom Risotto, Grilled Salmon, and Beef Wellington. You can view our full menu on our website.";
            } else if (userMessage.includes('reservation') || userMessage.includes('book') || userMessage.includes('table')) {
                response = "You can make a reservation through our website or by calling (555) 123-4567. How many people and for what date/time?";
            } else if (userMessage.includes('hours') || userMessage.includes('open')) {
                response = "We're open Tuesday to Sunday from 5:00 PM to 11:00 PM. Closed on Mondays.";
            } else if (userMessage.includes('parking') || userMessage.includes('valet')) {
                response = "We offer complimentary valet parking for all our guests. Just pull up to the entrance and our staff will assist you.";
            } else if (userMessage.includes('dress') || userMessage.includes('code')) {
                response = "We maintain a smart casual dress code. We recommend collared shirts for gentlemen and elegant attire for ladies.";
            } else if (userMessage.includes('vegan') || userMessage.includes('vegetarian')) {
                response = "We have several vegetarian and vegan options available. Our chef can also prepare custom dishes based on dietary requirements.";
            } else {
                response = "I'm here to assist with your dining experience. You can ask about our menu, make a reservation, or inquire about special events.";
            }
            
            addMessage(response, 'bot');
        }
        
        // Event listeners
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Add initial bot message
        window.addEventListener('load', () => {
            setTimeout(() => {
                addMessage("Welcome to Balu! How may I assist with your dining experience today?", 'bot');
            }, 1500);
        });
        
        // Header scroll effect
        window.addEventListener('scroll', () => {
            const header = document.querySelector('header');
            if (window.scrollY > 100) {
                header.style.padding = '15px 50px';
                header.style.background = 'rgba(10, 10, 10, 0.98)';
            } else {
                header.style.padding = '20px 50px';
                header.style.background = 'rgba(10, 10, 10, 0.95)';
            }
        });
    </script>
</body>
</html>
    """
    return render_template_string(html)

@app.route('/fetch')
def fetch_data():
    url = 'https://jsonplaceholder.typicode.com/todos'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[:5]
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

@app.route('/health')
def health():
    return jsonify({"status": "App is healthy and running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
