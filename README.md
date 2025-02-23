# RootWise: Sustainable Farming & Cooking App


## Setup Instructions

1. Create and activate a virtual environment:
```
python3 -m venv your_env 
source your_env/bin/activate 
```
2. Install required dependencies:
```
pip install -r requirements.txt
```
3. Set up environment variables:
```
export NGC_API_KEY="{your api key}"
export NVIDIA_API_KEY="{your api key}"
```
4. Setup GPU (specific to personal dev with brev gpu, retrieve token from startup page):
```
brew install brevdev/homebrew-brev/brev && brev login --token ***
brev shell rootwise-t4-jupyter
```
5. Pull and run nvidia/nv-embedqa-e5-v5 using Docker (this will download the full model and run it in your local environment):
```
docker login nvcr.io
    Username: $oauthtoken
    Password: <API_KEY>
```
6. Pull and run the NVIDIA NIM with the command below. This will download the optimized model for your infrastructure.
```
export NGC_API_KEY=<API_KEY>
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"
docker run -it --rm \
    --gpus all \
    --shm-size=16GB \
    -e NGC_API_KEY \
    -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
    -u $(id -u) \
    -p 8000:8000 \
    nvcr.io/nim/nvidia/nv-embedqa-e5-v5:latest

```
7. Open a new terminal and rerun for CLI
```
brev shell rootwise-t4-jupyter
```
8. Verify running containers
```
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```
9. Launch the webapp (make sure that all files in the gpu deployment are up-to-date *I've been using the jupyter notebook*)
```
python3 app.py
```


To stop the application:
```
docker compose down
```

## Concept

This application promotes sustainable farming and cooking by providing users with personalized recipes, food storage strategies, and community-driven tips based on seasonal and local ingredients. It also integrates computer vision to identify vegetables from farm stand photos, emphasizing zero-waste cooking and supporting local farms.

### Motivations:
1. Reduce food waste.
2. Support local farms and markets.
3. Simplify eating natural, healthy foods.

### Key Features:
1. **Inputs**:
   - **Season and Location**: Suggests a list of seasonal vegetables.
   - **Vegetables of Interest**: Choose from the suggested list.
   - **Farm Stand Photo {stretch feature}**: Uses computer vision to identify vegetables.
   - **Number of People**: Adjusts recipe portions.
   - **Dietary Restrictions**: Filters recipes to meet dietary needs.

2. **Outputs**:
   - **Recipes**:
     - Cook time.
     - Community notes and tips.
   - **Food Scrap Recommendations**:
     - Composting tips.
     - Freezing methods for future use (e.g., stir-fry mix, chopped fruit).
     - Zero-waste cooking ideas (e.g., carrot top pesto).
   - **Additional Features**:
     - Food donation resources, including Food Not Bombs drop-off locations.
     - Food lifespan and storage tips (e.g., using paper towels to extend the life of greens).
     - "Food as Medicine" insights:
       - Health benefits (e.g., turmeric for inflammation).
       - Spiritual properties (e.g., calming effects of certain herbs).
---
