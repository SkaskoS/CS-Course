import pandas as pd
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

class Task:
    def __init__(self):
        pass
    
    def t1_1(self, books_path):
      
        corpus = []
        files = os.listdir(books_path)
        
        for file in files:
            
            with open(os.path.join(books_path, file), 'r', encoding='utf-8') as f:
                
                text = f.read()
                
                corpus.append(text)
                
        return corpus
    
    def t1_2(self, corpus):

        # Create a TfidfVectorizer object
        TF_IDF_vectorizer = TfidfVectorizer()

        # Fit and transform the corpus to obtain the TF-IDF matrix
        TF_IDF_matrix = TF_IDF_vectorizer.fit_transform(corpus)

        # Convert the TF-IDF matrix 
        TF_IDF_df = pd.DataFrame(TF_IDF_matrix.toarray(), columns=TF_IDF_vectorizer.get_feature_names_out())

        return TF_IDF_df

    def t2(self, TF_IDF_df):
        
        max_terms = []

        for index, row in TF_IDF_df.iterrows():
            
            max_term = row.idxmax()
            max_value = row[max_term]
            
            max_terms.append((max_term, max_value))
        
        max_terms_df = pd.DataFrame(max_terms, columns=['Term', 'Max TF-IDF'])
        
        return max_terms_df
        

    def t3(self, corpus):

        num_documents = len(corpus)
        idf_values = []
        vectorizer = TfidfVectorizer()

        term_document_matrix = vectorizer.fit_transform(corpus)

        document_frequencies = term_document_matrix.sum(axis=0).A1

        idf_values = np.log((num_documents + 1) / (document_frequencies + 1)) + 1

        idf_df = pd.DataFrame({'Term': vectorizer.get_feature_names_out(), 'IDF': idf_values})

        return idf_df


 
    def t4(self, corpus, tolerance=1e-6):
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Use inverse_transform to get IDF values
        idf_sklearn = np.log(vectorizer.idf_ + 1)  # Adding 1 for the smoothing term
        idf_manual = np.log(self.t3(corpus)['IDF'].values + 1)  # Adding 1 for the smoothing term
        
        num_matching_documents = np.sum(np.abs(idf_manual - idf_sklearn) < tolerance)
        percentage_matching = (num_matching_documents / len(corpus)) * 100
        return percentage_matching




        
if __name__ == "__main__":
    task = Task()
    books = task.t1_1(os.getcwd()+"/public")
    TF_IDF_df = task.t1_2(books)
    print("-------------- Task 1.2 ---------------")
    print(TF_IDF_df)
    print()
    print("-------------- Task 2 ---------------")
    print(task.t2(TF_IDF_df))
    print()
    print("-------------- Task 3 ---------------")
    print(task.t3(books))
    print()
    print("-------------- Task 4 ---------------")
    print(task.t4(books))
    print()