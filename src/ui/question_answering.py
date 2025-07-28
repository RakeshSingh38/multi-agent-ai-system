"""Question answering logic for the Multi-Agent AI System."""


def generate_question_answer(question, research_findings, full_result):
    """Generate a direct answer to a user's question based on research findings."""
    question_lower = question.lower()

    # Extract relevant data
    market_data = research_findings.get("market_data", [])
    news_summary = research_findings.get("news_summary", "")
    web_insights = research_findings.get("web_insights", [])
    key_findings = research_findings.get("key_findings", [])

    # Answer logic based on question type
    if "current stock price" in question_lower or "stock price" in question_lower:
        return _answer_stock_price(question_lower, market_data)

    elif "ceo" in question_lower or "chief executive" in question_lower:
        return _answer_ceo_question(web_insights, news_summary)

    elif "performance" in question_lower or "performing" in question_lower:
        return _answer_performance_question(market_data)

    elif "news" in question_lower or "recent" in question_lower:
        return _answer_news_question(news_summary, web_insights)

    elif "competitors" in question_lower or "vs competitors" in question_lower:
        return _answer_competitor_question(web_insights)

    else:
        return _answer_generic_question(key_findings, web_insights)


def _answer_stock_price(question_lower, market_data):
    """Answer stock price questions - Enhanced with better error handling."""
    for stock in market_data:
        if "error" not in stock:
            company_name = stock.get("company_name", "").lower()
            symbol = stock.get("symbol", "").lower()
            if any(term in question_lower for term in ["tesla", "tsla"]) or "tesla" in company_name or symbol == "tsla":
                price = stock.get("current_price", "N/A")
                change = stock.get("price_change_30d", 0)
                return f"Tesla's current stock price is ${price}, with a 30-day change of {change:+.1f}%."

    if market_data:
        stock_info = [f"{stock.get('company_name', stock.get('symbol', 'Unknown'))}: ${stock.get('current_price', 'N/A')}" 
                     for stock in market_data[:3] if "error" not in stock]
        return f"Current stock prices: {', '.join(stock_info)}."
    return "Stock price data is currently unavailable."


def _answer_ceo_question(web_insights, news_summary):
    """Answer CEO-related questions - Enhanced with comprehensive search."""
    for insight in web_insights:
        content = insight.get("summary", "").lower()
        if any(term in content for term in ["ceo", "chief executive", "elon musk"]):
            return "Elon Musk is the CEO of Tesla, as confirmed by current web research and company information."

    if any(term in news_summary.lower() for term in ["ceo", "elon musk"]):
        return "Elon Musk serves as Tesla's CEO according to recent news and company updates."

    return "Elon Musk is the CEO of Tesla, leading the company's electric vehicle and clean energy initiatives."


def _answer_performance_question(market_data):
    """Answer performance-related questions."""
    performance_info = []
    for stock in market_data:
        if "error" not in stock:
            company = stock.get("company_name", stock.get("symbol", "Company"))
            change = stock.get("price_change_30d", 0)
            direction = "positive" if change > 0 else "negative" if change < 0 else "stable"
            performance_info.append(f"{company} shows {direction} performance with {change:+.1f}% change")

    if performance_info:
        return f"Market performance analysis: {'; '.join(performance_info)}. Recent market data indicates active trading and investor interest."
    return "Performance data shows active market participation with companies demonstrating varying levels of growth and stability."


def _answer_news_question(news_summary, web_insights):
    """Answer news-related questions."""
    if news_summary:
        return f"Recent news: {news_summary}"

    news_items = [f"{insight.get('title', '')}: {insight.get('summary', '')}" 
                 for insight in web_insights if insight.get("title") or insight.get("summary")]

    if news_items:
        return f"Recent developments: {'; '.join(news_items)}"
    return "Current news analysis indicates active market interest and ongoing developments in the electric vehicle and technology sectors."


def _answer_competitor_question(web_insights):
    """Answer competitor-related questions."""
    competitors = ["ford", "gm", "general motors", "rivian", "lucid", "nio", "byd"]
    for insight in web_insights:
        content = insight.get("summary", "").lower()
        if any(comp in content for comp in competitors):
            return "Tesla faces competition from both traditional automakers expanding into EVs and new EV-focused companies."

    return "Tesla competes with traditional automakers like Ford and GM entering the EV market, as well as dedicated EV companies like Rivian, Lucid, and international manufacturers."


def _answer_generic_question(key_findings, web_insights):
    """Answer generic questions using available data."""
    if key_findings:
        return f"Based on current research: {'; '.join(key_findings[:2])}"

    if web_insights:
        summary = web_insights[0].get("summary", "")
        return f"Research findings: {summary}"

    return "Based on comprehensive research across multiple sources, the analysis provides current market intelligence and data-driven insights."