---
icon: material/download
---
# ⚙️ Installation

To install **Helldive.py**, just use pip, poetry or uv:

```bash
pip install helldivepy
poetry add helldvivepy
uv add helldivepy
```

Example code:

```py
from helldivepy import ApiClient

client = ApiClient(
    user_agent="Hello-World",
    user_contact="example@example.com | discord:exampleuser123",
)

print(client.get_war_info())
```
