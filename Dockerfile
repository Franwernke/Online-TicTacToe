FROM gcc as base

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . ./

FROM python:3.9


WORKDIR /usr/src/app

ENV PORT=8000

COPY --from=base ./ ./

EXPOSE $PORT

CMD python3 server/main.py ${PORT}
