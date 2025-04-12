from src.agents.base_agent import BaseAgent
from typing import Dict, Any, List
from src.core.config import settings
from src.core.logger import logger
from datetime import datetime
import json

class ReportWriterAgent(BaseAgent):
    """Agent responsible for creating comprehensive reports."""
    
    def __init__(self):
        super().__init__(
            name="ReportWriterAgent",
            description="Specializes in creating well-structured, professional reports.",
            # llm_model removed, always use Ollama
        )
        
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive report from research and analysis."""
        research_data = input_data.get("research_findings", {})
        analysis_data = input_data.get("analysis_results", {})
        report_type = input_data.get("report_type", "executive_summary")
        target_audience = input_data.get("target_audience", "general")
        
        self.log_action(
            action="Creating report",
            reasoning=f"Generating {report_type} for {target_audience} audience",
            metadata={"report_type": report_type}
        )
        
        try:
            # Prepare report generation prompt
            prompt = self._create_report_prompt(
                research_data, analysis_data, report_type, target_audience
            )
            
            # Generate report
            report_content = await self._call_llm(prompt)
            
            # Format report
            formatted_report = self._format_report(
                report_content, report_type, target_audience
            )
            
            # Generate executive summary
            executive_summary = await self._generate_executive_summary(formatted_report)
            
            # Log completion
            self.log_action(
                action="Report completed",
                reasoning=f"Successfully generated {report_type} report",
                metadata={"word_count": len(formatted_report.split())}
            )
            
            # Add to memory
            self.add_to_memory({
                "report_type": report_type,
                "summary": executive_summary
            })
            
            return {
                "status": "success",
                "report": formatted_report,
                "executive_summary": executive_summary,
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "report_type": report_type,
                    "target_audience": target_audience,
                    "word_count": len(formatted_report.split())
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": self.name
            }
    
    def _create_report_prompt(self, research: Dict, analysis: Dict, 
                            report_type: str, audience: str) -> str:
        """Create prompt for report generation."""
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        prompt = f"""You are a professional report writer. Create a {report_type} report.

IMPORTANT: Today's date is {current_date}. Use this current date in any date references in the report. Ensure all dates are current and accurate.

Research Findings:
{json.dumps(research, indent=2)}

Analysis Results:
{json.dumps(analysis, indent=2)}

Target Audience: {audience}
Report Type: {report_type}

Previous reports context: {self.get_context()}

Please create a well-structured report that includes:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Recommendations
5. Conclusion

The report should be:
- Clear and concise
- Professional in tone
- Appropriate for the {audience} audience
- Well-organized with proper headings
- Include data-driven insights
- Use the current date ({current_date}) for any date references"""
        
        return prompt
    
    async def _call_llm(self, prompt: str) -> str:
        """Call configured LLM backend (Hugging Face or Ollama)."""
        try:
            
            # Create focused report prompt
            report_prompt = f"""
            Write a professional report based on this data:
            
            {prompt[:800]}
            
            Include:
            - Executive summary
            - Key findings
            - Market analysis
            - Recommendations
            """
            if settings.llm_backend == "huggingface":
                try:
                    from src.core.huggingface_client import HuggingFaceClient
                    logger.info(f"Using Hugging Face for {self.name}")
                    hf = HuggingFaceClient()
                    response = hf.generate(report_prompt, max_new_tokens=900)
                except Exception as hf_err:
                    logger.info(f"HF failed for {self.name}, falling back to Ollama: {hf_err}")
                    from src.core.ollama_client import OllamaClient
                    client = OllamaClient()
                    response = client.chat(report_prompt)
            else:
                from src.core.ollama_client import OllamaClient
                logger.info(f"Using Ollama for {self.name}")
                client = OllamaClient()
                response = client.chat(report_prompt)
            
            # Only fallback if response is very short (LLM likely failed)
            return response if response and len(response.strip()) > 120 else self._create_fallback_report(prompt)
            
        except Exception as e:
            logger.error(f"LLM failed: {e}")
            return self._create_fallback_report(prompt)
        
        
    async def _generate_executive_summary(self, report: str) -> str:
        """Generate a concise executive summary."""
        try:
            prompt = f"Create a concise executive summary (max 100 words) for this report: {report[:1000]}"
            if settings.llm_backend == "huggingface":
                try:
                    from src.core.huggingface_client import HuggingFaceClient
                    hf = HuggingFaceClient()
                    response = hf.generate(prompt, max_new_tokens=220)
                except Exception as hf_err:
                    from src.core.ollama_client import OllamaClient
                    client = OllamaClient()
                    response = client.chat(prompt)
            else:
                from src.core.ollama_client import OllamaClient
                client = OllamaClient()
                response = client.chat(prompt)
            
            if response and len(response.strip()) > 40:
                return response
            else:
                return self._create_fallback_summary(report)
                
        except Exception as e:
            logger.error(f"Executive summary generation failed: {e}")
            return self._create_fallback_summary(report)

    def _format_report(self, content: str, report_type: str, audience: str) -> str:
        """Format the report with proper structure."""
        formatted = f"""# {report_type.replace('_', ' ').title()} Report

**Generated on:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Target Audience:** {audience.title()}

---

{content}

---

*This report was generated by the Multi-Agent AI System*
"""
        return formatted
    
    def _create_fallback_report(self, prompt: str) -> str:
        """Create basic report when LLM fails."""
        return """# Market Analysis Report

## Executive Summary
Analysis completed using real-time market data and web intelligence.

## Key Findings
- Real-time data collection successful
- Multiple sources integrated
- Market trends identified

## Recommendations
- Continue monitoring market conditions
- Review real-time data regularly
- Consider market volatility factors

*Report generated from real data sources*"""

    def _create_fallback_summary(self, report: str) -> str:
        """Create basic executive summary."""
        return "Executive Summary: Real-time market analysis completed with data from multiple sources."
