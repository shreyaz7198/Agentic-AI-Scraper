# Dynamic Hybrid Agentic Scraper 🚀

An enterprise-grade, hybrid Web Automation and AI Extraction engine built with **Python 3.14+**, **Playwright**, and **Google Gemini 2.5 Flash**. 

This script accepts dynamic search keywords and target locations directly from the terminal console, executes automated web browsing routines natively via Playwright to preserve API token quotas, and leverages Gemini's computer vision to contextually extract business details (Names, Contacts, Addresses, and Websites) without relying on fragile HTML XPaths or CSS class selectors.

---

## 🛠️ Key Architectural Features

* **Dynamic Matrix Processing:** Accepts multiple comma-separated keywords and locations at runtime, automatically calculating and running all combinatorial search variations.
* **Hybrid Execution Stack:** Utilizes local Playwright loops for browser navigation and page queries (completely free), calling the Gemini API exclusively for the final semantic extraction data layer to efficiently maximize Free Tier resource ceilings.
* **Proactive Exception Shielding:** Includes structural fallback intercepts for `429 RESOURCE_EXHAUSTED` and rate-limiting blocks, outputting clean user warnings on the console instead of standard unhandled Python tracebacks.
* **Production Excel Grid Generation:** Bypasses framework file system restrictions by streaming data arrays back into local Python memory via a strict `Pydantic` schema, outputting a polished `.xlsx` spreadsheet straight to your physical machine's `Downloads` folder.

---

## ⚙️ Prerequisites & Installation

Ensure you are inside your project's virtual environment (`venv`) before initializing setups:

```powershell
# 1. Activate your virtual environment sandbox
.\venv\Scripts\Activate.ps1

# 2. Install the necessary production dependencies
pip install google-genai playwright pandas openpyxl pydantic browser-use

# 3. Download the system Chromium browser binaries required by Playwright
playwright install chromium
