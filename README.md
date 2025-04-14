# Temporal Expressions Normalization spaCy (TeNs)

<b>Temporal Expressions Normalization spaCy (TeNs)</b> is a powerful pipeline component for spaCy that seamlessly
identifies and parses date entities in text. It leverages the <b>[Temporal Expressions Normalization Framework](
https://github.com/iliedorobat/timespan-normalization)</b> to recognize a wide variety of date formats using an
extensive set of regular expressions (RegEx), ensuring robust and adaptable date extraction across diverse
textual sources.

Unlike conventional solutions that primarily focus on well-structured date formats, TeNs excels in handling
real-world text by <b>identifying</b> not only standard date representations but also <b>abbreviated, informal, or even
misspelled temporal expressions.</b> This makes it particularly effective for processing noisy or unstructured data,
such as historical records, user-generated content, and scanned documents with OCR inaccuracies.

Moreover, TeNs is designed to <b>integrate seamlessly into existing NLP pipelines,</b> allowing for enhanced temporal
information processing in tasks such as event extraction, timeline construction, and knowledge graph population.
By providing a flexible and accurate approach to temporal data normalization, it significantly improves the
quality and reliability of date-related information extracted from text.

<b>Table I.</b> Types of temporal expressions which can be processed
<table>
    <tr>
        <th>Type of Temporal Expressions</th>
        <th>Examples of Temporal Expressions*</th>
    </tr>
    <tr>
        <td>dates</td>
        <td>
            YMD: 1881-08-31; 1857 mai 10; etc.<br/>
            DMY: 09.11.1518; 1 noiembrie 1624; etc.<br/>
            MY: ianuarie 632; etc.
        </td>
    </tr>
    <tr>
        <td>timespans</td>
        <td>
            centuries: s:; sc; se.; sec; sec.; secol; secolele; secolul; sex.<br/>
            millenniums: mil; mil.; mileniul; mileniului; mileniile
        </td>
    </tr>
    <tr>
        <td>years</td>
        <td>77; 78; 1652; [1873]; aproximativ 1834; cca. 1420; etc.</td>
    </tr>
</table>
* The values are mentioned in the reference language – Romanian language



## Getting started
To integrate TeNs into spaCy pipelines you need the following:

### Prerequisites
- Python 3.x
- JRE 11+
- spaCy 3.x
- py4j 0.10.9.9
- langdetect 1.0.9

### Install
```bash
pip install temporal-normalization-spacy
```

### Supported languages
- [Romanian](https://universaldependencies.org/tagset-conversion/ro-multext-uposf.html)



## Use with spaCy library

### Importing Modules & Defining Constants

```python
import subprocess

import spacy

from temporal_normalization.commons.print_utils import console
from temporal_normalization.index import create_normalized_component, TemporalNormalization  # noqa: F401

LANG = "ro"
MODEL = "ro_core_news_sm"
TEXT_RO = ("Sec al II-lea a.ch. a fost o perioadă de mari schimbări. "
           "În secolul XX, tehnologia a avansat semnificativ. "
           "Sec. 21 este adesea asociat cu globalizarea rapidă.")
```

### Adding the Component to spaCy Pipeline
```python
# Display a warning if the language of the text is not Romanian.
console.lang_warning(TEXT_RO, target_lang=LANG)

try:
    # Load the spaCy model if it has already been downloaded
    nlp = spacy.load(MODEL)
except OSError:
    console.warning(f'Started downloading {MODEL}...')
    # Download the Romanian model if it wasn't already downloaded
    subprocess.run(["python", "-m", "spacy", "download", MODEL])
    # Load the spaCy model
    nlp = spacy.load(MODEL)

# Add "temporal_normalization" component to the spaCy pipeline
nlp.add_pipe("temporal_normalization", last=True)
```

### Processing Text with the Pipeline
```python
doc = nlp(TEXT_RO)

# Display NLP-specific linguistic annotations
console.tokens_table(doc)
print()
```

### Accessing the Parsed Temporal Expressions
```python
# Display information about the identified and normalized dates in the text.
for entity in doc.ents:
    edges = entity._.time_series.edges

    print("Start Edge:")
    print(edges.start.serialize("\t"))
    print()

    print("End Edge:")
    print(edges.end.serialize("\t"))
    print()

    print("Periods:")
    for period in entity._.time_series.periods:
        print(period.serialize("\t"))
        print()
    print("---------------------")
```

## Standalone usage
** **Important Note:** Even if you choose the standalone approach, the **spaCy library will 
still be loaded on first run,** and this process may take a few seconds/tens of seconds.

### Importing Modules & Defining Constants
```python
from temporal_normalization import console, TemporalExpression, start_process

LANG = "ro"
TEXT_RO = (
    "Sec al II-lea a.ch. a fost o perioadă de mari schimbări. "
    "În secolul XX, tehnologia a avansat semnificativ. "
    "Sec. 21 este adesea asociat cu globalizarea rapidă."
)
```

### Parsing the Content
```python
# Display a warning if the language of the text is not Romanian.
console.lang_warning(TEXT_RO, target_lang=LANG)

expressions: list[TemporalExpression] = []
start_process(TEXT_RO, expressions)
```

### Accessing the Parsed Temporal Expressions
```python
for expression in expressions:
    for time_series in expression.time_series:
        edges = time_series.edges

        print("Start Edge:")
        print(edges.start.serialize("\t"))
        print()

        print("End Edge:")
        print(edges.end.serialize("\t"))
        print()

        print("Periods:")
        for period in time_series.periods:
            print(period.serialize("\t"))
            print()
        print("---------------------")
```

## Result
### First Sentence
```text
Start Edge:
	Matched value: Sec al II-lea a.ch.
	Matched Type: century
	Normalized label: 2nd century BC
	DBpedia uri: https://dbpedia.org/page/2nd_century_BC

End Edge:
	Matched value: Sec al II-lea a.ch.
	Matched Type: century
	Normalized label: 2nd century BC
	DBpedia uri: https://dbpedia.org/page/2nd_century_BC

Periods:
	Matched value: Sec al II-lea a.ch.
	Matched Type: century
	Normalized label: 1st millennium BC
	DBpedia uri: https://dbpedia.org/page/1st_millennium_BC

	Matched value: Sec al II-lea a.ch.
	Matched Type: century
	Normalized label: 2nd century BC
	DBpedia uri: https://dbpedia.org/page/2nd_century_BC
```

### Second Sentence
```text
Start Edge:
	Matched value: secolul XX
	Matched Type: century
	Normalized label: 20th century
	DBpedia uri: https://dbpedia.org/page/20th_century

End Edge:
	Matched value: secolul XX
	Matched Type: century
	Normalized label: 20th century
	DBpedia uri: https://dbpedia.org/page/20th_century

Periods:
	Matched value: secolul XX
	Matched Type: century
	Normalized label: 2nd millennium
	DBpedia uri: https://dbpedia.org/page/2nd_millennium

	Matched value: secolul XX
	Matched Type: century
	Normalized label: 20th century
	DBpedia uri: https://dbpedia.org/page/20th_century
```

### Third Sentence
```text
Start Edge:
	Matched value: Sec. 21
	Matched Type: century
	Normalized label: 21st century
	DBpedia uri: https://dbpedia.org/page/21st_century

End Edge:
	Matched value: Sec. 21
	Matched Type: century
	Normalized label: 21st century
	DBpedia uri: https://dbpedia.org/page/21st_century

Periods:
	Matched value: Sec. 21
	Matched Type: century
	Normalized label: 3rd millennium
	DBpedia uri: https://dbpedia.org/page/3rd_millennium

	Matched value: Sec. 21
	Matched Type: century
	Normalized label: 21st century
	DBpedia uri: https://dbpedia.org/page/21st_century
```



## Publications
ECAI 2021: [The Power of Regular Expressions in Recognizing Dates and Epochs (2021)](https://ieeexplore.ieee.org/document/9515139)
```
@inproceedings{9515139,
  author={Dorobăț, Ilie Cristian and Posea, Vlad},
  booktitle={2021 13th International Conference on Electronics, Computers and Artificial Intelligence (ECAI)}, 
  title={The Power of Regular Expressions in Recognizing Dates and Epochs}, 
  year={2021},
  pages={1-3},
  doi={10.1109/ECAI52376.2021.9515139}}
```
