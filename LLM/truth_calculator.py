"""
Sophisticated Truth Score Calculator
Advanced algorithms for calculating truth scores, confidence, and accuracy
"""

import numpy as np
import logging
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math

from .config import config
from .content_analyzer import ContentAnalysis
from .advanced_llm_processor import LLMAnalysisResult
from .weighted_scoring import weighted_scorer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TruthScoreBreakdown:
    """Detailed breakdown of truth score calculation"""
    base_truth_score: float
    credibility_adjustment: float
    temporal_adjustment: float
    regional_adjustment: float
    consistency_adjustment: float
    variation_penalty: float
    final_truth_score: float
    calculation_details: Dict[str, Any]

@dataclass
class ConfidenceScoreBreakdown:
    """Detailed breakdown of confidence score calculation"""
    source_quantity_factor: float
    source_credibility_factor: float
    evidence_consistency_factor: float
    temporal_relevance_factor: float
    regional_diversity_factor: float
    final_confidence_score: float
    confidence_level: str  # "HIGH", "MEDIUM", "LOW"

@dataclass
class ComprehensiveScores:
    """Comprehensive scoring result"""
    truth_score_breakdown: TruthScoreBreakdown
    confidence_score_breakdown: ConfidenceScoreBreakdown
    accuracy_score: float
    final_verdict: str
    score_explanation: str
    reliability_indicators: Dict[str, float]

class SophisticatedTruthCalculator:
    """Advanced truth score calculator with sophisticated algorithms"""
    
    def __init__(self):
        self.min_sources_for_high_confidence = config.MIN_SOURCES_FOR_HIGH_CONFIDENCE
        self.source_agreement_threshold = config.SOURCE_AGREEMENT_THRESHOLD
        self.variation_penalty_factor = config.VARIATION_PENALTY_FACTOR
        
    def calculate_comprehensive_scores(self, content_analysis: ContentAnalysis,
                                     llm_analysis: LLMAnalysisResult, claim: str = "") -> ComprehensiveScores:
        """
        Calculate comprehensive truth, confidence, and accuracy scores using weighted system

        Args:
            content_analysis: Content analysis results
            llm_analysis: LLM analysis results
            claim: Original claim text for category/region detection

        Returns:
            ComprehensiveScores with detailed breakdowns
        """
        logger.info("🧮 Calculating sophisticated truth scores with weighted system...")

        # Use new weighted scoring system
        weighted_results = weighted_scorer.calculate_comprehensive_scores(
            claim=claim,
            supporting_articles=content_analysis.supporting_articles,
            contradicting_articles=content_analysis.contradicting_articles
        )

        # Convert weighted results to legacy format for compatibility
        truth_breakdown = TruthScoreBreakdown(
            base_truth_score=weighted_results["truth_score"],
            credibility_adjustment=0.0,  # Now included in weighted calculation
            temporal_adjustment=0.0,     # Now included in weighted calculation
            regional_adjustment=0.0,     # Now included in weighted calculation
            consistency_adjustment=0.0,  # Now included in weighted calculation
            variation_penalty=0.0,       # Now included in weighted calculation
            final_truth_score=weighted_results["truth_score"],
            calculation_details=weighted_results["truth_details"]
        )

        confidence_breakdown = ConfidenceScoreBreakdown(
            source_quantity_factor=weighted_results["confidence_details"]["quantity"],
            source_credibility_factor=0.0,  # Now included in composite calculation
            evidence_consistency_factor=0.0, # Now included in composite calculation
            temporal_relevance_factor=weighted_results["confidence_details"]["recency"],
            regional_diversity_factor=weighted_results["confidence_details"]["diversity"],
            final_confidence_score=weighted_results["confidence_score"],
            confidence_level=self._get_confidence_level(weighted_results["confidence_score"])
        )

        # Calculate accuracy score (combination of truth and confidence)
        accuracy_score = (weighted_results["truth_score"] + weighted_results["confidence_score"]) / 2

        # Use weighted verdict
        final_verdict = weighted_results["verdict"]

        # Generate explanation
        score_explanation = self._generate_weighted_explanation(weighted_results)

        # Calculate reliability indicators
        reliability_indicators = self._calculate_weighted_reliability_indicators(weighted_results)

        result = ComprehensiveScores(
            truth_score_breakdown=truth_breakdown,
            confidence_score_breakdown=confidence_breakdown,
            accuracy_score=accuracy_score,
            final_verdict=final_verdict,
            score_explanation=score_explanation,
            reliability_indicators=reliability_indicators
        )

        logger.info(f"✅ Weighted Truth: {weighted_results['truth_score']:.1%}, "
                   f"Confidence: {weighted_results['confidence_score']:.1%}, "
                   f"Verdict: {final_verdict}")

        return result

    def _get_confidence_level(self, confidence_score: float) -> str:
        """Convert confidence score to level"""
        if confidence_score >= 0.8:
            return "HIGH"
        elif confidence_score >= 0.5:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_weighted_explanation(self, weighted_results: Dict) -> str:
        """Generate explanation for weighted scoring results"""
        truth_score = weighted_results["truth_score"] * 100
        confidence_score = weighted_results["confidence_score"] * 100
        verdict = weighted_results["verdict"]

        explanation = f"Weighted Analysis Results:\n"
        explanation += f"• Truth Score: {truth_score:.1f}% (based on source credibility and agreement)\n"
        explanation += f"• Confidence Score: {confidence_score:.1f}% (based on quantity, diversity, recency)\n"
        explanation += f"• Supporting Articles: {weighted_results['supporting_count']}\n"
        explanation += f"• Contradicting Articles: {weighted_results['contradicting_count']}\n"
        explanation += f"• Final Verdict: {verdict}\n"

        # Add source breakdown if available
        if "truth_details" in weighted_results:
            details = weighted_results["truth_details"]
            explanation += f"• Claim Category: {details.get('claim_category', 'Unknown')}\n"
            explanation += f"• Claim Region: {details.get('claim_region', 'Unknown')}\n"

        return explanation

    def _calculate_weighted_reliability_indicators(self, weighted_results: Dict) -> Dict[str, float]:
        """Calculate reliability indicators from weighted results"""
        confidence_details = weighted_results.get("confidence_details", {})

        return {
            "source_diversity": confidence_details.get("diversity", 0.0),
            "temporal_relevance": confidence_details.get("recency", 0.0),
            "article_quantity": confidence_details.get("quantity", 0.0),
            "overall_reliability": weighted_results["confidence_score"]
        }

    def _calculate_truth_score_breakdown(self, content_analysis: ContentAnalysis,
                                       llm_analysis: LLMAnalysisResult) -> TruthScoreBreakdown:
        """Calculate truth score with detailed breakdown"""
        
        supporting_count = len(content_analysis.supporting_articles)
        contradicting_count = len(content_analysis.contradicting_articles)
        total_articles = supporting_count + contradicting_count
        
        # Base truth score calculation
        if total_articles == 0:
            base_truth_score = config.NO_SOURCES_SCORE
        else:
            base_truth_score = supporting_count / total_articles
        
        # Credibility adjustment
        credibility_score = content_analysis.source_credibility_analysis['overall_credibility_score']
        credibility_adjustment = (credibility_score - 0.5) * 0.3  # ±0.15 max adjustment
        
        # Temporal adjustment (recent articles get bonus)
        temporal_score = content_analysis.temporal_analysis['recency_score']
        temporal_adjustment = (temporal_score - 0.5) * 0.2  # ±0.1 max adjustment
        
        # Regional adjustment (diverse sources get bonus)
        regional_diversity = content_analysis.regional_analysis['regional_diversity_score']
        regional_adjustment = min(regional_diversity * 0.1, 0.1)  # Max 0.1 bonus
        
        # Consistency adjustment (consistent evidence gets bonus)
        if total_articles > 0:
            consistency_ratio = abs(supporting_count - contradicting_count) / total_articles
            consistency_adjustment = consistency_ratio * 0.15  # Max 0.15 bonus
        else:
            consistency_adjustment = 0.0
        
        # Variation penalty (conflicting evidence gets penalty)
        if total_articles > 0:
            variation_ratio = min(supporting_count, contradicting_count) / total_articles
            variation_penalty = variation_ratio * self.variation_penalty_factor
        else:
            variation_penalty = 0.0
        
        # Calculate final truth score
        final_truth_score = base_truth_score + credibility_adjustment + temporal_adjustment + \
                           regional_adjustment + consistency_adjustment - variation_penalty
        
        # Apply bounds and special cases
        final_truth_score = max(0.0, min(1.0, final_truth_score))
        
        # Special case: Perfect agreement with high credibility sources
        if (supporting_count >= self.min_sources_for_high_confidence and 
            contradicting_count == 0 and 
            credibility_score >= 0.8):
            final_truth_score = min(config.PERFECT_MATCH_SCORE, final_truth_score + 0.1)
        
        # Special case: No credible sources
        if total_articles == 0 or credibility_score < 0.3:
            final_truth_score = config.NO_SOURCES_SCORE
        
        calculation_details = {
            'supporting_articles': supporting_count,
            'contradicting_articles': contradicting_count,
            'total_articles': total_articles,
            'base_ratio': supporting_count / max(total_articles, 1),
            'credibility_score': credibility_score,
            'temporal_score': temporal_score,
            'regional_diversity': regional_diversity,
            'consistency_ratio': consistency_ratio if total_articles > 0 else 0,
            'variation_ratio': variation_ratio if total_articles > 0 else 0
        }
        
        return TruthScoreBreakdown(
            base_truth_score=base_truth_score,
            credibility_adjustment=credibility_adjustment,
            temporal_adjustment=temporal_adjustment,
            regional_adjustment=regional_adjustment,
            consistency_adjustment=consistency_adjustment,
            variation_penalty=variation_penalty,
            final_truth_score=final_truth_score,
            calculation_details=calculation_details
        )
    
    def _calculate_confidence_score_breakdown(self, content_analysis: ContentAnalysis, 
                                            llm_analysis: LLMAnalysisResult) -> ConfidenceScoreBreakdown:
        """Calculate confidence score with detailed breakdown"""
        
        total_articles = len(content_analysis.supporting_articles) + len(content_analysis.contradicting_articles)
        
        # Source quantity factor (more sources = higher confidence)
        source_quantity_factor = min(total_articles / 10, 1.0)  # Normalize to 10 sources
        
        # Source credibility factor
        source_credibility_factor = content_analysis.source_credibility_analysis['overall_credibility_score']
        
        # Evidence consistency factor
        if total_articles > 0:
            supporting_count = len(content_analysis.supporting_articles)
            contradicting_count = len(content_analysis.contradicting_articles)
            agreement_ratio = abs(supporting_count - contradicting_count) / total_articles
            evidence_consistency_factor = agreement_ratio
        else:
            evidence_consistency_factor = 0.0
        
        # Temporal relevance factor
        temporal_relevance_factor = content_analysis.temporal_analysis['recency_score']
        
        # Regional diversity factor
        regional_diversity_factor = min(content_analysis.regional_analysis['regional_diversity_score'], 1.0)
        
        # Calculate weighted confidence score
        weights = {
            'source_quantity': 0.25,
            'source_credibility': 0.30,
            'evidence_consistency': 0.25,
            'temporal_relevance': 0.10,
            'regional_diversity': 0.10
        }
        
        final_confidence_score = (
            source_quantity_factor * weights['source_quantity'] +
            source_credibility_factor * weights['source_credibility'] +
            evidence_consistency_factor * weights['evidence_consistency'] +
            temporal_relevance_factor * weights['temporal_relevance'] +
            regional_diversity_factor * weights['regional_diversity']
        )
        
        # Determine confidence level
        if final_confidence_score >= 0.8:
            confidence_level = "HIGH"
        elif final_confidence_score >= 0.6:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        
        return ConfidenceScoreBreakdown(
            source_quantity_factor=source_quantity_factor,
            source_credibility_factor=source_credibility_factor,
            evidence_consistency_factor=evidence_consistency_factor,
            temporal_relevance_factor=temporal_relevance_factor,
            regional_diversity_factor=regional_diversity_factor,
            final_confidence_score=final_confidence_score,
            confidence_level=confidence_level
        )
    
    def _calculate_accuracy_score(self, content_analysis: ContentAnalysis, 
                                llm_analysis: LLMAnalysisResult) -> float:
        """Calculate accuracy score based on source quality and analysis depth"""
        
        # Source quality component
        source_quality = content_analysis.source_credibility_analysis['overall_credibility_score']
        
        # Analysis depth component (based on number of articles and diversity)
        total_articles = len(content_analysis.supporting_articles) + len(content_analysis.contradicting_articles)
        depth_score = min(total_articles / 15, 1.0)  # Normalize to 15 articles
        
        # Regional diversity component
        regional_diversity = content_analysis.regional_analysis['regional_diversity_score']
        
        # Temporal coverage component
        temporal_coverage = content_analysis.temporal_analysis['recency_score']
        
        # LLM analysis quality (based on processing success)
        llm_quality = 1.0 if llm_analysis.processing_time < 60 else 0.8  # Penalize slow processing
        
        # Weighted accuracy calculation
        accuracy_score = (
            source_quality * 0.35 +
            depth_score * 0.25 +
            regional_diversity * 0.15 +
            temporal_coverage * 0.15 +
            llm_quality * 0.10
        )
        
        return min(1.0, accuracy_score)
    
    def _determine_final_verdict(self, truth_breakdown: TruthScoreBreakdown, 
                               confidence_breakdown: ConfidenceScoreBreakdown) -> str:
        """Determine final verdict based on truth and confidence scores"""
        
        truth_score = truth_breakdown.final_truth_score
        confidence_score = confidence_breakdown.final_confidence_score
        total_articles = truth_breakdown.calculation_details['total_articles']
        
        # High confidence verdicts
        if confidence_score >= 0.7:
            if truth_score >= 0.8:
                return "TRUE"
            elif truth_score <= 0.2:
                return "FALSE"
            elif 0.4 <= truth_score <= 0.6:
                return "MIXED"
        
        # Medium confidence verdicts
        elif confidence_score >= 0.5:
            if truth_score >= 0.85:
                return "TRUE"
            elif truth_score <= 0.15:
                return "FALSE"
            else:
                return "MIXED"
        
        # Low confidence or insufficient data
        if total_articles < 3:
            return "INSUFFICIENT_DATA"
        else:
            return "MIXED"
    
    def _generate_score_explanation(self, truth_breakdown: TruthScoreBreakdown, 
                                  confidence_breakdown: ConfidenceScoreBreakdown) -> str:
        """Generate human-readable explanation of scores"""
        
        details = truth_breakdown.calculation_details
        
        explanation_parts = []
        
        # Truth score explanation
        explanation_parts.append(f"Truth Score ({truth_breakdown.final_truth_score:.1%}):")
        explanation_parts.append(f"  • Base evidence ratio: {details['supporting_articles']}/{details['total_articles']} supporting")
        
        if truth_breakdown.credibility_adjustment != 0:
            direction = "increased" if truth_breakdown.credibility_adjustment > 0 else "decreased"
            explanation_parts.append(f"  • Source credibility {direction} score by {abs(truth_breakdown.credibility_adjustment):.1%}")
        
        if truth_breakdown.variation_penalty > 0:
            explanation_parts.append(f"  • Conflicting evidence penalty: -{truth_breakdown.variation_penalty:.1%}")
        
        # Confidence score explanation
        explanation_parts.append(f"\nConfidence Score ({confidence_breakdown.final_confidence_score:.1%}):")
        explanation_parts.append(f"  • Source quantity: {confidence_breakdown.source_quantity_factor:.1%}")
        explanation_parts.append(f"  • Source credibility: {confidence_breakdown.source_credibility_factor:.1%}")
        explanation_parts.append(f"  • Evidence consistency: {confidence_breakdown.evidence_consistency_factor:.1%}")
        
        return "\n".join(explanation_parts)
    
    def _calculate_reliability_indicators(self, content_analysis: ContentAnalysis, 
                                        llm_analysis: LLMAnalysisResult) -> Dict[str, float]:
        """Calculate various reliability indicators"""
        
        total_articles = len(content_analysis.supporting_articles) + len(content_analysis.contradicting_articles)
        
        indicators = {
            'source_diversity': content_analysis.regional_analysis['regional_diversity_score'],
            'temporal_relevance': content_analysis.temporal_analysis['recency_score'],
            'source_credibility': content_analysis.source_credibility_analysis['overall_credibility_score'],
            'evidence_volume': min(total_articles / 20, 1.0),  # Normalize to 20 articles
            'analysis_depth': 1.0 if llm_analysis.processing_time > 5 else 0.7,  # Deeper analysis takes time
            'consistency_score': abs(len(content_analysis.supporting_articles) - len(content_analysis.contradicting_articles)) / max(total_articles, 1)
        }
        
        # Overall reliability score
        indicators['overall_reliability'] = sum(indicators.values()) / len(indicators)
        
        return indicators

# Convenience function
def calculate_sophisticated_scores(content_analysis: ContentAnalysis,
                                 llm_analysis: LLMAnalysisResult,
                                 claim: str = "") -> ComprehensiveScores:
    """
    Calculate sophisticated truth scores with weighted system

    Args:
        content_analysis: Content analysis results
        llm_analysis: LLM analysis results
        claim: Original claim text for weighted scoring

    Returns:
        ComprehensiveScores with detailed breakdowns
    """
    calculator = SophisticatedTruthCalculator()
    return calculator.calculate_comprehensive_scores(content_analysis, llm_analysis, claim)
