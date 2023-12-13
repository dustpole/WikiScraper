# WikiScraper

WikiScraper is a Python module for creating custom word-lists from a webpage.

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

WikiScraper.WordList(https://en.wikipedia.org/wiki/List_of_Pok%C3%A9mon, 2, wordlist, yes)
```



## License

[MIT](https://choosealicense.com/licenses/mit/)