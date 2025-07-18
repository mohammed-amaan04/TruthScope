"""
Sophisticated Text Paraphraser Module
Generates multiple paraphrased versions of input text for enhanced web scraping
"""

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
import spacy
import re
import logging
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
import asyncio
from concurrent.futures import ThreadPoolExecutor

from config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ParaphraseResult:
    """Result of text paraphrasing"""
    original_text: str
    paraphrases: List[str]
    keywords: List[str]
    entities: List[Dict[str, str]]
    search_queries: List[str]
    processing_time: float

class TextParaphraser:
    """Advanced text paraphraser using T5 and spaCy for intelligent paraphrasing"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.nlp = None
        self.device = config.DEVICE
        self.model_path = config.PARAPHRASE_MODEL
        self.num_paraphrases = config.NUM_PARAPHRASES
        self.diversity = config.PARAPHRASE_DIVERSITY
        
    def load_models(self):
        """Load T5 paraphrasing model and spaCy NLP pipeline"""
        logger.info(f"🤖 Loading paraphrasing model: {self.model_path}")
        
        try:
            # Load T5 model for paraphrasing
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)
            
            if self.device == "cuda" and torch.cuda.is_available():
                self.model = self.model.to(self.device)
                logger.info("✅ Model loaded on CUDA")
            else:
                logger.info("✅ Model loaded on CPU")
            
            # Load spaCy for NLP processing
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("✅ spaCy model loaded")
            except OSError:
                logger.warning("⚠️ spaCy model not found. Install with: python -m spacy download en_core_web_sm")
                self.nlp = None
                
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
            raise
    
    async def generate_paraphrases(self, text: str) -> ParaphraseResult:
        """
        Generate multiple paraphrased versions of the input text
        
        Args:
            text: Original text to paraphrase
            
        Returns:
            ParaphraseResult with paraphrases, keywords, and search queries
        """
        import time
        start_time = time.time()
        
        if not self.model:
            self.load_models()
        
        logger.info(f"🔄 Generating {self.num_paraphrases} paraphrases for: {text[:100]}...")
        
        # Step 1: Extract keywords and entities
        keywords, entities = self._extract_keywords_and_entities(text)
        
        # Step 2: Generate paraphrases using different strategies
        paraphrases = await self._generate_diverse_paraphrases(text)
        
        # Step 3: Create search queries
        search_queries = self._create_search_queries(text, paraphrases, keywords)
        
        processing_time = time.time() - start_time
        
        result = ParaphraseResult(
            original_text=text,
            paraphrases=paraphrases,
            keywords=keywords,
            entities=entities,
            search_queries=search_queries,
            processing_time=processing_time
        )
        
        logger.info(f"✅ Generated {len(paraphrases)} paraphrases in {processing_time:.2f}s")
        return result
    
    def _extract_keywords_and_entities(self, text: str) -> Tuple[List[str], List[Dict[str, str]]]:
        """Extract keywords and named entities from text"""
        keywords = []
        entities = []
        
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract keywords (nouns, proper nouns, adjectives)
            keywords = [
                token.lemma_.lower() for token in doc 
                if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] 
                and not token.is_stop 
                and len(token.text) > 2
                and token.is_alpha
            ]
            
            # Extract named entities
            entities = [
                {
                    'text': ent.text,
                    'label': ent.label_,
                    'description': spacy.explain(ent.label_)
                }
                for ent in doc.ents
            ]
        else:
            # Fallback: simple keyword extraction
            words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
            keywords = list(set(words))[:10]  # Limit to 10 keywords
        
        return keywords[:15], entities  # Limit keywords to 15
    
    async def _generate_diverse_paraphrases(self, text: str) -> List[str]:
        """Generate diverse paraphrases using multiple strategies"""
        paraphrases = set()
        
        # Strategy 1: Direct T5 paraphrasing
        direct_paraphrases = await self._t5_paraphrase(text, num_return_sequences=5)
        paraphrases.update(direct_paraphrases)
        
        # Strategy 2: Question-based paraphrasing
        question_paraphrases = await self._question_based_paraphrase(text)
        paraphrases.update(question_paraphrases)
        
        # Strategy 3: Keyword-focused paraphrasing
        keyword_paraphrases = await self._keyword_focused_paraphrase(text)
        paraphrases.update(keyword_paraphrases)
        
        # Remove original text and filter
        paraphrases.discard(text)
        filtered_paraphrases = self._filter_paraphrases(list(paraphrases), text)
        
        return filtered_paraphrases[:self.num_paraphrases]
    
    async def _t5_paraphrase(self, text: str, num_return_sequences: int = 3) -> List[str]:
        """Generate paraphrases using T5 model"""
        try:
            # Prepare input for T5
            input_text = f"paraphrase: {text}"
            inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
            
            if self.device == "cuda":
                inputs = inputs.to(self.device)
            
            # Generate paraphrases
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=150,
                    num_return_sequences=num_return_sequences,
                    temperature=self.diversity,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    no_repeat_ngram_size=2
                )
            
            # Decode outputs
            paraphrases = []
            for output in outputs:
                paraphrase = self.tokenizer.decode(output, skip_special_tokens=True)
                if paraphrase and paraphrase != text:
                    paraphrases.append(paraphrase)
            
            return paraphrases
            
        except Exception as e:
            logger.error(f"❌ T5 paraphrasing failed: {e}")
            return []
    
    async def _question_based_paraphrase(self, text: str) -> List[str]:
        """Generate paraphrases by converting to questions and back"""
        question_templates = [
            f"Is it true that {text.lower()}?",
            f"What about the claim that {text.lower()}?",
            f"How accurate is the statement: {text}?",
            f"Can we verify that {text.lower()}?"
        ]
        return question_templates
    
    async def _keyword_focused_paraphrase(self, text: str) -> List[str]:
        """Generate paraphrases focusing on key terms"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        key_phrases = []
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:
                key_phrases.append(chunk.text)
        
        # Create focused queries
        focused_paraphrases = []
        for phrase in key_phrases[:3]:
            focused_paraphrases.extend([
                f"{phrase} news verification",
                f"{phrase} fact check",
                f"latest news about {phrase}",
                f"{phrase} recent developments"
            ])
        
        return focused_paraphrases
    
    def _filter_paraphrases(self, paraphrases: List[str], original: str) -> List[str]:
        """Filter and rank paraphrases by quality"""
        filtered = []
        
        for paraphrase in paraphrases:
            # Basic quality checks
            if (len(paraphrase) >= config.MIN_PARAPHRASE_LENGTH and
                paraphrase.lower() != original.lower() and
                self._is_meaningful_paraphrase(paraphrase, original)):
                filtered.append(paraphrase)
        
        return filtered
    
    def _is_meaningful_paraphrase(self, paraphrase: str, original: str) -> bool:
        """Check if paraphrase is meaningful and different enough"""
        # Simple similarity check (can be enhanced with semantic similarity)
        paraphrase_words = set(paraphrase.lower().split())
        original_words = set(original.lower().split())
        
        # Calculate Jaccard similarity
        intersection = len(paraphrase_words.intersection(original_words))
        union = len(paraphrase_words.union(original_words))
        
        if union == 0:
            return False
        
        similarity = intersection / union
        return 0.3 <= similarity <= 0.8  # Not too similar, not too different
    
    def _create_search_queries(self, original: str, paraphrases: List[str], keywords: List[str]) -> List[str]:
        """Create optimized search queries for web scraping"""
        search_queries = []
        
        # Add original text
        search_queries.append(original)
        
        # Add paraphrases
        search_queries.extend(paraphrases)
        
        # Add keyword combinations
        if len(keywords) >= 2:
            for i in range(0, len(keywords), 2):
                if i + 1 < len(keywords):
                    search_queries.append(f"{keywords[i]} {keywords[i+1]}")
        
        # Add fact-checking specific queries
        fact_check_queries = [
            f"{original} fact check",
            f"{original} verification",
            f"{original} true or false",
            f"is {original.lower()} real"
        ]
        search_queries.extend(fact_check_queries)
        
        # Remove duplicates and limit
        unique_queries = list(dict.fromkeys(search_queries))  # Preserve order
        return unique_queries[:20]  # Limit to 20 queries

# Convenience function
async def generate_paraphrases(text: str) -> ParaphraseResult:
    """
    Generate paraphrases for the given text
    
    Args:
        text: Text to paraphrase
        
    Returns:
        ParaphraseResult with paraphrases and search queries
    """
    paraphraser = TextParaphraser()
    return await paraphraser.generate_paraphrases(text)
