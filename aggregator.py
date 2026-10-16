class SharkAggregator:
 
    def aggregate(
        self,
        finance_result,
        market_result,
        legal_result
    ):
 
        finance = finance_result["overall_score"]
        market = market_result["overall_score"]
        legal = legal_result["overall_score"]
 
        overall_score = round(
            (finance + market + legal) / 3,
            1
        )
 
        if overall_score >= 8:
            verdict = "Strong Investment"
 
        elif overall_score >= 6.5:
            verdict = "Potential Investment"
 
        elif overall_score >= 5:
            verdict = "Needs Improvement"
 
        else:
            verdict = "Do Not Invest"
 
        return {
            "finance_score": finance,
            "market_score": market,
            "legal_score": legal,
            "overall_score": overall_score,
            "verdict": verdict
        }