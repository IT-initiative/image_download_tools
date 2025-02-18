import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
from urllib.parse import urljoin

def download_images(url, product_no, leading_zeros):
    """
    Download hover images from YarnArt product page and save them as PNG files with custom names.
    
    Args:
        url (str): The URL of the YarnArt product page
        product_no (str): Four-character product number for filenames
        leading_zeros (int): Number of leading zeros to add to the color code
    """
    if not re.match(r'^[A-Za-z0-9]{4}$', product_no):
        raise ValueError("Product number must be exactly 4 alphanumeric characters")

    if not isinstance(leading_zeros, int) or leading_zeros < 0:
        raise ValueError("Number of leading zeros must be a non-negative integer")

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
    
    # Find all product headings (they contain the color codes)
    product_headings = soup.find_all('h3')
    if not product_headings:
        print("Error: Could not find any h3 elements")
        print("HTML content:", soup.prettify()[:500])  # Print first 500 chars for debugging
        return
    
    successful_downloads = 0
    failed_downloads = 0

    for heading in product_headings:
        try:
            # Get the color code from the heading text
            code_text = heading.text.strip()
            if not code_text.isdigit():
                continue  # Skip non-numeric headings silently
            
            print(f"Found color code: {code_text}")
            
            # Add specified number of leading zeros to the code
            color_code = code_text.zfill(len(code_text) + leading_zeros)
            
            # Find the parent container
            parent = heading.parent
            if not parent:
                print(f"Warning: Skipping code {color_code} - no parent element found")
                continue
            
            # Try to find hover image
            hover_span = parent.find('span', class_='hover_image')
            if not hover_span:
                # Try looking in previous siblings
                prev_sibling = parent.find_previous_sibling()
                if prev_sibling:
                    hover_span = prev_sibling.find('span', class_='hover_image')
            
            if not hover_span:
                print(f"Warning: Skipping code {color_code} - no hover image span found")
                continue
            
            # Get the image from hover span
            img = hover_span.find('img')
            if not img or not img.get('src'):
                print(f"Warning: Skipping code {color_code} - no hover image found")
                continue
            
            # Handle relative URLs by joining with base URL
            img_url = img['src']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(url, img_url)
            
            # Generate filename
            filename = f"YAR-{product_no}-{color_code}.png"
            
            print(f"Downloading hover image for code {color_code} from {img_url}...")
            
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
    url = input("Enter the YarnArt product URL: ")
    product_no = input("Enter the four-character product number: ")
    leading_zeros = int(input("Enter the number of leading zeros to add to color codes: "))
    
    try:
        download_images(url, product_no, leading_zeros)
    except Exception as e:
        print(f"Error: {e}") 