# Bro-ssessment

## Project Structure

```
Bro-ssessment/
├── *.py                    # TO BE REFACTOR, a collection of scripts to perform analysis tasks
├── brossessment            # Internal python modules, such as DB models
├── data                    # Raw documents
│   ├── posts
│   │   ├── <posts_1>.excel
│   │   ├── <posts_2>.excel
│   │   └── <...more...posts>
│   ├── syllabus
│   │   ├── <class_1>.txt
│   │   ├── <class_2>.txt
│   │   └── <...more...syllabus>
│   └── <...more...>
├── infra                   # OPTIONAL, handy scripts to spin up a Postgres instance with zero effort
├── misc                    # A collection of utility scripts for preprocessing raw documents
└── sql                     # SQL scripts use to create database tables
```

## Behaviour Metrics
### Off-topic posts
We use Laten Semantic Analysis to compare course syllabus and posts from discussion forum to identify off-topic posts. In the case of PeppeR project, all syllabus are provided in the format of `.pdf` and `.docs`. We provid a handy script to convert them into regular text file for the sake of convinence for parsing.

We use [textract](https://textract.readthedocs.io/en/stable/index.html) library to extract texts from those files. Follow the installation [instruction](https://textract.readthedocs.io/en/stable/installation.html). You can find a list of supported extension in their documentation.

Place all your files with the naming convention of `<course_id>.{pdf,docx,doc,etc}` under `data/syllabus`. Then run

```sh
$ python misc/pdf_2_txt.py data/syllabus
```

Run the off topic analysis.py

```sh
$ python off_topic_analysis.py
```

### Parse CCS result

```sh
$ python misc/extract_ccs.py
```

### Produce features.csv for modeling

```sh
# Run the script, and the csv file will be avaliable inside the /data folder
$ python extract_features.py
```

Then you may use the `analysis.Rmd` file to train the model.

## Development

```sh
# Setup python virtual environment
$ pip3 install --user virtualenv
$ virtualenv venv --python=python3
$ source venv/bin/activate

# Install python dependencies
$ pip install -r requirements.txt

# Setup environment variable
$ cp .env.example .env
$ source .env
```
