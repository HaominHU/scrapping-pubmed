from Bio import Entrez
import pandas as pd
import numpy as np


# Get searched results
def search(query):
    Entrez.email = 'hah90@pitt.edu'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='5',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


# Get papers based on the results ids
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'hah90@pitt.edu'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def get_pmc_id(pm_id):
    try:
        Entrez.email = 'hah90@pitt.edu'
        handle = Entrez.elink(dbfrom="pubmed",
                              db="pmc",
                              linkname="pubmed_pmc",
                              id=pm_id,
                              retmode="text")
        result = Entrez.read(handle)
        return result[0]['LinkSetDb'][0]['Link'][0]['Id']
    except:
        return '0'


def get_papers_summary(id_list):
    papers = fetch_details(id_list)
    paper_arr = []
    for paper in papers['PubmedArticle']:
        pm_id = ''.join(paper['MedlineCitation']['PMID'])
        pmc_id = get_pmc_id(pm_id)
        article = {
            'title': paper['MedlineCitation']['Article']['ArticleTitle'],
            'abstract': ''.join(paper['MedlineCitation']['Article']['Abstract']['AbstractText']),
            'doi': ''.join(paper['MedlineCitation']['Article']['ELocationID']),
            'full_text': f'http://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/' if pmc_id != '0' else np.nan
        }
        paper_arr.append(article)
    paper_df = pd.DataFrame(paper_arr)
    paper_df.index += 1
    paper_df.to_excel('./pubmed_search.xlsx')


if __name__ == '__main__':
    results = search('delirium assessment')
    id_list = results['IdList']
    get_papers_summary(id_list)
