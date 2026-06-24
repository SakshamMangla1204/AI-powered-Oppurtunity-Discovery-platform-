from tavily import TavilyClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Tavily client
client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# Run search
response = client.search(
    query="AI startups India",
    max_results=5
)

# Basic information
print("\n" + "=" * 80)
print("TAVILY SEARCH RESULTS")
print("=" * 80)

# Loop through results
for index, result in enumerate(response["results"], start=1):

    print(f"\n\nRESULT #{index}")
    print("-" * 80)

    print("\nTITLE:")
    print(result.get("title", "No Title"))

    print("\nURL:")
    print(result.get("url", "No URL"))

    print("\nCONTENT:")
    print(result.get("content", "No Content"))

    print("\nSCORE:")
    print(result.get("score", "No Score"))

    print("\n" + "=" * 80)

# Optional debugging information
print("\n\nSEARCH METADATA")
print("-" * 80)
print("Response Time:", response.get("response_time"))
print("Request ID:", response.get("request_id"))