import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
from urllib.parse import urljoin

def download_images(url, product_no):
    """
    Download images from Nako product page and save them with custom names.
    
    Args:
        url (str): The URL of the Nako product page
        product_no (str): Four-character product number for filenames
    """
    if not re.match(r'^[A-Za-z0-9]{4}$', product_no):
        raise ValueError("Product number must be exactly 4 alphanumeric characters")

    print(f"Processing URL: {url}")
    
    try:
        # Send HTTP request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {e}")
        return

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the product variants container (parent div)
    variants_container = soup.find('div', class_='variant-list-group')
    if not variants_container:
        print("Error: Could not find variant-list-group container")
        return

    # Find the variant list within the container
    variants_div = variants_container.find('div', class_='variant-list')
    if not variants_div:
        print("Error: Could not find variant-list section")
        return

    # Find all spans with class variant-image
    spans = variants_div.find_all('span', class_='variant-image')
    if not spans:
        print("Warning: No color variants found in the variant-list div")
    
    successful_downloads = 0
    failed_downloads = 0

    for span in spans:
        try:
            # Get image URL
            img = span.find('img')
            if not img or not img.get('src'):
                print("Warning: Skipping span - no image or src attribute found")
                continue
            
            # Handle relative URLs by joining with base URL
            img_url = img['src']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(url, img_url)
            
            # Get color code from the span's data-option-title attribute
            color_code = span.get('data-option-title', '').split('_')[0]
            if not color_code:
                print("Warning: Skipping image - no color code found in data-option-title")
                continue
            
            # Generate filename
            filename = f"NAK-{product_no}-{color_code}.png"
            
            print(f"Downloading image for code {color_code} from {img_url}...")
            
            # Download image with timeout
            img_response = requests.get(img_url, timeout=10)
            img_response.raise_for_status()
            
            # Verify content type is an image
            content_type = img_response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"Warning: Skipping - URL does not point to an image (content-type: {content_type})")
                continue
            
            # Open and convert image
            img_data = Image.open(BytesIO(img_response.content))
            
            # Convert to PNG and save
            img_data = img_data.convert('RGBA')
            img_data.save(filename, 'PNG')
            
            print(f"Successfully saved {filename}")
            successful_downloads += 1
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            failed_downloads += 1
        except (IOError, OSError) as e:
            print(f"Error processing image: {e}")
            failed_downloads += 1
        except Exception as e:
            print(f"Unexpected error: {e}")
            failed_downloads += 1

    # Print summary
    print("\nDownload Summary:")
    print(f"Successfully downloaded: {successful_downloads} images")
    print(f"Failed downloads: {failed_downloads} images")
    if successful_downloads == 0:
        print("\nTroubleshooting tips:")
        print("1. Verify that the URL is correct and accessible")
        print("2. Check if the website structure has changed")
        print("3. Ensure you have a stable internet connection")

if __name__ == "__main__":
    # Example usage
    url = input("Enter the Nako product URL: ")
    product_no = input("Enter the four-character product number: ")
    
    try:
        download_images(url, product_no)
    except Exception as e:
        print(f"Error: {e}") 