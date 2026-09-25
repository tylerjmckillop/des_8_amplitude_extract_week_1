# Amplitude Data Export

Pulls the previous day's raw event data from Amplitude's Export API, unzips it, decompresses the `.json.gz` files inside, and drops the clean JSON into its own folder.

## What it does

1. Hits the Amplitude `/api/2/export` endpoint for yesterday (00:00–23:00)
2. Saves the response as a `.zip`
3. Extracts it, then gunzips each `.json.gz` file it finds
4. Moves the resulting `.json` files into a `clean/` subfolder
5. Logs everything (and prints to console) along the way
6. Deletes the zip and the intermediate extract folder once it's done

## Requirements

- Python 3.9+
- `requests`, `python-dotenv` (everything else used is stdlib)

```bash
pip install requests python-dotenv
```

## Setup

Create a `.env` file in the project root with your Amplitude API credentials:

```
AMP_API_KEY=your_api_key
AMP_SECRET_KEY=your_secret_key
```

Note the script is pointed at the EU endpoint (`analytics.eu.amplitude.com`). If your project is on the standard/US instance, change the `url` variable to `https://amplitude.com/api/2/export`.

## Running it

```bash
python amplitude_export.py
```

Each run creates a timestamped folder under `amplitude_data/`, e.g.:

```
amplitude_data/
  2026-09-24 09-00-00.zip
  2026-09-24 09-00-00/
    <amplitude export folder>/
      clean/
        <date>.json
        <date>.json
```

Logs go to `log/`, one file per run.

## Status code handling

| Code  | Meaning                                                            |
| ----- | ------------------------------------------------------------------ |
| 200   | Success — export is processed as above                             |
| 400   | Time range too large — shorten it and retry                        |
| 404   | No data available for that range                                   |
| 504   | Timeout due to data volume — use the S3 export destination instead |
| other | Unexpected error, logged as critical                               |

## Scheduling

Since it always pulls "yesterday," this is meant to run once a day (cron, Task Scheduler, Airflow, whatever you've got) rather than be triggered manually for backfills.

## Known improvements

The cleanup step at the bottom (`shutil.rmtree(gz_folder)` / `os.remove(zip_path)`) runs no matter what status code came back. If the request didn't return 200, `gz_folder` was never created and this will blow up with a `NameError`. Worth wrapping that cleanup in an `if status == 200:` check, or guarding it the same way the move step is guarded.
