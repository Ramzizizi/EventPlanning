![alt text](https://static.tildacdn.com/tild3561-6163-4531-b662-383539366166/WIS_LOGO_white_NEW.svg)

# Django Rest Framework

**Время на карточку**
- 44 ч.

**Темы**
1. REST: определение и требования к архитектуре
2. Class-based Views
3. Serializer
4. Filter, FilterSet
5. Search
6. Mixins, Generics
7. ModelViewSet

**Теоретические вопросы**
---

**_Request & Response_**

⁃ Какими ключевые параметры обладает Request?
- "data" для информации о данных в запросе, "query_params" для информации о параметрах запроса


⁃ Как в request попадают user, auth и что содержат?
- "user" как и "auth" попадают в запрос согласно установленной политике авторизации 


⁃ request.META, request.sessionResponse, атрибуты, render
- так как "request" основан на "HttpRequest" Django, он имеет все его атрибуты 

---

**_Views_**

⁃ ClassBasedViews - APIView, основные методы
⁃ FunctionBasedViews - api_view, schema
⁃ GenericAPIView - основные атрибуты и методы
⁃ Mixins - CRUD (create, retrieve, update, delete)
⁃ ViewSet - actions, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet, creating Custom ViewSet
- Какие атрибуты есть у views, и для чего они нужны?
- Как передать текущего пользователя в serializer?
- action декоратор. Для чего он нужен? Что использовать вместо него в DRF версии ниже 3.8?

---

**_Routing_**

⁃ SimpleRouter
- стандартный роут, позволяет включать пути созданные с помощью action


⁃ Mark extra actions for routing
- можно создать дополнительный рут с помощью декоратора "action"


⁃ DynamicRoute
- кастомизирует поведение "action"


⁃ Route
-


- какие типы router-ов есть, и в чем отличие?
- Simple, Default, Custom
Simple и Default похожи, но Default генерирует дополнительную информацию по внутреннему корню 


---

**_Serializers_**

⁃ Serializer - serializing, deserializing, create, update, save, dealing with nested objects
⁃ ModelSerializer - Meta, fields, depth, read_only_fields, Relational fields


⁃ HyperlinkedModelSerializer
- похож на ModelSerializer, но используется для установления связи между связанными моделями по средствам поелй


⁃ ListSerializer
⁃ BaseSerializer - data, is_valid
-


- какие аттрибуты может принимать class Meta у serializer-а, и для чего они нужны
- валидаторы, данные о модели, уровень глубины, данные о сериализаторе и доп параметры


- что такое контекст serializer-а? Для чего он нужен?
- контекст полученный при запросе, добавляет объекты запроса, viewset и формат


- как использовать serializer для сохранения изменений модели
- валидация полей serializer-а
- какие методы есть у serializer-а и для чего они нужны?

---

**_Permissions_**

- какие есть permissions в DRF?
- проверка аутенфикации, проверка чтения, проверка админа


- как создать кастомный permission?
- необходимо наследоваться от "permissions.BasePermission"


- какие методы можно предопределить от BasePermission и для чего они нужны?
- "has_permission" и "has_object_permission"


- как создать permission на rout, который создается при помощи декоратора action?
- указать в декораторе "permission_classes"


---

**_Filtering, ordering, search_**
- как можно реализовать фильтрацию, сортировку, и поиск по определенным полям?
- можно реализовать как с помощью переопределения "get_queryset", так и с помощью дополнительной библиотеки "django-filter"
при использовании библиотеки необходимо в настройках определить настройки "DEFAULT_FILTER_BACKENDS" или добавить "filter_backends = [DjangoFilterBackend]"
для фильтрации полей надо использовать "filterset_fields", для поиска "search_fields", для сортировки "ordering_fields"


---

**_Throttling в DRF_**
- принцип
- ограничение пропускной способности, ограничение происходит как по пользователю, так и по какой-то части API


---

**_HTTP_**
- модуль rest_framework.status
- содержит в себе статусы ответа от сервера


- коды ответов от сервера. какие есть, для чего нужны, какие в каких случаях использовать?
- 1хх - инфо, 2хх - успешные, 3хх - перенаправление, 4хх - ошибка клиента, 5хх - ошибка сервера


- методы HTTP - какие бывают? Как их использовать?
- post, put, patch, get, delete


- polling, long polling
- частые опросы сервера


- web sockets - как работает?

---

**Практическое задание**

Добавить API в имеющееся приложение на Django для основных сущностей.
Обратить внимание на соответствие разработанного API методологии REST.

**_Требования:_**
- Реализовать авторизацию по JWT
- Использование Permissions
- Использование валидаторов, в том числе кастомных
- использование в views как ViewSets, так и Generics
- Для ViewSets использовать как queryset, так и get_queryset
