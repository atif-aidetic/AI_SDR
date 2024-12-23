import tasks as tasks
import json
import api.services as services
from ..models import Collections
import os
from settings import ENV

env = ENV()

keys = {"openai_key": env.openai_api_key, "apollo_key": env.APOLLO_AUTH_KEY}


def generate_leads_view(request):
    try:
        if request.method == "POST":
            # one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
            # if Collections.objects.filter(created_at__gte=one_hour_ago).exists():
            #     context = {
            #         "message": "CAUTION: You can only use this facility once in an hour. Please try again after an hour!"
            #     }
            #     return render(request, "stop.html", context)
            query = request.POST["query"]
            title = request.POST.get("titles", None)
            seniority = request.POST.get("seniority", None)
            function = request.POST.get("function", None)
            email = request.POST["email"]
            positions = services.get_positions(title, seniority, function)
            collection_id = services.add_collection(email)
            content = {
                "query": query,
                "positions": positions,
                "email": email,
                "collection_id": collection_id,
            }
            content = json.dumps(content)
            tasks.generate_leads_task.delay(content, keys)
            context = {
                "message": "Processing has started. You will receive an email with the results when they are ready."
            }
            return render(request, "stop.html", context)
        return render(request, "startwo.html")
    except Exception as e:
        print({"error": str(e)})
        return JsonResponse({"error": str(e)})
