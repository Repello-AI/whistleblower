"""
Data structures for capturing audit report information during system prompt detection.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class PromptResponse:
    """Represents a single prompt-response pair with metadata."""
    timestamp: str
    prompt: str
    response: str
    score: Optional[int] = None
    improvement_suggestion: Optional[str] = None
    iteration: Optional[int] = None


@dataclass
class ContextQuestion:
    """Represents a context-gathering question and its response."""
    question: str
    response: str


@dataclass
class ReportData:
    """Container for all data needed to generate an audit report."""
    # Executive Summary
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    detection_status: str = "In Progress"
    
    # Target Information
    target_endpoint: str = ""
    api_key_used: bool = False
    request_body_structure: Dict[str, Any] = field(default_factory=dict)
    response_body_structure: Dict[str, Any] = field(default_factory=dict)
    openai_model: str = ""
    
    # Context Gathering
    context_questions: List[ContextQuestion] = field(default_factory=list)
    context_analysis: str = ""
    
    # Detection Process
    prompt_responses: List[PromptResponse] = field(default_factory=list)
    total_iterations: int = 0
    
    # Analysis Results
    inferred_system_prompt: str = ""
    final_score: Optional[int] = None
    
    def add_context_question(self, question: str, response: str):
        """Add a context gathering question and response."""
        self.context_questions.append(ContextQuestion(question=question, response=response))
    
    def add_prompt_response(self, prompt: str, response: str, score: Optional[int] = None, 
                           improvement: Optional[str] = None, iteration: Optional[int] = None):
        """Add a prompt-response pair from the detection process."""
        pr = PromptResponse(
            timestamp=datetime.now().isoformat(),
            prompt=prompt,
            response=response,
            score=score,
            improvement_suggestion=improvement,
            iteration=iteration
        )
        self.prompt_responses.append(pr)
    
    def finalize(self, inferred_prompt: str, status: str = "Completed"):
        """Mark the detection process as complete."""
        self.end_time = datetime.now().isoformat()
        self.inferred_system_prompt = inferred_prompt
        self.detection_status = status
        if self.prompt_responses:
            self.final_score = self.prompt_responses[-1].score
        self.total_iterations = len(self.prompt_responses)
    
    def get_duration(self) -> str:
        """Calculate and return the duration of the detection process."""
        if not self.end_time:
            return "N/A"
        try:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            duration = end - start
            return str(duration)
        except:
            return "N/A"
