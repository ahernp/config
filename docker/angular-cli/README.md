## Usage

1. Build container: `docker build -t angular-cli .`
2. `cd` to directory containing application source code.
3. Run container: `docker run -it --rm --name angular-cli -v "$PWD":/app
   angular-cli:latest bash`
3. Issue `ng`, `node` and `npm` commands for application.

