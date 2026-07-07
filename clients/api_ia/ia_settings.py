from google import genai

class IA_settings:
    def __init__(self, key, MODEL_ID):
        self.key: str = key 
        self.MODEL_ID: str = MODEL_ID
        self.client = None
    
    def ia_client(self):
        if self.client is None:
            self.client = genai.Client(api_key=self.key)
        return self.client
    
    def config_tokens(self):
        return genai.types.GenerateContentConfig(max_output_tokens=300, temperature=0.5)
