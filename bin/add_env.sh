#!/bin/bash

read -p "Django Secret Key: " django_secret_key
read -p "Django Debug: " django_debug
read -p "Django Allowed Host: " allowed_hosts
read -p "Vk Bot Group Secret Key (VkApi Token): " bot_secret_group_key
read -p "Vk Bot Info Message: " bot_info_message

read -p "Do you want to overwrite .env file? [Y/n]: " agre

if [[ "$agre" == Y || "$agre" == y ]]
then
{
    echo DJANGO_SECRET_KEY=$django_secret_key
    echo DJANGO_DEBUG=$django_debug
    echo DJANGO_ALLOWED_HOSTS=$allowed_hosts
    echo BOT_SECRET_GROUP_KEY=$bot_secret_group_key
    echo BOT_INFO_MESSAGE=$bot_info_message
} > .env

echo "Wrotten Successfuly"

else

echo "Operation cancelled"

fi
