import google.generativeai as genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API Key
API_KEY = "AIzaSyAAqJGmXYragcD6SchBIsPvyVNJBQGmzBY"

def test_gemini_api():
    try:
        logger.info("Configuring Gemini API...")
        genai.configure(api_key=API_KEY)
        
        logger.info("Listing available models...")
        models = genai.list_models()
        model_names = [model.name for model in models]
        logger.info(f"Found {len(model_names)} models")
        
        # Filter for models that contain 'gemini' in their name
        gemini_models = [name for name in model_names if 'gemini' in name]
        logger.info(f"Found {len(gemini_models)} Gemini models: {gemini_models}")
        
        if not gemini_models:
            logger.error("No Gemini models found!")
            return
            
        # Use a specific model that we know works
        model_to_use = "models/gemini-1.5-pro"
        if model_to_use not in model_names:
            model_to_use = gemini_models[0]  # Just use the first one if our preferred model isn't available
            
        logger.info(f"Using model: {model_to_use}")
        
        # Set up the model
        model = genai.GenerativeModel(model_to_use)
        
        # Try generating a response
        test_prompt = "What is the meaning of life according to the Bhagavad Gita? Keep it short."
        logger.info(f"Sending test prompt: {test_prompt}")
        
        response = model.generate_content(test_prompt)
        logger.info(f"Response received: {response.text}")
        
        logger.info("Test completed successfully!")
        
    except Exception as e:
        logger.error(f"Error testing Gemini API: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    test_gemini_api() 