import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
from urllib.parse import urljoin

def download_images(url, product_no):
    """
    Download images from Himalaya product page and save them with custom names.
    
    Args:
        url (str): The URL of the Himalaya product page
        product_no (str): Four-character product number for filenames
    """
    if not re.match(r'^[A-Za-z0-9]{4}$', product_no):
        raise ValueError("Product number must be exactly 4 alphanumeric characters")

    print(f"Processing URL: {url}")
    
    try:
        # Send HTTP request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL: {e}")
        return

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the product section
    product_section = soup.find('section', class_='pages product-detail')
    if not product_section:
        print("Error: Could not find product detail section")
        return

    # Find the container with product images (col-sm-7)
    product_container = product_section.find('div', class_='col-sm-7')
    if not product_container:
        print("Error: Could not find product container")
        return

    # Find all product divs (col-xs-6 col-md-3)
    product_divs = product_container.find_all('div', class_='col-xs-6 col-md-3')
    if not product_divs:
        print("Warning: No product divs found")
        return
    
    successful_downloads = 0
    failed_downloads = 0

    for div in product_divs:
        try:
            # Get the color code from the text-center paragraph
            code_elem = div.find('p', class_='text-center')
            if not code_elem:
                print("Warning: Skipping div - no text-center paragraph found")
                continue
            
            # Extract the code from the text
            code_text = code_elem.text.strip()
            # Remove any parentheses and text within them
            code_text = re.sub(r'\([^)]*\)', '', code_text).strip()
            # Extract just the numeric part
            code_match = re.search(r'(\d+)', code_text)
            if not code_match:
                print(f"Warning: Skipping div - no numeric code found in text: {code_text}")
                continue
            
            color_code = code_match.group(1)
            
            # Get the image URL from the img tag
            img = div.find('img', class_='img-responsive')
            if not img or not img.get('src'):
                print(f"Warning: Skipping code {color_code} - no image found")
                continue
            
            # Handle relative URLs by joining with base URL
            img_url = img['src']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(url, img_url)
            
            # Generate filename
            filename = f"HIM-{product_no}-{color_code}.png"
            
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
        print("4. Try viewing the page source to verify the HTML structure")

if __name__ == "__main__":
    # Example usage
    url = input("Enter the Himalaya product URL: ")
    product_no = input("Enter the four-character product number: ")
    
    try:
        download_images(url, product_no)
    except Exception as e:
        print(f"Error: {e}") 