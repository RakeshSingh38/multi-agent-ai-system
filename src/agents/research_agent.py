from src.agents.base_agent import BaseAgent
from typing import Dict, Any, List
from src.core.config import settings
from src.core.logger import logger
from src.core.real_data_collector import RealDataCollector
import json
import asyncio

class ResearchAgent(BaseAgent):
    """Agent responsible for researching topics and gathering information."""
    
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Specializes in researching topics and gathering REAL information from web sources, news, and market data.",
            # llm_model removed, always use Ollama
        )
        self.data_collector = RealDataCollector()
        
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research a topic and return findings."""
        topic = input_data.get("topic", "")
        specific_questions = input_data.get("questions", [])
        
        self.log_action(
            action="Starting research",
            reasoning=f"Researching topic: {topic}",
            metadata={"topic": topic, "questions": specific_questions}
        )
        
        try:
            # 🔥 NEW: Collect REAL data from the internet
            logger.info(f"Collecting REAL data for: {topic}")
            real_data = await self.data_collector.comprehensive_research(topic, specific_questions)
            
            # Process and structure the real findings
            research_findings = self._process_real_data(real_data)
            
            # Log successful completion
            self.log_action(
                action="Research completed with REAL data",
                reasoning=f"Successfully gathered REAL information from {len(real_data.get('sources_used', []))} sources on {topic}",
                metadata={
                    "sources_used": real_data.get('sources_used', []),
                    "total_sources": real_data.get('total_sources', 0),
                    "findings_count": len(research_findings.get("key_findings", []))
                }
            )
            
            # Add to memory
            self.add_to_memory({
                "topic": topic,
                "findings": research_findings
            })
            
            return {
                "status": "success",
                "topic": topic,
                "research_findings": research_findings,
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            self.log_action(
                action="Research failed",
                reasoning=f"Error occurred: {str(e)}",
                metadata={"error": str(e)}
            )
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name
            }
    
    def _create_research_prompt(self, topic: str, questions: List[str]) -> str:
        """Create a detailed research prompt."""
        prompt = f"""You are an expert research assistant. Research the following topic thoroughly:

Topic: {topic}

Context from previous research: {self.get_context()}

Please provide:
1. Overview of the topic
2. Key findings and insights
3. Important statistics or data points
4. Current trends and developments
5. Potential challenges or considerations
"""
        
        if questions:
            prompt += "\n\nSpecific questions to address:\n"
            for i, question in enumerate(questions, 1):
                prompt += f"{i}. {question}\n"
                
        prompt += "\n\nProvide the response in a structured JSON format."
        
        return prompt
    
    def _process_real_data(self, real_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process real data from multiple sources into structured findings."""
        findings = {
            "overview": f"Research completed using {real_data.get('total_sources', 0)} real data sources",
            "key_findings": [],
            "detailed_sources": {},
            "market_data": None,
            "news_summary": None,
            "web_insights": [],
            "data_sources": real_data.get('sources_used', []),
            "research_timestamp": real_data.get('research_completed_at', '')
        }
        
        research_data = real_data.get('findings', {})
        
        # Process web search results - Limited for performance
        if 'web_search' in research_data:
            web_results = research_data['web_search']
            findings['detailed_sources']['web_search'] = web_results
            for result in web_results[:5]:  # Reduced to 5 results for performance
                findings['key_findings'].append(f"Web: {result.get('title', 'Unknown')} - {result.get('snippet', '')[:100]}...")
                findings['web_insights'].append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'summary': result.get('snippet', '')
                })
        
        # Process Wikipedia data
        if 'wikipedia' in research_data:
            wiki_data = research_data['wikipedia']
            findings['detailed_sources']['wikipedia'] = wiki_data
            if 'summary' in wiki_data:
                findings['key_findings'].append(f"Wikipedia: {wiki_data['title']} - {wiki_data['summary'][:150]}...")
                findings['overview'] = f"Wikipedia Overview: {wiki_data['summary'][:300]}..."
        
        # Process news articles
        if 'news' in research_data:
            news_articles = research_data['news']
            findings['detailed_sources']['news'] = news_articles
            news_titles = [article.get('title', '') for article in news_articles[:3]]
            findings['news_summary'] = f"Recent news: {', '.join(news_titles)}"
            for article in news_articles[:3]:
                findings['key_findings'].append(f"News: {article.get('title', '')} - {article.get('summary', '')[:100]}...")
        
        # Process market data
        if 'market_data' in research_data:
            market_data = research_data['market_data']
            findings['detailed_sources']['market_data'] = market_data
            findings['market_data'] = market_data
            for stock in market_data:
                if 'error' not in stock:
                    price_change = stock.get('price_change_30d', 0)
                    direction = "📈" if price_change > 0 else "📉" if price_change < 0 else "➡️"
                    findings['key_findings'].append(
                        f"Market: {stock.get('company_name', stock.get('symbol', 'Unknown'))} "
                        f"{direction} ${stock.get('current_price', 'N/A')} "
                        f"({price_change:+.1f}% 30d)"
                    )
        
        # Process detailed content
        if 'detailed_content' in research_data:
            detailed_content = research_data['detailed_content']
            findings['detailed_sources']['scraped_content'] = detailed_content
            for content in detailed_content[:2]:  # Top 2 detailed sources
                if 'error' not in content:
                    findings['key_findings'].append(f"Content: {content.get('title', 'Unknown')} - {content.get('content', '')[:150]}...")
        
        return findings

    def _parse_research_findings(self, llm_response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured findings."""
        try:
            # Try to parse as JSON first
            return json.loads(llm_response)
        except:
            # If not valid JSON, structure it ourselves
            return {
                "overview": llm_response[:500],
                "key_findings": [llm_response],
                "raw_response": llm_response
            }
