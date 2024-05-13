from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

class Anki:
    def __init__(self,word,deck_name):
        self.word = word
        self.deck_name = deck_name
        self.HTML = self.get_HTML()

    def get_HTML(self):
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'https://www.tagalog.com/dictionary/#{self.word}')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'search_result1')))
            link = driver.find_element(By.XPATH,"//a[@id='search_result1']")
            link.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'definitionbox')))
            return BeautifulSoup(driver.page_source, 'html.parser')
        finally:
            driver.quit()

    def get_translation(self):
        translation = self.HTML.find('div', id='definitionbox')
        return translation.text

    def get_sentence(self):
        sentence = self.HTML.find('div', class_='example-sentence-cell')
        return sentence.text
    
    def get_sentence_translation(self):
        sentence = self.HTML.find('div', class_='example-sentence-translation')
        return sentence.text

    def get_word_audio(self):
        translation = self.HTML.find('div', id='definitionbox')
        audio = translation.previous_sibling.previous_sibling
        audio_id = (audio.attrs['id'])[5:]
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'https://www.tagalog.com/get_audio_file.php?id={audio_id}')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
            HTML = BeautifulSoup(driver.page_source, 'html.parser')
            source = HTML.find('source').attrs['src']
            r = requests.get(source)
            with open(f'C:/Users/thede/AppData/Roaming/Anki2/User 1/collection.media/{self.word}.mp3', 'wb') as f:
                f.write(r.content)
            return f'[sound:{self.word}.mp3]'
        finally:
            driver.quit()

    def get_sentence_audio(self):
        sentence = self.HTML.find('div', class_='example-sentence-cell')
        audio = sentence.find('a').next_sibling
        audio_id = (audio.attrs['id'])[5:]
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'https://www.tagalog.com/get_audio_file.php?id={audio_id}')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
            HTML = BeautifulSoup(driver.page_source, 'html.parser')
            source = HTML.find('source').attrs['src']
            r = requests.get(source)
            with open(f'C:/Users/thede/AppData/Roaming/Anki2/User 1/collection.media/{self.word}_sentence.mp3', 'wb') as f:
                f.write(r.content)
            return f'[sound:{self.word}_sentence.mp3]'
        finally:
            driver.quit()

    def add_anki_card(self, model_name):
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Word": self.word,
                        "Translation": self.get_translation(),
                        "Sentence": self.get_sentence(),
                        "Sentence Translation": self.get_sentence_translation(),
                        "Word Audio": f"[sound:{self.word}.mp3]",
                        "Sentence Audio": f"[sound:{self.word}_sentence.mp3]",
                    },
                    "options": {
                        "allowDuplicate": False
                    },
                    "tags": []
                }
            }
        }
        requests.post('http://localhost:8765', json=payload)

if __name__ == '__main__':
    list_of_words = ['aking','kape','ay','pait','kanya','mga','kaibigan','kasama','ito','tamis','agahan','mansanas','asim','na','alat','hindi','ka','ano man','uri']
    deck_name = 'Tagalog Vocab'
    for word in list_of_words:
        try:
            card = Anki(word,deck_name)
            card.get_word_audio()
            card.get_sentence_audio()
            card.add_anki_card("Tagalog English")
            card.add_anki_card("English Tagalog")
            print(f'{word} added to Anki')
        except:
            print(f'Failed to add {word} to Anki')
