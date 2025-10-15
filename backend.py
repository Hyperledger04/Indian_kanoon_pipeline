import json
import time
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from urllib.parse import urlparse, parse_qs
import logging

# --- Selenium/Scraping Imports ---
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, WebDriverException
# -----------------------------------

# --- Initialization & Configuration ---
app = Flask(__name__)

# CORS configuration for production
CORS(app, resources={
    r"/scrape": {
        "origins": ["*"],  # Update with your GitHub Pages URL for production
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Setup logging to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Core Scraper Class ---

class KanoonScraper:
    def __init__(self, webhook_url=None):
        """Initialize the scraper with optional webhook URL"""
        self.webhook_url = webhook_url
        self.driver = None
    
    def setup_driver(self):
        """Setup Chrome driver with options for Railway/production deployment"""
        logger.info("=== SETTING UP CHROME DRIVER (PRODUCTION) ===")
        
        options = Options()
        
        # Essential for running in headless/containerized environments
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080") 
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Production environment detection
        is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
        is_docker = os.path.exists('/.dockerenv')
        
        options.page_load_strategy = 'normal'
        
        try:
            if is_railway or is_docker:
                # Railway/Docker: Use system Chrome
                logger.info("Running in containerized environment (Railway/Docker)")
                options.binary_location = "/usr/bin/chromium"
                service = Service("/usr/bin/chromedriver")
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                # Local development: Use local ChromeDriver
                logger.info("Running in local development mode")
                self.driver = webdriver.Chrome(options=options)
            
            logger.info("✓ ChromeDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"✗ Failed to initialize ChromeDriver: {e}")
            raise
        except Exception as e:
            logger.error(f"✗ Unexpected error during driver setup: {e}")
            raise

    def scrape_search_results(self, search_url, max_documents=None):
        """Scrape all judgment links from Indian Kanoon search results"""
        logger.info(f"=== Finding judgment links for: {search_url} ===")
        
        try:
            self.driver.get(search_url)
            time.sleep(3)
            
            judgment_links = self.driver.find_elements(By.XPATH, "//div[@class='result_title']//a")
            
            total_links = len(judgment_links)
            logger.info(f"Found {total_links} total judgment links")
            
            if max_documents and total_links > max_documents:
                judgment_links = judgment_links[:max_documents]
                logger.info(f"Limited processing to the first {max_documents} documents.")
            
            judgment_urls = []
            for link in judgment_links:
                url = link.get_attribute('href')
                if url:
                    judgment_urls.append(url)
            
            logger.info(f"Extracted {len(judgment_urls)} valid document URLs to process.")
            return judgment_urls
            
        except Exception as e:
            logger.error(f"Error in scrape_search_results: {e}")
            return []

    def scrape_judgment_text(self, judgment_url):
        """Scrape the full text of a single judgment"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get(judgment_url)
            
            wait = WebDriverWait(self.driver, 30)
            
            if "search" in self.driver.current_url:
                logger.warning(f"Link {judgment_url} redirected to a search page. Skipping.")
                raise Exception("Link redirected to a search page or was not a document.")
            
            judgment_div = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "judgments"))
            )
            
            judgment_html = judgment_div.get_attribute('innerHTML')
            soup = BeautifulSoup(judgment_html, 'html.parser')
            judgment_text = soup.get_text(separator='\n', strip=True)
            
            lines = judgment_text.split('\n')
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            cleaned_judgment = '\n'.join(cleaned_lines)
            
            logger.info(f"✓ Successfully scraped judgment ({len(cleaned_judgment)} characters)")
            
            return {
                'url': judgment_url,
                'full_text': cleaned_judgment,
                'status': 'success'
            }
            
        except TimeoutException:
            logger.error(f"✗ Error scraping judgment {judgment_url}: Timed out")
            return {
                'url': judgment_url,
                'full_text': None,
                'status': 'failed',
                'error': "Timeout waiting for judgment content"
            }
        except Exception as e:
            logger.error(f"✗ Error scraping judgment {judgment_url}: {e}")
            return {
                'url': judgment_url,
                'full_text': None,
                'status': 'failed',
                'error': str(e)
            }

    def send_to_webhook(self, data):
        """Send judgment data to n8n webhook"""
        if not self.webhook_url:
            logger.warning("No webhook URL configured")
            return False
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Kanoon-Scraper-Selenium/1.0'
            }
            
            payload = {
                "source": "KanoonScraper",
                "case_url": data['url'],
                "full_judgment_text": data['full_text'],
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✓ Webhook SUCCESS. Status: {response.status_code}")
                return True
            else:
                logger.error(f"✗ Webhook FAILED. Status: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error("✗ Webhook request timed out")
            return False
        except Exception as e:
            logger.error(f"✗ Critical error sending to webhook: {e}")
            return False
    
    def close(self):
        """Close the browser connection"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
            logger.info("✓ Browser closed")

# --- Flask Routes ---

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Indian Kanoon Scraper"}), 200

@app.route('/scrape', methods=['POST', 'OPTIONS'])
def scrape_indian_kanoon_api():
    """API endpoint to trigger the scraping and webhook process"""
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.json
    search_url = data.get('url')
    webhook_url = data.get('webhook_url')
    max_documents = data.get('max_documents', 5)

    if not search_url or not webhook_url:
        return jsonify({
            "error": "Both 'url' (Indian Kanoon search) and 'webhook_url' (n8n) are required."
        }), 400
    
    scraper = None
    results = {
        "success": False,
        "total_urls_found": 0,
        "total_webhooks_sent": 0,
        "n8n_results": []
    }
    
    try:
        scraper = KanoonScraper(webhook_url=webhook_url)
        scraper.setup_driver()
        
        judgment_urls = scraper.scrape_search_results(search_url, max_documents=max_documents)
        results["total_urls_found"] = len(judgment_urls)
        
        if not judgment_urls:
            return jsonify({
                "success": True, 
                "message": "No judgment URLs found on the search page.", 
                "details": results
            }), 200

        total_webhooks_sent = 0
        for i, url in enumerate(judgment_urls):
            logger.info(f"Processing {i+1}/{len(judgment_urls)}: {url}")
            
            judgment_data = scraper.scrape_judgment_text(url)
            
            if judgment_data['status'] == 'success':
                if scraper.send_to_webhook(judgment_data):
                    total_webhooks_sent += 1
                    results["n8n_results"].append({"url": url, "status": "SENT"})
                else:
                    results["n8n_results"].append({"url": url, "status": "WEBHOOK_FAILED"})
            else:
                results["n8n_results"].append({
                    "url": url, 
                    "status": "SCRAPE_FAILED", 
                    "error": judgment_data.get('error')
                })
            
            if i < len(judgment_urls) - 1:
                time.sleep(2)

        results["success"] = True
        results["total_webhooks_sent"] = total_webhooks_sent
        results["message"] = f"Successfully scraped and posted {total_webhooks_sent} judgments to n8n."
        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Critical execution error: {e}")
        return jsonify({
            "success": False, 
            "error": str(e), 
            "message": "Critical server error"
        }), 500
        
    finally:
        if scraper:
            scraper.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("----------------------------------------------------------------------")
    print(f"  FLASK SCRAPER API STARTING ON PORT {port}...")
    print(f"  Environment: {'PRODUCTION' if os.environ.get('RAILWAY_ENVIRONMENT') else 'DEVELOPMENT'}")
    print("----------------------------------------------------------------------")
    app.run(host='0.0.0.0', debug=False, port=port)

