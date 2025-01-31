# RootWise: Sustainable Farming & Cooking App

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

## Setup Instructions

1. Clone the repository and navigate to the project directory:
```bash
cd RAG/examples/basic_rag/llamaindex/
```
2. Create and activate a virtual environment:
```
python3 -m venv your_env 
source your_env/bin/activate 
```
3. Install required dependencies:
```
pip install -r requirements.txt
```
4. Set up environment variables:
```
export NGC_API_KEY="{your api key}"
export NVIDIA_API_KEY="{your api key}"
```
5. Modify Docker configuration:
```
nano ~/.docker/config.json
```
5a. Remove the line:
```
"credsStore": "osxkeychain"
```
6. Build the application
```
docker compose up -d --build

```
7. Verify running containers
```
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```
8. To stop the application:
```
docker compose down
```
