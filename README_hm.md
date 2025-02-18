# Himalaya Product Image Downloader

A Python script that downloads product color variant images from Himalaya product pages and saves them as PNG files with custom naming conventions.

## Features

- Downloads product images from Himalaya product pages
- Converts all images to PNG format
- Extracts color codes from product descriptions
- Custom naming format: "HIM-{product_no}-{color_code}.png"
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
python download_images_hm.py
```

The script will prompt you for two inputs:

1. **Himalaya product URL**
   - Example: https://www.himalaya.com.tr/dolphin-festival.html
   - Must be a valid Himalaya product page URL

2. **Four-character product number**
   - Must be exactly 4 alphanumeric characters
   - Example: "2222"
   - This will be used in the filename as "HIM-2222-..."

### Output Format

Images will be saved in the current directory with the following naming format:
`HIM-{product_no}-{color_code}.png`

Example:
- `HIM-2222-81101.png` (for color code 81101)
- `HIM-2222-81105.png` (for color code 81105)

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
4. The product page contains color variant images
5. The HTML structure matches expected format

## Example

```bash
$ python download_images_hm.py
Enter the Himalaya product URL: https://www.himalaya.com.tr/dolphin-festival.html
Enter the four-character product number: 2222

Processing URL: https://www.himalaya.com.tr/dolphin-festival.html
Found color code: 81101
Downloading image for code 81101 from https://www.himalaya.com.tr/uploads/pictures/...
Successfully saved HIM-2222-81101.png
...
``` 