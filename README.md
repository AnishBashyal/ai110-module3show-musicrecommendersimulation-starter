# 🎵 Music Recommender Simulation

## Project Summary

This project is a small music recommendation system, made to show how apps like spotify or tiktok guess what songs you'll like next. It's a simulation, so it runs on a tiny csv of songs instead of real data, and it runs in the terminal.

It's content based, meaning it looks at the songs themselves. It reads the songs from the csv, compares each one to a user's taste (genre, mood, energy, acousticness), gives it a score, and shows the top matches with reasons why.

---

## How The System Works

Real apps like spotify and youtube use a lot of data. They look at what you do (likes, skips, replays, playlists, listening history) and at the songs themselves (genre, mood, tempo, energy). There are two main ways to use it. Collaborative filtering says "people with a similar history liked this, so you might too". Content based says "this song's features are close to songs you like". My version is only content based, since I dont have any other users.

How my version splits it up:

- **Input data:** the songs in the csv and their features.
- **User preferences:** one taste profile (favorite genre, favorite mood, target energy, likes acoustic).
- **Ranking:** score every song against the profile, sort high to low, show the top K.

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
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run all the tests with:

```bash
pytest
```

There are 23 tests in two files:

- `tests/test_functions.py`: unit tests for `load_songs`, `score_song` and `recommend_songs` (each scoring rule, sorting, k, reasons), plus a few simple end to end checks with the real csv.
- `tests/test_recommender.py`: tests for the `Recommender` class (ranking and explanations).

---

## Sample Recommendation Output

Results print as a table (made with `tabulate`) with the reasons for each score in the last column. Output for the High-Energy Pop profile (`python -m src.main`):

```
Loaded songs: 18

=== High-Energy Pop ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

+-----+----------------+---------------+---------+-----------------------------+
|   # | Song           | Artist        |   Score | Why                         |
+=====+================+===============+=========+=============================+
|   1 | Sunrise City   | Neon Echo     |    4.39 | genre match (+2.0)          |
|     |                |               |         | mood match (+1.0)           |
|     |                |               |         | energy close to 0.8 (+0.98) |
|     |                |               |         | acousticness fit (+0.41)    |
+-----+----------------+---------------+---------+-----------------------------+
|   2 | Gym Hero       | Max Pulse     |    3.35 | genre match (+2.0)          |
|     |                |               |         | energy close to 0.8 (+0.87) |
|     |                |               |         | acousticness fit (+0.47)    |
+-----+----------------+---------------+---------+-----------------------------+
|   3 | Rooftop Lights | Indigo Parade |    2.29 | mood match (+1.0)           |
|     |                |               |         | energy close to 0.8 (+0.96) |
|     |                |               |         | acousticness fit (+0.33)    |
+-----+----------------+---------------+---------+-----------------------------+
|   4 | Concrete Kings | Blockhead Sam |    1.42 | energy close to 0.8 (+0.98) |
|     |                |               |         | acousticness fit (+0.44)    |
+-----+----------------+---------------+---------+-----------------------------+
|   5 | Storm Runner   | Voltline      |    1.34 | energy close to 0.8 (+0.89) |
|     |                |               |         | acousticness fit (+0.45)    |
+-----+----------------+---------------+---------+-----------------------------+
```

---

## Profile Test Outputs

Top 5 for each test profile (`python -m src.main` runs all of them). The first three are normal profiles, the last three are adversarial ones made to try to trick the scoring. My comments comparing each pair of profiles are in section 7 of the [model card](model_card.md).

### High-Energy Pop

```
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

+-----+----------------+---------------+---------+-----------------------------+
|   # | Song           | Artist        |   Score | Why                         |
+=====+================+===============+=========+=============================+
|   1 | Sunrise City   | Neon Echo     |    4.39 | genre match (+2.0)          |
|     |                |               |         | mood match (+1.0)           |
|     |                |               |         | energy close to 0.8 (+0.98) |
|     |                |               |         | acousticness fit (+0.41)    |
+-----+----------------+---------------+---------+-----------------------------+
|   2 | Gym Hero       | Max Pulse     |    3.35 | genre match (+2.0)          |
|     |                |               |         | energy close to 0.8 (+0.87) |
|     |                |               |         | acousticness fit (+0.47)    |
+-----+----------------+---------------+---------+-----------------------------+
|   3 | Rooftop Lights | Indigo Parade |    2.29 | mood match (+1.0)           |
|     |                |               |         | energy close to 0.8 (+0.96) |
|     |                |               |         | acousticness fit (+0.33)    |
+-----+----------------+---------------+---------+-----------------------------+
|   4 | Concrete Kings | Blockhead Sam |    1.42 | energy close to 0.8 (+0.98) |
|     |                |               |         | acousticness fit (+0.44)    |
+-----+----------------+---------------+---------+-----------------------------+
|   5 | Storm Runner   | Voltline      |    1.34 | energy close to 0.8 (+0.89) |
|     |                |               |         | acousticness fit (+0.45)    |
+-----+----------------+---------------+---------+-----------------------------+
```

### Chill Lofi

```
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}

Top recommendations:

+-----+---------------------+----------------+---------+------------------------------+
|   # | Song                | Artist         |   Score | Why                          |
+=====+=====================+================+=========+==============================+
|   1 | Library Rain        | Paper Lanterns |    4.43 | genre match (+2.0)           |
|     |                     |                |         | mood match (+1.0)            |
|     |                     |                |         | energy close to 0.35 (+1.00) |
|     |                     |                |         | acousticness fit (+0.43)     |
+-----+---------------------+----------------+---------+------------------------------+
|   2 | Midnight Coding     | LoRoom         |    4.29 | genre match (+2.0)           |
|     |                     |                |         | mood match (+1.0)            |
|     |                     |                |         | energy close to 0.35 (+0.93) |
|     |                     |                |         | acousticness fit (+0.35)     |
+-----+---------------------+----------------+---------+------------------------------+
|   3 | Focus Flow          | LoRoom         |    3.34 | genre match (+2.0)           |
|     |                     |                |         | energy close to 0.35 (+0.95) |
|     |                     |                |         | acousticness fit (+0.39)     |
+-----+---------------------+----------------+---------+------------------------------+
|   4 | Spacewalk Thoughts  | Orbit Bloom    |    2.39 | mood match (+1.0)            |
|     |                     |                |         | energy close to 0.35 (+0.93) |
|     |                     |                |         | acousticness fit (+0.46)     |
+-----+---------------------+----------------+---------+------------------------------+
|   5 | Coffee Shop Stories | Slow Stereo    |    1.43 | energy close to 0.35 (+0.98) |
|     |                     |                |         | acousticness fit (+0.45)     |
+-----+---------------------+----------------+---------+------------------------------+
```

### Deep Intense Rock

```
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}

Top recommendations:

+-----+----------------+-----------------+---------+------------------------------+
|   # | Song           | Artist          |   Score | Why                          |
+=====+================+=================+=========+==============================+
|   1 | Storm Runner   | Voltline        |    4.44 | genre match (+2.0)           |
|     |                |                 |         | mood match (+1.0)            |
|     |                |                 |         | energy close to 0.92 (+0.99) |
|     |                |                 |         | acousticness fit (+0.45)     |
+-----+----------------+-----------------+---------+------------------------------+
|   2 | Gym Hero       | Max Pulse       |    2.46 | mood match (+1.0)            |
|     |                |                 |         | energy close to 0.92 (+0.99) |
|     |                |                 |         | acousticness fit (+0.47)     |
+-----+----------------+-----------------+---------+------------------------------+
|   3 | Neon Overdrive | Pulse Theory    |    1.45 | energy close to 0.92 (+0.96) |
|     |                |                 |         | acousticness fit (+0.48)     |
+-----+----------------+-----------------+---------+------------------------------+
|   4 | Iron Requiem   | Black Cathedral |    1.42 | energy close to 0.92 (+0.94) |
|     |                |                 |         | acousticness fit (+0.48)     |
+-----+----------------+-----------------+---------+------------------------------+
|   5 | Sunrise City   | Neon Echo       |    1.31 | energy close to 0.92 (+0.90) |
|     |                |                 |         | acousticness fit (+0.41)     |
+-----+----------------+-----------------+---------+------------------------------+
```

### Sad but Energetic

```
User profile: {'genre': 'pop', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

+-----+----------------+-----------------+---------+-----------------------------+
|   # | Song           | Artist          |   Score | Why                         |
+=====+================+=================+=========+=============================+
|   1 | Gym Hero       | Max Pulse       |    3.44 | genre match (+2.0)          |
|     |                |                 |         | energy close to 0.9 (+0.97) |
|     |                |                 |         | acousticness fit (+0.47)    |
+-----+----------------+-----------------+---------+-----------------------------+
|   2 | Sunrise City   | Neon Echo       |    3.33 | genre match (+2.0)          |
|     |                |                 |         | energy close to 0.9 (+0.92) |
|     |                |                 |         | acousticness fit (+0.41)    |
+-----+----------------+-----------------+---------+-----------------------------+
|   3 | Storm Runner   | Voltline        |    1.44 | energy close to 0.9 (+0.99) |
|     |                |                 |         | acousticness fit (+0.45)    |
+-----+----------------+-----------------+---------+-----------------------------+
|   4 | Neon Overdrive | Pulse Theory    |    1.43 | energy close to 0.9 (+0.94) |
|     |                |                 |         | acousticness fit (+0.48)    |
+-----+----------------+-----------------+---------+-----------------------------+
|   5 | Iron Requiem   | Black Cathedral |    1.40 | energy close to 0.9 (+0.92) |
|     |                |                 |         | acousticness fit (+0.48)    |
+-----+----------------+-----------------+---------+-----------------------------+
```

### Unknown Genre (k-pop)

```
User profile: {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

Top recommendations:

+-----+----------------+---------------+---------+-----------------------------+
|   # | Song           | Artist        |   Score | Why                         |
+=====+================+===============+=========+=============================+
|   1 | Sunrise City   | Neon Echo     |    2.39 | mood match (+1.0)           |
|     |                |               |         | energy close to 0.8 (+0.98) |
|     |                |               |         | acousticness fit (+0.41)    |
+-----+----------------+---------------+---------+-----------------------------+
|   2 | Rooftop Lights | Indigo Parade |    2.29 | mood match (+1.0)           |
|     |                |               |         | energy close to 0.8 (+0.96) |
|     |                |               |         | acousticness fit (+0.33)    |
+-----+----------------+---------------+---------+-----------------------------+
|   3 | Concrete Kings | Blockhead Sam |    1.42 | energy close to 0.8 (+0.98) |
|     |                |               |         | acousticness fit (+0.44)    |
+-----+----------------+---------------+---------+-----------------------------+
|   4 | Gym Hero       | Max Pulse     |    1.34 | energy close to 0.8 (+0.87) |
|     |                |               |         | acousticness fit (+0.47)    |
+-----+----------------+---------------+---------+-----------------------------+
|   5 | Storm Runner   | Voltline      |    1.34 | energy close to 0.8 (+0.89) |
|     |                |               |         | acousticness fit (+0.45)    |
+-----+----------------+---------------+---------+-----------------------------+
```

### Conflicting Taste

```
User profile: {'genre': 'classical', 'mood': 'aggressive', 'energy': 0.95, 'likes_acoustic': True}

Top recommendations:

+-----+----------------------+-----------------+---------+------------------------------+
|   # | Song                 | Artist          |   Score | Why                          |
+=====+======================+=================+=========+==============================+
|   1 | Moonlit Sonata Redux | Elise Varga     |    2.71 | genre match (+2.0)           |
|     |                      |                 |         | energy close to 0.95 (+0.23) |
|     |                      |                 |         | acousticness fit (+0.48)     |
+-----+----------------------+-----------------+---------+------------------------------+
|   2 | Iron Requiem         | Black Cathedral |    1.99 | mood match (+1.0)            |
|     |                      |                 |         | energy close to 0.95 (+0.97) |
|     |                      |                 |         | acousticness fit (+0.02)     |
+-----+----------------------+-----------------+---------+------------------------------+
|   3 | Storm Runner         | Voltline        |    1.01 | energy close to 0.95 (+0.96) |
|     |                      |                 |         | acousticness fit (+0.05)     |
+-----+----------------------+-----------------+---------+------------------------------+
|   4 | Gym Hero             | Max Pulse       |    1.01 | energy close to 0.95 (+0.98) |
|     |                      |                 |         | acousticness fit (+0.03)     |
+-----+----------------------+-----------------+---------+------------------------------+
|   5 | Neon Overdrive       | Pulse Theory    |    1.00 | energy close to 0.95 (+0.99) |
|     |                      |                 |         | acousticness fit (+0.02)     |
+-----+----------------------+-----------------+---------+------------------------------+
```

---

## Experiments You Tried

### Weight shift: energy x2, genre x0.5

I changed energy from 1.0 to 2.0 and genre from 2.0 to 1.0, then ran all 6 profiles. Max score stays 4.5 so the math is still fine. After testing I put the weights back to the original.

What happened:

- #1 song stayed the same for 5 out of 6 profiles. Strong matches (genre + mood + energy) win either way.
- High-Energy Pop: Rooftop Lights (indie pop, happy) moved above Gym Hero (intense pop). I think this is better, since the user wants happy.
- Deep Intense Rock: Gym Hero is still #2 and Iron Requiem (metal) is still #4. The problem there is mood words not matching ("intense" vs "aggressive"), so changing weights didnt fix it.
- Conflicting Taste: the classical song dropped from #1 to #5 and Iron Requiem took #1, because energy now matters more than genre.
- Scores in the middle of the list went up and got closer together (like Concrete Kings 1.42 to 2.40), so the lower picks are less clearly separated.

So the change was mostly just different, not more accurate. It helped happy pop a bit but made the conflicting profile lean fully on energy.

---

## Limitations and Risks

- Tiny catalog: 18 songs, and 13 of the 15 genres have only one song, so the lists dont have much variety.
- Energy gives points to every song, so a few high energy songs (Gym Hero, Storm Runner) show up for almost everyone. Gym Hero was in 5 of 6 test lists.
- Genre and mood need an exact match, so "intense" and "aggressive" count as totally different, and a mood that isnt in the catalog (like "sad") is just ignored.
- A profile only holds one genre and one mood, so mixed taste isnt possible.
- It doesnt understand lyrics, language, or what other people listen to.

More detail in the [model card](model_card.md).

---

## Reflection

A recommender turns data into predictions by comparing numbers and labels. My version just adds up points for matching genre, mood, energy and acousticness, then sorts. That simple idea still felt like a real recommender, because the reasons next to each song showed why it ranked where it did.

Bias showed up in places I didnt expect. The tiny catalog meant the same few songs kept appearing, and the exact word matching meant a close mood still got zero points. In a real app the same thing could happen at a bigger scale, where popular songs or big genres get pushed to everyone and smaller ones never get heard. Full reflection is in the [model card](model_card.md).



