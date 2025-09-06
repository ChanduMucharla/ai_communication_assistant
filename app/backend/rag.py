
import os, glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleRAG:
    def __init__(self, kb_dir: str):
        self.kb_dir = kb_dir
        self.docs = []
        self.paths = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.matrix = None
        self._load()

    def _load(self):
        paths = glob.glob(os.path.join(self.kb_dir, "*.md"))
        self.paths = paths
        self.docs = [open(p, "r", encoding="utf-8", errors="ignore").read() for p in paths]
        if not self.docs:
            self.docs = ["No knowledge base content found."]
            self.paths = ["EMPTY"]
        self.matrix = self.vectorizer.fit_transform(self.docs)

    def top_k(self, query: str, k: int = 2):
        if self.matrix is None:
            return []
        qv = self.vectorizer.transform([query or ""])
        sims = cosine_similarity(qv, self.matrix).flatten()
        idxs = sims.argsort()[::-1][:k]
        out = []
        for i in idxs:
            out.append({"path": self.paths[i], "score": float(sims[i]), "chunk": self.docs[i]})
        return out
