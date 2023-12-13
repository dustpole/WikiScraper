# WikiScraper
*by Dustin Pollreis*

WikiScraper is a Python script that scrapes a given URL for words, filters out stop words, and creates a word list file.

## The why...
Wordlist creation is a tedious process and time consuming. My motivation in creating this script was to provide an easier was to create word-list files. These word-list files can then be used with programs such as hashcat as dictionaries and in the creation of combinations of with a pattern of characters in order to crack passwords. This process of cracking passwords based on dictionary/word-lists is prevalent in many CTF, Capture the Flag activities on sites such as NCL Cyber Skyline.

## Parameters
WikiScraper can use ran using the following four parameters. 

> ### url
> *Required parameter*
> This parameter requires a valid URL string.
> Example: https://en.uesp.net/wiki/Main_Page
_________________________________________________
> ### minimumlength  
> *Optional parameter*
> *Default: 1*
> This parameter is used to determine the minimum word length you wish to have added to your wordlist. This value needs to be an non-negative integer.
_________________________________________________
> ### outputfile
> *Optional parameter*
> *Default: 'wordlist.txt'*
> This parameter is used to determine the file name of the output text file created. This value does not need to include the file extension.
> Example: my_file
_________________________________________________
> ### stop_words_value
> *Optional parameter*
> *Default: no*
> This parameter is used to determine if the word-list file will have the common stop words filtered.
> These words include words that are common and may not be suitable to include in your word-list.  

_________________________________________________

*The stop word list used in this script was sourced from the following github.*
https://github.com/stopwords-iso/stopwords-en


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install WikiScraper.

```bash
pip install WikiScraper-dustpole
```


## Stand Alone Usage

```bash
python -m WikiScraper
```

## Stand Alone Usage - Example

```
python -m WikiScraper

Source URL to be scraped for words: 
https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon

Minimum character length of words in wordlist: 
2

Output wordlist filename: 
wordlist

Do you want to filter out common stop words? (yes, no): 
no
```

## Imported Module Usage

```python
import WikiScraper

WikiScraper.WordList(url, minimumlength, outputfile, stop_words_value)
```

## Imported Module Usage - Example

```python
import WikiScraper

WikiScraper.WordList(https://en.uesp.net/wiki/Main_Page, 2, wordlist, yes)
```

## How it works

I will go through the code in chunks to explain how it works.  


	
Lines 1-3 are used to show the author, version, name of the script.
```python
__author__ = "Dustin Pollreis (dustpole@gmail.com)"
__version__ = "1.1"
__all__ = ['WikiScraper']
```

Lines 6-17 are used to import the needed libraries with error detection.
```python
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
```

Lines 19-25 are used to define the class WordList and it's parameters.
```python
class WordList:

   def __init__(self, url, minimumlength=1, outputfile='wordlist', stop_words_value='no'):
      self.url = url
      self.outputfile = outputfile
      self.stop_words_value = stop_words_value
      self.minimumlength = minimumlength
```

Lines 27-37 are used in handling the minimum length parameter. The value is verified as valid and also converted to an integer from a string. To determine if the parameters value is valid it checks weather it is an integer type object and also that the integer is greater than 0. If not valid a TypeError is raised.

```python
      # Convert minimumlength to an integer.
      try:
          minimumlength = int(minimumlength)
      except:
          raise TypeError('Invalid minimum word length.')  
  
      def Verify_minimumlength(minimumlength):
         if not isinstance(minimumlength, int) or minimumlength < 0:
            raise TypeError('Invalid minimum word length.')

      Verify_minimumlength(minimumlength)
```

Lines 40 -45 are used in handling the URL parameter. The value is verified as valid by the use of the Requests library's "status_code" functionality. The URL is supplied to the status_code function and if the HTTP response code is equal to 200 (successful) it is considered a valid url. If not valid a ValueError is raised.
```python
      # Verify URL is valid.
      def Verify_URL(url):
         if requests.get(url).status_code != 200:
            raise ValueError('Invalid URL.')
      Verify_URL(url)
```

Lines 47-52 are use in handling the stop_words_value parameter. This value is verified as valid by comparing it to the strings 'yes' and 'no'. If the value is not one of those it is considered not valid and a ValueError is raised.
```python
      # Verify Stop Words Value.
      def Verify_Stop_Words_Value(stop_words_value):
         if stop_words_value not in ('yes', 'no'):
            raise ValueError("Invalid filter option value. (Allowed values yes/no)")

      Verify_Stop_Words_Value(stop_words_value)
```

Lines 54-58 hand the opening of a stop_words_file if the stop_words_value parameter was 'yes'. The importlib library is used to access the english.txt file included in the WikiScraper module. This text file is then opened and added to a list separating each line into an item.
```python
      # Open Stop Words List.
      if stop_words_value == 'yes':
            stop_words_file = (impresources.files(stop_lists) / 'english.txt')
            with stop_words_file.open('r', encoding='utf8') as file:
               stop_words_list = file.read().splitlines()
```

Lines 60-67 are used to retrieve the html data from the URL specified in the URL parameter using the requests library. The retrieve html data is then parsed for any string/text and added to a string. A blank words_filtered list is also created for use later in the code.
```python
      page = requests.get(url)

      # Parses out text into a string from html.
      soup = BeautifulSoup(page.text, 'html.parser')

      text_orig = soup.text  

      words_filtered = []
```

Lines 69-80 are used to process the list of text string created by the previous lines. This processing includes removing any characters that are of not of an ascii hex value of 0x00-0x7f. This process leverages the regex library to remove this characters of a string when compared to a specified pattern/criteria. The resulting string then has all 'new line' characters replaced with a space and turned lowercase. Next a list is created from the string separating items  by the space character. Lastly the resulting list has any non alpha-characters removed using a lambda function.
```python
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
```

Lines 82-92 are used to filter the list_orig list by removing any items that are alike when comparing the list_orig with the stop_words_list. The items are also filtered at this point to include only items that are at least as many characters as the value of the minimumlength parameter. These filtered items are then appended to the words_filtered list and sorted.
```python
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
```

Lines 95-103 are used to open a text file with the name being the value of the outputfile parameter. This file will be located in the current working path that you ran the WikiScraper module. The file is then wrote to with the words_filtered list with each item on a separate line. After which the file is closed.
```python
      # Save words list as a wordslist.txt file with each item on it's own line.
      outputfile = outputfile + '.txt'
      script_dir = os.getcwd() + '\\'
      file_path = script_dir + outputfile
      with open(file_path, mode='wt', encoding='utf-8') as wordlist_file:
         wordlist_file.write('\n'.join(words_filtered))
      # Close Open File.
      wordlist_file.close()
```

Lines 105-109 are used to specify a completion function and to return that function which includes that the word-list was created successfully and the full file path in which is located on your computer.
```python
      def print_info():
         print(f'Word list created. \n{file_path}')

      # Confirmation of successful execution and the destination output file's path.
      return print_info()
```

Lines 111 to 126 are used to declare what code should execute when ran as a Script, but not when it’s imported as a module. This includes input prompts and example comments for each of the parameters and a line that runs the WordList class with those provided parameters.
```python
if __name__ == "__main__":

   url = input('Source URL to be scraped for words: \n')
   # url = 'https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon'

   minimumlength = input('Minimum character length of words in wordlist: \n')
   # minimumlength = 1

   outputfile = input('Output wordlist filename: \n')
   # outputfile = 'wordlist'

   stop_words_value = input('Do you want to filter out common stop words? (yes, no): \n')
   # stop_words_file = 'yes'

   WordList(url, minimumlength, outputfile, stop_words_value)
```


### Code Flow Graph 
*Generated by codetoflow.com* 

[Code Flow](https://github.com/dustpole/WikiScraper/blob/31ae8d3e7af143a65eb672c5458f0b129b2b8e0a/codetoflow.png)
## License

[MIT](https://choosealicense.com/licenses/mit/)
