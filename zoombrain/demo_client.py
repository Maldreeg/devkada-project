# Example usage (upload + summarize)

import requests
import os
from pathlib import Path


class ZoomBrainClient:
    """Client for interacting with ZoomBrain API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the ZoomBrain API
        """
        self.base_url = base_url
    
    def health_check(self):
        """Check if the API is running"""
        try:
            response = requests.get(f"{self.base_url}/")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API: {e}")
            return None
    
    def upload_file(self, file_path: str):
        """
        Upload a file to the API
        
        Args:
            file_path: Path to the file to upload
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f)}
                response = requests.post(f"{self.base_url}/upload", files=files)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error uploading file: {e}")
            return None
    
    def summarize(self, query: str, top_k: int = 5):
        """
        Query the API for a summary
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
        """
        try:
            params = {'query': query, 'top_k': top_k}
            response = requests.post(f"{self.base_url}/summarize", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting summary: {e}")
            return None
    
    def list_documents(self):
        """List all indexed documents"""
        try:
            response = requests.get(f"{self.base_url}/documents")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error listing documents: {e}")
            return None


def demo():
    """Run a demo of the ZoomBrain client"""
    print("=== ZoomBrain Demo Client ===\n")
    
    # Initialize client
    client = ZoomBrainClient()
    
    # Health check
    print("1. Checking API health...")
    health = client.health_check()
    if health:
        print(f"   ✓ API is running: {health}")
    else:
        print("   ✗ API is not responding. Make sure the server is running.")
        return
    
    print("\n2. Uploading a sample file...")
    # Example: Upload a file (you'll need to provide an actual file path)
    # result = client.upload_file("path/to/your/file.pdf")
    # if result:
    #     print(f"   ✓ Upload successful: {result}")
    print("   (Skipped - provide a file path to test)")
    
    print("\n3. Querying for a summary...")
    summary = client.summarize("What are the main points?", top_k=3)
    if summary:
        print(f"   ✓ Summary: {summary}")
    
    print("\n4. Listing all documents...")
    docs = client.list_documents()
    if docs:
        print(f"   ✓ Documents: {docs}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
