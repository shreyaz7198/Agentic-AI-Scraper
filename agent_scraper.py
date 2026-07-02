import os
import sys
import json
import asyncio
import pandas as pd
from pathlib import Path
from google import genai
from playwright.async_api import async_playwright

# Verification: Ensure the environment key is mapped correctly
if not os.environ.get("GOOGLE_API_KEY"):
    print("❌ Configuration Error: GOOGLE_API_KEY environment variable is missing!")
    print("Please set it in your terminal: $env:GOOGLE_API_KEY='your_key'")
    sys.exit(1)

async def extract_leads_with_ai(page_content, keyword, location):
    """Passes raw web page text content to Gemini with automated 429 backoff handling."""
    client = genai.Client()
    
    prompt = f"""
    You are an expert data QA extraction assistant. Analyze this text content from a Google Maps page for '{keyword}' in '{location}'.
    Identify up to 3 distinct businesses.
    
    Return your response strictly as a valid JSON array of objects. No markdown wraps, no backticks.
    Use exactly these property keys:
    "searched_keyword": "{keyword}",
    "target_location": "{location}",
    "name": "Business Name",
    "contact_number": "Phone number or empty string if none",
    "address": "Full business address layout",
    "website": "URL website link or empty string if none"
    
    Data:
    {page_content[:12000]}
    """
    
    # Simple retry loop for short-term rate limit windows
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                )
            clean_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print(f"⚠️  Rate limit encountered. Attempt {attempt + 1}/3. Waiting 35 seconds...")
                await asyncio.sleep(35)  # Backs off to let the API limit window clear safely
                continue
            print(f"❌ Non-429 Error parsing data: {error_msg}")
            break
    return []

async def run_hybrid_matrix_scraper():
    print("📋 --- V5 Dynamic Hybrid Agentic Scraper ---")
    
    raw_keywords = input("🔍 Enter Search Keywords (separated by commas): ").strip()
    raw_locations = input("📍 Enter Target Locations (separated by commas): ").strip()
    
    if not raw_keywords or not raw_locations:
        print("❌ Error: Inputs cannot be empty.")
        return

    keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]
    locations = [l.strip() for l in raw_locations.split(",") if l.strip()]
    
    master_records = []
    print(f"\n🚀 Launching browser automation stack across a matrix of {len(keywords) * len(locations)} pairs...")

    async with async_playwright() as p:
        # headless=False enables you to watch the browser window execute on your desktop live!
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        for keyword in keywords:
            for location in locations:
                print(f"\n🔄 Fetching web layout for: [ {keyword} ] in [ {location} ]...")
                
                search_query = f"{keyword}+{location}".replace(" ", "+")
                target_url = f"https://www.google.com/maps/search/{search_query}"
                
                try:
                    await page.goto(target_url, timeout=60000)
                    await page.wait_for_timeout(4000)
                    
                    raw_text_content = await page.locator("body").inner_text()
                    
                    print("🧠 Calling Gemini semantic extraction brain...")
                    extracted_batch = await extract_leads_with_ai(raw_text_content, keyword, location)
                    
                    if isinstance(extracted_batch, list) and extracted_batch:
                        master_records.extend(extracted_batch)
                        print(f"✅ Isolated {len(extracted_batch)} leads successfully.")
                    else:
                        print("ℹ️ No leads extracted for this batch.")
                    
                    await asyncio.sleep(2)
                    
                except Exception as loop_error:
                    print(f"⚠️ Skipping batch due to loop error: {loop_error}")
                    continue
                    
        await browser.close()
        
    if master_records:
        print("\n💾 Compiling results matrix and mapping to Excel grid structures...")
        df = pd.DataFrame(master_records)
        output_excel_path = str(Path.home() / "Downloads" / "dynamic_agentic_master_leads.xlsx")
        df.to_excel(output_excel_path, index=False)
        print(f"🏆 Task Complete! Dynamic spreadsheet saved to user directory:\n👉 {output_excel_path}")
    else:
        print("\n❌ No structured dataset could be collected because the Gemini API quota is fully exhausted.")

if __name__ == "__main__":
    asyncio.run(run_hybrid_matrix_scraper())