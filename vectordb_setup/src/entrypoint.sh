#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Running ETL to Load Q&A to vector DB"

# Run the ETL script
python ingest_documents.py
