# README

## 初回起動
```
$ docker compose build

```

## 起動
```
$ docker compose up -d
```
http://0.0.0.0:3030

## test
set breakpoint

```
breakpoint()
```

run
```
$ docker exec -it oroshi_api bash
$ pytest test_app.py --pdb
```