from flask import Flask, request, jsonify, render_template
import boto3

app = Flask(__name__)
comprehend = boto3.client('comprehend', region_name='us-east-1')

# Mood to music mapping
mood_map = {
    "POSITIVE": ["Happy Pop", "Upbeat Indie", "Feel Good Classics"],
    "NEGATIVE": ["Calming Lo-fi", "Soft Piano", "Relaxing Instrumentals"],
    "NEUTRAL": ["Chill Vibes", "Coffeehouse Jazz", "Focus Beats"],
    "MIXED": ["Emotional Tracks", "Motivational Pop", "Mellow Vibes"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_mood', methods=['POST'])
def get_mood():
    user_text = request.form['text']
    response = comprehend.detect_sentiment(Text=user_text, LanguageCode='en')
    sentiment = response['Sentiment']
    music_suggestions = mood_map.get(sentiment.upper(), ["Lo-fi Beats", "Classical"])

    return jsonify({
        "sentiment": sentiment,
        "suggestions": music_suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)

