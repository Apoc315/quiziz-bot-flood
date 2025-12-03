import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style, init
from tqdm import tqdm
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from name_generator import NameGenerator
from logger import Logger

init()  # Initialize colorama

class QuizizzBotFlood:
    def __init__(self, game_code, bot_count=10, delay=1.5, headless=False, strategy='normal'):
        self.game_code = game_code
        self.bot_count = bot_count
        self.delay = delay
        self.headless = headless
        self.strategy = strategy
        
        self.driver = None
        self.name_generator = NameGenerator()
        self.logger = Logger()
        self.stats = {
            'connected': 0,
            'failed': 0,
            'total': bot_count
        }
        
    def setup_driver(self):
        """Setup Chrome driver with advanced options"""
        print(f"{Fore.CYAN}🚀 Setting up ChromeDriver...{Style.RESET_ALL}")
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')  # New headless mode
        
        # Anti-detection options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Performance options
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        
        # Window size
        chrome_options.add_argument('--window-size=1920,1080')
        
        # User agents pool
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        try:
            # Auto-download ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": random.choice(user_agents)
            })
            
            print(f"{Fore.GREEN}✅ ChromeDriver ready!{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to setup ChromeDriver: {e}{Style.RESET_ALL}")
            return False
    
    def join_game(self, username, attempt=1):
        """Join a Quizizz game with given username"""
        try:
            # Navigate to join page with game code
            self.driver.get(f'https://quizizz.com/join?gc={self.game_code}')
            
            # Random delay to appear human
            time.sleep(random.uniform(1.0, 2.5))
            
            # Try multiple selectors for name input
            selectors = [
                "input[placeholder*='name']",
                "input[placeholder*='Name']",
                "input[type='text']",
                "input[name='playerName']",
                "input#playerName"
            ]
            
            name_input = None
            for selector in selectors:
                try:
                    name_input = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not name_input:
                raise Exception("Could not find name input field")
            
            # Type username with human-like delays
            name_input.clear()
            for char in username:
                name_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))  # Human typing speed
            
            # Find submit button
            submit_selectors = [
                "button[type='submit']",
                "button:contains('Submit')",
                "button:contains('Join')",
                "button:contains('Play')",
                "button.join-button"
            ]
            
            submit_btn = None
            for selector in submit_selectors:
                try:
                    if 'contains' in selector:
                        # Simple text contains matching
                        buttons = self.driver.find_elements(By.TAG_NAME, "button")
                        for btn in buttons:
                            if any(word in btn.text for word in ['Submit', 'Join', 'Play']):
                                submit_btn = btn
                                break
                    else:
                        submit_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if submit_btn:
                submit_btn.click()
                time.sleep(random.uniform(1.0, 2.0))
                
                # Check for success indicators
                success_indicators = [
                    ".player-lobby",
                    ".waiting-room",
                    "[data-cy='lobby']",
                    ".game-lobby",
                    "div:contains('Waiting for host')"
                ]
                
                for indicator in success_indicators:
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, indicator))
                        )
                        return True
                    except:
                        continue
                
                # If we get here but no error, assume success
                return True
            else:
                raise Exception("Could not find submit button")
            
        except Exception as e:
            if attempt < 3:  # Retry up to 3 times
                print(f"{Fore.YELLOW}🔄 Retrying {username} (Attempt {attempt + 1})...{Style.RESET_ALL}")
                return self.join_game(username, attempt + 1)
            return False
    
    def start_flood(self):
        """Start the bot flood with progress bar"""
        print(f"{Fore.CYAN}🤖 Starting Bot Flood{Style.RESET_ALL}")
        print(f"{Fore.BLUE}🎮 Game Code: {self.game_code}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}👥 Target Bots: {self.bot_count}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}⏱️ Delay: {self.delay}s{Style.RESET_ALL}")
        print()
        
        if not self.setup_driver():
            return
        
        # Progress bar for bot joining
        with tqdm(total=self.bot_count, desc="Joining Bots", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            for i in range(self.bot_count):
                if i > 0:
                    # Open new tab for each bot
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                
                username = self.name_generator.generate()
                
                success = self.join_game(username)
                
                if success:
                    self.stats['connected'] += 1
                    self.logger.log_success(f"✅ {username} joined successfully!")
                else:
                    self.stats['failed'] += 1
                    self.logger.log_error(f"❌ {username} failed to join")
                
                # Update progress bar
                pbar.update(1)
                pbar.set_postfix({
                    'Success': self.stats['connected'],
                    'Failed': self.stats['failed']
                })
                
                # Delay between bots
                if i < self.bot_count - 1:
                    time.sleep(self.delay + random.uniform(-0.5, 0.5))  # Random variation
        
        # Show final statistics
        self.show_stats()
        
        # Keep browser open if not headless
        if not self.headless:
            input(f"\n{Fore.CYAN}🤖 Bot flood complete! Press Enter to close browsers...{Style.RESET_ALL}")
        
        self.driver.quit()
    
    def show_stats(self):
        """Display final statistics in a nice format"""
        success_rate = (self.stats['connected'] / self.stats['total']) * 100
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 BOT FLOOD STATISTICS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Connected: {self.stats['connected']}{Style.RESET_ALL}")
        print(f"{Fore.RED}❌ Failed: {self.stats['failed']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}📋 Total Attempted: {self.stats['total']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📈 Success Rate: {success_rate:.1f}%{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}🎮 Game Code: {self.game_code}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}⏱️ Total Time: ~{self.bot_count * self.delay:.1f} seconds{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        # Save stats to log
        self.logger.save_stats(self.stats)
