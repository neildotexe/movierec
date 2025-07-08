import json
import logging
from typing import List, Dict, Union, Any

from django.conf import settings
import google.generativeai as genai
# from google.generativeai.types import GenerationResponse

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# Initialize Gemini client with the key from settings
# It's good practice to wrap this in a try-except if settings.GEMINI_API_KEY might be missing
try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
except AttributeError:
    logger.error("GEMINI_API_KEY is not defined in Django settings.")
    client = None # Or raise an exception, depending on desired behavior

def get_recommendations_after_last_watch(user: Any, n: int = 5) -> List[str]:
    """
    Generates movie recommendations for a user based on their most recent movie review
    using the Google Gemini API.

    Args:
        user: An object representing the user, expected to have a 'reviews'
              related manager that can be ordered by 'created_at'.
              Each review should have 'movie.title' and 'rating' attributes.
        n: The number of movie recommendations to generate. Defaults to 5.

    Returns:
        A list of recommended movie titles as strings. Returns an empty list
        if no last watch is found, if the API client is not initialized,
        if the API call fails, or if the response cannot be parsed as JSON.
    """
    if client is None:
        logger.error("Gemini client is not initialized. Cannot fetch recommendations.")
        return []

    # Get the user's last reviewed movie
    # Assuming 'reviews' is a Django ManyToMany/ForeignKey related manager
    # and 'created_at' is a field on the Review model.
    last_review = user.reviews.order_by("-created_at").first()

    if not last_review:
        logger.info(f"User {user} has no reviews. No recommendations can be made.")
        return []

    title: str = last_review.movie.title
    rating: float = float(last_review.rating)
    liked: bool = rating >= 3.0  # Assuming 3.0 or higher means "liked"

    # Construct the prompt for the Gemini model
    # Explicitly ask for JSON array format to ensure parseable output
    prompt: str = (
        f"The user just watched “{title}” and "
        f"{'loved' if liked else 'did not enjoy'} it (rated {rating}).\n"
        f"Based on that, recommend {n} similar movies they might "
        f"{'enjoy' if liked else 'like'}.\n"
        f"Return only a JSON array of movie titles. Do not include any other text, "
        f"explanations, or formatting outside the JSON array. For example: "
        f'["Movie A", "Movie B", "Movie C"].'
    )

    try:
        resp = client.models.generate_content(
            model="gemini-1.5-flash",  # Use 1.5-flash for better JSON formatting adherence
            contents=prompt,
            temperature=0.7,          # A moderate temperature for some creativity
            max_tokens=200,           # Max tokens should be sufficient for a JSON array of titles
        )

        # Access the text content from the response
        response_text: str = resp.text
        logger.debug(f"Gemini raw response: {response_text}")

        # Attempt to parse the JSON response
        # The model might sometimes return extra whitespace or markdown ticks
        json_string = response_text.strip().strip('`').strip('json')
        recommendations: List[str] = json.loads(json_string)

        # Basic validation that it's a list of strings
        if not isinstance(recommendations, list) or not all(isinstance(item, str) for item in recommendations):
            logger.warning(f"Gemini returned malformed JSON or non-string list: {response_text}")
            return []

        return recommendations[:n] # Return up to 'n' recommendations

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from Gemini: {e}. Raw response: {response_text}")
        return []
    except genai.types.APIError as e:
        logger.error(f"Gemini API error occurred: {e}")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred during recommendation generation: {e}")
        return []