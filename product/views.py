from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Lesson

def product_list(request):
    products = Product.objects.all()
    data = []

    for product in products:
        lessons_count = Lesson.objects.filter(product=product).count()
        product_data = {
            'id': product.id,
            'creator': product.creator.id,
            'name': product.name,
            'start_date': product.start_date,
            'cost': product.cost,
            'lessons_count': lessons_count
        }
        data.append(product_data)

    return JsonResponse(data, safe=False)

def lesson_list(request, product_id):
    # Проверяем, имеет ли пользователь доступ к продукту
    if not request.user.has_perm('app.view_product'):
        return JsonResponse({'error': 'У вас нет доступа к данному продукту'})

    # Получаем список уроков для заданного продукта
    lessons = Lesson.objects.filter(product_id=product_id)

    # Создаем список словарей, содержащих данные об уроках
    lesson_data = []
    for lesson in lessons:
        lesson_dict = {
            'name': lesson.name,
            'video_link': lesson.video_link,
            # Другие поля урока, если необходимо
        }
        lesson_data.append(lesson_dict)

    return JsonResponse({'lessons': lesson_data})