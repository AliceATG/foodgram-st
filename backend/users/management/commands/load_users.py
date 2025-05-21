import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User


class Command(BaseCommand):
    help = "Загрузка пользователей из JSON в базу данных"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, "data", "users.json")

        if not os.path.exists(file_path):
            self.stderr.write(f"Файл {file_path} не найден.")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            message = (
                f"""Загружены пользователи:
                {len(User.objects.bulk_create(
                    Command.create_user(**item) for item in json.load(file)
                ))}"""
            )

        self.stdout.write(self.style.SUCCESS(message))

    @staticmethod
    def create_user(**kwargs):
        user = User(**kwargs)
        user.set_password(kwargs['password'])
        return user
