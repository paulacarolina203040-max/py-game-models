import json
from pathlib import Path
from db.models import Guild
from db.models import Player
from db.models import Race
from db.models import Skill
import init_django_orm  # noqa: F401


def main() -> None:
    Player.objects.all().delete()
    Guild.objects.all().delete()
    Skill.objects.all().delete()
    Race.objects.all().delete()

    base_dir = Path(__file__).resolve().parent
    json_path = base_dir / "players.json"

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for race_data in data.get("races", []):
        Race.objects.create(
            name=race_data["name"],
            description=race_data["description"]
        )

    for guild_data in data.get("guilds", []):
        Guild.objects.create(
            name=guild_data["name"],
            description=guild_data.get(
                "description"
            )
        )

    for skill_data in data.get("skills", []):
        race_obj = Race.objects.get(
            name=skill_data["race"]
        )
        Skill.objects.create(
            name=skill_data["name"],
            description=skill_data["description"],
            race=race_obj
        )

    for player_data in data.get("players", []):
        race_obj = Race.objects.get(
            name=player_data["race"]
        )
        guild_name = player_data.get("guild")
        guild_obj = (
            Guild.objects.get(name=guild_name)
            if guild_name else None
        )

        player = Player.objects.create(
            nickname=player_data["nickname"],
            email=player_data["email"],
            bio=player_data["bio"],
            race=race_obj,
            guild=guild_obj
        )

        if "skills" in player_data:
            for skill_name in player_data["skills"]:
                skill_obj = Skill.objects.get(
                    name=skill_name,
                    race=race_obj
                )
                player.skills.add(skill_obj)


if __name__ == "__main__":
    main()
