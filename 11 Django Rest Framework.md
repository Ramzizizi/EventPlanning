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
⁃ Как в request попадают user, auth и что содержат?
⁃ request.META, request.sessionResponse, атрибуты, render

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
⁃ Mark extra actions for routing
⁃ DynamicRoute
⁃ Route
- какие типы router-ов есть, и в чем отличие?

---

**_Serializers_**

⁃ Serializer - serializing, deserializing, create, update, save, dealing with nested objects
⁃ ModelSerializer - Meta, fields, depth, read_only_fields, Relational fields
⁃ HyperlinkedModelSerializer
⁃ ListSerializer
⁃ BaseSerializer - data, is_valid
- какие аттрибуты может принимать class Meta у serializer-а, и для чего они нужны
- что такое контекст serializer-а? Для чего он нужен?
- как использовать serializer для сохранения изменений модели
- валидация полей serializer-а
- какие методы есть у serializer-а и для чего они нужны?

---

**_Permissions_**

- какие есть permissions в DRF?
- как создать кастомный permission?
- какие методы можно предопределить от BasePermission и для чего они нужны?
- как создать permission на rout, который создается при помощи декоратора action?

---

**_Filtering, ordering, search_**
- как можно реализовать фильтрацию, сортировку, и поиск по определенным полям?

---

**_Throttling в DRF_**
- принцип

---

**_HTTP_**
- модуль rest_framework.status
- коды ответов от сервера. какие есть, для чего нужны, какие в каких случаях использовать?
- методы HTTP - какие бывают? Как их использовать?
- polling, long polling
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
