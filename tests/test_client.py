"""Unit tests for async submission behavior in the HTTP client."""

from unittest.mock import AsyncMock

import pytest

from core.client import NanoBananaClient


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running NanoBanana operations should default to async submission."""
    client = NanoBananaClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "generate"})
    assert payload["callback_url"] == "https://api.acedata.cloud/health"


@pytest.mark.asyncio
async def test_generate_image_injects_async_callback_without_polling(mock_image_response) -> None:
    """generate_image should inject callback_url and not poll for results."""
    client = NanoBananaClient(api_token="test-token", base_url="https://api.test.com")
    client.request = AsyncMock(return_value=mock_image_response)
    client.query_task = AsyncMock()

    result = await client.generate_image(action="generate", prompt="test")

    assert result == mock_image_response
    # callback_url must have been injected by _with_async_callback
    called_payload = client.request.call_args[0][1]
    assert called_payload["callback_url"] == "https://api.acedata.cloud/health"
    client.query_task.assert_not_called()
