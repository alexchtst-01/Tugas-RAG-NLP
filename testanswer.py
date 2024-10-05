from groq import Groq
from dotenv import load_dotenv
import argparse
import os

load_dotenv()
apikey = os.getenv('GROQ_API_KEY')

client = Groq(api_key=apikey)

def getanswer(query):
    return client.chat.completions.create(
        messages=[{
            'role': 'user',
            'content': query
        }],
        model='llama3-8b-8192'
    ).choices[0].message.content


def PROMPT_TEMPLATE(context, query):
    return (f"""
answer the question based on the context:
{context}

question: {query}
""")

# Initialize the parser
parser = argparse.ArgumentParser(description="Process some files.")

# Add positional and optional arguments
parser.add_argument(
    '--query', 
    type=str, 
    required=True, 
    help='query for the model'
)

parser.add_argument(
    '--context', 
    type=str, 
    required=False, 
    help='context for the model'
)

# Parse arguments
args = parser.parse_args()
queryInput = PROMPT_TEMPLATE(context="", query=args.query)

print(getanswer(
    query=queryInput
))