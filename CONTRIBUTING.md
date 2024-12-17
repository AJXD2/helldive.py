# Contributing

Thanks for wanting to help make this project better! 🛠️

1. Fork the repo and clone it locally.
2. [Optional] [Run local instance of APIs](#run-local-instance-of-apis)
3. Create a branch: `git checkout -b feature/<name>`  
4. Push your branch and submit a PR.  
5. Keep it clean and follow code style guidelines.  

## Run local instance of APIs
Run local versions of the APIs to avoid rate limiting from the hosted versions.

### [Community API](https://github.com/helldivers-2/api)

1. Clone the repo and cd into it.

   ```sh
   git clone --recurse-submodules https://github.com/helldivers-2/api
   cd api
   ```

2. Edit the `src\Helldivers-2-API\appsettings.json` to your likig. Make sure you set the `ValidAudiences` to `["*"]` or else you will have problems. [More info](https://github.com/helldivers-2/api/blob/master/docs/containers.md#configuring-api-keys-for-the-self-hosted-version)

   ```json
    {
      "Helldivers": {
        "API": {
          "RateLimit": 5,
          "RateLimitWindow": 10,
          "Blacklist": "",
          "Authentication": {
            "Enabled": false,
            "ValidIssuers": [],
            "ValidAudiences": ["*"]
          }
        }
      }
    }
   ```

3. Build the image.

   ```sh
    docker build -f ./src/Helldivers-2-API/Dockerfile -t helldivers2-api .
   ```

4. Run

    ```sh
    docker compose up -d helldivers-api 
    ```

### [DiveHarder](https://github.com/helldivers-2/api)

1. Clone the repo and cd into it.

    ```sh
    git clone https://github.com/helldivers-2/diveharder_api.py
    cd diveharder_api.py
    ```

2. Build image

    ```sh
    docker build . -t diveharder-api.py
    ```

3. Run

    ```sh
    docker compose up -d diveharder-api
    ```
Report bugs and feature requests by opening an issue.  
