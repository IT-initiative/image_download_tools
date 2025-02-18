# Nako Product Image Downloader

A Python script that downloads product color variant images from Nako product pages and saves them as PNG files with custom naming conventions.

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:
```bash
python download_images.py
```

The script will prompt you for:
1. The Nako product URL (e.g., https://www.nako.com.tr/urun/sport-wool) or YarnArt product URL (e.g., https://yarnart.info/en/macrame-xl-131/)
2. A four-character prefix code for the filenames (e.g., "2222")

### Output Format

Images will be saved in the current directory with the following naming format:
`NAK-{prefix}-{color_code}.png`

Example: `NAK-2222-123456.png`

### Error Handling

The script includes error handling for:
- Invalid URLs
- Network errors
- Missing webpage elements
- Download failures
- Image conversion issues

## Requirements

- Python 3.6 or higher
- requests
- beautifulsoup4
- Pillow (PIL) 