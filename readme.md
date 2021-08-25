# Job Generator
#### R. Holley, August 2021

Several months ago, I decided to learn how to web scrape - [so I did.](https://github.com/MementoMakoMori/ScrapingPractice) Then I scraped some data that was interesting to me: descriptions from online job posts with 'data science' as the search filter. **After filtering out duplicates,** I ended up with 848 job descriptions.<sup>1</sup>

In R, I played around with the text data to make pretty charts of which data tools were mentioned most frequently. In Python, I decided to get a bit more creative and train a neural net on the job description texts.

## A Basic Neural Net
Neural nets are fun and easy to implement. There are a lot of great libraries available for training neural nets on text; I chose to use [textgenrnn.](https://github.com/minimaxir/textgenrnn)

Here are the config parameters I used for basic word-level training:
```python
model_cfg = {
    'rnn_size': 128, # number of LSTM cells per layer
    'rnn_layers': 3, # number of LSTM layers
    'rnn_bidirectional': False, # this could help, but will also make each epoch longer
    'max_length': 7, # number of tokens to consider for prediction the next token
    'max_words': 10000,
    'word_level': True} # neural net could be trained at the word level or character level

train_cfg = {
    'line_delimited': True, # each text is its own line in the .txt file
    'num_epochs': 30, # I'm impatient; ~50 epochs would give me better results
    'gen_epochs': 10, # generate example output in the console every x number of epochs
    'batch_size': 1024,
    'train_size': 0.8, # I could use the other 0.2 of data for validation
    'validation': False, # but I won't because this is just for fun, not for reaching some accuracy metric
    'dropout': 0.05, # ignore a proportion of source tokens each epoch
    'max_gen_length': 400, # the average number of words per job description was 588, I want it a bit smaller
    'is_csv': False}
```

Running on my PC, each epoch took ~ 1:20 minutes for a total runtime of 38 minutes.
Here's some output after the final epoch:
```text
titan america, llc s a data science team is committed to help our communities grow through and refine it. our technology platform that enhance the financial aspects of our work. other information is made to a diverse organization, culture, you will be the world in the azure. do you make an impact on the measurement of your data, analytics, and engineering teams to build tools, maximize the performance of their credit risk. position is all based on one - year program. the data science librarian will be used for all applications to build the models and datasets supporting the sales team and an individual should have a bachelor s degree in computer science, mathematics, statistics or related field.
```
That's okay, but it could be better. I decided to train a new model with character-level training to see what kind of differences may appear (with the config settings appropriately tweaked). I also decided to be a tiny bit more patient and up the epochs to 25. The character sequence length was set to only 20, but that still meant nearly 2.5 **million** sequences to train on! Maybe I should have stuck with only 20 epochs, because each epoch in this training took around 15 minutes.  

The most noticeable change is the inclusion of uppercase letters; in word-level training, the text is converted to all lowercase so that identical words with different capitalization are counted as the same token.

Here's some character-level output:
```text
At Best Employee Store organizations management to helping certification in written and oral communications. Conferences (i.e., Advantal Education & Experience BS end-to-end your patience for the general (Tableau) Experience creating audiences - collaborate with stakeholders will be Dirrond qualifi
```

## Jobs in a Galaxy Far, Far Away
Those first few neural nets were fun and all, but do I really want to look at more job descriptions? I already do that all day! Instead of looking at job posts here on earth, I'd rather see what jobs are available in a galaxy far, far away.

### Wookieepedia <img src="https://static.wikia.nocookie.net/starwars/images/e/e6/Site-logo.png/revision/latest?cb=20210602103636" width="150" height="150">

'Wookieepieda' is the [online, fan-maintained Star Wars wiki.](starwars.wikia.com)<sup>2</sup> There is an entire category for 'Occupations' in the Star Wars wiki, so I grabbed those articles with [a pywikibot.](https://doc.wikimedia.org/pywikibot/master/index.html) Cleaning the article text was a bit involved because I only wanted the paragraph content, with no section headers or references. The code for grabbing the articles with the bot and cleaning them into a text file is in [wookiee/sw_jobs.py file](https://github.com/MementoMakoMori/JobGenerator/tree/master/wookiee/sw_jobs.py).

Grabbing both the 'Canon' (according to Disney) and 'Legends' (pre-Disney Expanded Universe) articles got me 981 texts. It's important to note that many articles have both a 'Canon' *and* a 'Legends' version, and each version is counted as a separate text. Only using 'Canon' articles could lead to different results, but to get started I included both types of articles.

Here's an example of duplicate articles for 'Flight Instructor':
```text
Canon: A flight instructor was an individual who trained pilots. During the Clone Wars, Mandalorian Protector Fenn Rau served as a flight instructor for the Grand Army of the Republic. Goran and Vult Skerris served as instructors at Skystrike Academy, an Imperial Academy on Montross. Jake Farrell served as a flight instructor for the Galactic Empire before retiring on Derango 4. Yurib Nakan served as a flight instructor at the Imperial Academy on Carida.
```
```text
Legends: A flight instructor, also known as pilot trainers, were individuals who trained other beings how to fly.T'Charek Haathi served as a flight instructor for the Alliance to Restore the Republic. Ohwun De Maal was a freelance flight instructor who would teach anyone who could pay how to fly.
```

### Job-Star Wars Combo Net
Next, I combined the Star Wars articles with the job descriptions into one .txt file to feed the neural net. I specifically chose word-level training as there are many unique words in Star Wars that may throw a wrench in into the model learning 'correct' English character patterns. I decided a project of this importance was worth waiting for, so I upped the epochs to 75.

75 epochs later, here is what I got:
```text
geospatial analytics, novel, model and culture design. you will need to ship these complex datasets using siri to build algorithms to manage data to improve predictive modeling solutions in the global business and build department with mattel enterprise. 
support the application of this position, this role will be able to closely with the engineering manager of statisticians, statistics experience in data locations. 
basic knowledge of skills * preferred qualifications: strong computer languages and has python for analysis platforms experience with big data processing (preferred) ability to query languages such as cyber, language, 
decision trees, or. deliver clustering and testing with flexibility to their ability and a minimum qualifications and have experience with nlp / programming languages. 
knowledge of aws services such as a deep learning based on business intelligence projects, it could be providing support the highest - public rank or in - use this line, rank of commander within the double - command of alliance commander and assigned the title. high colonels ranked below senior / or below two (for federal, service) is preferred. 
minimum 3. basic qualifications: related an earned. sql programming experience, data analysis, and other healthcare data visualization software is a proven ability to work on some of the, 
go to have a lot of going field that could be on the policy of the black, the black sun and the old order to help the first order to hide the eternal fleet defense, enabling reference to protection.
```

Everything is pretty standard job-post jargon until the very end (Black Sun is a large smuggling organization in Star Wars, the First Order is a classic space-fascist enemy). Something I saw over and over with these generated examples are sections that are clearly 'job-related' or 'Star Wars-related', but rarely did the two types mix.

Congratulations to me! I accidentally made an *unsupervised binary classifier*. I fed the neural net a single dataset consisting of two types of data, and the word generator (correctly) learned that Star Wars-y words only occur with other Star Wars-y words, and the same is true for the job-related words.

### An Elegant Model for a More Civilized Age
#### - Obi-wan Kenobi probably at some point

There's a few linguistic issues between the two text types that simply feeding a neural net won't solve. The source texts are written in different verb tenses, which adds a layer of grammatical complexity that the neural net isn't trained to recognize, i.e. there is no semantic tagging that recognizes 'is' and 'was' as identical word-level tokens. Wookieepedia articles are written in past tense (everything happened *a long time ago,* in a galaxy far, far away), while most of the job descriptions seem to be in present tense or simple future.

What I really *want* is to make is job posts for the Star Wars universe, which means I need the Star Wars vocabulary generated in the grammar of the job descriptions. The next step in this project will be getting elbows-deep into Parts-of-Speech Tagging!


### Sources
Max Wolf, textgenrnn Python package
[https://github.com/minimaxir/textgenrnn](https://github.com/minimaxir/textgenrnn)

Wookieepedia
[https://starwars.fandom.com](https://starwars.fandom.com)

PyWikiBot Python pacakge
[https://doc.wikimedia.org/pywikibot/master/index.html](https://doc.wikimedia.org/pywikibot/master/index.html)


### Notes
<sup>1</sup> My original dataset was 4393 job descriptions from posts with unique ids, but nearly 81% of them were character-for-character exact duplicates. I know companies repost positions, but was surprised at the scale.

<sup>2</sup> Wookieepedia has been my favorite place on the internet since I first learned about it in 5th grade. It's awesome.