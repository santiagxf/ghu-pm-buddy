"""Extensions for chat clients with retry logic for rate limiting."""

import logging
from typing import override
from agent_framework import ChatResponse
from openai import RateLimitError
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.exceptions import ServiceResponseException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryCallState

logger = logging.getLogger(__name__)


class AzureOpenAIChatClientWithRetry(AzureOpenAIChatClient):
    """Azure OpenAI Chat Client with built-in retry logic for handling rate limits."""

    retry_attempts = 3
    """Number of retry attempts for rate limit errors."""

    @staticmethod
    def _is_rate_limit_error(exception: BaseException) -> bool:
        """Check if the exception is a rate limit error (429).
        
        Args:
            exception: The exception to check
            
        Returns:
            True if the exception is a ServiceResponseException with a 429 status code
        """
        if isinstance(exception, ServiceResponseException):
            inner = getattr(exception, 'inner_exception', None)
            if inner is not None:
                status_code = getattr(inner, 'status_code', None)
                return status_code == 429
        return False

    @staticmethod
    def _before_sleep_log(retry_state: RetryCallState) -> None:
        """Log when rate limiting is reached and retry is about to sleep."""
        attempt_number = retry_state.attempt_number
        wait_time = retry_state.next_action.sleep if retry_state.next_action else 0
        logger.warning(
            "Rate limiting reached. Attempt %d failed. Retrying in %.2f seconds...",
            attempt_number,
            wait_time,
        )

    @override
    @retry(
        stop=stop_after_attempt(retry_attempts),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ServiceResponseException),
        reraise=True,
        before_sleep=_before_sleep_log
    )
    async def _inner_get_response(self, *args, **kwargs) -> ChatResponse:
        """Get response with retry on rate limit errors (429 status code only)."""
        return await super()._inner_get_response(*args, **kwargs)
