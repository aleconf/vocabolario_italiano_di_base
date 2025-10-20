from collections import Counter
import json
import pdfplumber
import pymupdf


def find_bold_italics():
    to_exclude = [
        "Il Nuovo vocabolario di base",
        "della lingua italiana",
        "A cura di Tullio De Mauro",
        "Dizionario",
        "neretto tondo",
        "fondamentali",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "corsivo chiaro",
        "alta disponibilità",
    ]

    result_bold = list()
    result_italic = list()
    doc = pymupdf.open("data/nuovovocabolariodibase.pdf")
    for page in doc:
        blocks = page.get_text("dict", flags=11)["blocks"]
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    if "Bold" in span["font"] and span["text"] not in to_exclude:
                        result_bold.append(span["text"])
                    elif "Italic" in span["font"] and span["text"] not in to_exclude:
                        result_italic.append(span["text"])
    return (result_bold, result_italic)


def clean_set(words):
    cleansed = list()
    for i in range(len(words)):
        while True:
            prev = len(words[i])
            words[i] = words[i].strip("\n")
            words[i] = words[i].strip()
            if len(words[i]) == prev:
                break
    for i in range(len(words)):
        if i > 0 and words[i - 1][-1] == "-":
            continue
        elif words[i][-1] == "-":
            cleansed.append(words[i][:-1] + words[i + 1])
        else:
            cleansed.append(words[i])

    result = set()
    for i in range(len(cleansed)):
        if i > 0 and cleansed[i - 1][0] in ["1", "2", "3", "4"]:
            continue
        elif cleansed[i][0] in ["1", "2", "3", "4"]:
            result.add(cleansed[i] + cleansed[i + 1])
        else:
            result.add(cleansed[i])
    return result


def text_parser():
    letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    text_pages = list()
    with pdfplumber.open("data/nuovovocabolariodibase.pdf") as pdf:
        for index, page in enumerate(pdf.pages):
            aux = page.extract_text()
            aux = aux.split("2016")[-1]
            footer = f"Il Nuovo vocabolario di base della lingua italiana - Tullio De Mauro - Internazionale (dizionario.internazionale.it/nuovovocabolariodibase 1) {index + 1}"
            aux = aux.replace(footer, "")
            for letter in letters:
                aux = aux.replace("\n" + letter + "\n", ",\n")
            text_pages.append(aux)

    parole = "\n".join(text_pages)
    while True:
        prev = len(parole)
        parole = parole.replace("\n\n", "\n")
        if len(parole) == prev:
            break
    parole = parole.replace("\n", "#")
    parole = parole.replace("-#", "")
    parole = parole.replace("#", " ")
    while True:
        prev = len(parole)
        parole = parole.replace("  ", " ")
        if len(parole) == prev:
            break
    parole = parole.strip()
    return parole


def livello1(field1, field2):
    return field2.startswith(field1) or " " + field1 in field2


def livello2(field1, field2):
    return " " + field1 in field2 or "." + field1 in field2


clean_bold = clean_set(find_bold_italics()[0])
clean_italic = clean_set(find_bold_italics()[1])
# both = clean_bold & clean_italic

words = text_parser().split(",")
for i in range(len(words)):
    words[i] = words[i].strip()

prefixes = [word.split(" ")[0] for word in words]
clean_words = list()
for i in range(len(words) - 1):
    if "." in prefixes[i]:
        continue
    for j in range(i + 1, len(words)):
        if "." not in prefixes[j]:
            break
    clean_words.append(", ".join(words[i:j]))
if "." not in prefixes[-1]:
    clean_words.append(words[-1])
else:
    clean_words[-1] = clean_words[-1] + ", " + words[-1]

words_dict = dict()
for word in clean_words[1:]:
    aux = word.split(" ")
    while len(aux) > 1 and "." not in aux[1]:
        aux[0] = aux[0] + " " + aux[1]
        del aux[1]
    words_dict[aux[0]] = dict()
    if aux[0][0] in ["1", "2", "3", "4"]:
        words_dict[aux[0]]["parola"] = aux[0][1:]
    else:
        words_dict[aux[0]]["parola"] = aux[0]
    words_dict[aux[0]]["qualifica_grammaticale"] = " ".join(aux[1:])
    if aux[0] in clean_bold:
        words_dict[aux[0]]["marca_d_uso"] = "parola fondamentale"
    elif aux[0] in clean_italic:
        words_dict[aux[0]]["marca_d_uso"] = "parola di alta disponibilità"
    else:
        words_dict[aux[0]]["marca_d_uso"] = "parola di alto uso"

with open("output/vocabolario.json", "w", encoding="utf-8") as f:
    json.dump(words_dict, f, ensure_ascii=False, indent=4)

print("\n\n############################## Osservazioni #############################\n")
words = [x.split(" ")[0] for x in clean_words]
count = Counter(words)

doubles = [x for x in count if count[x] > 1]
print("-- I seguenti lemmi appaiono due volte nel file PDF:", doubles)
polirematici = [(lemma, words_dict[lemma]) for lemma in words_dict if " " in lemma]
print("-- Lemmi polirematici presenti:", polirematici)
senza_qualifica = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if words_dict[lemma]["qualifica_grammaticale"] == ""
]
print("-- Lemmi senza qualifica grammaticale:", senza_qualifica)

print("\n############################## Statistiche ##############################\n")

print("Numero totale di lemmi presenti:", len(words_dict))

fondamentali = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if words_dict[lemma]["marca_d_uso"] == "parola fondamentale"
]

alta_disponibilita = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if words_dict[lemma]["marca_d_uso"] == "parola di alta disponibilità"
]

alto_uso = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if words_dict[lemma]["marca_d_uso"] == "parola di alto uso"
]

print("\nSuddivisione in base alla marca d'uso:\n")
print("-- numero di lemmi con marca d'uso «parola fondamentale»:", len(fondamentali))

print(
    "-- numero di lemmi con marca d'uso «parola di alta disponibilità»:",
    len(alta_disponibilita),
)

print("-- numero di lemmi con marca d'uso «parola di alto uso»:", len(alto_uso), "\n")

print("\n########################### Esempi di analisi ###########################")

s_m_fond = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if words_dict[lemma]["marca_d_uso"] == "parola fondamentale"
    and livello1("s.", words_dict[lemma]["qualifica_grammaticale"])
    and livello2("m.", words_dict[lemma]["qualifica_grammaticale"])
]

print(
    f"\nNel vocabolario ci sono {len(s_m_fond)} lemmi sostantivi maschili "
    + "con marca d'uso «parola fondamentale».\n"
)

tr_intr = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if livello1("v.", words_dict[lemma]["qualifica_grammaticale"])
    and livello2("tr.", words_dict[lemma]["qualifica_grammaticale"])
    and livello2("intr.", words_dict[lemma]["qualifica_grammaticale"])
]

print(
    f"\nNel vocabolario ci sono {len(tr_intr)} lemmi che sono verbi sia "
    + "transitivi che intransitivi.\n"
)

pronom_tr_intr = [
    (lemma, words_dict[lemma])
    for lemma in words_dict
    if livello1("v.", words_dict[lemma]["qualifica_grammaticale"])
    and livello2("tr.", words_dict[lemma]["qualifica_grammaticale"])
    and livello2("intr.", words_dict[lemma]["qualifica_grammaticale"])
    and livello2("pronom.", words_dict[lemma]["qualifica_grammaticale"])
]

print(
    "\nQuesto è l'elenco dei verbi pronominali che sono sia transitivi che"
    + " intransitivi:",
    pronom_tr_intr,
    "\n",
)
