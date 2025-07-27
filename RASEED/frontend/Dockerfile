FROM node:20-alpine as build
WORKDIR /app
ARG _REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=${_REACT_APP_BACKEND_URL}
COPY package.json package-lock.json* ./
RUN npm install || yarn install
COPY . .
RUN echo "REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL" > .env
RUN npm run build || yarn build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]