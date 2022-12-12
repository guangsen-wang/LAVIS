#!/bin/bash
#TAG="gcr.io/salesforce-research-internal/lavis_oss_streamlit_gpu"
TAG="gcr.io/salesforce-research-internal/<your-image-name>"
gcloud builds submit . -t=$TAG --machine-type=n1-highcpu-32 --timeout=9000                                                                                                                  
