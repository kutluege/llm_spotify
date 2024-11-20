from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
import os

def generate_api_call(playlist_id, access_token):
    examples = [
        {
            "action": f"ID'si {playlist_id} olan Playlist'i getir.",
            "instruction": "Kullanıcı belirli bir playlisti getirmek istiyor. Aşağıdaki API çağrısını kullanarak bu aksiyonu gerçekleştir.",
            "api_call": f"curl --request GET --url https://api.spotify.com/v1/playlists/{playlist_id} --header 'Authorization: Bearer {access_token}'"
        }
    ]
    
    prompt = create_prompt(f"ID'si {playlist_id} olan bir playlisti getir.", examples)

    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

    # Tokenize input prompt
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    # Generate response
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.5,
        top_p=1,
        top_k=0,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode the generated response
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract URL and headers from the response
    url = re.search(r"--url (https?://[^\s]+)", full_response)
    auth_header = re.search(r"--header 'Authorization: Bearer ([^']+)'", full_response)
    
    url = url.group(1) if url else None
    auth_token = auth_header.group(1) if auth_header else None
    
    return url, {"Authorization": f"Bearer {auth_token}"}

# Example usage
if __name__ == "__main__":
    playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
    access_token = "your_spotify_access_token_here"  # Directly include your token here
    url, headers = generate_api_call(playlist_id, access_token)
    print("URL:", url)
    print("Headers:", headers)