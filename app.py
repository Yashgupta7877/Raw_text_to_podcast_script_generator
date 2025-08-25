# # app.py
# import requests
# import google.generativeai as genai
# from flask import Flask, render_template, request, redirect, url_for, flash
#
# app = Flask(__name__)
# app.secret_key = 'supersecretkey'
#
# # --- API Key Configuration ---
# # This is the corrected section with your API keys placed directly.
# GOOGLE_API_KEY = "AIzaSyBNpO8tTZ80lZNdX0r86rPLPHQaqZCnQWk"
# GNEWS_API_KEY = "270c4d3b050ef683e0e49faefef74bf9"
#
# # --- Model Initialization ---
# try:
#     if not GOOGLE_API_KEY or "PASTE" in GOOGLE_API_KEY:
#          raise ValueError("Google API key is missing or is a placeholder.")
#     if not GNEWS_API_KEY or "PASTE" in GNEWS_API_KEY:
#         raise ValueError("GNews API key is missing or is a placeholder.")
#
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     print("Successfully configured Gemini model.")
#
# except (ValueError, KeyError) as e:
#     print(f"API Configuration Error: {e}")
#     model = None
#
#
# def fetch_ai_news():
#     """Fetches the top 5 AI news articles from the GNews API."""
#     if not GNEWS_API_KEY:
#         return None, "GNews API key is not configured."
#
#     url = f"https://gnews.io/api/v4/search?q=AI&lang=en&max=5&token={GNEWS_API_KEY}"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         return data.get("articles", []), None
#     except requests.exceptions.RequestException as e:
#         return None, f"Error fetching news from GNews API: {e}"
#     except Exception as e:
#         return None, f"An unexpected error occurred: {e}"
#
#
# def generate_podcast_script(raw_text):
#     """Generates a podcast script from raw text using the Gemini API."""
#     if not model:
#         return None, "Gemini API is not configured. Check your API key."
#
#     if not raw_text or not raw_text.strip():
#         return None, "The provided news content was empty."
#
#     prompt = f"""
#     You are an expert podcast scriptwriter, known for creating engaging and professional content.
#     Your task is to transform the following raw news text into a polished and captivating podcast script.
#
#     The script must include:
#     1.  An engaging introduction that hooks the listener and introduces the topic of today's AI news.
#     2.  Smooth and clear transitions between each news segment.
#     3.  A strong and memorable outro that summarizes the main points and includes a clear call to action (e.g., "subscribe," "follow us on social media").
#     4.  A bulleted list of three key takeaways or show notes from the content.
#
#     Please use only the provided raw transcript to generate the script. Do not add any external information.
#
#     Raw Transcript:
#     {raw_text}
#
#     Polished Podcast Script:
#     """
#     try:
#         response = model.generate_content(prompt)
#         return response.text, None
#     except Exception as e:
#         return None, f"Error generating script with Gemini API: {e}"
#
#
# @app.route('/', methods=['GET'])
# def index():
#     """This function connects to index.html and renders it."""
#     return render_template('index.html')
#
#
# @app.route('/generate-script', methods=['POST'])
# def generate_script():
#     """Fetches news and generates the podcast script."""
#     if not model:
#         flash("The Gemini model is not configured. Please check your API keys in app.py.", 'danger')
#         return redirect(url_for('index'))
#
#     articles, error = fetch_ai_news()
#
#     if error:
#         flash(error, 'danger')
#         return redirect(url_for('index'))
#
#     if not articles:
#         flash("No articles were found for the topic 'AI'.", 'warning')
#         return redirect(url_for('index'))
#
#     articles_text = [f"Title: {a.get('title', 'N/A')}. Description: {a.get('description', 'N/A')}" for a in articles]
#     raw_text = " ".join(articles_text)
#
#     script, error = generate_podcast_script(raw_text)
#
#     if error:
#         flash(error, 'danger')
#         return redirect(url_for('index'))
#
#     return render_template('index.html', script=script, articles=articles)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
# app.py
import requests
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# --- API Key Configuration ---
# Your API keys are placed directly here for simplicity.
GOOGLE_API_KEY = "AIzaSyBNpO8tTZ80lZNdX0r86rPLPHQaqZCnQWk"

# --- Model Initialization ---
try:
    if not GOOGLE_API_KEY or "PASTE" in GOOGLE_API_KEY:
         raise ValueError("Google API key is missing or is a placeholder.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Successfully configured Gemini model.")

except (ValueError, KeyError) as e:
    print(f"API Configuration Error: {e}")
    model = None


def generate_podcast_script(raw_text):
    """Generates a podcast script from the user's raw text."""
    if not model:
        return None, "Gemini API is not configured. Check your API key."

    prompt = f"""
    You are an expert podcast scriptwriter, known for creating engaging and professional content.
    Your task is to transform the following raw text into a polished and captivating podcast script.

    The script must include:
    1.  An engaging introduction that hooks the listener and introduces the topic.
    2.  Smooth and clear transitions if there are multiple points.
    3.  A strong and memorable outro that summarizes the main points and includes a clear call to action (e.g., "subscribe," "follow us on social media").
    4.  A bulleted list of three key takeaways or show notes from the content.

    Please use only the provided raw transcript to generate the script. Do not add any external information.

    Raw Transcript:
    {raw_text}

    Polished Podcast Script:
    """
    try:
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"Error generating script with Gemini API: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles both displaying the page and generating the script from user input."""
    script = None
    raw_text_input = ""

    if request.method == 'POST':
        raw_text_input = request.form.get('raw_text')

        if not raw_text_input or not raw_text_input.strip():
            flash("Please paste some text into the box before generating a script.", 'warning')
            return render_template('index.html', script=None, raw_text=raw_text_input)

        if not model:
            flash("The Gemini model is not configured. Please check your API key in app.py.", 'danger')
            return render_template('index.html', script=None, raw_text=raw_text_input)

        script, error = generate_podcast_script(raw_text_input)

        if error:
            flash(error, 'danger')
            return render_template('index.html', script=None, raw_text=raw_text_input)

    return render_template('index.html', script=script, raw_text=raw_text_input)


if __name__ == '__main__':
    app.run(debug=True)



# import os
# import requests
# import google.generativeai as genai
# from flask import Flask, render_template, request, redirect, url_for, flash

# app = Flask(__name__)
# app.secret_key = 'supersecretkey'

# # --- API Key Configuration (from Environment Variable) ---
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")   # ✅ Now read from environment

# # --- Model Initialization ---
# try:
#     if not GOOGLE_API_KEY:
#         raise ValueError("Google API key is missing. Please set GOOGLE_API_KEY in your environment variables.")

#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     print("✅ Successfully configured Gemini model.")

# except (ValueError, KeyError) as e:
#     print(f"❌ API Configuration Error: {e}")
#     model = None


# def generate_podcast_script(raw_text):
#     """Generates a podcast script from the user's raw text."""
#     if not model:
#         return None, "Gemini API is not configured. Check your API key."

#     prompt = f"""
#     You are an expert podcast scriptwriter, known for creating engaging and professional content.
#     Your task is to transform the following raw text into a polished and captivating podcast script.

#     The script must include:
#     1.  An engaging introduction that hooks the listener and introduces the topic.
#     2.  Smooth and clear transitions if there are multiple points.
#     3.  A strong and memorable outro that summarizes the main points and includes a clear call to action (e.g., "subscribe," "follow us on social media").
#     4.  A bulleted list of three key takeaways or show notes from the content.

#     Please use only the provided raw transcript to generate the script. Do not add any external information.

#     Raw Transcript:
#     {raw_text}

#     Polished Podcast Script:
#     """
#     try:
#         response = model.generate_content(prompt)
#         return response.text, None
#     except Exception as e:
#         return None, f"Error generating script with Gemini API: {e}"


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     """Handles both displaying the page and generating the script from user input."""
#     script = None
#     raw_text_input = ""

#     if request.method == 'POST':
#         raw_text_input = request.form.get('raw_text')

#         if not raw_text_input or not raw_text_input.strip():
#             flash("Please paste some text into the box before generating a script.", 'warning')
#             return render_template('index.html', script=None, raw_text=raw_text_input)

#         if not model:
#             flash("The Gemini model is not configured. Please check your API key.", 'danger')
#             return render_template('index.html', script=None, raw_text=raw_text_input)

#         script, error = generate_podcast_script(raw_text_input)

#         if error:
#             flash(error, 'danger')
#             return render_template('index.html', script=None, raw_text=raw_text_input)

#     return render_template('index.html', script=script, raw_text=raw_text_input)


# if __name__ == '__main__':
#     app.run(debug=True)