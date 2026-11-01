import pytest

from src.recommender import load_songs, score_song, recommend_songs

# a fixed song so the unit tests dont depend on the csv
SONG = {
    "id": 1, "title": "Test Song", "artist": "Test Artist",
    "genre": "pop", "mood": "happy", "energy": 0.8,
    "tempo_bpm": 120.0, "valence": 0.8, "danceability": 0.8, "acousticness": 0.0,
}

# matches SONG on everything
PERFECT = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}


# ---------- unit tests: load_songs ----------

def test_load_songs_loads_all_rows():
    assert len(load_songs("data/songs.csv")) == 18


def test_load_songs_converts_numbers():
    song = load_songs("data/songs.csv")[0]
    assert isinstance(song["id"], int)
    assert isinstance(song["energy"], float)
    assert isinstance(song["tempo_bpm"], float)
    assert isinstance(song["title"], str)


# ---------- unit tests: score_song ----------

def test_score_song_perfect_match_is_max_score():
    score, _ = score_song(PERFECT, SONG)
    assert score == pytest.approx(4.5)


def test_score_song_genre_match_adds_2_points():
    other = {**PERFECT, "genre": "rock"}
    match, _ = score_song(PERFECT, SONG)
    no_match, _ = score_song(other, SONG)
    assert match - no_match == pytest.approx(2.0)


def test_score_song_mood_match_adds_1_point():
    other = {**PERFECT, "mood": "sad"}
    match, _ = score_song(PERFECT, SONG)
    no_match, _ = score_song(other, SONG)
    assert match - no_match == pytest.approx(1.0)


def test_score_song_closer_energy_scores_higher():
    close, _ = score_song({**PERFECT, "energy": 0.75}, SONG)
    far, _ = score_song({**PERFECT, "energy": 0.2}, SONG)
    assert close > far


def test_score_song_energy_is_about_closeness_not_high_or_low():
    # a gap of 0.2 above or below should be worth the same
    above, _ = score_song({**PERFECT, "energy": 1.0}, SONG)
    below, _ = score_song({**PERFECT, "energy": 0.6}, SONG)
    assert above == pytest.approx(below)


def test_score_song_acoustic_preference_flips_points():
    likes, _ = score_song({**PERFECT, "likes_acoustic": True}, SONG)
    dislikes, _ = score_song({**PERFECT, "likes_acoustic": False}, SONG)
    # SONG has acousticness 0.0 so the "dislikes" user should score higher
    assert dislikes > likes


def test_score_song_skips_acoustic_if_not_in_prefs():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    score, reasons = score_song(prefs, SONG)
    assert score == pytest.approx(4.0)
    assert not any("acousticness" in r for r in reasons)


def test_score_song_returns_reasons():
    _, reasons = score_song(PERFECT, SONG)
    assert "genre match (+2.0)" in reasons
    assert "mood match (+1.0)" in reasons
    assert len(reasons) == 4


def test_score_song_no_genre_reason_when_genre_differs():
    _, reasons = score_song({**PERFECT, "genre": "rock"}, SONG)
    assert not any("genre match" in r for r in reasons)


# ---------- unit tests: recommend_songs ----------

def test_recommend_songs_returns_k_results():
    songs = load_songs("data/songs.csv")
    assert len(recommend_songs(PERFECT, songs, k=3)) == 3


def test_recommend_songs_k_bigger_than_catalog():
    songs = load_songs("data/songs.csv")
    assert len(recommend_songs(PERFECT, songs, k=100)) == 18


def test_recommend_songs_sorted_highest_first():
    songs = load_songs("data/songs.csv")
    scores = [score for _, score, _ in recommend_songs(PERFECT, songs, k=10)]
    assert scores == sorted(scores, reverse=True)


def test_recommend_songs_result_shape():
    songs = load_songs("data/songs.csv")
    song, score, explanation = recommend_songs(PERFECT, songs, k=1)[0]
    assert isinstance(song, dict)
    assert isinstance(score, float)
    assert isinstance(explanation, str) and explanation != ""


def test_recommend_songs_does_not_change_input_list():
    songs = load_songs("data/songs.csv")
    order_before = [s["id"] for s in songs]
    recommend_songs(PERFECT, songs, k=5)
    assert [s["id"] for s in songs] == order_before


# ---------- simple end to end tests (real csv, real profiles) ----------

def test_pop_happy_user_gets_sunrise_city_first():
    songs = load_songs("data/songs.csv")
    top = recommend_songs(PERFECT | {"energy": 0.8}, songs, k=1)[0][0]
    assert top["title"] == "Sunrise City"


def test_chill_lofi_user_gets_lofi_first():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}
    top = recommend_songs(prefs, songs, k=1)[0][0]
    assert top["genre"] == "lofi"


def test_unknown_genre_does_not_crash():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "k-pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    assert len(recommend_songs(prefs, songs, k=5)) == 5
