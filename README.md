# Amplitude to S3 Pipeline

A Python pipeline that exports event data from Amplitude and uploads it to an AWS S3 bucket. Everything is run from a single entry point, `main.py`.

## How it works

1. **Extract** (`modules/amplitude_extract_module.py`): downloads yesterday's data from Amplitude.
2. **Load** (`modules/amplitude_load_module.py`): uploads the extracted files to S3.
3. **Logging** (`modules/loginitialise.py`): sets up a timestamped log file for each run.

## Setup

### 1. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` should include `requests`, `boto3` and `python-dotenv`.

### 2. Create a `.env` file

In the project root, add:

```
AMP_API_KEY=your_amplitude_api_key
AMP_SECRET_KEY=your_amplitude_secret_key
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_bucket_name
```

`.env` is listed in `.gitignore`. Never commit it.

## Usage

Run from the project root:

```bash
python main.py
```

## What each module does

### `amplitude_extract_module.py`

- Calls the Amplitude Export API (EU endpoint) for **yesterday's data**, from 00:00 to 23:00.
- Saves the response as a temporary zip file and extracts it.
- Decompresses the `.json.gz` files into `.json`.
- Moves the finished files to `amplitude_data/clean/`.
- Deletes the temporary zip and extract folder.
- Logs each step (success, warnings and errors).

Amplitude status codes handled:

| Code  | Meaning                                                  |
| ----- | -------------------------------------------------------- |
| 200   | Success, data is downloaded and processed                |
| 400   | Data too large, shorten the time range                   |
| 404   | No data for the requested time range                     |
| 504   | Timeout, use the Amazon S3 destination for large volumes |
| Other | Logged as a critical error                               |

### `amplitude_load_module.py`

- Connects to S3 using your AWS credentials.
- Reads every file in `amplitude_data/clean/`.
- Uploads each file to the S3 bucket, using the filename as the object key.
- **Deletes each local file after a successful upload.** Files that fail to upload are kept so you can retry.
- Logs each upload (success or error).

### `loginitialise.py`

- Creates the log folder (`logs/`) if it doesn't exist.
- Configures logging so messages are written to a timestamped `.log` file, one per run.

## Project structure

```
.
├── main.py                        # Entry point: runs extract, then load
├── modules/
│   ├── amplitude_extract_module.py
│   ├── amplitude_load_module.py
│   └── loginitialise.py
├── amplitude_data/
│   └── clean/                     # JSON files waiting to be uploaded
├── logs/                          # Log files, one per run
├── archive/
├── .env                           # Secrets (not committed)
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

## Notes

- The extract step always pulls the **previous day**. To backfill other dates, change the start and end times in the extract module.
- Run everything from the project root, as paths are relative.
- If `amplitude_data/clean/` is empty, the load step does nothing.
