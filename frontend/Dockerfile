FROM node:24-alpine

RUN npm install -g @vue/cli

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run dev && rm -rf node_modules

EXPOSE 8080

# CMD ["npm", "run", "dev"]
