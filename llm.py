from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
import os

def create_prompt(new_act, examples):
    prompt = "Aşağıdaki Spotify API eylemlerini, verilen örnekleri kullanarak API çağrılarına dönüştürün.\n\n"
    for example in examples:
        prompt += f"Action: **{example['action']}**\nInstruction:\n{example['instruction']}\nAPI Call:\n```bash\n{example['api_call']}\n```\n\n"
    prompt += f"**Now, convert this action:**\n\nAction: **{new_act}**\nAPI Call:\n"
    return prompt
def generate_api_call(playlist_id, access_token):
    examples = [
        {
            "action": f"ID'si {playlist_id} olan Playlist'i getir.",
            "instruction": "Kullanıcı belirli bir playlisti getirmek istiyor. Aşağıdaki API çağrısını kullanarak bu aksiyonu gerçekleştir.",
            "api_call": f"curl --request GET --url https://api.spotify.com/v1/playlists/{playlist_id} --header 'Authorization: Bearer {access_token}'"
        }
    ]
    
    prompt = create_prompt(f"ID'si {playlist_id} olan bir playlisti getir.", examples)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.5,
        top_p=1,
        top_k=0,
        pad_token_id=tokenizer.eos_token_id
    )

    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    url = re.search(r"--url (https?://[^\s]+)", full_response)
    auth_header = re.search(r"--header 'Authorization: Bearer ([^']+)'", full_response)
    
    url = url.group(1) if url else None
    auth_token = auth_header.group(1) if auth_header else None
    
    return url, {"Authorization": f"Bearer {auth_token}"}

if __name__ == "__main__":
    playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
    access_token = ""  # Directly include your token here
    url, headers = generate_api_call(playlist_id, access_token)
    print("URL:", url)
    print("Headers:", headers)