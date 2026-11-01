"""
Command line runner for the Music Recommender Simulation.

Loads the songs, then prints the top 5 recommendations for each test profile.
"""

from src.recommender import load_songs, recommend_songs

# normal profiles
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    # adversarial profiles, made to see if the scoring gets tricked
    "Sad but Energetic": {"genre": "pop", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    "Unknown Genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Conflicting Taste": {"genre": "classical", "mood": "aggressive", "energy": 0.95, "likes_acoustic": True},
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        print(f"User profile: {user_prefs}")
        print("\nTop recommendations:\n")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            # one reason per line so it's easy to read
            for reason in explanation.split("; "):
                print(f"   - {reason}")
            print()


if __name__ == "__main__":
    main()
