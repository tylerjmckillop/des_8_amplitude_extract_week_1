# Amplitude to S3 Pipeline

Two Python scripts that export event data from Amplitude and upload it to an AWS S3 bucket.

1. **`extract_amplitude.py`**: downloads yesterday's Amplitude data and unpacks it into JSON files.
2. **`upload_to_s3.py`**: uploads those JSON files to S3.

Run them in that order, from the project root.

## Setup

### 1. Install dependencies

```bash
pip install requests boto3 python-dotenv
```

### 2. Create a `.env` file

In the project root, add:

```
AMP_API_KEY=your_amplitude_api_key
AMP_SECRET_KEY=your_amplitude_secret_key
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_bucket_name
```

Never commit `.env` to version control.

## Usage

```bash
python extract_amplitude.py
python upload_to_s3.py
```

## What each script does

### `extract_amplitude.py`

- Calls the Amplitude Export API (EU endpoint) for **yesterday's data**, from 00:00 to 23:00.
- Saves the response as a temporary zip file and extracts it.
- Decompresses the `.json.gz` files into `.json`.
- Moves the finished files to `amplitude_data/clean/`.
- Deletes the temporary zip and extract folder.
- Logs to `log/logging_amplitude_data_<timestamp>.log`.

Amplitude status codes handled:

| Code  | Meaning                                                  |
| ----- | -------------------------------------------------------- |
| 200   | Success, data is downloaded and processed                |
| 400   | Data too large, shorten the time range                   |
| 404   | No data for the requested time range                     |
| 504   | Timeout, use the Amazon S3 destination for large volumes |
| Other | Logged as a critical error                               |

### `upload_to_s3.py`

- Reads every file in `amplitude_data/clean/`.
- Uploads each file to the S3 bucket, using the filename as the object key.
- **Deletes each local file after a successful upload.** Files that fail to upload are kept so you can retry.
- Logs to `load_log/<timestamp>.log`.

## Folder structure

```
.
├── .env
├── extract_amplitude.py
├── upload_to_s3.py
├── amplitude_data/
│   └── clean/        # JSON files waiting to be uploaded
├── log/              # Extract logs
└── load_log/         # Upload logs
```

## Notes

- Both scripts use relative paths, so run them from the project root.
- The extract script always pulls the previous day. To backfill other dates, change `start_time` and `end_time` in the script.
- If the upload script finds no files in `amplitude_data/clean/`, it does nothing.
