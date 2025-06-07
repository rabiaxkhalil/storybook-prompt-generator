import openai
import os
from dotenv import load_dotenv
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import textwrap
import re

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Download required NLTK data
nltk.download('vader_lexicon')

# Define emotional keywords
EMOTION_KEYWORDS = {
    'happy': ['happy', 'joy', 'wonderful', 'great', 'amazing', 'lovely', 'beautiful', 'excited'],
    'sad': ['sad', 'tired', 'overwhelmed', 'drained', 'challenging', 'difficult'],
    'nervous': ['nervous', 'anxious', 'worried', 'challenging', 'overwhelmed'],
    'excited': ['excited', 'wonderful', 'amazing', 'productive', 'successful', 'great']
}

def analyze_sentiment_keywords(text):
    """Analyze sentiment using keyword matching."""
    text = text.lower()
    emotions = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword in text)
        emotions[emotion] = count
    if emotions:
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        return dominant_emotion[0] if dominant_emotion[1] > 0 else "neutral"
    return "neutral"

def analyze_sentiment(text):
    """Analyze the sentiment of a given text using VADER."""
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    return scores

def get_emotional_tone(compound_score):
    """Convert compound sentiment score to emotional tone."""
    if compound_score >= 0.5:
        return "very positive"
    elif compound_score > 0:
        return "positive"
    elif compound_score >= -0.5:
        return "neutral"
    elif compound_score > -0.8:
        return "negative"
    else:
        return "very negative"

def generate_story_arc(entries):
    """Generate a 3-part children's story arc based on the week's entries."""
    # Analyze overall emotional progression
    sentiments = [analyze_sentiment(entry)['compound'] for entry in entries]
    keyword_emotions = [analyze_sentiment_keywords(entry) for entry in entries]
    
    # Count emotion frequencies
    emotion_counts = {}
    for emotion in keyword_emotions:
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    # Determine dominant emotions
    dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
    
    # Generate story based on emotional patterns
    if dominant_emotion == 'happy' or dominant_emotion == 'excited':
        story = {
            "beginning": "Once upon a time, in a magical forest, there lived a cheerful little rabbit named Hop. "
                        "Hop was known throughout the forest for their infectious laughter and kind heart. "
                        "Every morning, they would wake up with a big smile, ready to spread joy to all their friends.",
            
            "challenge": "One day, a dark cloud appeared over the forest, making all the animals feel gloomy. "
                        "The flowers stopped blooming, and the birds stopped singing. "
                        "Hop knew they had to do something to bring back the forest's happiness.",
            
            "resolution": "With determination and a heart full of hope, Hop organized a grand forest festival. "
                         "They invited all the animals to share their talents and stories. "
                         "As the music played and laughter filled the air, the dark cloud slowly disappeared. "
                         "The forest learned that together, they could overcome any sadness and create their own sunshine."
        }
    elif dominant_emotion == 'sad' or dominant_emotion == 'nervous':
        story = {
            "beginning": "In a quiet corner of the magical forest, there lived a thoughtful little rabbit named Hop. "
                        "Hop was known for being very careful and always thinking things through. "
                        "They loved their peaceful life but sometimes worried about trying new things.",
            
            "challenge": "One day, a great storm came to the forest, and many animals were scared and unsure. "
                        "The paths they knew so well were covered in fallen leaves, and everything seemed different. "
                        "Hop felt nervous but knew they had to be brave for their friends.",
            
            "resolution": "Taking a deep breath, Hop decided to lead the way. "
                         "They discovered that by working together and supporting each other, "
                         "they could find new paths and make the forest even better than before. "
                         "Hop learned that being brave doesn't mean not being afraid, but facing fears with friends by your side."
        }
    else:
        story = {
            "beginning": "In the heart of the magical forest, there lived a curious little rabbit named Hop. "
                        "Hop loved exploring and learning new things every day. "
                        "They believed that every day brought new opportunities to grow and discover.",
            
            "challenge": "One day, Hop noticed that the forest was changing. "
                        "Some animals were happy, some were sad, and others were unsure about what to do. "
                        "Hop wanted to help everyone find their way.",
            
            "resolution": "With patience and understanding, Hop listened to everyone's stories. "
                         "They learned that different feelings were part of being alive, "
                         "and that by sharing and caring for each other, "
                         "they could create a forest where everyone belonged."
        }
    
    return story

def rewrite_story_with_gpt4(story_arc):
    prompt = (
        "Rewrite the following children's story arc into a Pixar-style children's story, "
        "told in the first person from the child's perspective. Make it warm, emotional, and engaging.\n\n"
        f"Beginning: {story_arc['beginning']}\n"
        f"Challenge: {story_arc['challenge']}\n"
        f"Resolution: {story_arc['resolution']}\n\n"
        "Pixar-style story (first person):"
    )
    client = openai.OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

def generate_from_entries(entries):
    """Generate a story from a list of journal entries."""
    # Generate story arc
    story = generate_story_arc(entries)
    
    # Rewrite story in Pixar style
    pixar_story = rewrite_story_with_gpt4(story)
    
    # Create analysis and story text
    analysis_text = "=== Emotional Analysis ===\n\n"
    for idx, entry in enumerate(entries):
        sentiment = analyze_sentiment(entry)
        tone = get_emotional_tone(sentiment['compound'])
        keyword_emotion = analyze_sentiment_keywords(entry)
        analysis_text += f"Entry {idx + 1}:\n"
        analysis_text += f"VADER Emotional tone: {tone}\n"
        analysis_text += f"Keyword-based emotion: {keyword_emotion}\n"
        analysis_text += f"Sentiment score: {sentiment['compound']:.2f}\n\n"
    
    story_text = "\n=== Children's Story Arc ===\n\n"
    story_text += "The Beginning:\n"
    story_text += textwrap.fill(story['beginning'], width=80) + "\n\n"
    story_text += "The Challenge:\n"
    story_text += textwrap.fill(story['challenge'], width=80) + "\n\n"
    story_text += "The Resolution:\n"
    story_text += textwrap.fill(story['resolution'], width=80) + "\n\n"
    story_text += "\n=== Pixar-style Children's Story (First Person) ===\n\n"
    story_text += pixar_story + "\n"
    
    return analysis_text + story_text

def main():
    try:
        # Read the CSV file
        df = pd.read_csv('journal_entries.csv')
        
        # Ensure required columns exist
        if not all(col in df.columns for col in ['date', 'entry_text']):
            raise ValueError("CSV must contain 'date' and 'entry_text' columns")
        
        # Process entries
        entries = df['entry_text'].tolist()
        
        # Generate story using the new function
        story_text = generate_from_entries(entries)
        
        # Write results to output file
        with open('weekly_story.txt', 'w') as f:
            f.write(story_text)
            
        print("Story generation complete! Check 'weekly_story.txt' for results.")
        
    except FileNotFoundError:
        print("Error: journal_entries.csv not found. Please ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
