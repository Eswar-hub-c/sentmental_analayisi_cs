import nltk
import openpyxl as op
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

Positive_Score=0
Negative_Score= 0
Polarity_Score= 0
Subjectivity_Score=0
Average_Sentence_Length=0
Percentage_of_Complex_Words=0
Fog_Index= 0
Average_Words_per_Sentence=0 
Complex_Word_Count= 0
Word_Count= 0
Average_Word_Length=0 

# Download NLTK resources if not downloaded
"""nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')
print("hello")"""
# Load positive and negative words
with open("/home/eswar/python/ds/dataextractin/MasterDictionary-20231130T135046Z-001/MasterDictionary/positive-words.txt", "r", encoding="latin-1") as pos_file:
    positive_words = pos_file.read().splitlines()

with open("/home/eswar/python/ds/dataextractin/MasterDictionary-20231130T135046Z-001/MasterDictionary/negative-words.txt", "r", encoding="latin-1") as neg_file:
    negative_words = neg_file.read().splitlines()

    negative_words = neg_file.read().splitlines()
# Function to calculate sentiment scores
def sentiment_analysis(text):
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    
    sentences = sent_tokenize(text)
    word_count = 0
    positive_score = 0
    negative_score = 0
    
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [word for word in words if word not in stop_words and word not in punctuation]
        
        for word in words:
            if word in positive_words:
                positive_score += 1
            elif word in negative_words:
                negative_score += 1
            word_count += 1
    
    polarity_score = (positive_score - negative_score) / (word_count + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)
    
    return {
        positive_score,
        negative_score,
        polarity_score,
        subjectivity_score
    }

# Function to calculate readability metrics
def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    word_count = len(words)
    sentence_count = len(sentences)
    
    syllable_count = 0
    complex_words = 0
    
    cmu = nltk.corpus.cmudict.dict()
    for word in words:
        if word in cmu:
            syllable_count += max([len(list(y for y in x if y[-1].isdigit())) for x in cmu[word.lower()]])
            if len(list(cmu[word.lower()])) > 2:
                complex_words += 1
    
    average_sentence_length = word_count / sentence_count
    percentage_complex_words = (complex_words / word_count) * 100
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    
    average_words_per_sentence = word_count / sentence_count
    average_word_length = sum(len(word) for word in words) / word_count
    
    return {
        average_sentence_length,
        percentage_complex_words,
        fog_index,
        average_words_per_sentence,
        complex_words,
        word_count,
        average_word_length,
    }

# Load your file
with open("txt/321.0", "r") as myfile:
    data = myfile.read().replace('\n', ' ')

# Perform sentiment analysis
sentiment_result = sentiment_analysis(data)

# Calculate readability metrics
readability_result = calculate_readability(data)
