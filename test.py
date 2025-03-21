import requests

# API endpoint for Draw Things
api_url = "http://localhost:7860/sdapi/v1/txt2img"

# Payload with parameters for image generation
payload = {
    "prompt": "A futuristic cityscape at night with neon lights",
    "width": 512,
    "height": 512,
    "steps": 50,
    "seed": -1
}

# Send POST request to the API
response = requests.post(api_url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # The API returns images in base64 format
    images = response.json().get('images', [])
    for i, img_data in enumerate(images):
        # Decode the base64 image data
        img_bytes = base64.b64decode(img_data)
        # Save the image to a file
        with open(f"generated_image_{i}.png", "wb") as img_file:
            img_file.write(img_bytes)
else:
    print(f"Error: {response.status_code}")
