
import unittest
from unittest.mock import patch

from app.llms import get_openai_model


class TestLLMs(unittest.TestCase):

    @patch("app.llms.ChatOpenAI")
    @patch("app.llms.OPENAI_MODEL", "gpt-4.1-mini")
    @patch("app.llms.OPENAI_API_KEY", "test-api-key")
    def test_get_gpt4_model(self, mock_chat_openai):

        get_openai_model(temperature=0.9)

        mock_chat_openai.assert_called_once_with(
            model="gpt-4.1-mini",
            temperature=0.9,
            api_key="test-api-key"
        )

    @patch("app.llms.ChatOpenAI")
    @patch("app.llms.OPENAI_MODEL", "gpt-6.1-sol")
    @patch("app.llms.OPENAI_API_KEY", "test-api-key")
    def test_get_gpt6_model(self, mock_chat_openai):

        get_openai_model(temperature=0.9)

        mock_chat_openai.assert_called_once_with(
            model="gpt-6.1-sol",
            api_key="test-api-key",
            use_responses_api=True,
            reasoning={"effort": "low"}
        )

    @patch("app.llms.OPENAI_API_KEY", None)
    def test_missing_api_key(self):

        with self.assertRaises(ValueError):
            get_openai_model()


if __name__ == "__main__":
    unittest.main()
