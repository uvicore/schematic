# Welcome

Welcome to your new uvicore application or library!

Visit https://uvicore.io for the docs!


## The CLI

After starting your preferred virtual environment and installing dependencies...

```bash
./uvicore
./uvicore appstub welcome
```


## Web and API

Assuming you chose the `web` extras

```bash
# Still in your virtual environment
./uvicore http routes
./uvicore http serve
```

- Visit http://127.0.0.1:5000
- Visit http://127.0.0.1:5000/api/docs
- Try `curl http://127.0.0.1:5000/api/welcome`


## Benchmarks?

Lets see how fast uvicore is!

Install https://github.com/wg/wrk on your os

```bash
# Still in your virtual environment
./serve-gunicorn
```

In another terminal

```bash
curl http://127.0.0.1:5000/api/welcome
wrk -c50 -t8 -d10 http://127.0.0.1:5000/api/welcome
```

40,000 requests a second, pretty good for a hello world!  Thanks [FastAPI](https://github.com/fastapi/fastapi)!
```
Running 10s test @ http://127.0.0.1:5000/api/welcome
  8 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.23ms  354.23us  10.40ms   69.95%
    Req/Sec     4.92k   432.18     6.15k    65.30%
  394740 requests in 10.10s, 57.97MB read
Requests/sec:  39083.14
Transfer/sec:      5.74MB
```

What about [Starlette](https://github.com/encode/starlette) with our Welcome [Jinja](https://github.com/pallets/jinja) templates?

```bash
curl http://127.0.0.1:5000/api/welcome
wrk -c50 -t8 -d10 http://127.0.0.1:5000/api/welcome
```

Wow 44,000 requests a second! [Starlette](https://github.com/encode/starlette) is blazing fast!

```
Running 10s test @ http://127.0.0.1:5000
  8 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.11ms  348.15us  12.08ms   72.46%
    Req/Sec     5.44k   664.22     7.26k    66.91%
  436883 requests in 10.10s, 0.85GB read
Requests/sec:  43255.92
Transfer/sec:     86.30MB
```
