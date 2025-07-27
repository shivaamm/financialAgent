import asyncio
import os
from typing import List
from litellm import image_generation
import base64

class OpenAIImageGeneration:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_images(
        self,
        prompt: str,
        model: str = "gpt-image-1",
        number_of_images: int = 1
    ) -> List[bytes]:
        """
        Generates images using OpenAI's image generation API via LiteLLM.
        
        Args:
            prompt (str): The prompt to generate images from
            model (str): The model to use for generation
            number_of_images (int): Number of images to generate
            
        Returns:
            List[bytes]: List of generated image bytes
        """
        try:
            response = image_generation(
                model=f"openai/{model}",
                prompt=prompt,
                n=number_of_images,
                api_key=self.api_key
            )
            
            # Convert URLs to bytes
            image_bytes_list = []
            for img in response.data:
                image_bytes_list.append(base64.b64decode(img.b64_json))
            
            return image_bytes_list
        except Exception as e:
            raise Exception(f"Failed to generate images: {str(e)}")

