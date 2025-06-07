import re
from typing import List, Dict

class SafetyChecker:
    def __init__(self):
        self.redFlags = [
            r"kill(ing|ed|s)?myself",
            r"ending my life",
            r"suicid(e|al)",
            r"self-harm",
            r"self-harm(ed|ing)?",
        ]
        self.warningPatterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.redFlags]
        self.crisisResources = {
            "kenya": "1190 Suicide",
            "USA": "988 National",
            "UK": "0800 689 5652",
            "Canada": "1-833-456-4566",
            "Australia": "13 11 14",
            "India": "1860 266 2345",
            "South Africa": "0800 567 567",
            "Nigeria": "0809 234 1234",
            "Germany": "0800 111 0 111",
            "France": "01 45 39 40 00",
            "Japan": "03-5286-9090",
            "Brazil": "188 CVV",
            "Mexico": "800 911 2000",
            "Argentina": "135 SAPTEL",
            "Italy": "800 860 022",
            "Spain": "024",
            "Netherlands": "0900 0113",
            "Sweden": "020 22 00 60",
            "Norway": "116 123",
            "Finland": "010 19 012",
            "Russia": "8 800 2000 122",
            "China": "800 810 1117",
            "South Korea": "1393", 
        }
        
    def checkSafety(self, text: str) -> bool:
        """
        Check if the input text contains any red flags indicating potential self-harm or suicidal thoughts.
        
        Args:
            text (str): The input text to check for safety.
        
        Returns:
            bool: True if no red flags are found, False if any red flags are detected.
        """
        if not text.strip():
            return True
        
        for pattern in self.warningPatterns:
            if pattern.search(text):
                return False
        return True
    
    def getCrisisResources(self, countryCode: str) -> str:    
        """
        Get crisis resources based on the country code.
        
        Args:
            countryCode (str): The country code to look up resources.
        
        Returns:
            str: Crisis resource information or a default message if not found.
        """
        return self.crisisResources.get(countryCode, self.crisisResources.get["kenya"])
    
safetyChecker = SafetyChecker()

def checkSafety(text: str) -> bool:
    """
    Check if the input text is safe (does not contain red flags).
    
    Args:
        text (str): The input text to check.
    
    Returns:
        bool: True if the text is safe, False if it contains red flags.
    """
    return safetyChecker.checkSafety(text) 
        