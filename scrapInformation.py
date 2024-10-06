import requests
from bs4 import BeautifulSoup
import os 
import argparse

def scrap_documents(url):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    pList = [para.get_text().replace('\n', '') for para in paragraphs]
    
    # delete duplicate text
    pList = list(dict.fromkeys(pList))
    # delete row that only contain white
    pList = [i for i in pList if i != '\n']
    
    document_text = '\n'.join(pList)
    print(f"FINISHED SCRAPED from {url}")
    return document_text


def createDocument(docText, fname):
    folderPath = "dataDocument"
    
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        print('data folder dont exist, creating data folder [dataDocument]')
    
    fname = os.path.join(folderPath, fname)
    with open(fname, 'w') as f:
        f.write(docText)
        print(f"Success make file in {fname}")

parser = argparse.ArgumentParser(description="hehe")

parser.add_argument(
    '--url', 
    type=str, 
    required=True,
    help='url document for scrapped'
)

parser.add_argument(
    '--filename',
    type=str, 
    required=True, 
    help='file name for the document that has been scraped'
)


def main():
    args = parser.parse_args()
    doc_result = scrap_documents(url=args.url)
    createDocument(docText=doc_result, fname=args.filename)

if __name__ == "__main__":
    main()


# manual use
# doc_result = scrap_documents(url='https://www.mayoclinic.org/diseases-conditions/brain-tumor/symptoms-causes/syc-20350084')
# createDocument(docText=doc_result, fname='Brain_tumor.txt')