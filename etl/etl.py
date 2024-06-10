import arxiv
import datetime
import pytz  
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()
from supabase.client import Client, create_client

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq

groq_api = os.getenv("GROQ_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase_client = create_client(supabase_url, supabase_key)

client = arxiv.Client()

keyword = ["rag","large language model"]
search = arxiv.Search(
  query = keyword[1],
  max_results = 30,
  sort_by = arxiv.SortCriterion.SubmittedDate,
  sort_order = arxiv.SortOrder.Descending
)

results = client.results(search)
all_papers = list(results)

utc_timezone = pytz.timezone('UTC')
current_datetime_utc = datetime.datetime.now(utc_timezone)

seven_days_ago = current_datetime_utc - datetime.timedelta(days=7)

this_week_papers = [paper for paper in all_papers if paper.published >= seven_days_ago]

model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

model = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key = groq_api)

class Paper(BaseModel):
    problem: str = Field(description="Extract the main research problem from the abstract")
    solution: str = Field(description="Extract the proposed method, approach, or solution from the abstract. Be concise and specific")
    result: str = Field(description="A summary of the main findings or outcomes derived from applying the proposed solution.")

parser = JsonOutputParser(pydantic_object=Paper)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

for i in range(len(this_week_papers)):

    try:
        result = chain.invoke({"query": this_week_papers[i].summary})
        result['author'] = ', '.join([author.name for author in this_week_papers[i].authors])
        result['url'] = next((link.href for link in this_week_papers[i].links if link.title == 'pdf'), None)
        result['embedding'] = embeddings.embed_query(result['solution'])
        result['title'] = this_week_papers[i].title
        result['published_date'] = pd.Timestamp(this_week_papers[i].published).strftime("%Y%m%d_%H%M%S")
        
        supabase_client.table('research_papers').upsert(result,  returning="minimal", on_conflict="title").execute()
        print(f"Success to process {this_week_papers[i].title}")
    except:
        print(f"Fail to process {this_week_papers[i].title}")