"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "Chill study (lofi/ambient/jazz)": {
        "favorite_genres": ["lofi", "ambient"],
        "favorite_moods": ["chill", "focused"],
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_tempo": 80,
        "target_acousticness": 0.80,
    },
    "Intense workout (rock + pop)": {
        "favorite_genres": ["rock", "pop"],
        "favorite_moods": ["intense"],
        "target_energy": 0.92,
        "target_tempo": 140,
        "target_danceability": 0.80,
        "target_acousticness": 0.10,
    },
    "Rainy-day wind down (folk/classical)": {
        "favorite_genres": ["folk", "classical"],
        "favorite_moods": ["nostalgic", "sad"],
        "target_energy": 0.30,
        "target_valence": 0.40,
        "target_acousticness": 0.92,
    },
}


PROFILE_LABELS = {
    "favorite_genres": "Genres",
    "favorite_moods": "Moods",
    "target_energy": "Energy",
    "target_valence": "Valence",
    "target_danceability": "Danceability",
    "target_acousticness": "Acousticness",
    "target_tempo": "Tempo",
}


def print_profile(name: str, user_prefs: dict) -> None:
    print(f"\n{'=' * 60}")
    print(f"USER PROFILE: {name}")
    print("=" * 60)
    for key, label in PROFILE_LABELS.items():
        value = user_prefs.get(key)
        if value is None:
            continue
        shown = ", ".join(value) if isinstance(value, list) else f"{value:g}"
        print(f"  {label:<14}{shown}")


def print_recommendations(recommendations: list) -> None:
    print(f"\nTOP {len(recommendations)} RECOMMENDATIONS")
    print("-" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']}")
        print(f"   {song['genre']} / {song['mood']}   Score: {score:.2f}")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        print_profile(name, user_prefs)
        print_recommendations(recommend_songs(user_prefs, songs, k=5))


if __name__ == "__main__":
    main()
