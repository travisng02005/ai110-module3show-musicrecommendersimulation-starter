import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Relative importance of each feature. Weights are renormalized over the
# features a user actually specified, so unspecified targets cost nothing.
WEIGHTS = {
    "genre": 0.30,
    "mood": 0.20,
    "energy": 0.20,
    "valence": 0.10,
    "tempo": 0.0,  # not part of the recipe; kept so a tempo target is ignored, not a KeyError
    "danceability": 0.10,
    "acousticness": 0.10,
}

TEMPO_RANGE = 120.0  # roughly the 60-180 BPM span of the catalog

# Pairs that earn partial credit instead of an all-or-nothing genre/mood match.
RELATED_GENRES = {
    frozenset(p) for p in [
        ("pop", "indie pop"), ("pop", "edm"), ("lofi", "ambient"),
        ("lofi", "jazz"), ("ambient", "classical"), ("synthwave", "edm"),
        ("rock", "indie pop"), ("hip hop", "r&b"), ("jazz", "r&b"),
        ("folk", "indie pop"),
    ]
}
RELATED_MOODS = {
    frozenset(p) for p in [
        ("chill", "relaxed"), ("chill", "focused"), ("relaxed", "focused"),
        ("happy", "euphoric"), ("intense", "euphoric"), ("moody", "sad"),
        ("sad", "nostalgic"), ("nostalgic", "romantic"),
    ]
}
PARTIAL_CREDIT = 0.6


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

    The first four fields are the original profile. The optional fields widen
    it: lists of genres/moods, and targets for the remaining song features.
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    favorite_genres: Optional[List[str]] = None
    favorite_moods: Optional[List[str]] = None
    target_valence: Optional[float] = None
    target_tempo: Optional[float] = None
    target_danceability: Optional[float] = None
    target_acousticness: Optional[float] = None  # overrides likes_acoustic


def _proximity(value: float, target: float, scale: float = 1.0) -> float:
    """1.0 at the target, falling linearly with distance in either direction."""
    return max(0.0, 1.0 - abs(value - target) / scale)


def _category_match(value: str, favorites: List[str], related: set) -> float:
    """1.0 for an exact match, partial credit for a related value, else 0."""
    if value in favorites:
        return 1.0
    if any(frozenset((value, f)) in related for f in favorites):
        return PARTIAL_CREDIT
    return 0.0


def _favorites(prefs: Dict, plural: str, singular: str) -> List[str]:
    """Returns the user's preferred values as a list, from the plural key or else the singular one."""
    values = prefs.get(plural)
    if values:
        return list(values)
    single = prefs.get(singular)
    return [single] if single else []


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song from 0-1 against the user's preferences and returns (score, reasons)."""
    parts: List[Tuple[str, float, str]] = []  # (feature, 0-1 match, reason)

    genres = _favorites(user_prefs, "favorite_genres", "favorite_genre")
    if genres:
        m = _category_match(song["genre"], genres, RELATED_GENRES)
        label = "genre match" if m == 1.0 else "related genre"
        parts.append(("genre", m, f"{label} ({song['genre']})" if m else ""))

    moods = _favorites(user_prefs, "favorite_moods", "favorite_mood")
    if moods:
        m = _category_match(song["mood"], moods, RELATED_MOODS)
        label = "mood match" if m == 1.0 else "related mood"
        parts.append(("mood", m, f"{label} ({song['mood']})" if m else ""))

    target_acoustic = user_prefs.get("target_acousticness")
    if target_acoustic is None and "likes_acoustic" in user_prefs:
        target_acoustic = 0.8 if user_prefs["likes_acoustic"] else 0.2

    numeric = [
        ("energy", user_prefs.get("target_energy"), song["energy"], 1.0),
        ("valence", user_prefs.get("target_valence"), song["valence"], 1.0),
        ("danceability", user_prefs.get("target_danceability"), song["danceability"], 1.0),
        ("tempo", user_prefs.get("target_tempo"), song["tempo_bpm"], TEMPO_RANGE),
        ("acousticness", target_acoustic, song["acousticness"], 1.0),
    ]
    for name, target, value, scale in numeric:
        if target is None:
            continue
        m = _proximity(value, target, scale)
        parts.append((name, m, f"{name} close to target ({value:g} vs {target:g})" if m >= 0.8 else ""))

    total_weight = sum(WEIGHTS[name] for name, _, _ in parts)
    if total_weight == 0:
        return 0.0, ["no preferences specified"]

    score = sum(WEIGHTS[name] * m for name, m, _ in parts) / total_weight
    reasons = [r for _, _, r in parts if r]
    return score, reasons or ["weak match on every feature"]


def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs from a CSV file into a list of dicts with numeric fields cast to int/float."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in int_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song and returns the top k as (song, score, explanation), highest score first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    # Highest score first; ties broken by title so results are deterministic.
    scored.sort(key=lambda item: (-item[1], item[0]["title"]))
    return scored[:k]


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the k songs that best match the user's profile, highest score first."""
        prefs = asdict(user)
        ranked = sorted(
            self.songs,
            key=lambda s: (-score_song(prefs, asdict(s))[0], s.title),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a short string with the song's score and the reasons it matches the user."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)
