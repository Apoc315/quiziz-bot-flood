import requests
from colorama import Fore, Style, init
from datetime import datetime

init()

class QuizizzGameChecker:
    def __init__(self, game_code):
        self.game_code = game_code
        self.status = {}
    
    def check_game(self):
        """Check if game exists and get status"""
        print(f"{Fore.CYAN}🎮 Checking game: {self.game_code}{Style.RESET_ALL}")
        
        try:
            url = f"https://quizizz.com/join/game/{self.game_code}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                if "game not found" in response.text.lower() or "invalid" in response.text.lower():
                    self.status = {
                        'exists': False,
                        'message': 'Game not found or invalid code',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                else:
                    self.status = {
                        'exists': True,
                        'message': 'Game exists and is joinable',
                        'url': url,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'players': 'Unknown',  # Would need more advanced parsing
                        'status': 'Waiting for players'
                    }
                return True
            else:
                self.status = {
                    'exists': False,
                    'message': f'HTTP Error {response.status_code}',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return False
                
        except requests.exceptions.Timeout:
            self.status = {
                'exists': False,
                'message': 'Request timeout - check your connection',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return False
        except Exception as e:
            self.status = {
                'exists': False,
                'message': str(e),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return False
    
    def display_status(self):
        """Display game status in terminal"""
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎮 GAME STATUS CHECK{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        if self.status.get('exists'):
            print(f"{Fore.GREEN}✅ {self.status['message']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}🔗 URL: {self.status.get('url', 'N/A')}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}👥 Players: {self.status.get('players', 'Unknown')}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}📊 Status: {self.status.get('status', 'Unknown')}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ {self.status.get('message', 'Unknown error')}{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}🕐 Checked at: {self.status.get('timestamp', 'N/A')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
