#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Starting Hypno Q&A chatbot frontend..."

# Run the ETL scripts
streamlit run main.py --server.enableCORS=false --server.enableXsrfProtection=false --server.port=8501
#streamlit run main.py --server.port=8501