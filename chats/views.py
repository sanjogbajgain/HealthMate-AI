from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Chat, Feedback
from main_app.models import consultation
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def post_message(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', '').strip()
        consultation_id = request.session.get('consultation_id')

        if msg and consultation_id:
            try:
                consultation_obj = consultation.objects.get(id=consultation_id)
                chat = Chat.objects.create(consultation_id=consultation_obj, sender=request.user, message=msg)
                return JsonResponse({'msg': chat.message, 'user': request.user.username})
            except consultation.DoesNotExist:
                return JsonResponse({'error': 'Consultation not found.'})
        return JsonResponse({'error': 'Empty message or consultation_id missing.'})
    return JsonResponse({'error': 'Invalid request.'})

def get_messages(request):
    if request.method == "GET":
        consultation_id = request.session.get('consultation_id')
        chat = Chat.objects.filter(consultation_id=consultation_id)
        return render(request, 'consultation/chat_body.html', {'chat': chat})


@csrf_exempt
def post_feedback(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback', '').strip()
        if feedback:
            Feedback.objects.create(sender=request.user, feedback=feedback)
            return HttpResponse("Feedback successfully sent.")
        else:
            return HttpResponse("Feedback field is empty.")

def get_feedback(request):
    if request.method == "GET":
        obj = Feedback.objects.all()
        return render(request, 'consultation/chat_body.html', {"obj": obj})
