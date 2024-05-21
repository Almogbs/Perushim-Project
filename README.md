# Perushim-Project

Perushim Project is an AI project that utilizes the Sefira API to gather and prepare data for generating AI models. The main goal of this project is to create a generative AI model that, given a pasuk (verse) from the Tanach (Hebrew Bible), will generate a commentary on it, using existing commentaries as training data.

## Features

- Data gathering: The project uses the Sefira API to gather the necessary data, including existing commentaries on the Tanach.
- Data preparation: The gathered data is then prepared for model training.
- Model training: The prepared data is used to train a generative AI model - Google mt5-large.

## Requirements

This project requires Python 3.6 or later and the following Python packages:
- numpy
- pandas
- requests
- accelerate
- transformers 
- datasets
- sacrebleu
- evaluate
- torch
- torchvision
- sentencepiece

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

## How to Use

To use this project, you need to have Python installed on your machine. Follow the steps below:

1. Clone the repository to your local machine: `git clone https://github.com/Almogbs/Perushim-Project.git`
2. Navigate to the project directory: `cd Perusim-Project`
3. Install the necessary Python packages by running: `pip install -r requirements.txt`
4. Train the model (preferebly on a GPU) running the the `fine-tuning.ipynb` notebook, using the dataset from
   `data/dataset.csv` (or run the `src/data_prep.py`, which will download the data from the sefaria using the provided API)
5. Run the `prompt.py` script using: `python prompt.py pasuk [max_length min_length temp rep_pen]` in order to generate
   a commentary

Exaxmples:
- input: `python prompt.py "בראשית ברא אלוהים את השמים ואת הארץ" 500 70 1.0 100.0`
- output: "בראשית. הוא העולם הראשון שברא אלוהים את השמים והארץ, ואחר כך בא ללמדנו כי ב
תחילה לא נאמר "בראשונה" כמו שהביאו על מנת להיות אע ג וכו לפי מה שנזכר למעלה
ראשת כל האשורות בני אל חגוגו"

- input: `python prompt.py "נחמו נחמו עמי יאמר אליהכם" 500 70 1.0 100.0`
- output: "יאמר אליהכם והוא ענין חסד, כמו (שמות ל ב ה כג) ונחמת מלך אשור שהיה נצחון עליהם כי ל א יוכלו להיות אתם"

- input: `python prompt.py "דניאל ואלמוג" 500 70 1.0 100.0`
- output: "דניאל. א"ר אלעזר, מניין להלן (שם) שהוא נזכר בספר שמואל וכן כתיב במסכת סנהדרין"

