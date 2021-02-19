# Sir Chattalot

![](chattalot.gif)

Sir Chattalot is a general knowledge, configurable chatbot. The knowledge set is based on the 'data.csv' file, so switch this out for any data set you wish* to get your own specialised knowledge chatbot.

**find all restrictions on this in the Personalisation section*

### Requirements 
[Python 3.5](https://www.python.org/downloads/) and above
[NumPy 1.19.x](https://numpy.org/install/) and above
[NLTK 3.5](https://www.nltk.org/install.html) and above
[scikit-learn-0.24.1](https://scikit-learn.org/stable/install.html) and above
[spaCy v3](https://spacy.io/usage) and above
[textdistance 4.2.1](https://pypi.org/project/textdistance/) and above

### Features
- Answer questions (based on data set)
- User name management
- Minimal small talk

### Installation
To install this program, just download the project files. These should all be in the same folder.

Required files:
- processor.py
- functions.py
- chat.py
- data.csv

### Usage
To run the program, follow these steps (from within the project folder):

1. Run `python processor.py`. This should take around 2-3* minutes (don't worry, you only need to do this once!) and generate 3 files:
  - bow.pickle
  - vocabulary.pickle
  - corpus.pickle
Once you have these 3 files, you do not need to do this step unless you change the dataset (**data.csv**).
2. Run `python chat.py`. This will start the program and you can begin chatting!

**If you change the data.csv file, this number will vary*

### Personalisation
Sir Chattalot can become an expert on any topic you wish. Simply change the data in the **data.csv** file, retrain the bot (run **processor.py** again) and you're good to go!

Please note:
- You must not change the name of this file.
- You must not change the structure of this file (questions must remain in column 2 and answers in column 3)

You can find a great list of datasets [here](https://github.com/ad-freiburg/large-qa-datasets).
