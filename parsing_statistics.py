import pandas as pd
from import_pdf import open_and_read_pdf

pages_and_texts = open_and_read_pdf('human-nutrition-text.pdf')


df = pd.DataFrame(pages_and_texts)

df_head =  df.head()

df_head = df.describe().round(2)


"""
df.head() and df.describe() both give us statistics.

Why do we care about token count?
Token count is important to think about because:
1. Embedding models don't deal with infinite tokens.
2. LLMs don't deal with infinite tokens.

For examplean embedding model may have been trained to embed sequences of 384 tokens into numerical space.  (All mpnet-base-v2)

"""



from spacy.lang.en import English

nlp = English()

# Add a sentencizer pipeline, see https://spacy.io/api/sentencizer

nlp.add_pipe('sentencizer')

# Create document instance as an example
doc = nlp('This is a sentence. This is another sentence. I like elephants.') # We are passing in three sentence as an example.
assert len(list(doc.sents)) == 3

# Print out sentences split
x= list(doc.sents)


from import_pdf import open_and_read_pdf
from tqdm.auto import tqdm
import random
pages_and_texts = open_and_read_pdf('human-nutrition-text.pdf')

for index, item in tqdm(enumerate(pages_and_texts)):
	item['sentences'] = list(nlp(item["text"]).sents)

	# Make sure all sentences are strings (teh default type is a spaCy datatype)
	item['sentences'] = [str(sentence) for sentence in item['sentences']]

	# Count the sentences
	item["page_sentence_count_spacy"]  =  len(item['sentences'])


df = pd.DataFrame(pages_and_texts)
x= df.describe().round(2)

# for page in pages_and_text:
	# print(pages_and_text)



"""Chunking our sentences together -- this is an active area of research, so experiment, experiment, experiment

The concept of splitting larger pieces of text int4o smaller ones is often referred to as text splitting or chunking.add()

There is no 100% correct wat to do this.

We'll keep it simple and split into groups of ten sentences (however, you could also try 7, 8, 9, whatever you'd like).

There are frameworks such as LangChain, which can help you with this. However, we are using python for now.

https://python.langchain.com/docs/modules/data_connection/document_transformers/

Why we do this:
1. So our texts are easier to filter (smaller groups of text can be easier to inspect than large passages of text).
2. So our text chunks can fit into our embedding model context window (e.g. 384 tokens as a limit in this use case).
3. So our contexts passed to an LLM can be more specific and focused.add()

"""

#Define split size to turn groups of sentences into chunks
num_sentence_chunk_size = 10

# Create a function to split list of texts recursively into chunk size
# E.G. [20] > [10,10] or [25] -> [10,10, 5]

def split_list(input_list: list,
			   slice_size:int=num_sentence_chunk_size) -> list[list[str]]:
		return [input_list[i:i + slice_size] for i in range (0, len(input_list), slice_size)]


# loop through pages and texts and split sentences into chunks
for item in tqdm(pages_and_texts):
	item['sentence_chunks'] = split_list(input_list=item['sentences'],
									  slice_size = num_sentence_chunk_size)
	item['num_chunks'] = len(item['sentence_chunks'])

x = random.sample(pages_and_texts, k=1)
print(x)
