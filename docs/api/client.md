# Client

`HelldiveAPIClient` is the main entry point. Instantiate it with your app name and contact info, then access data through its module attributes (`client.planets`, `client.assignments`, etc.).

Use it as a context manager to ensure the underlying HTTP connection is closed cleanly:

```python
with HelldiveAPIClient(client="myapp", contact="me@example.com") as client:
    war = client.war.get()
```

::: helldivepy.client.HelldiveAPIClient
