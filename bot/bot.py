#code by Vilocer - 2019
#github profile: https://github.com/Vilocer

import os
import re
import sys
import time
import uuid
import threading
import random
import json
import vk_api
from vk_api import keyboard as VkKey 
from termcolor import cprint

red = lambda x: cprint(x, 'red', attrs=['bold'], file=sys.stderr)
green = lambda x: cprint(x, 'green', attrs=['bold'], file=sys.stderr)
blue =  lambda x: cprint(x, 'blue', attrs=['bold'], file=sys.stderr)

TOKEN = os.environ['BOT_SECRET_GROUP_KEY'] # Секретный ключ сообщества

INFO_LIST = os.environ.get('BOT_INFO_MESSAGE', 'This bot coded by V1locer. 2019')

FRIEND_GROUPS = [ -24608732 ]

def key():
    while True:
        try:
            command = input('>')
 
        except KeyboardInterrupt:
            sys.exit()
        except EOFError:
            sys.exit() 

def send(id, text, keyboard=''):
    vk = vk_api.VkApi(token=TOKEN)
    try: 
        if keyboard == '':
            vk.method('messages.send', {'random_id': random.randint(-2147483648, 2147483647), 'peer_id': id, 'message': text})
        else:
            vk.method('messages.send', {'random_id': random.randint(-2147483648, 2147483647), 'peer_id': id, 'message': text, 'keyboard': keyboard})

    except vk_api.exceptions.ApiError:
        time.sleep(5)

        if keyboard == '':
            vk.method('messages.send', {'random_id': random.randint(-2147483648, 2147483647), 'peer_id': id, 'message': text})
        else:
            vk.method('messages.send', {'random_id': random.randint(-2147483648, 2147483647), 'peer_id': id, 'message': text, 'keyboard': keyboard})

    except:
        if keyboard == '':
            vk.method('messages.send', {'random_id': random.randint(-2147483648, 2147483647), 'peer_id': id, 'message': text})
        else:
            vk.method('messages.send', {'random_id': random.randint(-2147483648, 2147483647), 'peer_id': id, 'message': text, 'keyboard': keyboard})

def app(token, user_id, authBy):
    global vk, INFO_LIST, FRIEND_GROUPS

    threads = {

        'autoAddFriends' : None,
        'autoComments' : None,
        'autoAddLikely': None,
        'autoStatus': None,
        'online' : None,
        'autoAddByComment' : None

    }

    state = {

        'autoAddFriends' : True, #False == True - активно; True == False - остановленно; 
        'autoComments' : True,
        'autoAddLikely': True,
        'autoStatus': True,
        'online' : True,
        'autoAddByComment' : True

    }

    def keyboardMaster(state):

        keyboard = VkKey.VkKeyboard(one_time=True)

        if state['autoAddFriends']:
            keyboard.add_button('Автодобавление друзей(выкл.)', color=VkKey.VkKeyboardColor.PRIMARY)
        else:
            keyboard.add_button('Автодобавление друзей(вкл.)', color=VkKey.VkKeyboardColor.POSITIVE)
        keyboard.add_line()

        if state['autoComments']:
            keyboard.add_button('Автокомментирование(выкл.)', color=VkKey.VkKeyboardColor.PRIMARY)
        else:
            keyboard.add_button('Автокомментирование(вкл.)', color=VkKey.VkKeyboardColor.POSITIVE)
        keyboard.add_line()

        if state['autoAddLikely']:
            keyboard.add_button('Автодобавление возможных друзей(выкл.)', color=VkKey.VkKeyboardColor.PRIMARY)
        else:
            keyboard.add_button('Автодобавление возможных друзей(вкл.)', color=VkKey.VkKeyboardColor.POSITIVE)
        keyboard.add_line()

        if state['autoAddByComment']:
            keyboard.add_button('Добавление друзей по комментарию(выкл.)', color=VkKey.VkKeyboardColor.PRIMARY)
        else:
            keyboard.add_button('Добавление друзей по комментарию(вкл.)', color=VkKey.VkKeyboardColor.POSITIVE)
        keyboard.add_line()

        if state['autoStatus']:
            keyboard.add_button('Меняющийся статус(выкл.)', color=VkKey.VkKeyboardColor.PRIMARY)
        else:
            keyboard.add_button('Меняющийся статус(вкл.)', color=VkKey.VkKeyboardColor.POSITIVE)
        keyboard.add_line()

        """if authBy == 'data':

            if state['online']:
                keyboard.add_button('Онлайн(выкл.)', color=VkKey.VkKeyboardColor.PRIMARY)
            else:
                keyboard.add_button('Онлайн(вкл.)', color=VkKey.VkKeyboardColor.POSITIVE)
            keyboard.add_line()"""

        keyboard.add_button('Инфо', color=VkKey.VkKeyboardColor.PRIMARY)
        keyboard.add_button('Выйти', color=VkKey.VkKeyboardColor.NEGATIVE)
        return (keyboard.get_keyboard())

    def autoAddFriends(session, user_id, state):
        global vk

        flag = 5

        send(user_id, '(Автодобавление друзей) Функция включена')

        while True:
            if state():
                break

            req_list = []
            try:
                followers = session.users.getFollowers(fields='sex')
                for follower in followers['items']:
                    try:
                        follower['deactivated']

                    except KeyError:
                        req_list.append(follower['id'])

                for req in req_list:
                    if state():
                        break

                    while True:
                        if state():
                            break

                        if flag == 5:
                            flag = 0

                            try:
                                user = session.users.get(user_ids=req, fields='city')[0]
                                session.friends.add(user_id=req)
                                try:
                                    send(user_id, '(Автодобавление друзей) Принята заявка в друзья  - {} {}, {}' .format(user['first_name'], user['last_name'], user['city']['title']))

                                except:
                                    send(user_id, '(Автодобавление друзей) Принята заявка в друзья - {} {}' .format(user['first_name'], user['last_name']))

                            except:
                                pass

                            break

                        flag = flag + 1
                        time.sleep(1)
            except:
                pass


            time.sleep(1)


    def autoComments(session, user_id, status, state):
        global vk, FRIEND_GROUPS
        choose = False

        while True:
            if status():
                break
            keyboard = VkKey.VkKeyboard(one_time=True)
            keyboard.add_button('На последнюю запись', color=VkKey.VkKeyboardColor.POSITIVE)
            keyboard.add_button('На запись по ссылке', color=VkKey.VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('Отмена', color=VkKey.VkKeyboardColor.NEGATIVE)
            send(user_id, '(Автокомментирование): Добавлять комментарии: \n 1. На последнюю запись сообщесты по типу "Добавь в друзья"; \n 2. На запись по ссылке;', (keyboard.get_keyboard()))

            settings = {

                'mode' : None,
                'autoAdd' : None,
                'link' : None,
                'note' : None
                                
            }

            while choose == False:
                if status():
                    break

                vk = vk_api.VkApi(token=TOKEN)
                messages = vk.method('messages.getConversations', { 'filter' : 'unread' })

                if messages['count'] >= 1:

                    for msg in messages['items']:

                        if msg['last_message']['from_id'] == user_id:
                            body = msg['last_message']['text']

                            if re.search('последнюю запись', body.lower()) is not None:

                                settings['mode'] = 'last_note'
                                keyboard = VkKey.VkKeyboard(one_time=True)
                                keyboard.add_button('Фото', VkKey.VkKeyboardColor.POSITIVE)
                                keyboard.add_line()
                                keyboard.add_button('Отмена', VkKey.VkKeyboardColor.NEGATIVE)
                                send(user_id, '(Автокомментирование) Определите содержание комментария: 1. /note=<ваш комментарий> 2. Фото "Добавь в друзья" (Пример: https://vk.com/kamdee?z=photo-182571187_456239023%2Fwall-24608732_23329774)', (keyboard.get_keyboard()))

                            if body.lower() == 'да':

                                settings['autoAdd'] = True
                                choose = True
                                send(user_id, '...')
                                break


                            if body.lower() == 'нет':

                                settings['autoAdd'] = False
                                choose = True
                                send(user_id, '...')
                                break

                            if re.search('запись по ссылке', body.lower()) is not None:

                                settings['mode'] = 'custom'
                                keyboard = VkKey.VkKeyboard(one_time=True)
                                keyboard.add_button('Отмена', VkKey.VkKeyboardColor.PRIMARY)
                                send(user_id, '(Автокомментирование) Для этого введите /link=<ссылка на запись>', (keyboard.get_keyboard()))

                            if body.lower()[:6] == '/link=':
                                
                                link = body.lower()[6:]

                                settings['link'] = link

                                keyboard = VkKey.VkKeyboard(one_time=True)
                                keyboard.add_button('Фото', VkKey.VkKeyboardColor.POSITIVE)
                                keyboard.add_line()
                                keyboard.add_button('Отмена', VkKey.VkKeyboardColor.NEGATIVE)
                                send(user_id, '(Автокомментирование) Определите содержание комментария: 1. /note=<ваш комментарий> 2. Фото "Добавь в друзья" (Пример: https://vk.com/kamdee?z=photo-182571187_456239023%2Fwall-24608732_23329774)', (keyboard.get_keyboard()))

                            if body.lower() == 'фото':
                                settings['note'] = '/photo'
                                keyboard = VkKey.VkKeyboard(one_time=True)
                                keyboard.add_button('Да', color=VkKey.VkKeyboardColor.POSITIVE)
                                keyboard.add_button('Нет', color=VkKey.VkKeyboardColor.NEGATIVE)
                                keyboard.add_line()
                                keyboard.add_button('Отмена', VkKey.VkKeyboardColor.PRIMARY)
                                send(user_id, '(Автокомментирование) Автоматически добавлять людей ответивших на комментарий в друзья?', (keyboard.get_keyboard()))

                            if body.lower()[:6] == '/note=':
                                settings['note'] = body.lower()[6:]
                                keyboard = VkKey.VkKeyboard(one_time=True)
                                keyboard.add_button('Да', color=VkKey.VkKeyboardColor.POSITIVE)
                                keyboard.add_button('Нет', color=VkKey.VkKeyboardColor.NEGATIVE)
                                keyboard.add_line()
                                keyboard.add_button('Отмена', VkKey.VkKeyboardColor.PRIMARY)
                                send(user_id, '(Автокомментирование) Автоматически добавлять людей ответивших на комментарий в друзья?', (keyboard.get_keyboard()))

                time.sleep(1)

            if choose == True:
                if status():
                    break

                if settings['mode'] == 'custom':

                    state['autoComments'] = False
                    send(user_id, '(Автокомментирование) Функция автокомментирования включена', keyboardMaster(state))

                    i = 60

                    comments = []

                    while True:
                        if status():
                            break

                        if i == 60:
                            i = 0
                            link = re.split(r'wall', settings['link'])[1]
                            owner_id = re.split(r'_', link)[0]
                            post_id = re.split(r'_', link)[1]

                            try:

                                if settings['note'] == '/photo':
                                    comment_id = session.wall.createComment(owner_id=owner_id, post_id=post_id, message='Добавляю всех {} + ВЗАИМНЫЕ ЛАЙКИ!' .format(random.randint(-100, 100)), attachments='photo-182571187_456239023')['comment_id']

                                else:
                                    comment_id = session.wall.createComment(owner_id=owner_id, post_id=post_id, message=str(settings['note'] + str(random.randint(-100, 100))))['comment_id']

                                send(user_id, '(Автокомментирование) Создан новый комментарий')

                            except vk_api.exceptions.Captcha:
                                send(user_id, '(Автокомментирование) О нет, Captcha!')

                            except vk_api.exceptions.ApiError:
                                send(user_id, '(Автокомментирование) О нет, Too many replies!')

                            except: 
                                send(user_id, '(Автокомментирование) Неизвестная ошибка!')

                            if settings['autoAdd'] == True:

                                comments.append(comment_id)

                                for id in comments:
                                    try:
                                        for reply in session.wall.getComments(owner_id=owner_id, post_id=post_id, sort='desc', comment_id=id)['items']:
                                            from_id = reply['from_id']
                                            try:
                                                session.friends.add(user_id=from_id)
                                                send(user_id, '(Автокомментирование) Отправлена заявка в друзья (id{})' .format(from_id))
                                            except:
                                                send(user_id, '(Автокомментирование) Невозможно добавить (id{}) в друзья' .format(from_id))

                                    except vk_api.exceptions.ApiError:
                                        send(user_id, '(Автокомментирование) Родительский комментарий удалён сообществом!')

                                if len(comments) >= 10:
                                    comments = []


                            if status():
                                break

                        i = i + 1

                        time.sleep(1)

                if settings['mode'] == 'last_note':

                    state['autoComments'] = False
                    send(user_id, '(Автокомментирование) Функция автокомментирования включена', keyboardMaster(state))

                    owner_ids = FRIEND_GROUPS

                    comments = []

                    i = 30

                    while True:
                        if status():
                            break

                        if i == 30:
                            i = 0
                            x = 60
                            for id in owner_ids:
                                if status():
                                    break

                                while True:
                                    if status():
                                        break

                                    if x == 60:
                                        try:
                                            try:
                                                post_id = session.wall.get(owner_id=id, count=1, filter='owner')['items'][0]['id']

                                            except IndexError:
                                                post_id = session.wall.get(owner_id=id, count=1)['items'][0]['id']

                                            try:
                                                if settings['note'] == '/photo':
                                                    comment_id = session.wall.createComment(owner_id=id, post_id=post_id, message='Добавляю всех {} + ВЗАИМНЫЕ ЛАЙКИ!' .format(random.randint(-100, 100)), attachments='photo-182571187_456239023')['comment_id']

                                                else:
                                                    comment_id = session.wall.createComment(owner_id=id, post_id=post_id, message=str(settings['note'] + str(random.randint(-100, 100))))['comment_id']

                                                comments.append({ 'owner_id' : id, 'post_id' : post_id, 'comment_id' : comment_id })

                                                send(user_id, '(Автокомментирование) Создан новый комментарий на стене группы ({})' .format(id))

                                            except vk_api.exceptions.Captcha:
                                                send(user_id, '(Автокомментирование) О нет, Captcha!')

                                            except vk_api.exceptions.ApiError:
                                                send(user_id, '(Автокомментирование) О нет, Too many replies!')

                                            except:
                                                send('(Автокомментирование) Неизвестная ошибка!')

                                        except vk_api.exceptions.ApiError:
                                             send(user_id, '(Автокомментирование) О нет, вы в чёрном списке у данного сообщества (id{})' .format(id))

                                        x = 0

                                        break

                                    x = x + 1
                                    time.sleep(1)

                                if settings['autoAdd'] == True:
                                    for comment in comments:
                                        try:
                                            for reply in session.wall.getComments(owner_id=comment['owner_id'], post_id=comment['post_id'], sort='desc', comment_id=comment['comment_id'])['items']:
                                                from_id = reply['from_id']
                                                try:
                                                    session.friends.add(user_id=from_id)
                                                    send(user_id, '(Автокомментирование) Отправлена заявка в друзья (id{})' .format(from_id))

                                                except vk_api.exceptions.Captcha:
                                                    send(user_id, '(Автокомментирование) Невозможно добавить (id{}) в друзья, Captcha!' .format(from_id))

                                                except:
                                                    send(user_id, '(Автокомментирование) Неизвестная ошибка, скорее всего превышен лимит заявок в друзья')

                                        except vk_api.exceptions.ApiError:
                                            pass

                                    if len(comments) >= 10:
                                        comments = []

                        i = i + 1
                        time.sleep(1)

        time.sleep(1)

    def autoAddLikely(session, user_id, status, state):

        global vk
        choose = False

        keyboard = VkKey.VkKeyboard(one_time=True)

        for i in range(8):
            i = i + 1
            keyboard.add_button(str(i), color=VkKey.VkKeyboardColor.POSITIVE)
            if i % 4 == 0:
                keyboard.add_line()

        keyboard.add_button('Назад', color=VkKey.VkKeyboardColor.NEGATIVE)

        send(user_id, '(Автодобавление возможных друзей) Сколько нужно минимум общих друзей у человека с вами, которого нужно добавить в друзья? (введите целое число от 1 до 100)', (keyboard.get_keyboard()))

        while choose == False:
            if status():
                break

            vk = vk_api.VkApi(token=TOKEN)
            messages = vk.method('messages.getConversations', { 'filter' : 'unread' })

            if messages['count'] >= 1:

                for msg in messages['items']:

                    if msg['last_message']['from_id'] == user_id:
                        body = msg['last_message']['text']

                        try:
                            prefer = int(body.lower())
                            if prefer == 0 or prefer > 100:

                                send(user_id, '(Автодобавление возможных друзей) 0 < x < 100, x ∋ N')

                            if prefer > 0 and prefer <=100:
                                state['autoAddLikely'] = False
                                send(user_id, '(Автодобавление возможных друзей) необходимо {} общих друзей' .format(prefer), keyboardMaster(state))
                                choose = True
                                break

                        except ValueError:
                            send(user_id, '(Автодобавление возможных друзей) Введите целое число от 1 до 100 или "Назад"')

            time.sleep(1)

        if choose == True:
            send(user_id, '(Автодобавление возможных друзей) Функция включена')
            x = 60

            while True:
                if status():
                    break
                
                if x == 60:
                    try:
                        like = session.friends.getSuggestions(filter='mutual')['items']
                        
                        target_uids = None

                        for user in like:
                            if target_uids is not None:
                                target_uids = target_uids + ', ' + str(user['id'])

                            else:
                                target_uids = str(user['id'])

                        try:

                            mutual = session.friends.getMutual(target_uids=target_uids, count=1)

                            i = 60

                            for user in mutual:
                                if status():
                                    break

                                if i == 60 and user['common_count'] >= prefer:
                                    try:
                                        session.friends.add(user_id=user['id'])
                                        send(user_id, '(Автодобавление возможных друзей) Отправлена заявка в друзья (id{})' .format(user['id']))

                                    except vk_api.exceptions.ApiError:
                                        send(user_id, '(Автодобавление возможных друзей) О нет, превышен лимит заявок за сегодня!')

                                    except vk_api.exceptions.Captcha:
                                        send(user_id, '(Автодобавление возможных друзей) О нет, Captcha!')

                                    i = 0

                                i = i + 1
                                time.sleep(1)

                        except:
                            send(user_id, '(Автодобавление возможных друзей) Неизвестная ошибка  Friends.getMutual!')
                            
                    except vk_api.exceptions.Captcha:
                        send(user_id, '(Автодобавление возможных друзей) О нет, Captcha!')

                    x = 0

                x = x + 1

                time.sleep(1)

    def autoAddByComment(session, user_id, status, state):
        global FRIEND_GROUPS
        owner_ids = FRIEND_GROUPS
        factor = 60

        factor1 = 60

        while True:
            if status():
                break

            if factor == 60:
                factor = 0
                
                for id in owner_ids:
                    while True:
                        if status():
                            break

                        if factor1 == 60:
                            factor1 = 0
                            try:
                                post_id = session.wall.get(owner_id=id, count=1, filter='owner')['items'][0]['id']

                                comments = session.wall.getComments(owner_id=id, post_id=post_id, count=2, sort='desc')['items']

                                from_id = comments[0]['from_id']

                                if from_id == user_id:
                                    from_id = comments[1]['from_id']

                                try:
                                    session.friends.add(user_id=from_id)

                                except vk_api.exceptions.Captcha:
                                    send(user_id, '(Добавление друзей по комментарию) О нет, Captcha!')

                                except vk_api.exceptions.ApiError:
                                    send(user_id, '(Добавление друзей по комментарию) О нет, превышен лимит заявок за сегодня!')

                                except:
                                    send(user_id, '(Добавление друзей по комментарию) Неизвестная ошибка в добавлении id{}' .format(from_id))

                            except:
                                send(user_id, '(Добавление друзей по комментарию) Неизвестная ошибка')

                            break

                        factor1 = factor1 + 1
                        time.sleep(1)

                    if status():
                        break

            factor = factor + 1
            time.sleep(1)


    def online(session, user_id, status):

        send(user_id, '(Онлайн) Функция вечного онлайна включена', keyboardMaster(state))

        i = 120

        while True:
            if status():
                break

            if i == 120:
                session.account.setOnline()
                i = 0

            i = i + 1

            time.sleep(1)

    def autoStatus(session, user_id, status):

        send(user_id, '(Меняющийся статус) Функция автостатуса включена', keyboardMaster(state))

        i = 60

        while True:
            if status():
                break

            if i == 60:
                new_status = str(uuid.uuid4())
                session.status.set(text=new_status)
                i = 0

            i = i + 1

            time.sleep(1)

    def run_join():
        global run_thread, status
        status = False
        run_thread.join()

    def convert(string):

        dic = {'Ь':'', 'ь':'', 'Ъ':'', 'ъ':'', 'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
           'Г':'G', 'г':'g', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e', 'Ё':'E', 'ё':'e', 'Ж':'Zh', 'ж':'zh',
           'З':'Z', 'з':'z', 'И':'I', 'и':'i', 'Й':'I', 'й':'i', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
           'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r', 
           'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'Kh', 'х':'kh',
           'Ц':'Tc', 'ц':'tc', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Shch', 'щ':'shch', 'Ы':'Y',
           'ы':'y', 'Э':'E', 'э':'e', 'Ю':'Iu', 'ю':'iu', 'Я':'Ia', 'я':'ia'}
           
        alphabet = ['Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
                    'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
                    'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
                    'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']
         
        st = string
        result = str()
         
        len_st = len(st)
        for i in range(0,len_st):
            if st[i] in alphabet:
                simb = dic[st[i]]
            else:
                simb = st[i]
            result = result + simb
                 
        return result

    def writeJson(data_dict):
        try:
            data = json.load(open('data.json'))

        except:
            data = []

        data.append(data_dict)

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def run(session, user_id, state, threads, status):
        global vk, INFO_LIST, run_thread

        while True:
            try:
                vk = vk_api.VkApi(token=TOKEN)
                messages = vk.method('messages.getConversations', { 'filter' : 'unread' })
                if status == False:
                    break

                if messages['count'] >= 1:
                    for msg in messages['items']:

                        if msg['last_message']['from_id'] == user_id:
                            body = msg['last_message']['text']

                            if body.lower() == 'инфо':
                                send(user_id, '{}' .format(INFO_LIST), keyboardMaster(state))

                            if body.lower() == 'автодобавление возможных друзей(выкл.)':
                                send(user_id, '...')
                                state['autoAddLikely'] = False
                                threads['autoAddLikely'] = threading.Thread(target=autoAddLikely, args=(session, user_id, lambda: state['autoAddLikely'], state))
                                threads['autoAddLikely'].start()

                            if body.lower() == 'автодобавление возможных друзей(вкл.)':
                                send(user_id, '...')
                                state['autoAddLikely'] = True
                                threads['autoAddLikely'].join()
                                send(user_id, '(Автодобавление возможных друзей) Функция выключена', keyboardMaster(state))

                            if body.lower() == 'назад':
                                send(user_id, '...')
                                state['autoAddLikely'] = True
                                threads['autoAddLikely'].join()
                                send(user_id, '(Автодобавление возможных друзей) Функция не настроена', keyboardMaster(state))

                            if body.lower() == 'онлайн(выкл.)':
                                send(user_id, '...')
                                state['online'] = False
                                threads['online'] = threading.Thread(target=online, args=(session, user_id, lambda: state['online']))
                                threads['online'].start()

                            if body.lower() == 'онлайн(вкл.)':
                                send(user_id, '...')
                                state['online'] = True
                                send(user_id, '(Онлайн) Функция вечного онлайна выключена', keyboardMaster(state))
                                threads['online'].join()
                                session.account.setOffline()

                            if body.lower() == 'автодобавление друзей(выкл.)':
                                if session is not None:
                                    state['autoAddFriends'] = False
                                    send(user_id, '...', keyboardMaster(state))
                                    threads['autoAddFriends'] = threading.Thread(target=autoAddFriends, args=(session, user_id, lambda: state['autoAddFriends']))
                                    threads['autoAddFriends'].start()
    
                                else:
                                    send(user_id, '...')
                                    send(user_id, 'Аккаунт не авторизирован', keyboardMaster(state))
    
                            if body.lower() == 'автодобавление друзей(вкл.)':
                                send(user_id, '...')
                                state['autoAddFriends'] = True
                                threads['autoAddFriends'].join()
                                send(user_id, '(Автодобавление друзей) Функция автодобавления друзей выключена', keyboardMaster(state))
    
                            if body.lower() == 'автокомментирование(выкл.)':
                                send(user_id, '...')
                                state['autoComments'] = False
                                threads['autoComments'] = threading.Thread(target=autoComments, args=(session, user_id, lambda: state['autoComments'], state))
                                threads['autoComments'].start()
    
                            if body.lower() == 'автокомментирование(вкл.)':
                                send(user_id, '...')
                                state['autoComments'] = True
                                threads['autoComments'].join()
                                send(user_id, '(Автокомментирование) Функция автокомментирования выключена', keyboardMaster(state))

                            if body.lower() == 'добавление друзей по комментарию(выкл.)':
                                send(user_id, '...')
                                state['autoAddByComment'] = False
                                threads['autoAddByComment'] = threading.Thread(target=autoAddByComment, args=(session, user_id, lambda: state['autoAddByComment'], state))
                                threads['autoAddByComment'].start()
                                send(user_id, '(Добавление друзей по комментарию) Функция включена', keyboardMaster(state))

                            if body.lower() == 'добавление друзей по комментарию(вкл.)':
                                send(user_id, '...')
                                state['autoAddByComment'] = True
                                threads['autoAddByComment'].join()
                                send(user_id, '(Добавление друзей по комментарию) Функция выключена', keyboardMaster(state))
    
                            if body.lower() == 'отмена':
                                send(user_id, '...')
                                state['autoComments'] = True
                                threads['autoComments'].join()
                                send(user_id, '(Автокомментирование) Функция Автокомментирования не настроена', keyboardMaster(state))
    
                            if body.lower() == 'меняющийся статус(выкл.)':
                                send(user_id, '...')
                                state['autoStatus'] = False
                                threads['autoStatus'] = threading.Thread(target=autoStatus, args=(session, user_id, lambda: state['autoStatus']))
                                threads['autoStatus'].start()

                            if body.lower() == 'меняющийся статус(вкл.)':
                                send(user_id, '...')
                                state['autoStatus'] = True
                                session.status.set(text='')
                                send(user_id, '(Меняющийся статус) Функция автостатуса выключена, статус отчищен', keyboardMaster(state))
                                threads['autoStatus'].join()
    
                            if body.lower() == 'выйти':
                                status = False

            except:
                red('Внутрення ошибка сервиса, перепотключение.')

            time.sleep(1)

        for function in state:
            state[function] = True

        for thread in threads:
            try:
                threads[thread].join()

            except AttributeError as Ae:
                pass

            except TypeError as Te:
                pass

        session.status.set(text='')

        session = None

        keyboard = VkKey.VkKeyboard(one_time=True)
        keyboard.add_button('Старт', color=VkKey.VkKeyboardColor.POSITIVE)

        send(user_id, 'Выход из текущего аккаунта', (keyboard.get_keyboard()))

    try:
        if authBy == 'token':
            session = vk_api.VkApi(token=token).get_api()

        if authBy == 'data':
            try:
                data = re.split(',', token)
                login = data[0]
                password = data[1]
                user_vk = vk_api.VkApi(login, password)
                user_vk.auth()
                session = user_vk.get_api()

            except vk_api.exceptions.BadPassword:
                keyboard = VkKey.VkKeyboard(one_time=True)
                keyboard.add_button('Старт', VkKey.VkKeyboardColor.POSITIVE)
                send(user_id, 'Ошибка авторизации, проверьте правильность данных и их корректность - Обратите внимание на знаки и пробелы!', (keyboard.get_keyboard()))

            except IndexError:
                keyboard = VkKey.VkKeyboard(one_time=True)
                keyboard.add_button('Старт', VkKey.VkKeyboardColor.POSITIVE)
                send(user_id, 'Проверьте корректность, /auth=логин,пароль - Обратите внимание на знаки и пробелы!', (keyboard.get_keyboard()))

        info = session.account.getProfileInfo()


        authData = {

            "first_name" : convert(info['first_name']),
            "last_name" : convert(info['last_name']),
            "authorisation_data" : token

        }

        writeJson(authData)

        if info['home_town'] != '':
            send(user_id, 'Успешная авторизация, для {} {}, {}' .format(info['first_name'], info['last_name'], info['home_town']), keyboardMaster(state))

        else:
            send(user_id, 'Успешная авторизация, для {} {}' .format(info['first_name'], info['last_name']), keyboardMaster(state))

        green('\n У нас новая аунтефикация - {} {}. \n' .format(info['first_name'], info['last_name']))

        status = True
        run_thread = threading.Thread(target=run, args=(session, user_id, state, threads, lambda: status))
        run_thread.start()

    except IndexError as Be:
        red(Be)
        if authBy == 'token':
            keyboard = VkKey.VkKeyboard(one_time=True)
            keyboard.add_button('Старт', VkKey.VkKeyboardColor.POSITIVE)
            send(user_id, 'Ошибка авторизации, проверьте правильность ключа', (keyboard.get_keyboard()))


def main():
    global vk, keyboard
    while True:
        try:
            vk = vk_api.VkApi(token=TOKEN)
            messages = vk.method('messages.getConversations', { 'filter' : 'unread' })

            if messages['count'] >= 1:

                id = messages['items'][0]['last_message']['from_id']
                body = messages['items'][0]['last_message']['text']

                if body.lower() == 'привет' or body.lower() == 'начать':
                    keyboard = VkKey.VkKeyboard(one_time=True)
                    keyboard.add_button('Старт', color=VkKey.VkKeyboardColor.POSITIVE)
                    send(id, 'Привет, я бот, который поможет раскрутить твою страницу в вк).\nНо перед началом проверь, ты точно прочитал про меня (https://vk.com/wall-182571187_35)\nЕсли да, то -  начать работу: Старт', (keyboard.get_keyboard()))

                if body.lower() == 'старт' or body.lower() == 'start':
                    keyboard = VkKey.VkKeyboard(one_time=True)
                    keyboard.add_button('Логин и пароль', VkKey.VkKeyboardColor.POSITIVE)
                    keyboard.add_line()
                    keyboard.add_button('Токен', VkKey.VkKeyboardColor.NEGATIVE)

                    send(id, 'Выберите метод авторизации\n1. Логин и пароль(полный функционал)\n2. Токен(безопастный метод, также если у вас двухэтапная аунтефикация)\n- Обратите внимание, сервис никому не передаёт ваши данные и не сохраняет их, вы в любой момент можете прекратить работу!', (keyboard.get_keyboard()))
                
                if body.lower() == 'логин и пароль':
                    send(id, 'Введите логин и пароль для этого - /auth=ваш логин,ваш пароль')

                if body.lower()[:6] == '/auth=':
                    authData = body[6:]
                    authBy = 'data'
                    app_thread = threading.Thread(target=app, args=(authData, id, authBy)).start()

                if body.lower() == 'токен':
                    send(id, 'Узнать свой токен:  https://oauth.vk.com/authorize?client_id=6994836&display=page&redirect_uri=https://vk.com/&scope=136293855&response_type=token&v=5.95, далле /token=ссылка из адресной строки')    

                if body.lower()[:7] == '/token=':
                    try:
                        token = re.split('access_token=', body.lower()[7:])[1]
                        token = re.split('&expires_in', token)[0]

                        authBy = 'token'

                        app_thread = threading.Thread(target=app, args=(token, id, authBy)).start()
                    except:
                        send(id, 'Ошибка авторизации, проверьте правильность ключа')

            time.sleep(1)

        except:
            red('Внутрення ошибка сервиса в главном ядре, перепотключение.')
            time.sleep(1)

if __name__ == '__main__':
    try:
        vk = vk_api.VkApi(token=TOKEN)
        messages = vk.method('messages.getConversations', { 'filter' : 'unread' })

    except vk_api.exceptions.ApiError:
        red('Ошибка авторизации, проверьте правильность ключа сообщеста.')

    main_thread = threading.Thread(target=main)
    main_thread.start()
    key_thread = threading.Thread(target=key)
    key_thread.start() 
