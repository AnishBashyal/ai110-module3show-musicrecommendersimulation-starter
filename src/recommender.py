import csv
from dataclasses import asdict, dataclass
from typing import List, Dict, Tuple, Optional

# points for each scoring rule (max score = sum of all four)
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this user, highest score first."""
        prefs = user_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in one line why this song scores the way it does."""
        _, reasons = score_song(user_to_prefs(user), asdict(song))
        return "; ".join(reasons)

def user_to_prefs(user: UserProfile) -> Dict:
    """Turn a UserProfile into the prefs dict that score_song uses."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, with numbers converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user prefs and return (score, reasons)."""
    score = 0.0
    reasons = []

    # genre match
    if song["genre"] == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    # mood match
    if song["mood"] == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")

    # energy: closer to the target = more points
    energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_points
    reasons.append(f"energy close to {user_prefs['energy']} (+{energy_points:.2f})")

    # acousticness: aim for 1.0 if the user likes acoustic, 0.0 if not
    if "likes_acoustic" in user_prefs:
        target = 1.0 if user_prefs["likes_acoustic"] else 0.0
        acoustic_points = ACOUSTIC_WEIGHT * (1 - abs(song["acousticness"] - target))
        score += acoustic_points
        reasons.append(f"acousticness fit (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation)."""
    # score every song, keeping the reasons as one readable string
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # sort by score (highest first) and keep the top k
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
