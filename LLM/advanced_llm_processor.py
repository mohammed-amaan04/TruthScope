"""
Advanced LLM Processor
Sophisticated LLM processing with enhanced prompt engineering and multi-step analysis
"""

import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM,
    BitsAndBytesConfig, pipeline
)
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re
import time
from datetime import datetime

from config import config
from content_analyzer import ContentAnalysis

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMAnalysisResult:
    """Advanced LLM analysis result"""
    truth_score: float  # 0.0 to 1.0
    confidence_score: float  # 0.0 to 1.0
    accuracy_score: float  # 0.0 to 1.0
    factual_summary: str
    supporting_evidence_summary: str
    contradicting_evidence_summary: str
    key_facts_verified: List[str]
    key_facts_disputed: List[str]
    regional_context_analysis: str
    temporal_context_analysis: str
    source_reliability_assessment: str
    final_verdict: str  # "TRUE", "FALSE", "MIXED", "INSUFFICIENT_DATA"
    reasoning_chain: List[str]
    confidence_factors: Dict[str, float]
    processing_time: float

class AdvancedLLMProcessor:
    """Sophisticated LLM processor for fact-checking analysis"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = config.DEVICE
        self.model_path = config.LLAMA_MODEL_PATH
        self.max_length = config.MAX_LENGTH
        self.temperature = config.TEMPERATURE
        
    def load_model(self):
        """Load the LLM model with optimizations"""
        logger.info(f"🤖 Loading advanced LLM model: {self.model_path}")
        
        try:
            # Configure quantization for memory efficiency
            if self.device == "cuda" and torch.cuda.is_available():
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    quantization_config=quantization_config,
                    device_map="auto",
                    torch_dtype=torch.float16
                )
                logger.info("✅ Model loaded with 4-bit quantization on CUDA")
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path,
                    torch_dtype=torch.float32
                )
                logger.info("✅ Model loaded on CPU")
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            # Fallback to smaller model
            logger.info("🔄 Falling back to T5 model...")
            self._load_fallback_model()
    
    def _load_fallback_model(self):
        """Load fallback T5 model"""
        try:
            self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
            self.tokenizer = AutoTokenizer.from_pretrained("t5-base")
            if self.device == "cuda":
                self.model = self.model.to(self.device)
            logger.info("✅ Fallback T5 model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load fallback model: {e}")
            raise
    
    async def process_analysis(self, content_analysis: ContentAnalysis) -> LLMAnalysisResult:
        """
        Process content analysis with advanced LLM reasoning
        
        Args:
            content_analysis: Comprehensive content analysis
            
        Returns:
            LLMAnalysisResult with sophisticated analysis
        """
        start_time = time.time()
        
        if not self.model:
            self.load_model()
        
        logger.info(f"🧠 Processing advanced LLM analysis for: {content_analysis.original_claim[:100]}...")
        
        # Step 1: Multi-step analysis
        reasoning_chain = []
        
        # Step 1a: Initial fact assessment
        fact_assessment = await self._assess_factual_content(content_analysis)
        reasoning_chain.append(f"Fact Assessment: {fact_assessment}")
        
        # Step 1b: Source credibility evaluation
        credibility_assessment = await self._evaluate_source_credibility(content_analysis)
        reasoning_chain.append(f"Source Credibility: {credibility_assessment}")
        
        # Step 1c: Evidence consistency analysis
        consistency_analysis = await self._analyze_evidence_consistency(content_analysis)
        reasoning_chain.append(f"Evidence Consistency: {consistency_analysis}")
        
        # Step 2: Generate comprehensive analysis
        comprehensive_analysis = await self._generate_comprehensive_analysis(content_analysis, reasoning_chain)
        
        # Step 3: Calculate sophisticated scores
        scores = self._calculate_sophisticated_scores(content_analysis, comprehensive_analysis)
        
        # Step 4: Extract key insights
        key_insights = self._extract_key_insights(comprehensive_analysis, content_analysis)
        
        processing_time = time.time() - start_time
        
        result = LLMAnalysisResult(
            truth_score=scores['truth_score'],
            confidence_score=scores['confidence_score'],
            accuracy_score=scores['accuracy_score'],
            factual_summary=key_insights['factual_summary'],
            supporting_evidence_summary=key_insights['supporting_summary'],
            contradicting_evidence_summary=key_insights['contradicting_summary'],
            key_facts_verified=key_insights['verified_facts'],
            key_facts_disputed=key_insights['disputed_facts'],
            regional_context_analysis=key_insights['regional_analysis'],
            temporal_context_analysis=key_insights['temporal_analysis'],
            source_reliability_assessment=credibility_assessment,
            final_verdict=scores['verdict'],
            reasoning_chain=reasoning_chain,
            confidence_factors=scores['confidence_factors'],
            processing_time=processing_time
        )
        
        logger.info(f"✅ Advanced LLM analysis complete in {processing_time:.2f}s")
        logger.info(f"📊 Truth: {result.truth_score:.1%}, Confidence: {result.confidence_score:.1%}")
        
        return result
    
    async def _assess_factual_content(self, analysis: ContentAnalysis) -> str:
        """Assess factual content of the claim"""
        prompt = self._create_fact_assessment_prompt(analysis)
        response = await self._generate_llm_response(prompt, max_tokens=200)
        return response
    
    async def _evaluate_source_credibility(self, analysis: ContentAnalysis) -> str:
        """Evaluate credibility of sources"""
        prompt = self._create_credibility_prompt(analysis)
        response = await self._generate_llm_response(prompt, max_tokens=150)
        return response
    
    async def _analyze_evidence_consistency(self, analysis: ContentAnalysis) -> str:
        """Analyze consistency of evidence"""
        prompt = self._create_consistency_prompt(analysis)
        response = await self._generate_llm_response(prompt, max_tokens=200)
        return response
    
    async def _generate_comprehensive_analysis(self, analysis: ContentAnalysis, reasoning_chain: List[str]) -> str:
        """Generate comprehensive final analysis"""
        prompt = self._create_comprehensive_prompt(analysis, reasoning_chain)
        response = await self._generate_llm_response(prompt, max_tokens=500)
        return response
    
    def _create_fact_assessment_prompt(self, analysis: ContentAnalysis) -> str:
        """Create prompt for factual assessment"""
        structured_data = analysis.structured_json_for_llm
        
        prompt = f"""
Analyze the following claim for factual accuracy based on the evidence provided:

CLAIM: {analysis.original_claim}

EVIDENCE SUMMARY:
- Supporting sources: {structured_data['evidence_summary']['supporting_sources']}
- Contradicting sources: {structured_data['evidence_summary']['contradicting_sources']}
- Overall source credibility: {structured_data['source_analysis']['overall_credibility']:.2f}

KEY SUPPORTING EVIDENCE:
{self._format_evidence_list(analysis.supporting_articles[:3])}

KEY CONTRADICTING EVIDENCE:
{self._format_evidence_list(analysis.contradicting_articles[:3])}

Provide a factual assessment focusing on:
1. What aspects of the claim can be verified
2. What aspects are disputed or unverified
3. The quality and reliability of available evidence

Assessment:"""
        
        return prompt
    
    def _create_credibility_prompt(self, analysis: ContentAnalysis) -> str:
        """Create prompt for source credibility evaluation"""
        credibility_data = analysis.source_credibility_analysis
        
        prompt = f"""
Evaluate the credibility of sources for this fact-check:

CLAIM: {analysis.original_claim}

SOURCE CREDIBILITY ANALYSIS:
- Overall credibility score: {credibility_data['overall_credibility_score']:.2f}
- High credibility sources: {credibility_data['credibility_distribution']['high']}
- Medium credibility sources: {credibility_data['credibility_distribution']['medium']}
- Low credibility sources: {credibility_data['credibility_distribution']['low']}

MOST CREDIBLE SOURCES:
{self._format_credible_sources(credibility_data['most_credible_sources'][:3])}

Evaluate the source reliability and its impact on the analysis:"""
        
        return prompt
    
    def _create_consistency_prompt(self, analysis: ContentAnalysis) -> str:
        """Create prompt for evidence consistency analysis"""
        prompt = f"""
Analyze the consistency of evidence for this claim:

CLAIM: {analysis.original_claim}

EVIDENCE DISTRIBUTION:
- Supporting: {len(analysis.supporting_articles)}
- Contradicting: {len(analysis.contradicting_articles)}
- Neutral: {len(analysis.neutral_articles)}

TEMPORAL CONTEXT:
- Recent articles (last week): {analysis.temporal_analysis['temporal_clustering'].get('last_week', 0)}
- Recency score: {analysis.temporal_analysis['recency_score']:.2f}

REGIONAL DIVERSITY:
- Regions covered: {analysis.regional_analysis['total_regions']}
- Diversity score: {analysis.regional_analysis['regional_diversity_score']:.2f}

Analyze the consistency and reliability of the evidence pattern:"""
        
        return prompt
    
    def _create_comprehensive_prompt(self, analysis: ContentAnalysis, reasoning_chain: List[str]) -> str:
        """Create comprehensive analysis prompt"""
        prompt = f"""
Provide a comprehensive fact-check analysis based on all available evidence:

CLAIM: {analysis.original_claim}

PREVIOUS ANALYSIS STEPS:
{chr(10).join(reasoning_chain)}

COMPLETE EVIDENCE SUMMARY:
{json.dumps(analysis.structured_json_for_llm, indent=2)[:1500]}...

Provide a comprehensive analysis including:
1. Factual summary of what is actually true
2. Truth percentage (0-100%)
3. Confidence level (0-100%)
4. Final verdict (TRUE/FALSE/MIXED/INSUFFICIENT_DATA)
5. Key supporting and contradicting points
6. Regional and temporal context impact

Comprehensive Analysis:"""
        
        return prompt
    
    async def _generate_llm_response(self, prompt: str, max_tokens: int = 300) -> str:
        """Generate response from LLM"""
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=2048, truncation=True)
            
            if self.device == "cuda" and torch.cuda.is_available():
                inputs = inputs.to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_tokens,
                    temperature=self.temperature,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode only the new tokens
            response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
            return response.strip()
            
        except Exception as e:
            logger.error(f"❌ LLM generation failed: {e}")
            return "Analysis unavailable due to processing error."
    
    def _calculate_sophisticated_scores(self, analysis: ContentAnalysis, llm_response: str) -> Dict[str, Any]:
        """Calculate sophisticated truth, confidence, and accuracy scores"""
        
        # Base calculations
        total_articles = len(analysis.supporting_articles) + len(analysis.contradicting_articles)
        supporting_count = len(analysis.supporting_articles)
        contradicting_count = len(analysis.contradicting_articles)
        
        # Truth Score Calculation (0% no sources, 100% perfect agreement)
        if total_articles == 0:
            truth_score = config.NO_SOURCES_SCORE
        else:
            support_ratio = supporting_count / total_articles
            
            # Apply source credibility weighting
            credibility_weight = analysis.source_credibility_analysis['overall_credibility_score']
            
            # Apply variation penalty
            variation_penalty = abs(supporting_count - contradicting_count) / max(total_articles, 1)
            variation_penalty *= config.VARIATION_PENALTY_FACTOR
            
            # Calculate base truth score
            truth_score = support_ratio * credibility_weight
            
            # Apply bonuses for high agreement
            if supporting_count >= config.MIN_SOURCES_FOR_HIGH_CONFIDENCE and contradicting_count == 0:
                truth_score = min(config.PERFECT_MATCH_SCORE, truth_score + 0.2)
            
            # Apply variation penalty
            truth_score = max(0.0, truth_score - variation_penalty)
        
        # Confidence Score Calculation
        confidence_factors = {
            'source_quantity': min(total_articles / 10, 1.0),
            'source_credibility': analysis.source_credibility_analysis['overall_credibility_score'],
            'temporal_relevance': analysis.temporal_analysis['recency_score'],
            'regional_diversity': analysis.regional_analysis['regional_diversity_score'],
            'evidence_consistency': 1.0 - (abs(supporting_count - contradicting_count) / max(total_articles, 1))
        }
        
        confidence_score = sum(confidence_factors.values()) / len(confidence_factors)
        
        # Accuracy Score (based on source quality and consistency)
        accuracy_score = (
            confidence_factors['source_credibility'] * 0.4 +
            confidence_factors['evidence_consistency'] * 0.3 +
            confidence_factors['source_quantity'] * 0.2 +
            confidence_factors['temporal_relevance'] * 0.1
        )
        
        # Determine verdict
        if truth_score >= 0.8 and confidence_score >= 0.7:
            verdict = "TRUE"
        elif truth_score <= 0.2 and confidence_score >= 0.7:
            verdict = "FALSE"
        elif total_articles >= 3 and abs(supporting_count - contradicting_count) <= 1:
            verdict = "MIXED"
        else:
            verdict = "INSUFFICIENT_DATA"
        
        return {
            'truth_score': truth_score,
            'confidence_score': confidence_score,
            'accuracy_score': accuracy_score,
            'verdict': verdict,
            'confidence_factors': confidence_factors
        }
    
    def _extract_key_insights(self, llm_response: str, analysis: ContentAnalysis) -> Dict[str, Any]:
        """Extract key insights from LLM response and analysis"""
        
        # Extract factual summary (simplified - in production, use more sophisticated NLP)
        factual_summary = llm_response[:300] if llm_response else "No summary available"
        
        # Generate evidence summaries
        supporting_summary = self._summarize_evidence(analysis.supporting_articles[:3], "supporting")
        contradicting_summary = self._summarize_evidence(analysis.contradicting_articles[:3], "contradicting")
        
        # Extract key facts (simplified)
        verified_facts = [article['title'] for article in analysis.supporting_articles[:3]]
        disputed_facts = [article['title'] for article in analysis.contradicting_articles[:3]]
        
        # Regional and temporal analysis
        dominant_regions = list(analysis.regional_analysis.get('dominant_regions', {}).keys())[:2]
        regional_analysis = f"Coverage from {analysis.regional_analysis['total_regions']} regions, " \
                          f"dominated by {dominant_regions if dominant_regions else ['No specific regions']}"
        
        temporal_analysis = f"Recency score: {analysis.temporal_analysis['recency_score']:.1%}, " \
                          f"with {analysis.temporal_analysis['temporal_clustering'].get('last_week', 0)} recent articles"
        
        return {
            'factual_summary': factual_summary,
            'supporting_summary': supporting_summary,
            'contradicting_summary': contradicting_summary,
            'verified_facts': verified_facts,
            'disputed_facts': disputed_facts,
            'regional_analysis': regional_analysis,
            'temporal_analysis': temporal_analysis
        }
    
    def _summarize_evidence(self, articles: List[Dict], stance: str) -> str:
        """Summarize evidence articles"""
        if not articles:
            return f"No {stance} evidence found"
        
        sources = [article['source'] for article in articles]
        return f"{len(articles)} {stance} articles from {', '.join(sources[:3])}"
    
    def _format_evidence_list(self, articles: List[Dict]) -> str:
        """Format evidence list for prompts"""
        if not articles:
            return "None"
        
        formatted = []
        for i, article in enumerate(articles[:3], 1):
            formatted.append(f"{i}. {article['title']} ({article['source']})")
        
        return "\n".join(formatted)
    
    def _format_credible_sources(self, sources: List[tuple]) -> str:
        """Format credible sources for prompts"""
        if not sources:
            return "None"
        
        formatted = []
        for source, score in sources:
            formatted.append(f"- {source}: {score:.2f}")
        
        return "\n".join(formatted)

# Convenience function
async def process_with_advanced_llm(content_analysis: ContentAnalysis) -> LLMAnalysisResult:
    """
    Process content analysis with advanced LLM
    
    Args:
        content_analysis: Comprehensive content analysis
        
    Returns:
        LLMAnalysisResult with sophisticated analysis
    """
    processor = AdvancedLLMProcessor()
    return await processor.process_analysis(content_analysis)
