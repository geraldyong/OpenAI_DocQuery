FROM cr.weaviate.io/semitechnologies/weaviate:1.26.0-rc.0-e5a99e6

# Environment Variables
ENV QUERY_DEFAULTS_LIMIT=25
ENV AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
ENV PERSISTENCE_DATA_PATH=/var/lib/weaviate
ENV DEFAULT_VECTORIZER_MODULE=none
ENV ENABLE_MODULES=text2vec-cohere,text2vec-huggingface,text2vec-palm,text2vec-openai,generative-openai,generative-cohere,generative-palm,ref2vec-centroid,reranker-cohere,qna-openai
ENV CLUSTER_HOSTNAME=node1

CMD ["--host", "0.0.0.0", "--port", "8083", "--scheme", "http"]

EXPOSE 8083
EXPOSE 50053
