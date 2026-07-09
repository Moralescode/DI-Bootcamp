# -*- coding: utf-8 -*-
"""
Défi quotidien : Analyse textuelle de livres de Lewis Carroll
Utilisation de NLTK et spaCy pour le prétraitement,
Bag of Words (BoW) et TF-IDF pour l'analyse statistique.
"""

# ============================================================================
# 1. IMPORT DES BIBLIOTHÈQUES
# ============================================================================
import re                          # Expressions régulières pour le nettoyage
import requests                    # Requêtes HTTP pour télécharger les textes
import matplotlib.pyplot as plt    # Graphiques (diagrammes circulaires)
from wordcloud import WordCloud    # Génération de nuages de mots
import nltk                        # Natural Language Toolkit
from nltk.corpus import stopwords  # Mots vides (stopwords)
from nltk.stem import PorterStemmer  # Racinisation (stemming)
from nltk import pos_tag, ne_chunk # Étiquetage POS et entités nommées
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer  # BoW et TF-IDF
import spacy                        # Lemmatisation avec modèle pré-entraîné

# ============================================================================
# 2. TÉLÉCHARGEMENT DES RESSOURCES NLTK
# ============================================================================
# Ces ressources sont nécessaires pour la tokenisation, l'étiquetage et le chunking
nltk.download('punkt_tab', quiet=True)                    # Tokeniseur par phrases
nltk.download('punkt', quiet=True)                        # Tokeniseur de mots
nltk.download('stopwords', quiet=True)                    # Liste des mots vides anglais
nltk.download('averaged_perceptron_tagger', quiet=True)   # Étiqueteur POS
nltk.download('averaged_perceptron_tagger_eng', quiet=True) # Étiqueteur POS (anglais)
nltk.download('maxent_ne_chunker', quiet=True)            # Extracteur d'entités nommées
nltk.download('maxent_ne_chunker_tab', quiet=True)        # Tables pour le chunking NE
nltk.download('words', quiet=True)                        # Liste de mots pour NE

# ============================================================================
# 3. DÉFINITION DES URLS ET TEXTES DE SECOURS
# ============================================================================
# URLs des livres de Lewis Carroll sur Project Gutenberg
URLS = [
    'https://www.gutenberg.org/cache/epub/11/pg11.txt',   # Alice au pays des merveilles
    'https://www.gutenberg.org/cache/epub/12/pg12.txt',   # De l'autre côté du miroir
    'https://www.gutenberg.org/cache/epub/29042/pg29042.txt'  # Une histoire complexe
]

# Textes de secours si le téléchargement échoue (connexion coupée, site indisponible, etc.)
FALLBACK_TEXTS = [
    # Extrait représentatif d'Alice au pays des merveilles
    (
        "Alice was beginning to get very tired of sitting by her sister on the bank, "
        "and of having nothing to do: once or twice she had peeped into the book her sister was reading, "
        "but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice "
        "'without pictures or conversation?' So she was considering in her own mind (as well as she could, "
        "for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain "
        "would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit "
        "with pink eyes ran close by her. There was nothing so very remarkable in that; nor did Alice think "
        "it so very much out of the way to hear the Rabbit say to itself, 'Oh dear! Oh dear! I shall be late!'"
        " when she ran across the field after it, and fortunately was just in time to see it pop down a "
        "large rabbit-hole under the hedge. In another moment down went Alice after it, never once "
        "considering how in the world she was to get out again."
    ),
    # Extrait représentatif de De l'autre côté du miroir
    (
        "Through the Looking-Glass is the sequel to Alice's Adventures in Wonderland. "
        "Alice again finds herself in a fantastical world, this time through a mirror. "
        "Everything is reversed, including logic and language. She meets the Red Queen, "
        "the White Queen, Tweedledum and Tweedledee, Humpty Dumpty, and many other characters. "
        "The world is like a giant chessboard, and Alice must advance across it to become a queen. "
        "She encounters strange poetry, talking flowers, and living chess pieces. "
        "The story explores themes of identity, logic, and growing up."
    ),
    # Extrait représentatif d'Une histoire complexe
    (
        "A Tangled Tale is a collection of mathematical puzzles presented in the form of a story. "
        "Lewis Carroll weaves mathematics into charming narratives. Each chapter presents a problem "
        "in arithmetic, algebra, or geometry, followed by solutions and discussions. "
        "The tales feature characters like the Knotty Knots, who debate mathematical concepts. "
        "Carroll uses humor and whimsy to make mathematics accessible and entertaining. "
        "The stories include topics such as probability, logic, and number theory. "
        "This charming book showcases Carroll's talent for blending wit with intellectual rigor."
    )
]

# ============================================================================
# 4. FONCTION DE NETTOYAGE DE TEXTE
# ============================================================================
def clean_text(text):
    """
    Nettoie un texte brut de Project Gutenberg :
    - Supprime les caractères nuls
    - Garde uniquement les lettres et espaces (supprime ponctuation, chiffres, etc.)
    - Recherche les marqueurs 'START OF THE PROJECT GUTENBERG EBOOK' et 'END OF THE PROJECT GUTENBERG'
      pour ne garder que le corps du texte (sans les mentions légales)
    """
    text = text.replace('\x00', '')  # Suppression des caractères nuls
    #Remplace tout ce qui n'est pas une lettre ou un espace par un espace
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Recherche du début du vrai contenu après le marqueur Gutenberg
    start = 0
    for marker in ['START OF THE PROJECT GUTENBERG EBOOK', 'CHAPTER I', 'CHAPTER 1']:
        idx = text.find(marker)
        if idx != -1:
            # On place le curseur juste après le marqueur trouvé
            start = max(start, idx + len(marker))

    # Recherche de la fin du vrai contenu avant le marqueur de fin
    end = len(text)
    for marker in ['END OF THE PROJECT GUTENBERG', 'End of the Project Gutenberg']:
        idx = text.rfind(marker)
        if idx != -1:
            end = min(end, idx)

    # Découpage du texte
    if start < end:
        text = text[start:end]
    return text

# ============================================================================
# 5. FONCTION DE CHARGEMENT DES TEXTES
# ============================================================================
def load_texts(urls):
    """
    Reçoit une liste d'URLs, télécharge chaque texte, le nettoie
    et renvoie la liste des textes nettoyés (corpus).
    En cas d'erreur réseau, utilise les textes de secours.
    """
    corpus = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=15)  # Téléchargement avec timeout de 15s
            text = resp.text                       # Contenu brut de la page
            corpus.append(clean_text(text))        # Nettoyage et ajout au corpus
        except Exception as e:
            print(f"Chargement échoué pour {url}, utilisation du texte local.")
            # Utilisation du texte de secours correspondant, ou du premier si index hors limites
            corpus.append(FALLBACK_TEXTS[len(corpus)] if len(corpus) < len(FALLBACK_TEXTS) else FALLBACK_TEXTS[0])
    return corpus

# ============================================================================
# 6. CHARGEMENT DU CORPUS
# ============================================================================
corpus = load_texts(URLS)

# ============================================================================
# 7. AFFICHAGE DES 200 PREMIERS CARACTÈRES DE CHAQUE TEXTE
# ============================================================================
print("=== 2. 200 premiers caractères de chaque texte ===")
for i, text in enumerate(corpus):
    print(f"Livre {i+1} (200 premiers caractères) :\n{text[:200]}\n")

# ============================================================================
# 8. TOKENISATION
# ============================================================================
"""
La tokenisation découpe le texte en mots (tokens).
NLTK utilise le tokeniseur Punkt qui gère la ponctuation
et les contractions (ex: "don't" -> ["do", "n't"]).
"""
print("=== 3. 150 premiers tokens de chaque livre ===")
tokenized_corpus = []  # Liste de listes de tokens
for text in corpus:
    tokens = nltk.word_tokenize(text)
    tokenized_corpus.append(tokens)

for i, tokens in enumerate(tokenized_corpus):
    print(f"Livre {i+1} (150 premiers tokens) : {tokens[:150]}\n")

# ============================================================================
# 9. SUPPRESSION DES MOTS VIDES (STOPWORDS)
# ============================================================================
"""
Les stopwords sont des mots très fréquents qui n'apportent pas
beaucoup d'information sémantique (articles, prépositions, pronoms, etc.).
On les supprime pour ne garder que les mots porteurs de sens.
"""
print("=== 4. Suppression des mots vides (stopwords) ===")
stop_words_en = set(stopwords.words('english'))  # Récupération des 179 stopwords anglais NLTK
filtered_corpus = []  # corpus sans stopwords
for tokens in tokenized_corpus:
    # Filtrage : on garde le token uniquement s'il n'est PAS dans les stopwords (en minuscules)
    filtered = [t for t in tokens if t.lower() not in stop_words_en]
    filtered_corpus.append(filtered)

# Vérification : on recherche certains stopwords spécifiques demandés dans l'exercice
# Si la suppression a bien fonctionné, leur count() doit être 0
for word in ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves']:
    for i, tokens in enumerate(filtered_corpus):
        print(f"Livre {i+1} : '{word}' trouvé {tokens.count(word)} fois")

# ============================================================================
# 10. RACINISATION (STEMMING) AVEC PORTER STEMMER
# ============================================================================
"""
Le stemming (ou racinisation) coupe les mots selon des règles heuristiques
pour en extraire la racine. Le PorterStemmer est l'algorithme le plus classique.
Inconvénient : la racine obtenue n'est pas toujours un mot réel du dictionnaire.
Exemple : 'running' -> 'run', 'studies' -> 'studi', 'better' -> 'better'
"""
print("\n=== 5. 50 premiers tokens stemmés (PorterStemmer) ===")
ps = PorterStemmer()
for i, tokens in enumerate(filtered_corpus):
    stemmed = [ps.stem(t) for t in tokens[:50]]
    print(f"Livre {i+1} (50 premiers stemmings) : {stemmed}\n")

# ============================================================================
# 11. LEMMATISATION AVEC SPACY
# ============================================================================
"""
La lemmatisation ramène chaque mot à sa forme canonique (lemme) en utilisant
un dictionnaire et l'analyse du contexte. Le modèle en_core_web_sm est un modèle
petit mais efficace pour l'anglais.
Avantage : le lemme est toujours un mot valide du dictionnaire.
Exemple : 'running' -> 'run', 'studies' -> 'study', 'better' -> 'good'
"""
print("=== 6. 50 premiers tokens lemmatisés (spaCy en_core_web_sm) ===")
nlp = spacy.load('en_core_web_sm')
for i, tokens in enumerate(filtered_corpus):
    # spaCy travaille sur une chaîne de caractères, pas sur une liste de tokens
    doc = nlp(' '.join(tokens))
    # Accès à l'attribut .lemma_ de chaque token
    lemmas = [token.lemma_ for token in doc][:50]
    print(f"Livre {i+1} (50 premiers lemmes spaCy) : {lemmas}\n")

# ============================================================================
# 12. DIFFÉRENCE LEMMATISATION VS RACINISATION
# ============================================================================
"""
Racinisation (PorterStemmer) :
  - Approche algorithmique : coupe de suffixes/préfixes selon des règles
  - Rapide, pas besoin de contexte
  - Racine parfois invalide : 'studi', 'happi'
  - Même racine pour mots différents : 'university' et 'universal' -> 'univers'

Lemmatisation (spaCy) :
  - Approche lexicale : utilise un dictionnaire + analyse morphologique
  - Plus lente, nécessite un modèle linguistique
  - Lemme toujours valide : 'studies' -> 'study', 'happily' -> 'happily' (ou 'happy')
  - Sensible à la POS : 'running' (VERB) -> 'run', 'running' (NOUN) -> 'running'
"""
print("=== 7. Différence lemmatisation vs racinisation ===")
print("La lemmatisation utilise un dictionnaire pour trouver la forme canonique du mot,")
print("tandis que le stemmer Porter coupe les mots selon des règles heuristiques (suffixes).")
print("Exemple : 'better' -> stemmer='better', lemmatiseur='good'.\n")

# ============================================================================
# 13. ÉTIQUETAGE MORPHOSYNTAXIQUE (POS TAGGING) AVEC NLTK
# ============================================================================
"""
Le POS tagging associe à chaque token une étiquette grammaticale :
NNP = nom propre singulier, NN = nom commun, VBD = verbe passé, JJ = adjectif, etc.
Le tagger utilisé est le PerceptronTagger ( averaged_perceptron_tagger_eng ).
"""
print("=== 8. POS tags NLTK ===")
for i, tokens in enumerate(filtered_corpus):
    pos_tags = pos_tag(tokens)  # Liste de tuples (mot, étiquette)
    print(f"Livre {i+1} POS tags (20 premiers) : {pos_tags[:20]}\n")

# ============================================================================
# 14. EXTRACTION D'ENTITÉS NOMMÉES (NER) AVEC NLTK
# ============================================================================
"""
L'extraction d'entités nommées identifie les personnes (PERSON), organisations (ORGANIZATION),
lieux (GPE), dates (DATE), etc. NLTK utilise un chunker Maxent basé sur des classifieurs.
Le résultat est un arbre (Tree) où les entités sont regroupées.
"""
print("=== 9. Entités nommées NLTK ===")
for i, tokens in enumerate(filtered_corpus):
    pos_tags = pos_tag(tokens)          # Étape 1 : POS tagging
    entities = ne_chunk(pos_tags)       # Étape 2 : chunking des entités
    print(f"Livre {i+1} entités nommées (20 premières) : {list(entities)[:20]}\n")

# ============================================================================
# 15. NUAGES DE MOTS (WORDCLOUD)
# ============================================================================
"""
WordCloud génère une image où la taille de chaque mot est proportionnelle
à sa fréquence dans le texte. Plus le mot est grand, plus il est fréquent.
Cela permet une visualisation rapide des thèmes dominants.
"""
print("=== Analyse du texte - Nuages de mots ===")
for i, text in enumerate(corpus):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Nuage de mots - Livre {i+1}')
    plt.savefig(f'img/wordcloud_livre_{i+1}.png')
    plt.close()

# ============================================================================
# 16. BAG OF WORDS (BoW) - COUNT VECTORIZER
# ============================================================================
"""
Le Bag of Words représente chaque document par un vecteur de dimensions = vocabulaire total.
Chaque case indique la fréquence brute du mot dans le document.
CountVectorizer de scikit-learn implémente le BoW.
Indice de l'exercice : le meilleur texte à utiliser est le texte filtré (sans stopwords),
car les stopwords polluent les résultats (ex: 'the', 'and', 'of' sont toujours en tête).
"""
print("=== Bag of Words : 5 mots les plus fréquents ===")
# Reconstruction des textes à partir des tokens filtrés
clean_texts = [' '.join(tokens) for tokens in filtered_corpus]

# Création de la matrice BoW : lignes = documents, colonnes = mots du vocabulaire
bow = CountVectorizer().fit_transform(clean_texts)
# Récupération de la liste des mots du vocabulaire pour l'affichage
words = CountVectorizer().fit(clean_texts).get_feature_names_out()

# Analyse des 5 mots les plus fréquents par document
for i in range(3):
    row = bow[i].toarray()[0]          # Ligne i de la matrice BoW (vecteur de fréquences)
    top_idx = row.argsort()[-5:][::-1] # Indices des 5 plus grandes valeurs (triées décroissant)
    print(f"Livre {i+1} - 5 mots les plus fréquents :")
    for idx in top_idx:
        # idx : position du mot dans le vocabulaire
        # words[idx] : le mot lui-même
        # row[idx] : sa fréquence dans le document
        print(f"  Doc {i} | Index {idx} | Mot '{words[idx]}' | Fréquence {int(row[idx])}")
    print()

# ============================================================================
# 17. DIAGRAMMES CIRCULAIRES BoW
# ============================================================================
"""
Visualisation des 5 mots les plus fréquents sous forme de pie charts.
"""
for i in range(3):
    row = bow[i].toarray()[0]
    top_idx = row.argsort()[-5:][::-1]
    labels = [words[j] for j in top_idx]   # Noms des mots pour la légende
    sizes = [row[j] for j in top_idx]      # Fréquences pour les pourcentages
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title(f'Top 5 mots - Livre {i+1} (BoW)')
    plt.savefig(f'img/pie_livre_{i+1}_bow.png')
    plt.close()

# ============================================================================
# 18. TF-IDF (TERM FREQUENCY - INVERSE DOCUMENT FREQUENCY)
# ============================================================================
"""
Le TF-IDF pondère chaque mot par sa rareté dans l'ensemble du corpus.
  TF(mot, doc) = fréquence brute du mot dans le document
  IDF(mot) = log(N / nb_docs_contenant_le_mot)
  TF-IDF = TF x IDF

Un mot fréquent dans UN SEUL document mais rare dans les autres aura un score TF-IDF élevé.
Un mot fréquent dans TOUS les documents aura un score TF-IDF faible.

min_df=1 : on garde les mots présents dans au moins 1 document
max_df=2 : on exclut les mots présents dans PLUS de 2 documents (trop génériques)
"""
print("=== TF-IDF : 5 mots les plus pertinents ===")
tfidf = TfidfVectorizer(min_df=1, max_df=2)
tfidf_matrix = tfidf.fit_transform(clean_texts)  # Matrice TF-IDF
tfidf_words = tfidf.get_feature_names_out()      # Vocabulaire TF-IDF

for i in range(3):
    row = tfidf_matrix[i].toarray()[0]
    top_idx = row.argsort()[-5:][::-1]
    print(f"Livre {i+1} TF-IDF - Top 5 mots :")
    for idx in top_idx:
        print(f"  Doc {i} | Index {idx} | Mot '{tfidf_words[idx]}' | Score TF-IDF {row[idx]:.4f}")
    print()

# ============================================================================
# 19. DIAGRAMMES CIRCULAIRES TF-IDF
# ============================================================================
"""
Visualisation des 5 mots les plus pertinents (TF-IDF) sous forme de pie charts.
Contrairement au BoW, ces mots sont spécifiques à chaque document.
"""
for i in range(3):
    row = tfidf_matrix[i].toarray()[0]
    top_idx = row.argsort()[-5:][::-1]
    labels = [tfidf_words[j] for j in top_idx]
    sizes = [row[j] for j in top_idx]
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title(f'Top 5 mots - Livre {i+1} (TF-IDF)')
    plt.savefig(f'img/pie_livre_{i+1}_tfidf.png')
    plt.close()
