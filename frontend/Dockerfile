FROM node:14-alpine

RUN npm install -g @vue/cli

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run dev

EXPOSE 8080

CMD ["npm", "run", "dev"]
