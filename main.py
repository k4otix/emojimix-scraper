import concurrent.futures
import requests
import threading
from itertools import combinations_with_replacement

MAX_WORKERS = 1000  # go crazy
COMBO_URL = "https://tenor.googleapis.com/v2/featured?key=AIzaSyACvEq5cnT7AcHpDdj64SE3TJZRhW-iHuo&client_key=emoji_kitchen_funbox&q={}_{}&collection=emoji_kitchen_v6&contentfilter=high"
_lock = threading.Lock()


def lprint(msg):
    with _lock:
        print(msg)


def combine_emojis(combo):
    try:
        response = requests.get(COMBO_URL.format(combo[0], combo[1]))
    except requests.exceptions.HTTPError as e:
        lprint(f"{combo}: Error requesting COMBO_URL ({e})")
    else:
        # Get URL for the resulting PNG
        try:
            png_url = response.json()["results"][0]["url"]
        except Exception as e:
            lprint(f"{combo}: URL not found in COMBO_URL response ({e})")
        else:
            try:
                png_response = requests.get(png_url, stream=True)
            except requests.exceptions.HTTPError as e:
                lprint(f"{combo}: Error downloading PNG ({e})")
            else:
                # Save PNG
                fname = png_url.split("/")[-1]
                with open(f"png/{fname}", "wb") as f:
                    for chunk in png_response.iter_content(1024):
                        f.write(chunk)
                lprint(f"{combo}: Successfully created {fname}")


if __name__ == "__main__":
    
    emojis = (
        "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😭", "😉",
        "😗", "😙", "😚", "😘", "🥰", "😍", "🤩", "🥳", "🫠", "🙃",
        "🙂", "🥲", "🥹", "😊", "☺️", "😌", "😏", "😴", "😪", "🤤",
        "😋", "😛", "😝", "😜", "🤪", "🥴", "😔", "🥺", "😬", "😑",
        "😐", "😶", "😶‍🌫️", "🫥", "🤐", "🫡", "🤔", "🤫", "🫢", "🤭",
        "🥱", "🤗", "🫣", "😱", "🤨", "🧐", "😒", "🙄", "😮‍💨", "😤",
        "😠", "😡", "🤬", "😞", "😓", "😟", "😥", "😢", "☹️", "🙁",
        "🫤", "😕", "😰", "😨", "😧", "😦", "😮", "😯", "😲", "😳",
        "🤯", "😖", "😣", "😩", "😫", "😵", "🥶", "🥵", "🤢", "🤮",
        "🤧", "🤒", "🤕", "😷", "🤥", "😇", "🤠", "🤑", "🤓", "😎",
        "🥸", "🤡", "😈", "👿", "👻", "🎃", "💩", "🤖", "👽", "👾",
        "🌛", "🌜", "🌞", "🔥", "💯", "💫", "⭐", "🌟", "🕳️", "🙈",
        "❤️", "🧡", "💛", "💚", "🩵", "💙", "💜", "🤎", "🖤", "🩶",
        "🤍", "🩷", "💘", "💝", "💖", "💗", "💓", "💞", "💕", "💌",
        "♥️", "❣️", "❤️‍🩹", "💔", "💋", "🦠", "💀", "👁️", "🫦", "💐",
        "🌹", "🌷", "🌸", "🌼", "🍄", "🌵", "🌲", "🪵", "🪨", "⛄",
        "🌈", "🌊", "🌪️", "🌧️", "☁️", "🌍", "🐵", "🦁", "🐯", "🐱",
        "🐶", "🐺", "🐻", "🐨", "🐼", "🐭", "🐰", "🦊", "🦝", "🐮",
        "🐷", "🦄", "🐢", "🐸", "🐩", "🐐", "🦌", "🦙", "🦥", "🦔",
        "🦇", "🐦", "🐔", "🦉", "🪿", "🐧", "🦈", "🐳", "🐟", "🐙",
        "🦂", "🕷️", "🐌", "🐝", "🍓", "🍒", "🍉", "🍊", "🍍", "🍌",
        "🍋", "🌶️", "🥑", "🍞", "🧀", "🌭", "🎂", "🧁", "🍬", "☕",
        "🍽️", "🌇", "🎊", "🎈", "🎁", "🏆", "⚽", "🏀", "🪄", "🎧",
        "👑", "💎", "📰", "🔮"
    )

    combos = list(combinations_with_replacement(emojis, 2))

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(combine_emojis, combos)
