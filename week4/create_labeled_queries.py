import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv
import string

from nltk.stem.snowball import SnowballStemmer

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.PorterStemmer()

def prepare_word(word):
    word = word.lower()
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    word = word.translate(word)
    word = ' '.join(word.split())
    return stemmer.stem(word)

def update_to_parent_category(cat, cats_to_be_updated, possible_parent_cats):
    if cat in cats_to_be_updated and not cat in possible_parent_cats:
        parent_of_cat_df = parents_df[parents_df['category'] == cat]
        if len(parent_of_cat_df) == 0:
            return cat
        parent_df_row = parent_of_cat_df.iloc[0]
        return parent_df_row['parent']
    else:
        return cat

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/labeled_query_data_test.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]

df['query'] = df['query'].transform(prepare_word)
categories_counts = df.groupby(['category']).size().reset_index(name='counts')
print(categories_counts)

while len(categories_counts[categories_counts["counts"] < min_queries].index) != 0:
    categories_df = categories_counts[categories_counts["counts"] < min_queries]
    categories_queries = categories_df['category'].values
    possible_parent_cats = parents_df[parents_df['category'].isin(categories_queries)]['parent'].values
    df['category'] = df['category'].transform(lambda x: update_to_parent_category(x, categories_queries, possible_parent_cats))
    categories_counts = df.groupby(['category']).size().reset_index(name='counts')
    print(len(df['category'].unique()))

def get_parent_code(category_code):
    if category_code == root_category_id:
        return category_code
    else:
        return parents_df[parents_df.category == category_code]['parent'].values[0]
        
df['parent_code'] = df['category'].apply(get_parent_code)

df['n_queries_per_category'] = df.groupby('category')['query'].transform(len)
MIN_COUNT = 100
conditions = [
    (df['n_queries_per_category'] <= MIN_COUNT),
    (df['n_queries_per_category'] > MIN_COUNT)
    ]
values = [df['parent_code'], df['category']]

df['category'] = np.select(conditions, values)

print(df.category.nunique())
# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)

