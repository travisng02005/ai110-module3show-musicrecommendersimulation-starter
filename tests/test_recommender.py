from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def _song_dict(**overrides):
    song = {
        "genre": "lofi", "mood": "chill", "energy": 0.4, "tempo_bpm": 80,
        "valence": 0.6, "danceability": 0.5, "acousticness": 0.9,
    }
    song.update(overrides)
    return song


def test_tempo_only_profile_still_ranks_by_tempo():
    from src.recommender import score_song
    prefs = {"target_tempo": 140}
    close, _ = score_song(prefs, _song_dict(tempo_bpm=138))
    far, _ = score_song(prefs, _song_dict(tempo_bpm=70))
    assert close > far > 0


def test_genre_and_mood_matching_ignores_case_and_whitespace():
    from src.recommender import score_song
    score, _ = score_song({"favorite_genres": [" Lofi"], "favorite_moods": ["CHILL"]}, _song_dict())
    assert score == 1.0


def test_out_of_range_targets_are_clamped():
    from src.recommender import score_song
    high, _ = score_song({"target_energy": 5.0}, _song_dict(energy=1.0))
    assert high == 1.0
    low, _ = score_song({"target_valence": -2}, _song_dict(valence=0.0))
    assert low == 1.0


def test_empty_profile_scores_zero_with_clear_reason():
    from src.recommender import score_song
    score, reasons = score_song({}, _song_dict())
    assert score == 0.0
    assert reasons == ["no preferences specified"]
