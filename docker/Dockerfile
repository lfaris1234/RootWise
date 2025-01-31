# Base image with Python & CUDA support
FROM nvcr.io/nvidia/pytorch:23.06-py3

# Set the working directory
WORKDIR /app

# Copy files
COPY src/ /app/src
COPY config/ /app/config
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000

# Set environment variables
ENV LOCAL_NIM_CACHE=/root/.cache/nim
ENV NGC_API_KEY=${NGC_API_KEY}

# Run the application
CMD ["python", "src/main.py"]

  


# code from website https://build.nvidia.com/nvidia/nv-embedqa-e5-v5?snippet_tab=Docker

#$ docker login nvcr.io
# Username: $oauthtoken
# Password: <PASTE_API_KEY_HERE>

# export NGC_API_KEY=<PASTE_API_KEY_HERE>
# export LOCAL_NIM_CACHE=~/.cache/nim
# mkdir -p "$LOCAL_NIM_CACHE"
# docker run -it --rm \
#     --gpus all \
#     --shm-size=16GB \
#     -e NGC_API_KEY \
#     -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
#     -u $(id -u) \
#     -p 8000:8000 \
#     nvcr.io/nim/nvidia/nv-embedqa-e5-v5:latest


# curl -X "POST" \
#     "http://localhost:8000/v1/embeddings" \
#     -H 'accept: application/json' \
#     -H 'Content-Type: application/json' \
#     -d '{
#       "input": ["Hello world"],
#       "model": "nvidia/nv-embedqa-e5-v5",
#       "input_type": "query"
#   }'
