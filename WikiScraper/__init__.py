__author__ = "Dustin Pollreis (dustpole@gmail.com)"
__version__ = "1"
__all__ = ['WikiScraper']


# Import modules needed for WikiScraper.
try:
         import requests
         from bs4 import BeautifulSoup
         from pathlib import Path
         import re
         import os
         from importlib import resources as impresources
         # relative-import of WikiScraper containing the stop_lists resources.
         from . import stop_lists
except ImportError:
         raise ImportError('Import Error')

class WordList:

   def __init__(self, url, minimumlength=1, outputfile='wordlist', stop_words_value='no'):
      self.url = url
      self.outputfile = outputfile
      self.stop_words_value = stop_words_value
      self.minimumlength = minimumlength

      # Convert minimumlength to an integer.
      try:
          minimumlength = int(minimumlength)
      except:
          raise TypeError('Invalid minimum word length.')  

      def Verify_minimumlength(minimumlength):
         if not isinstance(minimumlength, int) or minimumlength < 0:
            raise TypeError('Invalid minimum word length.')
      
      Verify_minimumlength(minimumlength)
      

      # Verify URL is valid.
      def Verify_URL(url):
         if requests.get(url).status_code != 200:
            raise ValueError('Invalid URL.')
      
      Verify_URL(url)

      # Verify Stop Words Value.
      def Verify_Stop_Words_Value(stop_words_value):
         if stop_words_value not in ('yes', 'no'):
            raise ValueError("Invalid filter option value. (Allowed values yes/no)")

      Verify_Stop_Words_Value(stop_words_value)

      # Open Stop Words List.
      if stop_words_value == 'yes':
            stop_words_file = (impresources.files(stop_lists) / 'english.txt')
            with stop_words_file.open('r', encoding='utf8') as file:
               stop_words_list = file.read().splitlines()

      page = requests.get(url)

      # Parses out text into a string from html.
      soup = BeautifulSoup(page.text, 'html.parser')

      text_orig = soup.text

      words_filtered = []

      # Remove ASCII characters above value 7f.
      text_orig = re.sub(r'[^\x00-\x7f]',r'', text_orig) 

      # Convert text to lowercase.
      text_lower = text_orig.lower()
      # Replace new-line in text with a space.
      text_lower = text_lower.replace('\n', ' ')
      # Create a list from text by splitting it on spaces.
      list_orig = text_lower.split(' ')

      # Remove non-alpha items from list.
      list_orig = list(filter(lambda x: ( x.isalpha() == 1), list_orig))

      # Filter list by removing duplicates, words less than 2-characters and words found in the stop words list.
      for i in list_orig:
         if stop_words_value == 'no': 
            if i not in words_filtered and len(i) >= minimumlength:
                  words_filtered.append(i)
         else:
            if i not in words_filtered and i not in stop_words_list and len(i) >= minimumlength:
               words_filtered.append(i)

      # Sort filtered words list.
      words_filtered.sort()


      # Save words list as a wordslist.txt file with each item on it's own line.
      outputfile = outputfile + '.txt'
      script_dir = os.getcwd() + '\\'
      file_path = script_dir + outputfile
      with open(file_path, mode='wt', encoding='utf-8') as wordlist_file:
         wordlist_file.write('\n'.join(words_filtered))
      
      # Close Open File.
      wordlist_file.close()
    
      def print_info():
         print(f'Word list created. \n{file_path}')

      # Confirmation of successful execution and the destination output file's path.
      return print_info()
   
if __name__ == "__main__":

   url = input('Source URL to be scraped for words: \n') 
   # url = 'https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon'

   minimumlength = input('Minimum character length of words in wordlist: \n')
   # minimumlength = 2

   outputfile = input('Output wordlist filename: \n')
   # outputfile = 'wordlist'

   stop_words_value = input('Do you want to filter out common stop words? (yes, no): \n')
   # stop_words_file = 'yes'


   WordList(url, minimumlength, outputfile, stop_words_value)