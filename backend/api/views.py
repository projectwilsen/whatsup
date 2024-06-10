from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TextEmbeddingSerializer
from rest_framework import status
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()
from supabase.client import Client, create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# {"text":"rag with knowledge graph"}

class SemanticSearchView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TextEmbeddingSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            
            model_name = "BAAI/bge-large-en-v1.5"
            model_kwargs = {"device": "cpu"}
            encode_kwargs = {"normalize_embeddings": True}
            embeddings_model = HuggingFaceBgeEmbeddings(
                model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
            )
            
            embeddings = embeddings_model.embed_query(text)

            params = {'query_embedding':embeddings, 'similarity_threshold':0.7,'match_count':6}
            data = supabase.rpc('vector_search', params).execute()
            
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
