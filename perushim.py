from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch import cuda
import sys

if __name__ == '__main__':
    max_length, min_length = 200, 100
    if len(sys.argv) == 2:
        print(f"Using default values for max_length={max_length} and min_length={min_length}")
    elif len(sys.argv) != 4:
        print("Usage: python perushim.py pasuk [max_length min_length]")
        exit(1)
    else:
        max_length, min_length = int(sys.argv[2]), int(sys.argv[3])

    device = 'cuda' if cuda.is_available() else 'cpu'
    print(f"Using {device} device")
    model_name = 'google/mt5-small/checkpoint-32160'    

    tokenizer = AutoTokenizer.from_pretrained(model_name, return_tensors="pt", device=device)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    text = str(sys.argv[1])
    print(f"Pasuk: {text[::-1]}")
    inputs = tokenizer(text, return_tensors='pt', ).to(device)
    summary_ids = model.generate(**inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print(f"Perush: {str(summary)[::-1]}")
