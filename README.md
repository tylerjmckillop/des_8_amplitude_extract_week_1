# Amplitude Data Export Script

This script downloads a day's worth of data from Amplitude, saves it, unzips it, and ends up with a clean folder of `.json` files I can use.

## What the script does

1. Loads my API keys from a `.env` file so I'm not putting secret passwords directly in the code.

2. Makes a folder called `amplitude_data` if it doesn't already exist. Every time I run the script, it makes a new folder inside that one, named with the current date and time, so old runs don't get overwritten.

3. Works out "yesterday's" date, since that's the data I want to pull each time.

4. Sends a request to Amplitude asking for that day's data.

5. If the request works (status code 200), Amplitude sends back a `.zip` file. The script:
   - saves that zip file to disk
   - unzips it

6. Inside that zip, the files aren't plain `.json` files — they're `.json.gz` files (basically a zipped-up version of a single file, different from a normal `.zip`). So the script goes through each one and unzips those too, turning each `.json.gz` into a normal `.json` file.

7. Once I have the real `.json` files, I move them into their own folder called `clean`, so I'm not left with a mix of `.gz` and `.json` files all jumbled together.

## Things I still need to fix

- The script doesn't delete anything when it's done. I still have leftover `.zip` files and the original `.gz` files sitting around. I need to add code to delete them once I'm finished with them.

- If the request fails (not status 200), the script doesn't really do anything smart yet — I want to add retrying later.

- My logging has two mistakes right now:
  1. I wrote `logger.inf(...)` somewhere but it should be `logger.info(...)` — this will crash if it runs.
  2. I made a folder called `log`, but then my log file tries to save into a folder called `logs` (with an s) — that folder doesn't exist, so it'll fail. I need to make both names match.

- Right now if something fails, I only use `print()` to show that — nothing gets saved in the log file. I want to fix that so failures actually get logged.

## What my folders look like after running it

    amplitude_data/
      2026-09-25 09-18-52/        (the raw stuff from the zip)
        100011471/
          *.json.gz                (original files from Amplitude)
          *.json                   (unzipped versions, not moved yet)
        clean/
          *.json                   (the files I actually want)
      2026-09-25 09-18-52.zip       (the original download, not deleted yet)

## Stuff to remember before I trust this fully

- Keep `.env` out of git (it has my secret keys in it).
- Old folders never get deleted — I'll build up a lot of them over time.
- Still need to finish the retry/error handling so it doesn't just silently fail.
