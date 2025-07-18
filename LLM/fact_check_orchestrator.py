"""
Sophisticated Fact-Check Orchestrator
Main pipeline coordinator that integrates all modular components
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from config import config
from text_paraphraser import generate_paraphrases, ParaphraseResult
from enhanced_web_scraper import scrape_enhanced_articles, EnhancedArticle
from content_analyzer import analyze_content, ContentAnalysis
from advanced_llm_processor import process_with_advanced_llm, LLMAnalysisResult
from truth_calculator import calculate_sophisticated_scores, ComprehensiveScores

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FactCheckResult:
    """Comprehensive fact-check result"""
    # Input
    original_claim: str
    processing_timestamp: str
    
    # Paraphrasing results
    paraphrase_result: ParaphraseResult
    
    # Web scraping results
    articles_found: int
    articles_analyzed: List[Dict[str, Any]]
    
    # Content analysis
    content_analysis: ContentAnalysis
    
    # LLM analysis
    llm_analysis: LLMAnalysisResult
    
    # Final scores
    comprehensive_scores: ComprehensiveScores
    
    # Summary results
    final_truth_score: float
    final_confidence_score: float
    final_accuracy_score: float
    final_verdict: str
    factual_summary: str
    supporting_sources: List[str]
    contradicting_sources: List[str]
    
    # Performance metrics
    total_processing_time: float
    component_timings: Dict[str, float]
    
    # Metadata
    version: str = "2.0.0"
    model_used: str = ""

class SophisticatedFactCheckOrchestrator:
    """Main orchestrator for the sophisticated fact-checking pipeline"""
    
    def __init__(self):
        self.start_time = None
        self.component_timings = {}
        
    async def verify_claim(self, claim: str) -> FactCheckResult:
        """
        Execute the complete sophisticated fact-checking pipeline
        
        Args:
            claim: The claim to verify
            
        Returns:
            FactCheckResult with comprehensive analysis
        """
        self.start_time = time.time()
        logger.info(f"🚀 Starting sophisticated fact-check pipeline for: {claim[:100]}...")
        
        try:
            # Step 1: Text Paraphrasing
            logger.info("📝 Step 1: Generating paraphrases and search queries...")
            step_start = time.time()
            paraphrase_result = await generate_paraphrases(claim)
            self.component_timings['paraphrasing'] = time.time() - step_start
            
            logger.info(f"✅ Generated {len(paraphrase_result.paraphrases)} paraphrases and "
                       f"{len(paraphrase_result.search_queries)} search queries")
            
            # Step 2: Enhanced Web Scraping
            logger.info("🌐 Step 2: Enhanced multi-source web scraping...")
            step_start = time.time()
            articles = await scrape_enhanced_articles(paraphrase_result.search_queries)
            self.component_timings['web_scraping'] = time.time() - step_start
            
            if not articles:
                logger.warning("⚠️ No articles found - creating minimal result")
                return self._create_no_evidence_result(claim, paraphrase_result)
            
            logger.info(f"✅ Scraped {len(articles)} enhanced articles")
            
            # Step 3: Content Analysis
            logger.info("🔍 Step 3: Sophisticated content analysis...")
            step_start = time.time()
            content_analysis = await analyze_content(claim, articles)
            self.component_timings['content_analysis'] = time.time() - step_start
            
            logger.info(f"✅ Analyzed content: {len(content_analysis.supporting_articles)} supporting, "
                       f"{len(content_analysis.contradicting_articles)} contradicting")
            
            # Step 4: Advanced LLM Processing
            logger.info("🧠 Step 4: Advanced LLM analysis...")
            step_start = time.time()
            llm_analysis = await process_with_advanced_llm(content_analysis)
            self.component_timings['llm_processing'] = time.time() - step_start
            
            logger.info(f"✅ LLM analysis complete: {llm_analysis.final_verdict}")
            
            # Step 5: Sophisticated Truth Calculation with Weighted Scoring
            logger.info("🧮 Step 5: Calculating sophisticated scores with weighted system...")
            step_start = time.time()
            comprehensive_scores = calculate_sophisticated_scores(content_analysis, llm_analysis, claim)
            self.component_timings['score_calculation'] = time.time() - step_start
            
            # Step 6: Compile Final Results
            logger.info("📊 Step 6: Compiling comprehensive results...")
            result = self._compile_comprehensive_result(
                claim, paraphrase_result, articles, content_analysis, 
                llm_analysis, comprehensive_scores
            )
            
            total_time = time.time() - self.start_time
            result.total_processing_time = total_time
            result.component_timings = self.component_timings
            
            logger.info(f"🎯 Sophisticated fact-check complete in {total_time:.2f}s")
            logger.info(f"📈 Final Results - Truth: {result.final_truth_score:.1%}, "
                       f"Confidence: {result.final_confidence_score:.1%}, "
                       f"Verdict: {result.final_verdict}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Fact-check pipeline failed: {e}")
            return self._create_error_result(claim, str(e))
    
    def _compile_comprehensive_result(self, claim: str, paraphrase_result: ParaphraseResult,
                                    articles: List[EnhancedArticle], content_analysis: ContentAnalysis,
                                    llm_analysis: LLMAnalysisResult, 
                                    comprehensive_scores: ComprehensiveScores) -> FactCheckResult:
        """Compile all results into comprehensive fact-check result"""
        
        # Convert articles to dictionaries
        articles_analyzed = []
        for article in articles:
            articles_analyzed.append({
                'title': article.title,
                'source': article.source,
                'url': article.url,
                'credibility_score': article.credibility_score,
                'published_date': article.published_date.isoformat() if article.published_date else None,
                'content_snippet': article.content[:200]
            })
        
        # Extract supporting and contradicting sources
        supporting_sources = list(set([
            article['source'] for article in content_analysis.supporting_articles
        ]))
        
        contradicting_sources = list(set([
            article['source'] for article in content_analysis.contradicting_articles
        ]))
        
        return FactCheckResult(
            original_claim=claim,
            processing_timestamp=datetime.now().isoformat(),
            paraphrase_result=paraphrase_result,
            articles_found=len(articles),
            articles_analyzed=articles_analyzed,
            content_analysis=content_analysis,
            llm_analysis=llm_analysis,
            comprehensive_scores=comprehensive_scores,
            final_truth_score=comprehensive_scores.truth_score_breakdown.final_truth_score,
            final_confidence_score=comprehensive_scores.confidence_score_breakdown.final_confidence_score,
            final_accuracy_score=comprehensive_scores.accuracy_score,
            final_verdict=comprehensive_scores.final_verdict,
            factual_summary=llm_analysis.factual_summary,
            supporting_sources=supporting_sources,
            contradicting_sources=contradicting_sources,
            total_processing_time=0.0,  # Will be set later
            component_timings={},  # Will be set later
            model_used=config.LLAMA_MODEL_PATH
        )
    
    def _create_no_evidence_result(self, claim: str, paraphrase_result: ParaphraseResult) -> FactCheckResult:
        """Create result when no evidence is found"""
        
        # Create minimal analysis objects
        from content_analyzer import ContentAnalysis
        from advanced_llm_processor import LLMAnalysisResult
        from truth_calculator import ComprehensiveScores, TruthScoreBreakdown, ConfidenceScoreBreakdown
        
        minimal_content_analysis = ContentAnalysis(
            original_claim=claim,
            total_articles=0,
            supporting_articles=[],
            contradicting_articles=[],
            neutral_articles=[],
            regional_analysis={'total_regions': 0, 'regional_diversity_score': 0.0, 'dominant_regions': {}},
            temporal_analysis={'recency_score': 0.0, 'temporal_clustering': {}, 'articles_with_dates': 0},
            source_credibility_analysis={'overall_credibility_score': 0.0, 'credibility_distribution': {'high': 0, 'medium': 0, 'low': 0}, 'most_credible_sources': []},
            content_similarity_scores=[],
            key_entities=[],
            sentiment_analysis={'average_sentiment': 0.0, 'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0}},
            structured_json_for_llm={},
            processing_time=0.0
        )
        
        minimal_llm_analysis = LLMAnalysisResult(
            truth_score=0.0,
            confidence_score=0.1,
            accuracy_score=0.1,
            factual_summary="No credible sources found to verify this claim",
            supporting_evidence_summary="No supporting evidence found",
            contradicting_evidence_summary="No contradicting evidence found",
            key_facts_verified=[],
            key_facts_disputed=[],
            regional_context_analysis="No regional context available",
            temporal_context_analysis="No temporal context available",
            source_reliability_assessment="No sources available for assessment",
            final_verdict="INSUFFICIENT_DATA",
            reasoning_chain=["No evidence found"],
            confidence_factors={},
            processing_time=0.0
        )
        
        truth_breakdown = TruthScoreBreakdown(
            base_truth_score=0.0,
            credibility_adjustment=0.0,
            temporal_adjustment=0.0,
            regional_adjustment=0.0,
            consistency_adjustment=0.0,
            variation_penalty=0.0,
            final_truth_score=0.0,
            calculation_details={}
        )
        
        confidence_breakdown = ConfidenceScoreBreakdown(
            source_quantity_factor=0.0,
            source_credibility_factor=0.0,
            evidence_consistency_factor=0.0,
            temporal_relevance_factor=0.0,
            regional_diversity_factor=0.0,
            final_confidence_score=0.1,
            confidence_level="LOW"
        )
        
        minimal_scores = ComprehensiveScores(
            truth_score_breakdown=truth_breakdown,
            confidence_score_breakdown=confidence_breakdown,
            accuracy_score=0.1,
            final_verdict="INSUFFICIENT_DATA",
            score_explanation="No evidence found",
            reliability_indicators={}
        )
        
        return FactCheckResult(
            original_claim=claim,
            processing_timestamp=datetime.now().isoformat(),
            paraphrase_result=paraphrase_result,
            articles_found=0,
            articles_analyzed=[],
            content_analysis=minimal_content_analysis,
            llm_analysis=minimal_llm_analysis,
            comprehensive_scores=minimal_scores,
            final_truth_score=0.0,
            final_confidence_score=0.1,
            final_accuracy_score=0.1,
            final_verdict="INSUFFICIENT_DATA",
            factual_summary="No credible sources found to verify this claim",
            supporting_sources=[],
            contradicting_sources=[],
            total_processing_time=time.time() - self.start_time if self.start_time else 0,
            component_timings=self.component_timings,
            model_used=config.LLAMA_MODEL_PATH
        )
    
    def _create_error_result(self, claim: str, error_message: str) -> FactCheckResult:
        """Create result when an error occurs"""
        # Similar to no evidence result but with error information
        return self._create_no_evidence_result(claim, ParaphraseResult(
            original_text=claim,
            paraphrases=[],
            keywords=[],
            entities=[],
            search_queries=[claim],
            processing_time=0.0
        ))

def format_comprehensive_output(result: FactCheckResult) -> str:
    """Format comprehensive result as human-readable text"""
    
    verdict_emoji = {
        'TRUE': '✅',
        'FALSE': '❌',
        'MIXED': '⚠️',
        'INSUFFICIENT_DATA': '❓'
    }
    
    output = f"""
🔍 VERITAS - SOPHISTICATED FACT-CHECK ANALYSIS
{'='*60}

📝 CLAIM: {result.original_claim}

📊 FINAL RESULTS:
   Truth Score:    {result.final_truth_score:.1%}
   Confidence:     {result.final_confidence_score:.1%}
   Accuracy:       {result.final_accuracy_score:.1%}
   Verdict:        {verdict_emoji.get(result.final_verdict, '❓')} {result.final_verdict}

🧠 FACTUAL SUMMARY:
{result.factual_summary}

📈 EVIDENCE ANALYSIS:
   Articles Analyzed: {result.articles_found}
   Supporting Sources: {len(result.supporting_sources)}
   Contradicting Sources: {len(result.contradicting_sources)}

🔗 SUPPORTING SOURCES:
{chr(10).join([f"   • {source}" for source in result.supporting_sources[:5]])}

❌ CONTRADICTING SOURCES:
{chr(10).join([f"   • {source}" for source in result.contradicting_sources[:5]])}

📊 SCORE BREAKDOWN:
{result.comprehensive_scores.score_explanation}

⏱️ PERFORMANCE:
   Total Processing Time: {result.total_processing_time:.2f}s
   Paraphrasing: {result.component_timings.get('paraphrasing', 0):.2f}s
   Web Scraping: {result.component_timings.get('web_scraping', 0):.2f}s
   Content Analysis: {result.component_timings.get('content_analysis', 0):.2f}s
   LLM Processing: {result.component_timings.get('llm_processing', 0):.2f}s

🤖 Model: {result.model_used}
⏰ Timestamp: {result.processing_timestamp}
"""
    
    return output

# Convenience function
async def verify_claim_comprehensive(claim: str) -> FactCheckResult:
    """
    Verify claim using the sophisticated fact-checking pipeline
    
    Args:
        claim: The claim to verify
        
    Returns:
        FactCheckResult with comprehensive analysis
    """
    orchestrator = SophisticatedFactCheckOrchestrator()
    return await orchestrator.verify_claim(claim)
