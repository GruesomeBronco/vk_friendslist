# vk_friendslist_app
Python console app for working with VK API

---

1. Регаем приложение в ВК для работы
2. Получаем `access_token`. Это сервисный ключ доступа в нашем приложении которое мы создали. 
3. Получить список друзей.
3.1. Получить user_id.(METHOD=users.get.user_ids)
3.2. Получить 
4. Сохранить его в нужном виде(CSV, TSV, JSON)


# Как получить Access Token?

https://habr.com/ru/post/306022/
https://dementiy.github.io/assignments/vk_api/#_1

Запросы к API ВКонтакте имеют следующий формат:
https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V


1. Имя;
2. Фамилия;
3. Страна; country
4. Город; city
5. Дата рождения в ISO формате; bdate
6. Пол; sex



1. Test IDs = [1, 2]
