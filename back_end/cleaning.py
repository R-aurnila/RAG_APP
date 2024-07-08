import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load the data with UTF-8 encoding
with open('app/data/gigalogy_data.txt', 'r', encoding='utf-8') as file:
    data = file.readlines()

# Function to clean text
def clean_text(text):
    # Ensure the input is treated as a string, not a filename
    text = str(text)
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove irrelevant characters except numbers
    text = re.sub(r'[^\w\s@]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Remove stop words and lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Process the data
cleaned_entries = []
num_lines = len(data)
for i in range(0, num_lines, 4):
    if i + 2 < num_lines:  # Ensure there are enough lines left for URL, Title, and Description
        url = data[i].strip()
        title = data[i + 1].strip().replace("Title: ", "")
        description = data[i + 2].strip().replace("Description: ", "")
        if title and description:
            cleaned_title = clean_text(title)
            cleaned_description = clean_text(description)
            cleaned_entries.append(f"{url}\nTitle: {cleaned_title}\nDescription: {cleaned_description}\n\n")

# Save the cleaned entries to a new text file with UTF-8 encoding
with open('app/data/cleaned_gigalogy_data.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(cleaned_entries)

