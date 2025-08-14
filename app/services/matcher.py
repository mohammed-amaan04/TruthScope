import logging
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)

ENABLE_EMBEDDINGS = os.getenv("ENABLE_EMBEDDINGS", "0") == "1"
ENABLE_NLI = os.getenv("ENABLE_NLI", "0") == "1"

# Safe import for sentence-transformers
try:
    if ENABLE_EMBEDDINGS:
        from sentence_transformers import SentenceTransformer, util  # type: ignore
    else:
        SentenceTransformer = None  # type: ignore
        util = None  # type: ignore
except Exception as e:
    logger.warning(f"SentenceTransformer unavailable; using SequenceMatcher similarity. Reason: {e}")
    SentenceTransformer = None  # type: ignore
    util = None  # type: ignore

_model = None

def _get_embedding_model():
    global _model
    if _model is None and SentenceTransformer is not None and ENABLE_EMBEDDINGS:
        try:
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Failed to load embedding model; fallback to SequenceMatcher: {e}")
            _model = None
    return _model

# Try to load an NLI cross-encoder for entailment/contradiction lazily
_nli_model = None

def _get_nli_model():
    global _nli_model
    if not ENABLE_NLI:
        return None
    if _nli_model is None:
        try:
            from sentence_transformers import CrossEncoder  # type: ignore
            _nli_model = CrossEncoder('cross-encoder/nli-deberta-v3-base')
        except Exception as e:
            logger.warning(f"NLI CrossEncoder unavailable, using heuristic stance detection. Reason: {e}")
            _nli_model = None
    return _nli_model

NEGATION_TOKENS = {"not", "no", "never", "without", "false", "deny", "denies", "refute", "refutes", "debunk", "myth"}


def _has_negation(text: str) -> bool:
    words = {w.strip('.,!?;:"\'').lower() for w in text.split()}
    return any(tok in words for tok in NEGATION_TOKENS)


def _similarity(claim: str, text: str) -> float:
    """Compute similarity in [0,1] using embeddings when enabled; otherwise SequenceMatcher."""
    model = _get_embedding_model()
    if model is not None and util is not None:
        try:
            claim_emb = model.encode(claim[:512], convert_to_tensor=True)
            text_emb = model.encode(text[:1024], convert_to_tensor=True)
            sim = float(util.cos_sim(claim_emb, text_emb)[0])
            return max(0.0, min(1.0, sim))
        except Exception as e:
            logger.warning(f"Embedding similarity failed; falling back: {e}")
    from difflib import SequenceMatcher
    return SequenceMatcher(a=claim.lower(), b=text.lower()).ratio()


def _classify_stance(claim: str, text: str) -> float:
    """
    Return stance score in [-1, 1]: >0 support, <0 contradict, ~0 neutral.
    Prefer NLI if enabled and available; otherwise use negation-aware heuristic with similarity.
    """
    nli_model = _get_nli_model()
    if nli_model is not None:
        try:
            scores = nli_model.predict([(claim, text)])
            if hasattr(scores, 'shape') and len(scores.shape) == 1 and scores.shape[0] == 3:
                c, e, n = float(scores[0]), float(scores[1]), float(scores[2])
            else:
                c, e, n = 0.0, float(scores[0]) if hasattr(scores, '__len__') else float(scores), 0.0
            if e >= c and e >= n:
                return min(1.0, e)
            if c >= e and c >= n:
                return max(-1.0, -c)
            return 0.0
        except Exception as e:
            logger.warning(f"NLI prediction failed, using heuristic: {e}")

    claim_neg = _has_negation(claim)
    text_neg = _has_negation(text)
    sim = _similarity(claim, text)

    if claim_neg != text_neg and sim >= 0.5:
        return -min(1.0, sim)
    if sim > 0.6:
        return min(1.0, sim)
    if sim < 0.4:
        return -min(1.0, 0.5 * (0.4 - sim))
    return 0.0


def _is_duplicate(title_a: str, title_b: str) -> bool:
    from difflib import SequenceMatcher
    return SequenceMatcher(a=title_a.lower(), b=title_b.lower()).ratio() >= 0.92


def match_articles(claim: str, articles: List[dict]) -> Tuple[List[dict], List[dict]]:
    if not articles:
        logger.warning("No articles provided to match.")
        return [], []

    seen_titles: List[str] = []
    support: List[dict] = []
    contradict: List[dict] = []

    for article in articles:
        content = article.get('content', article.get('snippet', '')) or ''
        title = article.get('title', '') or ''
        text = f"{title} {content}".strip()
        if not text:
            continue

        if any(_is_duplicate(title, t) for t in seen_titles):
            continue

        stance_score = _classify_stance(claim, text)
        sim_score = _similarity(claim, text)

        article["similarity_score"] = round(sim_score, 4)
        article["stance_score"] = round(stance_score, 4)

        logger.info(f"[MATCHER] '{title[:50]}...' → sim: {sim_score:.4f}, stance: {stance_score:.3f}")

        if stance_score > 0.2:
            support.append(article)
            seen_titles.append(title)
        elif stance_score < -0.2:
            contradict.append(article)
            seen_titles.append(title)
        else:
            if sim_score >= 0.7:
                support.append(article)
                seen_titles.append(title)

    if not support and not contradict:
        logger.warning("[MATCHER] No strong matches — returning top-N closest articles instead")
        articles.sort(key=lambda x: x.get("similarity_score", 0.0), reverse=True)
        return articles[:5], []

    return support, contradict
