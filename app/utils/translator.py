from deep_translator import GoogleTranslator, MyMemoryTranslator
from deep_translator.exceptions import RequestError, NotValidLength


# Translation configuration
# Google Translate is used as provider
# https://deep-translator.readthedocs.io/en/latest/README.html#id1

google_trans = GoogleTranslator(source='ka', target='en')
mymemory_trans = MyMemoryTranslator(source='ka-GE', target='en-US')


async def translate(text: str) -> str:  # noqa: C901
    """Simple deep_translator wrapper"""

    # Try execute with Google Tranlate (5000 chars limit)
    try:
        translated_text = google_trans.translate(text)
        return translated_text
    except RequestError:

        # If Google translate not responding, try MyMemory (500 chars limit)
        try:
            translated_text = mymemory_trans.translate(text)
            return translated_text
        except NotValidLength:

            CHAR_LIMIT = 500

            words = text.split()

            parts = []
            results = []
            current_part = ""

            for word in words:
                if len(current_part) + len(word) + 1 <= CHAR_LIMIT:
                    current_part += " " + word if current_part else word
                else:
                    parts.append(current_part)
                    current_part = word
            if current_part:
                parts.append(current_part)

            for part in parts:
                processed_result = mymemory_trans.translate(part)
                results.append(processed_result)

            translated_text = " ".join(results)
            return translated_text
