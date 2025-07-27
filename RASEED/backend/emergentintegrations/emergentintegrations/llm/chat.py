"""
LLM integration using LiteLLM for flexible provider support.
"""
import pathlib
import litellm
import base64
from litellm import ModelResponse
from typing import Callable, Dict, Any, List, Optional, Union

class FileContent:
    def __init__(self, content_type: str, file_content_base64: str) -> None:
        self.content_type = content_type
        self.file_content_base64 = file_content_base64
    
class ImageContent(FileContent):
    def __init__(self, image_base64: str) -> None:
        super().__init__("image", image_base64)
        
class FileContentWithMimeType(FileContent):
    def __init__(self, mime_type: str, file_path: str) -> None:
        file_bytes = pathlib.Path(file_path).read_bytes()
        file_content_base64 = base64.b64encode(file_bytes).decode('utf-8')
        super().__init__(mime_type, file_content_base64)

class UserMessage:
    def __init__(self, text: str = None, file_contents: list[FileContent] = None) -> None:
        self.text = text
        self.file_contents = file_contents or []  # Initialize as empty list if None

class LlmChat:
    """
    LLM integration using LiteLLM for generating chat completions.
    This class provides compatibility with OpenAI's API while supporting
    multiple LLM providers through LiteLLM.
    """

    def __init__(self, api_key: str, session_id: str, system_message: str, initial_messages: List[Dict[str, Any]] = None):
        self.api_key = api_key    
        self.model = "gpt-4o" 
        self.messages = initial_messages or [{"role": "system", "content": system_message}]
        self.max_tokens = 8192
        self.session_id = session_id
        self.provider = "openai"
        
    def with_model(self, provider: str, model: str) -> "LlmChat":
        self.provider = provider
        self.model = model
        return self
    
    def with_max_tokens(self, max_tokens: int) -> "LlmChat":
        self.max_tokens = max_tokens
        return self
    
    async def _add_assistant_message(self, messages: List[Dict[str, Any]], message: str):
        messages.append({"role": "assistant", "content": message})
        await self._save_messages(messages)
    
    async def _add_user_message(self, messages, message: UserMessage):
        # Check if file contents are being used with non-Gemini provider
        if message.file_contents and any(isinstance(content, FileContentWithMimeType) for content in message.file_contents):
            if self.provider != "gemini":
                raise ChatError("File attachments are only supported with Gemini provider")
        
        if message.text:
            messages.append({"role": "user", "content": [{"type": "text", "text": message.text}]})
        for content in message.file_contents:
            if content.content_type == "image":
                messages.append({"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{content.file_content_base64}"}}]})
            else:
                messages.append({"role": "user", "content": [{"type": "file", "file": { "file_data": "data:{};base64,{}".format(content.content_type, content.file_content_base64) }}]})
        await self._save_messages(messages)
        
    async def get_messages(self) -> List[Dict[str, Any]]:
        return self.messages
    
    async def _save_messages(self, messages):
        self.messages = messages

    async def send_message(self, user_message: UserMessage) -> str:
        messages = await self.get_messages()
        await self._add_user_message(messages, user_message)
        try:            
            params = {
                "model": f"{self.provider}/{self.model}",
                "messages": messages,
                "api_key": self.api_key,  # Always include the API key
                "max_tokens": self.max_tokens,
            }            
            response: ModelResponse = litellm.completion(**params)
            response_text = await self._extract_response_text(response)
            await self._add_assistant_message(messages, response_text)  # Pass both messages and response_text
            return response_text
        except Exception as e:
            raise ChatError(f"Failed to generate chat completion: {str(e)}")
        

    async def _extract_response_text(self, response: ModelResponse) -> str:
        """
        Extract the text or content from a chat completion response.
        Handles various response formats including text and images.

        Args:
            response (Dict[str, Any]): The response from a chat completion request.

        Returns:
            str: The extracted content, which could be text or a structured representation
                 of images/multimodal content.
        """
        try:
            if len(response.choices) > 0 and response.choices[0].message:
                return response.choices[0].message.content
            raise ChatError(f"Failed to extract response text")
        except Exception as e:
            raise ChatError(f"Failed to extract response text: {str(e)}")


class ChatError(Exception):
    """Exception raised for errors in the LLM chat integration."""
    pass
