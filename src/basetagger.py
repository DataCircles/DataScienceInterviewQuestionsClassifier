
from config import FileConfig
import os
import pandas as pd
import re

class BaseTagger(object):
    """Class to tag the data science questions."""
    
    def __init__(self):
        """Initializer."""
        self.rawdir = os.path.join(FileConfig.RAWDIR)
        self.intdir = os.path.join(FileConfig.INTDIR)
        self._load_data()
        self._load_tagger()
        self._tag_data()
    
    def _load_tagger(self):
        """Tag terms used for tagging the data."""
        
        tagterms = {}
        tagterms['statistics'] = ['statistic', 'regression', 'estimation', 'central limit theorem', 'sampling','type i error', 'p-value', 'distribution', 'linear model', 'false positive', 'correlated', 'dimensionality reduction', 'bayes', 'a(.*?)b test', 'randomized experiment', 'samples', 'experimental design', 'correlation', 'experiments', 'random sample', 'expected value', 'chance']
        tagterms['regression'] = ['regression']
        tagterms['probability'] = ['probabi', 'bayes', 'rolling (.*?) dice', 'dice', 'how many', 'what is total', 'random number']
        tagterms['hypothesis testing'] = ['p-value']
        tagterms['machine learning'] = ['machine learning', 'decision tree', 'training', 'testing', 'simulation']
        tagterms['neural networks'] = ['numerical optimization']
        tagterms['knowledge'] = ['know']
        tagterms['sql'] = ['table', 'sql', 'inner join', 'union', 'query', 'subquery', 'lookup table', 'joins']
        tagterms['programming'] = ['programming', 'algorithm', 'coding', 'how would you sort', 'hadoop', 'mapreduce', 'python', 'software', 'modules', 'r\b', 'packages', 'access the element', 'command', 'function', 'hash', 'optimize', 'cron job', 'coder', 'sort']
        tagterms['algorithms'] = ['algorithm', 'recommendation engine']
        tagterms['experience'] = ['contribute','what have you done','success stories']
        tagterms['metrics'] = ['precision', 'recall', 'loss', 'roc curve', 'metric']
        tagterms['modeling'] = ['model', 'predict']
        tagterms['data'] = ['data', 'selection bias', 'sparsity', 'outliers', 'survey','variable']
        tagterms['clustering'] = ['clustering']
        tagterms['analysis'] = ['analysis']
        tagterms['situational'] = ['initiative', 'conflict', 'tell me about', 'how would you deal']
        tagterms['general'] = ['data science']
        tagterms['cases'] = ['how (.*?) detect', 'solution', 'how would you (quantify|assess|analyze)']
        self.tagterms = tagterms
        
    def _load_data(self):
        df = pd.read_csv(os.path.join(self.rawdir, 'data_science_questions.csv'))
        df = df[~pd.isnull(df['question'])]
        #print(df.head())
        self.df = df

    def _tag_data(self):
        """Tag the data in the dataset"""
        df = self.df
        df['answer'] = ['' if pd.isnull(row['answer']) else row['answer'] for i, row in df.iterrows()]
        df['tags'] = ''
        #print(df.head())
        for tag, searchvars in self.tagterms.items():
            print(tag)
            re1 = re.compile(r'\b(%s)' % ('|'.join(searchvars)))
            df['tags'] = [row['tags'] + '|' + tag if re1.search((row['question']+' '+ row['answer']).lower()) is not None else row['tags'] for i, row in df.iterrows()]
            df['i_' + tag] = [1 if tag in row['tags'] else 0 for i, row in df.iterrows()]
        # questions without tags

        df['tags'] = [row['tags'].strip('|') for i, row in df.iterrows()]
        df['tags'] = ['other' if row['tags'] == '' else row['tags'] for i, row in df.iterrows()]
        df['numtags'] = [0 if row['tags'] == '' else len(row['tags'].split('|')) for i, row in df.iterrows()]
        print(df[df['numtags'] >= len(list(self.tagterms.keys()))])
        print("Tags per question")
        print(df['numtags'].value_counts())
        print("Questions without tags")
        print(len(df[df['numtags'] == 0]))
        for i, row in df.iterrows():
            if row['numtags'] == 0:
                print("Question: %s" % (row['question']))
                print("Answer: %s" % (row['answer']))
        df.to_csv(os.path.join(self.intdir, 'data_science_questions_tagged.csv'), index=False)
        self.df = df
        
    def get_questions(self, tag):
        """Get questions that fall into different tags"""
        df = self.df
        print("Number of tags in topics: %s" % (len(df[df['i_'+tag] == 1])))
        for i, row in df.iterrows():
            if row['i_'+ tag] == 1:
                print("Question: %s" % (row['question']))
        