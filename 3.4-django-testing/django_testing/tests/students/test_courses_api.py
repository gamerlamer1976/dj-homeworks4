import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    # 1. Arrange: создаем данные для теста
    course = course_factory()  # Фабрика создает один курс в тестовой БД

    # Строим URL. В DRF для получения одного объекта обычно используется суффикс '-detail'
    url = reverse('courses-detail', args=[course.id])

    # 2. Act: выполняем действие (делаем GET-запрос через тестовый клиент)
    response = api_client.get(url)

    # 3. Assert: проверяем результаты
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    # Преобразуем ответ из формата JSON в словарь Python
    data = response.json()

    # Проверяем, что ID и имя в ответе совпадают с тем курсом, который мы создали
    assert data['id'] == course.id
    assert data['name'] == course.name


@pytest.mark.django_db
def test_get_course_list(api_client, course_factory):
    # 1. Arrange: создаем несколько курсов (например, 3 штуки)
    # Параметр _quantity указывает фабрике, сколько объектов сгенерировать
    courses = course_factory(_quantity=3)

    # Строим URL для получения списка. Для списка в DRF обычно используется суффикс '-list'
    url = reverse('courses-list')

    # 2. Act: делаем GET-запрос
    response = api_client.get(url)

    # 3. Assert: проверяем результаты
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    data = response.json()

    # Проверяем, что в ответе вернулось ровно столько же курсов, сколько мы создали
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_course_by_id(api_client, course_factory):
    # 1. Arrange: создаем несколько курсов
    courses = course_factory(_quantity=3)

    # Выбираем один курс, по ID которого будем фильтровать (например, первый из созданных)
    target_course = courses[0]

    # Строим базовый URL списка
    url = reverse('courses-list')

    # 2. Act: делаем GET-запрос, передавая параметры фильтрации в аргумент data
    # DRF сам преобразует это в запрос вида: /api/v1/courses/?id=...
    response = api_client.get(url, data={'id': target_course.id})

    # 3. Assert: проверяем результаты
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    data = response.json()

    # Проверяем, что вернулся только один курс (так как ID уникален)
    assert len(data) == 1
    # Проверяем, что ID в ответе совпадает с тем, который мы искали
    assert data[0]['id'] == target_course.id


@pytest.mark.django_db
def test_filter_course_by_name(api_client, course_factory):
    # 1. Arrange: создаем несколько курсов
    courses = course_factory(_quantity=3)
    target_course = courses[0]

    # Строим базовый URL списка
    url = reverse('courses-list')

    # 2. Act: делаем GET-запрос с фильтром по названию (name)
    response = api_client.get(url, data={'name': target_course.name})

    # 3. Assert: проверяем результаты
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    data = response.json()

    # Проверяем, что фильтрация сработала корректно
    assert len(data) == 1
    assert data[0]['name'] == target_course.name


@pytest.mark.django_db
def test_create_course(api_client):
    # 1. Arrange: готовим данные для создания
    # Фабрика не нужна, так как мы хотим проверить именно создание через API
    course_data = {
        'name': 'Python Developer'
    }
    url = reverse('courses-list')

    # 2. Act: отправляем POST-запрос на создание
    # Указываем format='json', чтобы данные точно ушли в JSON-формате
    response = api_client.post(url, data=course_data, format='json')

    # 3. Assert: проверяем результаты
    # При успешном создании DRF по умолчанию возвращает статус 201 (Created)
    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

    data = response.json()
    # Проверяем, что сервер вернул объект с тем же именем, которое мы отправляли
    assert data['name'] == course_data['name']
    # Проверяем, что база данных присвоила новому курсу ID
    assert 'id' in data


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    # 1. Arrange: сначала создаем курс через фабрику, чтобы было что обновлять
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    # Готовим JSON-данные для обновления
    updated_data = {
        'name': 'Updated Python Course'
    }

    # 2. Act: отправляем PATCH-запрос (частичное обновление)
    response = api_client.patch(url, data=updated_data, format='json')

    # 3. Assert: проверяем результаты
    # При успешном обновлении возвращается статус 200 (OK)
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    data = response.json()
    # Убеждаемся, что имя курса действительно изменилось на новое
    assert data['name'] == updated_data['name']


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    # 1. Arrange: создаем курс для удаления
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    # 2. Act: отправляем DELETE-запрос
    response = api_client.delete(url)

    # 3. Assert: проверяем результаты
    # Успешное удаление в DRF обычно возвращает статус 204 (No Content) - нет содержимого
    assert response.status_code == 204, f"Ожидался статус 204, получен {response.status_code}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "students_count, expected_status",
    [
        (2, 201),  # Успешный исход (ровно по лимиту, статус Created)
        (3, 400),  # Неудачный исход (больше лимита, статус Bad Request)
    ]
)
def test_max_students_per_course(api_client, student_factory, settings, students_count, expected_status):
    # 1. Arrange: переопределяем настройку на время выполнения теста
    settings.MAX_STUDENTS_PER_COURSE = 2

    # Создаем нужное количество студентов через фабрику (2 или 3 в зависимости от итерации)
    students = student_factory(_quantity=students_count)
    # Извлекаем список их ID, так как в поле ManyToMany передаются именно идентификаторы
    students_ids = [student.id for student in students]

    # Формируем тело запроса
    course_data = {
        'name': 'Python Bootcamp',
        'students': students_ids
    }
    url = reverse('courses-list')

    # 2. Act: отправляем POST-запрос на создание курса
    response = api_client.post(url, data=course_data, format='json')

    # 3. Assert: проверяем, что сервер вернул ожидаемый HTTP-статус
    assert response.status_code == expected_status
