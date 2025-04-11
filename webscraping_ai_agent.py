


import asyncio
from crawl4ai import AsyncWebCrawler

async def extract_non_table_data():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://berascan.com/")
        if result.success:
            # Extract and display images
            images = result.media.get('images', [])
            if images:
                print(f"Found {len(images)} images:")
                for idx, img in enumerate(images):
                    print(f"Image {idx + 1}: URL: {img['src']}, Alt text: {img.get('alt', 'N/A')}")
            else:
                print("No images found on the page.")
            # Extract and display videos
            videos = result.media.get('videos', [])
            if videos:
                print(f"Found {len(videos)} videos:")
                for idx, video in enumerate(videos):
                    print(f"Video {idx + 1}: URL: {video['src']}")
            else:
                print("No videos found on the page.")
            # Extract and display audio
            audio_files = result.media.get('audio', [])
            if audio_files:
                print(f"Found {len(audio_files)} audio files:")
                for idx, audio in enumerate(audio_files):
                    print(f"Audio {idx + 1}: URL: {audio['src']}")
            else:
                print("No audio files found on the page.")
            # Extract and display links
            links = result.links.get('external', []) + result.links.get('internal', [])
            if links:
                print(f"Found {len(links)} links:")
                for idx, link in enumerate(links):
                    print(f"Link {idx + 1}: {link}")
            else:
                print("No links found on the page.")
            # Extract and display the generated Markdown content
            markdown_content = result.markdown
            if markdown_content:
                print("Generated Markdown content:")
                print(markdown_content)
            else:
                print("No Markdown content generated.")
        else:
            print("Failed to crawl the page.")


if __name__ == "__main__":
    asyncio.run(extract_non_table_data())
    
