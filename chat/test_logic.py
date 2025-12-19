import pytest
from django.urls import reverse
from django.core.cache import cache
from chat.models import ChatSession, Message


@pytest.fixture(autouse=True)
def mock_gemini_response(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.text = "I am a solar support bot. Transferring to human operator."

    def mock_generate(*args, **kwargs):
        return MockResponse()

    import google.genai.models as models
    monkeypatch.setattr(models.Models, "generate_content", mock_generate)


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def chat_session(db):
    return ChatSession.objects.create(session_id="test_user_123", tag="general")


@pytest.mark.django_db
class TestChatBot:

    def test_session_creation(self, client):

        url = reverse('process_prompt')
        data = {"prompt": "Hello", "session_id": "new_session"}

        response = client.post(url, data, content_type='application/json')

        assert response.status_code == 200
        assert ChatSession.objects.filter(session_id="new_session").exists()

    def test_context_retention_in_redis(self, client):

        url = reverse('process_prompt')
        session_id = "redis_test"
        data = {"prompt": "Context test", "session_id": session_id}

        client.post(url, data, content_type='application/json')

        cache_key = f"chat_history_{session_id}"
        history = cache.get(cache_key)

        assert history is not None
        assert len(history) >= 2

    def test_tagging_logic_billing(self, client):

        url = reverse('process_prompt')

        data = {"prompt": "How much does it cost?", "session_id": "tag_test"}

        client.post(url, data, content_type='application/json')

        session = ChatSession.objects.get(session_id="tag_test")
        assert session.tag == 'billing'

    def test_message_storage(self, client, chat_session):

        url = reverse('process_prompt')
        data = {"prompt": "Save me", "session_id": chat_session.session_id}

        client.post(url, data, content_type='application/json')

        messages = Message.objects.filter(session=chat_session)
        assert messages.count() == 2
