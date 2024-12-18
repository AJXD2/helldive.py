---
icon: material/download
---
# 🚀 Get Started

## ⚙️ Installation

=== "Pip"

    ```sh
    pip install helldivepy
    ```
=== "Poetry"
    ??? note "Poetry"
        Install poetry [here](https://python-poetry.org/docs/#installation).
    ```sh
    poetry add helldivepy
    ```

=== "UV"
    ??? note "UV"
        Install UV [here](https://docs.astral.sh/uv/getting-started/installation/).

    ```sh
    uv add helldivepy
    ```

Example code

=== "Without Rich"

    ```py
    from helldivepy import ApiClient
    client = ApiClient(
        user_agent="Hello-World",
        user_contact="example@example.com | discord:exampleuser123",
    )

    print(client.get_war_info().model_dump())
    >>>
        {
            'started': datetime.datetime(2024, 1, 23, 20, 5, 13, tzinfo=TzInfo(UTC)),
            'ended': datetime.datetime(2028, 2, 8, 20, 4, 55, tzinfo=TzInfo(UTC)),
            'now': datetime.datetime(1970, 11, 6, 14, 59, 50, tzinfo=TzInfo(UTC)),
            'client_version': '0.3.0',
            'factions': ['Humans', 'Terminids', 'Automaton', 'Illuminate'],
            'impact_multiplier': 0.034382936,
            'statistics': {
                'missions_won': 370390368,
                'missions_lost': 37224925,
                'mission_time': 1047433682627,
                'terminid_kills': 79906866134,
                'automaton_kills': 31552895947,
                'illuminate_kills': 3705435035,
                'bullets_fired': 571067857117,
                'bullets_hit': 645369797775,
                'time_played': 1047433682627,
                'deaths': 2564546790,
                'revives': 2,
                'friendlies': 361359530,
                'mission_success_rate': 90.0,
                'accuracy': 100,
                'player_count': 111316
            }
        }

    ```

=== "With rich"

    ```py
    from helldivepy import ApiClient
    from rich import print

    client = ApiClient(
        user_agent="Hello-World",
        user_contact="example@example.com | discord:exampleuser123",
    )

    print(client.get_war_info())
    >>> WarInfo(
        started=datetime.datetime(2024, 1, 23, 20, 5, 13, tzinfo=TzInfo(UTC)),
        ended=datetime.datetime(2028, 2, 8, 20, 4, 55, tzinfo=TzInfo(UTC)),
        now=datetime.datetime(1970, 11, 6, 14, 24, 40, tzinfo=TzInfo(UTC)),
        client_version='0.3.0',
        factions=['Humans', 'Terminids', 'Automaton', 'Illuminate'],
        impact_multiplier=0.03595309,
        statistics=Statistics(
            missions_won=370353637,
            missions_lost=37219878,
            mission_time=1047300170684,
            terminid_kills=79904593412,
            automaton_kills=31551843355,
            illuminate_kills=3687632552,
            bullets_fired=570972530827,
            bullets_hit=645273266867,
            time_played=1047300170684,
            deaths=2564288334,
            revives=2,
            friendlies=361317130,
            mission_success_rate=90.0,
            accuracy=100,
            player_count=102995
        )
    )
    ```
