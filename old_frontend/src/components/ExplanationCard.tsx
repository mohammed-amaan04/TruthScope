import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle, AlertTriangle, XCircle, Info } from 'lucide-react';

// Types for verification results
interface SourceInfo {
  source: string;
  url?: string;
  credibility_score?: number;
}

interface VerificationResult {
  truth_score: number;
  confidence_score: number;
  verdict: string;
  summary: string;
  supporting_sources: SourceInfo[];
  contradicting_sources: SourceInfo[];
  processing_time: number;
}

interface ExplanationCardProps {
  verificationResult?: VerificationResult;
}

const ExplanationCard: React.FC<ExplanationCardProps> = ({ verificationResult }) => {
  // If verification result is provided, show AI-generated analysis
  if (verificationResult) {
    const getVerdictColor = (verdict: string) => {
      switch (verdict) {
        case 'TRUE': return 'green';
        case 'FALSE': return 'red';
        case 'MIXED': return 'yellow';
        default: return 'gray';
      }
    };

    const verdictColor = getVerdictColor(verificationResult.verdict);

    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="h-5 w-5 text-blue-600" />
            AI Verification Analysis
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* AI Summary */}
          <div className={`flex items-start gap-3 p-3 rounded-lg bg-${verdictColor}-50 border border-${verdictColor}-200`}>
            <CheckCircle className={`h-5 w-5 text-${verdictColor}-600 mt-0.5 flex-shrink-0`} />
            <div>
              <h4 className={`font-semibold text-${verdictColor}-800`}>AI Analysis Summary</h4>
              <p className={`text-sm text-${verdictColor}-700`}>
                {verificationResult.summary}
              </p>
            </div>
          </div>

          {/* Supporting Sources */}
          {verificationResult.supporting_sources.length > 0 && (
            <div className="pt-4 border-t">
              <h4 className="font-semibold mb-2 text-green-800">Supporting Sources:</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                {verificationResult.supporting_sources.slice(0, 10).map((source, index) => (
                  <li key={index} className="flex items-center gap-2">
                    <CheckCircle className="h-3 w-3 text-green-600 flex-shrink-0" />
                    {source.source}
                    {source.credibility_score && (
                      <span className="text-xs text-green-600">
                        ({(source.credibility_score * 100).toFixed(0)}% credible)
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Contradicting Sources */}
          {verificationResult.contradicting_sources.length > 0 && (
            <div className="pt-4 border-t">
              <h4 className="font-semibold mb-2 text-red-800">Contradicting Sources:</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                {verificationResult.contradicting_sources.slice(0, 10).map((source, index) => (
                  <li key={index} className="flex items-center gap-2">
                    <XCircle className="h-3 w-3 text-red-600 flex-shrink-0" />
                    {source.source}
                    {source.credibility_score && (
                      <span className="text-xs text-red-600">
                        ({(source.credibility_score * 100).toFixed(0)}% credible)
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="pt-4 border-t">
            <p className="text-xs text-muted-foreground">
              Verified: {new Date().toLocaleDateString()} |
              Processing Time: {verificationResult.processing_time.toFixed(2)}s |
              Confidence: {(verificationResult.confidence_score * 100).toFixed(0)}%
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Default static content when no verification result
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Info className="h-5 w-5 text-blue-600" />
          Verification Analysis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <div className="flex items-start gap-3 p-3 rounded-lg bg-green-50 border border-green-200">
            <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="font-semibold text-green-800">Verified Claims</h4>
              <p className="text-sm text-green-700">
                The main statistical data mentioned in this article has been cross-referenced with official government sources and appears to be accurate.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 rounded-lg bg-yellow-50 border border-yellow-200">
            <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="font-semibold text-yellow-800">Needs Context</h4>
              <p className="text-sm text-yellow-700">
                Some quotes lack proper attribution and context. The timeline of events could be clearer to avoid potential misinterpretation.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-3 rounded-lg bg-red-50 border border-red-200">
            <XCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="font-semibold text-red-800">Potential Issues</h4>
              <p className="text-sm text-red-700">
                One claim about economic impact appears to be based on preliminary data that has since been revised. This should be updated.
              </p>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t">
          <h4 className="font-semibold mb-2">Sources Checked:</h4>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>• Government Statistical Office</li>
            <li>• Reuters News Agency</li>
            <li>• Academic Research Database</li>
            <li>• Expert Interview Transcripts</li>
          </ul>
        </div>

        <div className="pt-4 border-t">
          <p className="text-xs text-muted-foreground">
            Last verified: {new Date().toLocaleDateString()} | Confidence Level: High
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default ExplanationCard;
