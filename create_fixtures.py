import asyncio
import json
from sqlalchemy import delete, select

from app.container import DATABASE_URL
from core.db.models import Activity, Building, Organisation
from core.session import Database


async def create_fixtures():
    """Создание тестовых данных в базе"""
    database = Database(db_url=DATABASE_URL)
    async with database.session() as db:
        try:
            # Дропаем все модели
            stmt = delete(Building)
            await db.execute(stmt)
            stmt = delete(Activity)
            await db.execute(stmt)
            stmt = delete(Organisation)
            await db.execute(stmt)
            await db.commit()

            # Создание видов деятельности (дерево до 3 уровней)
            activities_data = [
                # Уровень 1
                {"id": 1, "title": "Еда", "parent_id": None},
                {"id": 2, "title": "Автомобили", "parent_id": None},
                {"id": 3, "title": "Одежда", "parent_id": None},

                # Уровень 2 - Еда
                {"id": 4, "title": "Мясная продукция", "parent_id": 1},
                {"id": 5, "title": "Молочная продукция", "parent_id": 1},
                {"id": 6, "title": "Бакалея", "parent_id": 1},

                # Уровень 2 - Автомобили
                {"id": 7, "title": "Грузовые", "parent_id": 2},
                {"id": 8, "title": "Легковые", "parent_id": 2},
                {"id": 9, "title": "Мотоциклы", "parent_id": 2},

                # Уровень 2 - Одежда
                {"id": 10, "title": "Мужская", "parent_id": 3},
                {"id": 11, "title": "Женская", "parent_id": 3},
                {"id": 12, "title": "Детская", "parent_id": 3},

                # Уровень 3 - Легковые
                {"id": 13, "title": "Запчасти", "parent_id": 8},
                {"id": 14, "title": "Аксессуары", "parent_id": 8},
                {"id": 15, "title": "Шины", "parent_id": 8},

                # Уровень 3 - Молочная продукция
                {"id": 16, "title": "Сыры", "parent_id": 5},
                {"id": 17, "title": "Йогурты", "parent_id": 5},
                {"id": 18, "title": "Молоко", "parent_id": 5},
            ]

            for activity_data in activities_data:
                activity = Activity(**activity_data)
                db.add(activity)

            buildings_data = [
                {
                    "id": 1,
                    "address": "г. Москва, ул. Ленина 1, офис 3",
                    "latitude": 55.7558,
                    "longitude": 37.6173
                },
                {
                    "id": 2,
                    "address": "г. Санкт-Петербург, Невский пр. 28",
                    "latitude": 59.9343,
                    "longitude": 30.3351
                },
                {
                    "id": 3,
                    "address": "г. Новосибирск, ул. Советская 20",
                    "latitude": 55.0084,
                    "longitude": 82.9357
                },
                {
                    "id": 4,
                    "address": "г. Екатеринбург, ул. Мамина-Сибиряка 145",
                    "latitude": 56.8389,
                    "longitude": 60.6057
                },
                {
                    "id": 5,
                    "address": "г. Казань, ул. Баумана 35",
                    "latitude": 55.7903,
                    "longitude": 49.1347
                },
                {
                    "id": 6,
                    "address": "г. Сочи, ул. Навагинская 15",
                    "latitude": 43.5855,
                    "longitude": 39.7231
                }
            ]

            for building_data in buildings_data:
                building = Building(**building_data)
                db.add(building)

            await db.commit()

            # Создание организаций
            organizations_data = [
                {
                    "title": "ООО 'Рога и Копыта'",
                    "phone": "8-923-666-13-13",
                    "building_id": 1,
                    "activity_ids": [4, 5]  # Мясная и молочная продукция
                },
                {
                    "title": "Автоцентр 'Мир колес'",
                    "phone": "8-912-345-67-89",
                    "building_id": 2,
                    "activity_ids": [8, 13, 15]  # Легковые, запчасти, шины
                },
                {
                    "title": "Грузоперевозки 'СибирьТранс'",
                    "phone": "5-555-555",
                    "building_id": 3,
                    "activity_ids": [7]  # Грузовые
                },
                {
                    "title": "Молочная ферма 'Уральская'",
                    "phone": "8-922-111-22-33",
                    "building_id": 4,
                    "activity_ids": [5, 16, 18]  # Молочная продукция, сыры, молоко
                },
                {
                    "title": "Мясной цех 'Татарстан'",
                    "phone": "7-777-777",
                    "building_id": 5,
                    "activity_ids": [4]  # Мясная продукция
                },
                {
                    "title": "Автозапчасти 'ЮгАвто'",
                    "phone": "8-913-444-55-66",
                    "building_id": 6,
                    "activity_ids": [13, 14]  # Запчасти, аксессуары
                },
                {
                    "title": "Супермаркет 'Продукты 24/7'",
                    "phone": "9-999-999",
                    "building_id": 1,
                    "activity_ids": [1, 4, 5, 6]  # Еда и все подкатегории
                },
                {
                    "title": "Автосалон 'Престиж'",
                    "phone": "8-925-777-88-99",
                    "building_id": 2,
                    "activity_ids": [8, 14]  # Легковые, аксессуары
                },
                {
                    "title": "Одежда 'Стиль'",
                    "phone": "2-123-456",
                    "building_id": 3,
                    "activity_ids": [10, 11]  # Мужская и женская одежда
                }
            ]

            for org_data in organizations_data:
                phone_json = json.dumps(org_data["phone"])

                organization = Organisation(
                    title=org_data["title"],
                    phone=phone_json,
                    building_id=org_data["building_id"]
                )

                stmt = select(Activity).where(Activity.id.in_(org_data["activity_ids"]))
                result = await db.execute(stmt)
                activities = result.scalars().all()

                organization.activities = activities
                db.add(organization)

            await db.commit()
            print('=' * 60)
            print("фикстуры созданы")
            print(
                f"Создано: {len(activities_data)} деятельностей, {len(buildings_data)} зданий, {len(organizations_data)} организаций"
            )
            print('=' * 60)
            await db.close()
        except Exception as e:
            await db.rollback()
            print(f"Ошибка при создании фикстур: {e}")
            raise
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(create_fixtures())
