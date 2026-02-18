"""
LLM Client for Deepseek API
"""
import os
from typing import Optional, List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DeepseekClient:
    """
    Wrapper for Deepseek API using LangChain's ChatOpenAI.
    
    This client provides both synchronous and streaming responses.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ):
        """
        Initialize Deepseek client.
        
        Args:
            api_key: Deepseek API key (defaults to DEEPSEEK_API_KEY env var)
            model: Model name (defaults to deepseek-chat)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY not found. Please set it in .env file or pass as parameter."
            )
        
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", temperature))
        self.max_tokens = int(os.getenv("DEEPSEEK_MAX_TOKENS", max_tokens))
        
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url="https://api.deepseek.com",
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
    
    def invoke(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ) -> str:
        """
        Synchronously invoke the LLM.
        
        Args:
            prompt: User prompt
            system_message: Optional system message for context
            
        Returns:
            Generated text response
        """
        messages: List[BaseMessage] = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessage(content=prompt))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Deepseek API call failed: {str(e)}")
    
    def stream(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ):
        """
        Stream responses from the LLM.
        
        Args:
            prompt: User prompt
            system_message: Optional system message for context
            
        Yields:
            Text chunks as they arrive
        """
        messages: List[BaseMessage] = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessage(content=prompt))
        
        try:
            for chunk in self.llm.stream(messages):
                if hasattr(chunk, 'content'):
                    yield chunk.content
        except Exception as e:
            raise RuntimeError(f"Deepseek API streaming failed: {str(e)}")
    
    def invoke_with_messages(self, messages: List[BaseMessage]) -> str:
        """
        Invoke with a list of messages (for multi-turn conversations).
        
        Args:
            messages: List of LangChain messages
            
        Returns:
            Generated text response
        """
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Deepseek API call failed: {str(e)}")
    
    def get_llm(self) -> ChatOpenAI:
        """
        Get the underlying LangChain ChatOpenAI instance.
        
        Useful for integration with LangChain tools and chains.
        
        Returns:
            ChatOpenAI instance
        """
        return self.llm


# Global client instance (lazy initialization)
_global_client: Optional[DeepseekClient] = None


def get_llm_client() -> DeepseekClient:
    """
    Get or create a global DeepseekClient instance.
    
    Returns:
        Shared DeepseekClient instance
    """
    global _global_client
    if _global_client is None:
        _global_client = DeepseekClient()
    return _global_client
