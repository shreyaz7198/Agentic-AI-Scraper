import os
import sys
import asyncio
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, Field
from browser_use import Agent, ChatGoogle

# --- 1. SYSTEM ENVIRONMENT HANDSHAKE ---
if not os.environ.get("GOOGLE_API_KEY"):
    print("\n" + "="*60)
    print("❌ SYSTEM CONFIGURATION ERROR: GOOGLE_API_KEY IS MISSING!")
    print("="*60)
    print("To fix this, map your key inside your terminal:")
    print("👉 $env:GOOGLE_API_KEY='your_actual_api_key_here'")
    print("="*60 + "\n")
    sys.exit(1)

# --- 2. STRUCTURED DATA SCHEMAS (Requirement 4 & 5) ---
class BusinessLead(BaseModel):
    searched_keyword: str = Field(description="The exact keyword used to uncover this lead")
    target_location: str = Field(description="The target city/location where the search took place")
    name: str = Field(description="The business profile name")
    contact_number: str = Field(description="Phone number found, or empty string if not listed")
    address: str = Field(description="The complete structural physical address map locator")
    website: str = Field(description="The business website landing link, or empty string if none")

class LeadDataCollection(BaseModel):
    leads: list[BusinessLead]

# --- 3. MAIN AGENT CORE PIPELINE ---
async def run_fully_agentic_scraper_v5():
    print("\n📋 --- Dynamic Pure-Agentic Scraper Matrix ---")
    print("💡 Senior Note: Free keys have a strict daily limit of 20 operations.\n")
    
    # Capture user inputs dynamically (Requirement 1)
    raw_keywords = input("🔍 Enter Search Keywords (separated by commas, e.g., DRDO, IIM): ").strip()
    raw_locations = input("📍 Enter Target Locations (separated by commas, e.g., Nagpur, Pune): ").strip()
    
    if not raw_keywords or not raw_locations:
        print("❌ Operational Halt: Input arrays cannot be left empty!")
        return

    # Turn raw input into clean, whitespace-free Python lists
    keywords = [k.strip() for k in raw_keywords.split(",") if k.strip()]
    locations = [l.strip() for l in raw_locations.split(",") if l.strip()]
    
    # Proactive QA Safeguard: Limit dynamic inputs to avoid rapid quota depletion
    if len(keywords) > 2 or len(locations) > 2:
        print("\n⚠️  QA Threshold Guard Activated!")
        print("To protect your free tier from crashing instantly, please use a maximum of 2 keywords and 2 places.")
        return

    # Build the plain English combinatorial task matrix (Requirement 2 & 3)
    task_instructions = f"""
    Go to Google Maps (https://www.google.com/maps).
    You must process these targets completely:
    - Keywords: {", ".join(keywords)}
    - Locations: {", ".join(locations)}
    
    Instructions:
    1. For each combination of keyword and location, search for them in the Google Maps search bar.
    2. Visually scan the left-hand results list and get the top 3 businesses for each combination.
    3. Requirement #5 (Pure Agentic): You MUST click on each of the top 3 businesses individually so their slide-out details panel opens up. Read that panel to extract their phone number and website link.
    4. Fill out the LeadDataCollection schema with the fields.
    5. Once all variations are processed, call done.
    """

    print(f"\n🔄 Compiling instructions for a total of {len(keywords) * len(locations)} search batches...")
    
    # Initialize the LLM Engine wrapper
    llm = ChatGoogle(model='gemini-2.5-flash')
    
    # Initialize the master agent pilot
    agent = Agent(
        task=task_instructions,
        llm=llm,
        use_vision=True,               # Gives the AI eyes to read the layout contextually
        output_model_schema=LeadDataCollection
    )
    
    print("🚀 Launching Chrome window... (Watch the AI execute clicks on your screen live)")
    
    try:
        # Run the agentic loop
        history = await agent.run()
        final_result = history.final_result()
        
        if final_result:
            parsed_data = LeadDataCollection.model_validate_json(final_result)
            leads_list = [lead.model_dump() for lead in parsed_data.leads]
            
            if leads_list:
                df = pd.DataFrame(leads_list)
                output_excel_path = str(Path.home() / "Downloads" / "dynamic_agentic_master_leads.xlsx")
                df.to_excel(output_excel_path, index=False)
                
                print("\n" + "🏆" * 20)
                print(f"🎉 SUCCESS! PIPELINE COMPLETE.\n👉 Excel generated at: {output_excel_path}")
                print("🏆" * 20 + "\n")
                return

        print("\nℹ️  Process ended normally, but no business data was collected by the agent.")

    # --- 4. GRACEFUL API INSTABILITY EXCEPTION PROTECTION ---
    except Exception as error_context:
        error_string = str(error_context)
        
        print("\n" + "!" * 60)
        print("🚨 AGENT ENCOUNTERED A RUNTIME BARRIER")
        print("!" * 60)
        
        # Intercept and catch the exact 429 quota exhaustion string natively
        if "429" in error_string or "RESOURCE_EXHAUSTED" in error_string:
            print("❌ GOOGLE API ERROR: 429 - RESOURCE QUOTA EXHAUSTED!")
            print("-" * 60)
            print("Why this happened:")
            print("You are utilizing a Free Tier Gemini API key. Google restricts this key")
            print("to 20 operations per day. Because 'Pure Agentic (Option B)' requires the AI")
            print("to take a full image screenshot for every single action (opening panels, scrolling),")
            print("the framework reached your daily limit mid-run.")
            print("-" * 60)
            print("💡 Senior Engineer Recommendation:")
            print("1. Wait for Google's 24-hour window to automatically refresh your free token quota.")
            print("2. Or go to Google AI Studio, click 'Create API Key in a NEW Project', and use that fresh key.")
        else:
            # Handle standard browser/runtime anomalies gracefully
            print(f"❌ Automation Engine Error: {error_string}")
            
        print("!" * 60 + "\n")

if __name__ == "__main__":
    # Change to True later if you want it to run entirely in the background
    # Note: browser-use looks at the internal loop parameters natively.
    asyncio.run(run_fully_agentic_scraper_v5())