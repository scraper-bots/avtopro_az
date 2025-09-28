import asyncio
import aiohttp
import pandas as pd
import json
from typing import List, Dict, Any
import time

class RegisterNumberScraper:
    def __init__(self, base_url: str = "https://api.avtopro.az/api/register_numbers"):
        self.base_url = base_url
        self.session = None
        self.all_data = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, page: int, paginate: int = 30) -> Dict[str, Any]:
        """Fetch a single page of data"""
        params = {
            'paginate': paginate,
            'number': '',
            'page': page
        }

        headers = {
            'Accept': 'application/json',
            'Origin': 'https://www.avtopro.az',
            'Referer': 'https://www.avtopro.az/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
        }

        try:
            async with self.session.get(self.base_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Fetched page {page} - {len(data['data']['data'])} records")
                    return data
                else:
                    print(f"✗ Failed to fetch page {page}: HTTP {response.status}")
                    return None
        except Exception as e:
            print(f"✗ Error fetching page {page}: {str(e)}")
            return None

    async def get_total_pages(self) -> int:
        """Get the total number of pages"""
        first_page = await self.fetch_page(1)
        if first_page and first_page.get('success'):
            return first_page['data']['last_page']
        return 0

    async def fetch_all_pages(self, max_concurrent: int = 10) -> List[Dict[str, Any]]:
        """Fetch all pages concurrently with rate limiting"""
        total_pages = await self.get_total_pages()
        if total_pages == 0:
            print("Could not determine total pages")
            return []

        print(f"Total pages to scrape: {total_pages}")

        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_with_semaphore(page: int):
            async with semaphore:
                # Add small delay between requests to be respectful
                await asyncio.sleep(0.1)
                return await self.fetch_page(page)

        # Create tasks for all pages
        tasks = [fetch_with_semaphore(page) for page in range(1, total_pages + 1)]

        # Execute all tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter successful results
        successful_results = [
            result for result in results
            if result is not None and not isinstance(result, Exception) and result.get('success')
        ]

        print(f"Successfully fetched {len(successful_results)} out of {total_pages} pages")
        return successful_results

    def process_data(self, api_responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process raw API responses into flat records"""
        all_records = []

        for response in api_responses:
            if not response.get('success'):
                continue

            for item in response['data']['data']:
                record = {
                    'id': item['id'],
                    'region_number_id': item['region_number_id'],
                    'first_letter': item['first_letter'],
                    'second_letter': item['second_letter'],
                    'number': item['number'],
                    'price': item['price'],
                    'currency': item['currency'],
                    'city_id': item['city_id'],
                    'views': item['views'],
                    'author_phone': item['author_phone'],
                    'author_name': item['author_name'],
                    'description': item['description'] or '',
                    'user_id': item['user_id'],
                    'status': item['status'],
                    'deleted_at': item['deleted_at'] or '',
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'region_number': item['region']['region_number'],
                    'region_name': item['region']['name'],
                    'city_name': item['city']['name']
                }
                all_records.append(record)

        return all_records

    def save_to_csv(self, records: List[Dict[str, Any]], filename: str = 'register_numbers.csv'):
        """Save records to CSV file"""
        if not records:
            print("No records to save")
            return

        df = pd.DataFrame(records)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✓ Saved {len(records)} records to {filename}")

    def save_to_xlsx(self, records: List[Dict[str, Any]], filename: str = 'register_numbers.xlsx'):
        """Save records to XLSX file"""
        if not records:
            print("No records to save")
            return

        df = pd.DataFrame(records)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✓ Saved {len(records)} records to {filename}")

    async def scrape_all(self, csv_filename: str = 'register_numbers.csv',
                        xlsx_filename: str = 'register_numbers.xlsx'):
        """Main method to scrape all data and save to files"""
        start_time = time.time()

        print("🚀 Starting scraper...")
        print("=" * 50)

        # Fetch all pages
        api_responses = await self.fetch_all_pages()

        if not api_responses:
            print("No data fetched")
            return

        # Process data
        print("\n📊 Processing data...")
        records = self.process_data(api_responses)

        # Save to files
        print("\n💾 Saving data...")
        self.save_to_csv(records, csv_filename)
        self.save_to_xlsx(records, xlsx_filename)

        end_time = time.time()
        print(f"\n🎉 Scraping completed in {end_time - start_time:.2f} seconds")
        print(f"Total records scraped: {len(records)}")

async def main():
    """Main function to run the scraper"""
    async with RegisterNumberScraper() as scraper:
        await scraper.scrape_all()

if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import aiohttp
        import pandas
        import openpyxl
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages:")
        print("pip install aiohttp pandas openpyxl")
        exit(1)

    # Run the scraper
    asyncio.run(main())