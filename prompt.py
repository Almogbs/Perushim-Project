from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch import cuda
import sys

def generate_perushim():
    """
    Generates perushim (commentaries) for a given pasuk (verse) using a pre-trained model.

    Args:
        None

    Returns:
        None
    """
    max_length, min_length, temp, rep_pen = 200, 100, 0.5, 50.0
    if len(sys.argv) == 2:
        print(f"Using default values for max_length={max_length} min_length={min_length} temp={temp} rep_pen={rep_pen}")
    elif len(sys.argv) != 4:
        print("Usage: python perushim.py pasuk [max_length min_length temp rep_pen]")
        exit(1)
    else:
        max_length, min_length, temp, rep_pen = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])

    device = 'cuda' if cuda.is_available() else 'cpu'
    print(f"Using {device} device")
    model_name = 'google/mt5-small/checkpoint-32160'    

    tokenizer = AutoTokenizer.from_pretrained(model_name, return_tensors="pt", device=device)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

    text = str(sys.argv[1])
    print(f"Pasuk: {text[::-1]}")
    inputs = tokenizer(text, return_tensors='pt', ).to(device)
    summary_ids = model.generate(**inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True, repetition_penalty=rep_pen, temperature=temp)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print(f"Perush: {str(summary)[::-1]}")

if __name__ == '__main__':
    generate_perushim()
