from bs4 import BeautifulSoup

import requests

sections_news = dict()

'''
функция принимает на вход Категорию новостей введенную пользователем (key)
проверяет в словаре sections_news, есть ли такая категория
парсим данные: название новости, краткое содержание, url
обрабатываем полученные данные, формируем из них списки и собираем из данных словарь
выводим данные словаря на печать
'''


def section_pars(key):
    page_section = requests.get(key)
    soup_section = BeautifulSoup(page_section.text, "html.parser")

    # парсим все необходимые данные методом findAll() передавая ему названия тегов и их классы
    all_news_soup = soup_section.findAll('span', class_='news-helpers_show_mobile-small')
    url_news_soup = soup_section.findAll('a', class_='news-tidings__link')
    desc_news_soup = soup_section.findAll('div', class_='news-tidings__speech')

    all_news_sec = []
    url_news_sec = []
    desc_news_sec = []

    for n in all_news_soup:
        all_news_sec.append(n.text.strip())  # перед добавлением в список, удаляем лишние пробелы по краям
    for url in url_news_soup:
        url_news_sec.append(url.get('href'))  # url.get('href') из тега <a> получаем url
    for d in desc_news_soup:
        desc_news_sec.append(d.text.strip())

    # формируем из списков словарь dict_news
    dict_news = dict()
    for n in range(len(all_news_sec)):
        dict_news.update({
            n: {'url': key + url_news_sec[n],
                'news': all_news_sec[n],
                'desc': desc_news_sec[n]}
        })

    for dn in range(len(dict_news)):
        print(f'''{dn + 1}.  {dict_news[dn]["news"]}
            {dict_news[dn]["desc"]}
            {dict_news[dn]["url"]}''')


# ->

page = requests.get('https://onliner.by')

if page.status_code == 200:  # page.status_code - статус код '200'- успешно подключены, всё ок
    # print(page.text)
    soup = BeautifulSoup(page.text, "html.parser")

    # парсим заголовок сайта из тега <title>, получаем текст находящийся внутри тега
    title = soup.title.text
    print(f'Парсинг новостей на сайте {title}\n')

    '''
    Парсинг категорий новостей и их url для дальнейшего перехода на необходимую страницу и продолжения парсинга


    # разберем HTML код блока, в котором находится информацию о категории новости (название категории, url):

    <header class="b-main-page-blocks-header-2 cfix">
        <h2>
            <a href="https://money.onliner.by">Кошелек</a>
        </h2>
    </header>


    # видим, что тег <a> обернут в тег <h2>, который в свою очередь обернут в тег <header>

    __________

    Поскольку теги категорий новостей <a> не имеет CSS классов для конкретизации поиска по тегу, 
    тег <h2> внутри которого лежит <a> также не имеет классов,
    а ссылок (тегов <a>) на сайте большое количество,
    парсинг начнем с <header>, внутри которого находятся необходимые нам данные

    '''

    # выполняем поиск тегов <header>
    sections = soup.findAll('header', class_='b-main-page-blocks-header-2')
    # print(type(sections))  # <class 'bs4.element.ResultSet'>
    # ResultSet является объектом подкласса list, можем работать с ним как с list

    if sections:
        for s in sections:
            # проходимся циклом по полученному списку и внутри тегов <header> ищем тег <h2>, а внутри <h2> уже <a>
            result_a = s.h2.a
            result_a_text = result_a.text.strip()  # получаем текст тега <a>

            # проверяем, является ли полученный текст категорией новостей (категории мы пометили предварительно)
            if result_a_text and result_a_text in 'Кошелек Авто Недвижимость Технологии':
                # если текст - категория новостей, получаем url категории .get('href')
                sections_news.update({
                    result_a_text: result_a.get('href')
                })
        print(' Доступны категории новостей:')
        for sect in sections_news:
            print(f'* {sect} - url: {sections_news[sect]}')

        user_select = (input('Для просмотра новостей введите название категории:\n -> ').strip().capitalize()
                       .replace('ё', 'е'))

        if user_select in sections_news.keys():
            section_pars(sections_news[user_select])
        else:
            print('Введенная категория не найдена')
