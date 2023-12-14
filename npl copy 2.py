import nltk
import pandas as pd
import openpyxl as op
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

# Download NLTK resources if not downloaded
"""nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')
print("hello")"""
# Load positive and negative words
# Load positive and negative words from files
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
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': polarity_score,
        'Subjectivity Score': subjectivity_score
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
        'Average Sentence Length': average_sentence_length,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Average Words per Sentence': average_words_per_sentence,
        'Complex Word Count': complex_words,
        'Word Count': word_count,
        'Average Word Length': average_word_length,
    }

# Read file names from Excel
urls_df = pd.read_excel(r"/home/eswar/python/ds/dataextractin/Input.xlsx", engine="openpyxl")
file_names = urls_df['URL_ID']  # Assuming the column name is 'File_Name'


# Read file names from Excel
urls_df = pd.read_excel(r"/home/eswar/python/ds/dataextractin/Input.xlsx", engine="openpyxl")
file_names = urls_df['URL_ID']  # Assuming the column name is 'File_Name'

# Create an empty DataFrame to store results
output_data = pd.DataFrame()
dfs = []
# Iterate through file names
for i, file_name in enumerate(file_names):
    # Construct the file path based on the directory where files are located
    file_path = f"txt/{file_name}"  # Update the directory path accordingly

    # Load each file
    with open(file_path, "r") as myfile:
        data = myfile.read().replace('\n', ' ')

    # Perform sentiment analysis
    sentiment_result = sentiment_analysis(data)

    # Calculate readability metrics
    readability_result = calculate_readability(data)

    # Merge sentiment and readability results into a single dictionary
    analysis_result = {**sentiment_result, **readability_result}

    # Create a DataFrame for the analysis result of this file
    file_df = pd.DataFrame(analysis_result, index=[0])

    # Assign the file name as a column value
    file_df['URL_ID'] = file_name

    # Append the analysis result to the output data
    """output_data = output_data.append(file_df, ignore_index=True)"""
    dfs.append(file_df)

# Concatenate all DataFrames in the list
output_data = pd.concat(dfs, ignore_index=True)
# Perform sentiment analysis
sentiment_result = sentiment_analysis(data)

# Save the output data to Excel
output_file_path = "output.xlsx"  # Define the output file path
output_data.to_excel(output_file_path, index=False)
# Calculate readability metrics
readability_result = calculate_readability(data)
print("Sentiment Analysis Results:")
for key, value in sentiment_result.items():
    print(f"{key}: {value}")

# Print readability analysis results

print("\nReadability Analysis Results:")
for key, value in readability_result.items():
    print(f"{key}: {value}")
