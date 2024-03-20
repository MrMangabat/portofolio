#portofolio

--- Pydantic ---
learn it


--- fastapi ---
uvicorn main:app --reload




--- PostgreSQL ---
https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database
sudo service postgresql status
sudo service postgr
sudo -u postgres psql start
sudo service postgresql stop
\c bumstuff_database

hostname: mangabat
port: 5432
serverhost / socket: "/var/run/psotgresql"
database name : bumstuff_database
access db: psql dbname = bumstuff_database

Start MySQL Server / check status: systemctl status mysql
To see what databases you have available, in the MySQL prompt, enter: SHOW DATABASES;

'''


## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

