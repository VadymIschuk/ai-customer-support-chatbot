from google.genai import types
from django.core.cache import cache
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession, Message
from google import genai


@api_view(['POST'])
def process_prompt(request):
    prompt = request.data.get('prompt', '')
    session_id = request.data.get('session_id', 'default_session')

    if not prompt:
        return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f"chat_history_{session_id}"
    history_for_gemini = cache.get(cache_key) or []

    system_instruction = (
        "You are the official support chatbot for 'TechSol'. Your name is Solar. "
        "You assist customers with software development inquiries and pricing plans. "
        "Style: Polite, professional, and concise. "
        "If you encounter a request beyond your knowledge or complex technical issues, "
        "ONLY then say: 'I am transferring your request to a human operator.'"
    )

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=history_for_gemini + [{"role": "user", "parts": [{"text": prompt}]}],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
        ai_response = response.text

        session, _ = ChatSession.objects.get_or_create(session_id=session_id)

        user_msg = prompt.lower()
        if any(word in user_msg for word in ['price', 'pricing', 'cost', 'billing', 'buy', 'pay']):
            session.tag = 'billing'
        elif any(word in user_msg for word in ['error', 'bug', 'not working', 'technical', 'issue', 'fix']):
            session.tag = 'tech'
        elif any(word in user_msg for word in ['complaint', 'bad', 'terrible', 'disappointed']):
            session.tag = 'complaint'

        escalation_keywords = ["operator", "human", "transfer", "manager", "support agent"]
        if any(word in ai_response.lower() for word in escalation_keywords):
            session.is_escalated = True

        session.save()

        new_history = history_for_gemini + [
            {"role": "user", "parts": [{"text": prompt}]},
            {"role": "model", "parts": [{"text": ai_response}]}
        ]
        cache.set(cache_key, new_history[-10:], timeout=3600)

        Message.objects.create(session=session, sender='user', text=prompt)
        Message.objects.create(session=session, sender='bot', text=ai_response)

        return Response({
            'response': ai_response,
            'is_escalated': session.is_escalated,
            'tag': session.tag
        }, status=status.HTTP_200_OK)

    except Exception as e:
        if "503" in str(e):
            return Response({'error': 'Service is currently overloaded. Please try again later.'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
