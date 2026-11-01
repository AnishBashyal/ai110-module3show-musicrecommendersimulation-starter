# 🎵 Music Recommender Simulation

## Project Summary

This project is a small music recommendation system, made to show how apps like spotify or tiktok guess what songs you'll like next. It's a simulation, so it runs on a tiny csv of songs instead of real data, and it runs in the terminal.

It's content based, meaning it looks at the songs themselves. It reads the songs from the csv, compares each one to a user's taste (genre, mood, energy, acousticness), gives it a score, and shows the top matches with reasons why.

---

## How The System Works

Real apps like spotify and youtube mostly use two things. One is collaborative filtering, which looks at what other people with similar taste liked (likes, skips, playlists). The other is content based, which looks at the song itself (genre, mood, tempo, energy). My version is only content based, since I dont have any other users. It just compares a song's features to what one user says they like, and gives it a score.

My version cares most about genre, then mood, then how close the energy is. I also look at acousticness a little.

**Song features:** genre, mood, energy, acousticness (the csv also has tempo, valence, danceability but I'm not scoring those)

**UserProfile features:** favorite genre, favorite mood, target energy, likes acoustic (yes/no)

### Algorithm Recipe

Every song in the csv gets a score, then I sort them and show the top K. Points for each song:

- genre matches: +2.0
- mood matches: +1.0
- energy closeness: up to +1.0, using `1 - |song energy - target energy|` (closer = more points, not just higher)
- acousticness closeness: up to +0.5 (goes toward 1.0 if user likes acoustic, toward 0.0 if not)

Max score is 4.5. Each point comes with a reason like "genre match (+2.0)" so you can see why a song was picked.

Flow: user prefs → loop over every song and score it → sort high to low → top K with reasons.

### Expected Biases

- Genre is worth the most, so it might push out songs that match the mood and energy but are a different genre. Gym Hero (intense pop) will probably keep showing up for pop users even if they want happy.
- Genre and mood need an exact match. "indie pop" gets nothing for a "pop" user even though its close.
- Profile only holds one genre and one mood, so someone who likes a mix gets ignored.
- Catalog is small (18 songs) and some genres only have 1 song, so results wont have much variety.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output for the default pop/happy profile (`python -m src.main`):

```
Loaded songs: 18

User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

1. Sunrise City by Neon Echo - Score: 4.39
   - genre match (+2.0)
   - mood match (+1.0)
   - energy close to 0.8 (+0.98)
   - acousticness fit (+0.41)

2. Gym Hero by Max Pulse - Score: 3.35
   - genre match (+2.0)
   - energy close to 0.8 (+0.87)
   - acousticness fit (+0.47)

3. Rooftop Lights by Indigo Parade - Score: 2.29
   - mood match (+1.0)
   - energy close to 0.8 (+0.96)
   - acousticness fit (+0.33)

4. Concrete Kings by Blockhead Sam - Score: 1.42
   - energy close to 0.8 (+0.98)
   - acousticness fit (+0.44)

5. Storm Runner by Voltline - Score: 1.34
   - energy close to 0.8 (+0.89)
   - acousticness fit (+0.45)
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



