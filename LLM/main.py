"""
Sophisticated LLM-based Fact-Checking System
Advanced multi-component pipeline with paraphrasing, enhanced scraping, and sophisticated analysis
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List
import argparse

from config import config
from fact_check_orchestrator import verify_claim_comprehensive, format_comprehensive_output, FactCheckResult

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SophisticatedFactChecker:
    """Main class for sophisticated LLM-based fact-checking"""

    def __init__(self):
        self.start_time = None

    async def verify_claim(self, claim: str) -> FactCheckResult:
        """
        Complete sophisticated verification pipeline

        Args:
            claim: The claim to verify

        Returns:
            FactCheckResult with comprehensive analysis
        """
        logger.info(f"🚀 Starting sophisticated fact-check for: {claim}")

        # Use the sophisticated orchestrator
        result = await verify_claim_comprehensive(claim)

        logger.info(f"🎯 Sophisticated verification complete")
        logger.info(f"📈 Truth: {result.final_truth_score:.1%}, "
                   f"Confidence: {result.final_confidence_score:.1%}, "
                   f"Verdict: {result.final_verdict}")

        return result
    
    def to_dict(self, result: FactCheckResult) -> Dict[str, Any]:
        """Convert FactCheckResult to dictionary for backward compatibility"""
        return {
            'claim': result.original_claim,
            'timestamp': result.processing_timestamp,
            'truth_score': result.final_truth_score,
            'confidence': result.final_confidence_score,
            'accuracy': result.final_accuracy_score,
            'verdict': result.final_verdict,
            'reasoning': result.factual_summary,
            'supporting_evidence': result.supporting_sources,
            'contradicting_evidence': result.contradicting_sources,
            'articles_analyzed': result.articles_found,
            'articles': result.articles_analyzed,
            'sources_used': result.supporting_sources + result.contradicting_sources,
            'model_used': result.model_used,
            'version': result.version,
            'processing_time': result.total_processing_time,
            'component_timings': result.component_timings,
            'paraphrases_generated': len(result.paraphrase_result.paraphrases),
            'search_queries_used': len(result.paraphrase_result.search_queries),
            'llm_reasoning_chain': result.llm_analysis.reasoning_chain,
            'confidence_factors': result.llm_analysis.confidence_factors,
            'score_breakdown': result.comprehensive_scores.score_explanation
        }

async def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Sophisticated LLM-based Fact-Checking')
    parser.add_argument('claim', help='The claim to verify')
    parser.add_argument('--output', choices=['json', 'text'], default=config.OUTPUT_FORMAT,
                       help='Output format')
    parser.add_argument('--save', help='Save results to file')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed component analysis')

    args = parser.parse_args()

    # Initialize sophisticated fact checker
    fact_checker = SophisticatedFactChecker()

    try:
        # Run sophisticated verification
        result = await fact_checker.verify_claim(args.claim)

        # Output results
        if args.output == 'json':
            if args.detailed:
                # Full detailed JSON output
                output = json.dumps(result.__dict__, indent=2, ensure_ascii=False, default=str)
            else:
                # Simplified JSON output
                simplified_result = fact_checker.to_dict(result)
                output = json.dumps(simplified_result, indent=2, ensure_ascii=False)
        else:
            output = format_comprehensive_output(result)

        print(output)

        # Save to file if requested
        if args.save:
            with open(args.save, 'w', encoding='utf-8') as f:
                if args.output == 'json':
                    if args.detailed:
                        json.dump(result.__dict__, f, indent=2, ensure_ascii=False, default=str)
                    else:
                        json.dump(fact_checker.to_dict(result), f, indent=2, ensure_ascii=False)
                else:
                    f.write(output)
            logger.info(f"💾 Results saved to {args.save}")

    except Exception as e:
        logger.error(f"❌ Sophisticated verification failed: {e}")
        return 1

    return 0

# The format_comprehensive_output function is now imported from fact_check_orchestrator

# Interactive mode
async def interactive_mode():
    """Interactive mode for testing claims"""
    fact_checker = SophisticatedFactChecker()

    print("🔍 VERITAS - Sophisticated Fact-Checking (Interactive Mode)")
    print("Type 'quit' to exit\n")

    while True:
        try:
            claim = input("Enter claim to verify: ").strip()

            if claim.lower() in ['quit', 'exit', 'q']:
                break

            if not claim:
                continue

            print("\n🔄 Processing with sophisticated pipeline...")
            result = await fact_checker.verify_claim(claim)

            print(format_comprehensive_output(result))
            print("\n" + "="*60 + "\n")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # No arguments - run interactive mode
        asyncio.run(interactive_mode())
    else:
        # Command line arguments provided
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
