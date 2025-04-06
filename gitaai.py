from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import os
import logging
import traceback
import json
import random
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the Flask app with the correct static folder
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure the Gemini API key
GEMINI_API_KEY = "AIzaSyAAqJGmXYragcD6SchBIsPvyVNJBQGmzBY"
logger.info(f"API Key configured: {'*' * (len(GEMINI_API_KEY) - 8)}{GEMINI_API_KEY[-8:]}")

# Fallback responses if the API fails
FALLBACK_RESPONSES = [
    "The purpose of life according to the Bhagavad Gita is to realize your true self and fulfill your dharma (duty). When you act with detachment from the fruits of your actions and with devotion to the divine, you achieve liberation from the cycle of birth and death. As I said in Chapter 2, verse 47: 'You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions.' Find joy in the journey, not just the destination. - Lord Krishna",
    
    "Arjuna, remember that true happiness comes from within. In the Gita, I teach that one who has controlled the mind finds peace within - not in external objects or achievements. Cultivate inner stillness through meditation, devotion, and selfless service. As I state in Chapter 6, verse 7: 'For one who has conquered the mind, the mind is the best of friends; but for one who has failed to do so, the mind will remain the greatest enemy.' - Lord Krishna",
    
    "My dear friend, the path of dharma (righteousness) is not always easy, but it is always rewarding. When you align your actions with cosmic law and perform your duties without attachment to results, you honor the divine order. As I explained in the Gita, 'It is better to perform one's own duties imperfectly than to master the duties of another.' (18.47) Find your unique purpose and fulfill it with devotion. - Lord Krishna",
    
    "The mind can be your greatest ally or your worst enemy. Practice discipline through yoga and meditation to bring it under control. As I teach in the Bhagavad Gita, 'For him who has conquered the mind, the mind is the best of friends; but for one who has failed to do so, his very mind will be the greatest enemy.' (Chapter 6, Verse 6) With a disciplined mind, you'll find peace even amidst life's storms. - Lord Krishna",
    
    "Remember that your true self - the atman - is eternal and unchanging. As I revealed to Arjuna, 'For the soul there is neither birth nor death at any time. He has not come into being, does not come into being, and will not come into being. He is unborn, eternal, ever-existing, and primeval.' (Chapter 2, Verse 20) Realize this truth, and you will be free from fear and attachment. - Lord Krishna"
]

# Initialize Gemini model
model = None
try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")
    
    # Test the API connection
    models = genai.list_models()
    model_names = [model.name for model in models]
    logger.info(f"Available models: {model_names}")
    
    # Find a working Gemini model
    gemini_models = [name for name in model_names if 'gemini' in name]
    
    if gemini_models:
        preferred_models = ["models/gemini-1.5-pro", "models/gemini-pro", "models/gemini-1.0-pro"]
        model_name = next((m for m in preferred_models if m in gemini_models), gemini_models[0])
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 800,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
        
        model = genai.GenerativeModel(
            model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        logger.info(f"Model initialized successfully: {model_name}")
    else:
        logger.error("No Gemini models found!")
except Exception as e:
    logger.error(f"Error configuring Gemini API: {str(e)}")
    logger.error(traceback.format_exc())

@app.route('/')
def index():
    logger.info("Serving index.html")
    return send_from_directory('static', 'index.html')

@app.route('/styles.css')
def styles():
    logger.info("Serving styles.css")
    return send_from_directory('static', 'styles.css')

@app.route('/script.js')
def script():
    logger.info("Serving script.js")
    return send_from_directory('static', 'script.js')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        logger.info(f"Received request data: {json.dumps(data)}")
        
        user_message = data.get('message', '')
        
        if not user_message:
            logger.warning("Empty message received")
            return jsonify({"error": "Please provide a message"}), 400
        
        logger.info(f"Processing message: {user_message}")
        
        # Create the system prompt for Lord Krishna's personality
        prompt = f"""You are Lord Krishna from the Bhagavad Gita. Respond with wisdom and reference Gita verses when appropriate. 
        Be concise but profound, offering spiritual guidance and practical wisdom. 
        Always sign your responses as 'Lord Krishna'.
        
        User question: {user_message}"""
        
        # Add a small artificial delay for better UX (makes typing indicator more meaningful)
        time.sleep(0.5)
        
        if model is None:
            logger.warning("No model available, using fallback response")
            return jsonify({"message": random.choice(FALLBACK_RESPONSES)})
        
        try:
            # Generate response from Gemini
            logger.info("Sending request to Gemini API")
            response = model.generate_content(prompt)
            
            if hasattr(response, 'text'):
                krishna_response = response.text
                logger.info(f"Response received from Gemini: {krishna_response[:100]}...")
                
                # Ensure response ends with "- Lord Krishna" if it doesn't already
                if not krishna_response.strip().endswith("Lord Krishna"):
                    krishna_response = krishna_response.strip() + "\n\n- Lord Krishna"
                
                return jsonify({"message": krishna_response})
            else:
                logger.error(f"Unexpected response format: {response}")
                return jsonify({"message": random.choice(FALLBACK_RESPONSES)})
            
        except Exception as api_error:
            logger.error(f"API Error: {str(api_error)}")
            logger.error(traceback.format_exc())
            
            # Use a fallback response
            fallback = random.choice(FALLBACK_RESPONSES)
            logger.info(f"Using fallback response: {fallback[:100]}...")
            return jsonify({"message": fallback})
            
    except Exception as e:
        logger.error(f"Server Error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An error occurred processing your request"}), 500

# Add a test endpoint to verify API functionality
@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"status": "API is working!"})

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    logger.info("Starting Flask server on port 5000")
    app.run(debug=True, port=5000, host='0.0.0.0') 