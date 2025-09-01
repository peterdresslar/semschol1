import os
import re
import time
import sys
from typing import Optional, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def extract_paper_id(url: str) -> Optional[str]:
    """Extract paper ID from Semantic Scholar URL."""
    # Pattern to match CorpusID in the URL
    match = re.search(r'CorpusID:(\d+)', url)
    if match:
        return match.group(1)
    
    # Alternative pattern for paper ID in different URL formats
    match = re.search(r'/([a-f0-9]{40})(?:\?|$)', url)
    if match:
        return match.group(1)
    
    return None


def resolve_one_url(url: str, api_key: str) -> Optional[str]:
    """
    Resolve a single Semantic Scholar URL to get the DOI.
    
    Args:
        url: Semantic Scholar URL containing paper ID
        api_key: API key for Semantic Scholar
        
    Returns:
        DOI string if found, None otherwise
    """
    paper_id = extract_paper_id(url)
    if not paper_id:
        print(f"Could not extract paper ID from URL: {url}")
        return None
    
    # Semantic Scholar API endpoint - use CorpusId: prefix
    api_url = f"https://api.semanticscholar.org/graph/v1/paper/CorpusId:{paper_id}"
    
    # Request parameters - only request the DOI field
    params = {
        'fields': 'externalIds'
    }
    
    # Headers with API key
    headers = {
        'x-api-key': api_key
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        
        # Handle rate limiting
        if response.status_code == 429:
            print(f"Rate limit reached for paper ID {paper_id}. Consider adding API key or increasing delay.")
            return None
            
        response.raise_for_status()
        
        data = response.json()
        
        # Extract DOI from externalIds
        external_ids = data.get('externalIds', {})
        doi = external_ids.get('DOI')
        
        if doi:
            return doi
        else:
            print(f"No DOI found for paper ID: {paper_id}")
            return None
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Paper not found for ID {paper_id}")
        else:
            print(f"HTTP error for paper ID {paper_id}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for paper ID {paper_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for paper ID {paper_id}: {e}")
        return None


def process_file(filename: str, api_key: str) -> List[str]:
    """
    Process citations file and resolve all Semantic Scholar URLs to DOIs.
    
    Args:
        filename: Path to the citations file
        api_key: API key for Semantic Scholar
        
    Returns:
        List of DOIs found
    """
    dois = []
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
        # Find all URLs in the content
        url_pattern = r'https://api\.semanticscholar\.org/CorpusID:\d+'
        urls = re.findall(url_pattern, content)
        
        print(f"Found {len(urls)} Semantic Scholar URLs to process")
        
        for i, url in enumerate(urls, 1):
            print(f"Processing URL {i}/{len(urls)}: {url}")
            
            doi = resolve_one_url(url, api_key)
            if doi:
                dois.append(doi)
                print(f"  -> DOI: {doi}")
            
            # Rate limiting - be respectful to the API
            # Semantic Scholar allows 100 requests per 5 minutes for free tier
            # Without API key, the rate limit is much lower
            if i < len(urls):  # Don't sleep after the last request
                if api_key:
                    time.sleep(1.5)  # 1 second delay with API key
                else:
                    time.sleep(3)  # 3 seconds delay without API key
                
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error processing file: {e}")
    
    return dois


def main():
    """Main function to process citations and output DOIs."""
    # Get API key from environment
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print("Warning: API_KEY not found in environment variables")
        print("The program will run without an API key, but may face severe rate limiting.")
        print("To get better performance, create a .env file with API_KEY=your_key_here")
        print("Get your free API key at: https://www.semanticscholar.org/product/api")
        print("\nContinuing without API key...\n")
        api_key = None  # Explicitly set to None
    
    # get citations filename from args
    citations_file = sys.argv[1]
    # citations_file = 'cits.txt'
    dois = process_file(citations_file, api_key)
    
    # Output results
    print(f"\nFound {len(dois)} DOIs:")
    if dois:
        # Print comma-separated list of DOIs
        doi_list = ', '.join(dois)
        print(doi_list)
        
        # Also save to a file for convenience
        output_file = 'dois_output.txt'
        with open(output_file, 'w') as f:
            f.write(doi_list)
        print(f"\nDOIs also saved to {output_file}")
    else:
        print("No DOIs were found.")


if __name__ == "__main__":
    main()