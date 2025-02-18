# YarnArt Product Image Downloader

A Python script that downloads hover images from YarnArt product pages and saves them as PNG files with custom naming conventions.

## Features

- Downloads hover images from YarnArt product pages
- Converts all images to PNG format
- Customizable number of leading zeros for color codes
- Custom naming format: "YAR-{product_no}-{color_code}.png"
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
python download_images_ya.py
```

The script will prompt you for three inputs:

1. **YarnArt product URL**
   - Example: https://yarnart.info/en/alpine-alpaca/
   - Must be a valid YarnArt product page URL

2. **Four-character product number**
   - Must be exactly 4 alphanumeric characters
   - Example: "2222"
   - This will be used in the filename as "YAR-2222-..."

3. **Number of leading zeros**
   - How many zeros to add before the color code
   - Must be a non-negative integer
   - Example: If you enter 2 and the color code is "123", it will become "00123"

### Output Format

Images will be saved in the current directory with the following naming format:
`YAR-{product_no}-{color_code}.png`

Examples:
- `YAR-2222-00123.png` (with 2 leading zeros)
- `YAR-2222-000123.png` (with 3 leading zeros)

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
4. The product page contains hover images

## Example

```bash
$ python download_images_ya.py
Enter the YarnArt product URL: https://yarnart.info/en/alpine-alpaca/
Enter the four-character product number: 2222
Enter the number of leading zeros to add to color codes: 2

Processing URL: https://yarnart.info/en/alpine-alpaca/
Found color code: 123
Downloading hover image for code 00123 from https://yarnart.info/images/123.jpg...
Successfully saved YAR-2222-00123.png
...
``` 