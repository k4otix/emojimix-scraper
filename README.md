# emojimix-scraper
Just a fun experiment to generate all possible emoji combinations from https://www.google.com/search?q=combine+emojis

## How does it work?
After playing around with the app for a bit with Chrome DevTools open, I was able to determine:
1. A file containing all of the emojis shown in the app (https://www.google.com/logos/fnbx/emoji_kitchen/emoji_kitchen_pairs.3.pb)
2. The URL used to submit the combination request
3. The response JSON which includes a subsequent URL with a PNG of the resulting combination

After that, it was pretty straightforward to enumerate and submit all combinations to the API, parse the response, and fetch the resulting image.

## By the numbers
- 234 emojis
- 27495 possible combinations with replacement (also called multichoose -- you are allowed to select the same emoji twice)
- not all combinations are supported; the app will sometimes gray-out a subset of emojis
- the resulting PNG dataset occupies ~360MB of disk space

## Usage:
- The only Python dependency is the requsts library
- Running `main.py` will output each combination to stdout along with the resulting filename, or an error if it fails
- Feel free to adjust `MAX_WORKERS`; a value of 1000 allowed the script to complete in a few minutes on a 2019 MBP Core i9
- I suggest redirecting the output to a text file; this allows you to later grep for an image filename and see which emojis combined to create it (if you can't tell by visual inspection).

NOTE: There may be a bug in this code somewhere; I got 27451 lines of output instead of the expected 27495 (a delta of 44 combinations). PR welcome if you happen to spot an error 😁
