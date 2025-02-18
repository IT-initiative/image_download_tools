# Nako Product Image Downloader

A Python script that downloads product color variant images from Nako product pages and saves them as PNG files with custom naming conventions.

## Features

- Downloads product images from Nako product pages
- Converts all images to PNG format
- Extracts color codes from variant data
- Custom naming format: "NAK-{product_no}-{color_code}.png"
- Comprehensive error handling and progress reporting

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:
```bash
python download_images_nk.py
```

The script will prompt you for two inputs:

1. **Nako product URL**
   - Example: https://www.nako.com.tr/urun/sport-wool
   - Must be a valid Nako product page URL

2. **Four-character product number**
   - Must be exactly 4 alphanumeric characters
   - Example: "2222"
   - This will be used in the filename as "NAK-2222-..."

### Output Format

Images will be saved in the current directory with the following naming format:
`NAK-{product_no}-{color_code}.png`

Example:
- `NAK-2222-00208.png` (for color code 00208)
- `NAK-2222-03079.png` (for color code 03079)

### Error Handling

The script includes error handling for:
- Invalid URLs
- Network errors
- Missing webpage elements
- Download failures
- Image conversion issues
- Invalid input validation

If any errors occur, the script will:
- Display specific error messages
- Skip problematic images
- Continue processing remaining images
- Provide a summary of successful and failed downloads

## Requirements

- Python 3.6 or higher
- requests
- beautifulsoup4
- Pillow (PIL)

## Troubleshooting

If no images are downloaded, check:
1. The URL is correct and accessible
2. The website structure hasn't changed
3. Your internet connection is stable
4. The product page contains variant images
5. The variant-list-group container is present

## Example

```bash
$ python download_images_nk.py
Enter the Nako product URL: https://www.nako.com.tr/urun/sport-wool
Enter the four-character product number: 2222

Processing URL: https://www.nako.com.tr/urun/sport-wool
Found color code: 00208
Downloading image for code 00208 from https://www.nako.com.tr/images/...
Successfully saved NAK-2222-00208.png
...
``` 