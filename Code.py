import time
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore

init(autoreset=True)


# Load movie information
try:
    movies = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "Sorry, the movie database file could not be found.")
    raise SystemExit


# Get all available genres
genre_list = sorted({
    genre.strip()
    for values in movies["Genre"].dropna().str.split(", ")
    for genre in values
})


def loading_animation():
    for _ in range(3):
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)
    print()


def analyze_sentiment(value):
    if value > 0:
        return "Positive 😊"
    elif value < 0:
        return "Negative 😞"
    else:
        return "Neutral 😐"


def choose_genre():
    print(Fore.GREEN + "\nAvailable movie genres:")

    for number, genre in enumerate(genre_list, 1):
        print(Fore.CYAN + f"{number}. {genre}")

    while True:
        choice = input(
            Fore.YELLOW + "\nSelect a genre by number or name: "
        ).strip()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(genre_list):
                return genre_list[number - 1]

        else:
            for genre in genre_list:
                if choice.lower() == genre.lower():
                    return genre

        print(Fore.RED + "That genre isn't available. Please try again.")


def choose_rating():
    while True:
        value = input(
            Fore.YELLOW +
            "Enter the minimum IMDb rating (7.6-9.3), or type 'skip': "
        ).strip()

        if value.lower() == "skip":
            return None

        try:
            rating = float(value)

            if 7.6 <= rating <= 9.3:
                return rating

            print(
                Fore.RED +
                "Please enter a rating between 7.6 and 9.3."
            )

        except ValueError:
            print(Fore.RED + "Please enter a valid rating.")


def find_movies(selected_genre, minimum_rating, number_of_movies=5):
    filtered = movies.copy()

    # Filter according to genre
    filtered = filtered[
        filtered["Genre"].str.contains(
            selected_genre,
            case=False,
            na=False
        )
    ]

    # Filter according to IMDb rating
    if minimum_rating is not None:
        filtered = filtered[
            filtered["IMDB_Rating"] >= minimum_rating
        ]

    if filtered.empty:
        return []

    # Shuffle the results so recommendations can vary
    filtered = filtered.sample(
        frac=1
    ).reset_index(drop=True)

    results = []

    for _, movie in filtered.iterrows():

        description = movie.get("Overview")

        if pd.isna(description):
            continue

        # Analyze the movie description
        sentiment_score = TextBlob(
            description
        ).sentiment.polarity

        results.append({
            "title": movie["Series_Title"],
            "rating": movie["IMDB_Rating"],
            "sentiment": sentiment_score
        })

        if len(results) == number_of_movies:
            break

    return results


def display_movies(movie_list, user_name):
    print(
        Fore.YELLOW +
        f"\n🍿 AI Movie Recommendations for {user_name}"
    )
    print(Fore.YELLOW + "-" * 50)

    for index, movie in enumerate(movie_list, 1):
        feeling = analyze_sentiment(movie["sentiment"])

        print(
            Fore.CYAN +
            f"{index}. 🎬 {movie['title']}"
        )

        print(
            f"   IMDb Rating: {movie['rating']}"
        )

        print(
            f"   Description Mood: {feeling} "
            f"(Polarity: {movie['sentiment']:.2f})"
        )

        print()


# ---------------- MAIN PROGRAM ----------------

print(
    Fore.BLUE +
    "\n🎥 Welcome to the AI Movie Recommendation Assistant! 🎥\n"
)

user_name = input(
    Fore.YELLOW + "What is your name? "
).strip()

print(
    Fore.GREEN +
    f"\nNice to meet you, {user_name}!"
)

print(
    Fore.LIGHTGREEN_EX +
    "\nLet's find a movie that matches your preferences.\n"
)

# Get user's preferred genre
selected_genre = choose_genre()

# Get user's current mood
mood = input(
    Fore.YELLOW +
    "\nHow are you feeling today? "
).strip()

print(
    Fore.BLUE +
    "\nAnalyzing your mood",
    end="",
    flush=True
)

loading_animation()

mood_score = TextBlob(mood).sentiment.polarity
mood_result = analyze_sentiment(mood_score)

print(
    Fore.GREEN +
    f"Your mood appears to be: {mood_result}"
)

print(
    Fore.GREEN +
    f"Sentiment score: {mood_score:.2f}\n"
)

# Get minimum rating
minimum_rating = choose_rating()

print(
    Fore.BLUE +
    f"\nSearching for movies for {user_name}",
    end="",
    flush=True
)

loading_animation()

recommendations = find_movies(
    selected_genre,
    minimum_rating,
    number_of_movies=5
)

if recommendations:
    display_movies(
        recommendations,
        user_name
    )
else:
    print(
        Fore.RED +
        "\nNo matching movies were found."
    )


# Ask if the user wants another set
while True:

    response = input(
        Fore.YELLOW +
        "Would you like another set of recommendations? (yes/no): "
    ).strip().lower()

    if response == "yes":

        print(
            Fore.BLUE +
            "\nFinding another set",
            end="",
            flush=True
        )

        loading_animation()

        recommendations = find_movies(
            selected_genre,
            minimum_rating,
            number_of_movies=5
        )

        if recommendations:
            display_movies(
                recommendations,
                user_name
            )
        else:
            print(
                Fore.RED +
                "\nNo matching movies were found."
            )

    elif response == "no":

        print(
            Fore.GREEN +
            f"\nEnjoy your movie recommendations, {user_name}! 🎬🍿"
        )
        break

    else:
        print(
            Fore.RED +
            "Please answer with yes or no."
        )