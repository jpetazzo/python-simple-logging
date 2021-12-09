# Python Logging In A Nutshell

About a decade ago, I remember being very confused about Python logging -
how it works, how it should be configured, filters, root loggers, handlers, etc.

After doing some research, this was my understanding:

- every Python module (library or main program) should get its own logger
  (typically by doing `logger = logging.getLogger(__name__)`)
- then it can do `logger.info(...)`, `logger.warning(...)`, etc.
- main programs may *configure* logging (with e.g. `logging.basicConfig(...)`
  or `logging.config.dictConfig(...)`)
- libraries should not configure logging

I've often had problems (trying to enable/disable logs for specific parts
of a system) because a library was configuring logging. My understanding is
that libraries *should not* configure logging. They're just emitting a firehose
of unformatted, unfiltered logs, and the main program will do whatever it wants.

Here are a few examples of how to configure logging from the main program.

## Level zero: do nothing

Don't configure logging. In that case, logs of priority WARNING and higher
get printed on stderr.

## Level one: `logging.basicConfig()`

Logs are then prefixed with their severity + logging source, for instance:


```
WARNING:mylib:howdy pardner
```

Here, `mylib` is the name of the logger that generated the log. In other
words, it means that somewhere in the code, something like this happened:

```python
logger = logging.getLogger("mylib")
logger.warning("howdy pardner")
```

## Level two: `logging.basicConfig(...somestuff...)`

This lets you customize a few things, for instance:

- change the log level with `logging.basicConfig(level=logging.DEBUG)`
- change the format string to add timestamps, line numbers, etc.

This is what I use in the majority of my small projects (say, anything between
100 and 1000 lines of code).

Very often, I do this:

```python
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING"))
```

This means that I can change the log level with an environment variable.
This covers 99% of my logging needs in Python.

*Keep in mind that I'm not working on giant code bases, though.
You might need more complex logging setup and that's okay.*

## Level three: `logging.basicConfig(...)` + `setLevel()`

What if I want debug logs, but only for a specific library/package?
Or what if I want debug logs for my app, but not for a very chatty dependency?

Then, in my main file, I do this:

```python
logging.basicConfig()
logging.getLogger("the_specific_lib_or_package").setLevel(logging.DEBUG)
```

I *do not* change anything in the code of the library (I shouldn't need to,
especially if that's a third party dependency and not my own code).

Keep in mind that Python loggers are a tree, which means that if I enable
logging for `foo`, I also get `foo.bar` and `foo.baz` (but I can turn these
off individually too if I need to).

If I needed to often enable/disable logs for specific packages or parts
of the code easily without having to update the code or a config file,
I think I would use environment variables like shown above.

Maybe something like this:

```python
for kv in os.environ.get("LOG_LEVELS", "").split():
  logger_name, logger_level = kv.split("=")
  logging.getLogger(logger_name).setLevel(logger_level)
```

Then I could do e.g.:

```bash
export LOG_LEVELS="mylib=DEBUG urllib3=WARNING"
```

## Level four: `logging.config.dictConfig(...)`

If you need more advanced log routing, for instance, if you want to:

- write some logs to some files
- send other logs to a logging platform/API
- have some logs in plain text, others in JSON
- sometimes include the timestamp, sometimes not (because the logging platform will add it anyway)
- etc.

Then you might have to use a "real" Python logging config.

There is a pretty good example in [How to log in Python like a pro].

[How to log in Python like a pro]: https://guicommits.com/how-to-log-in-python-like-a-pro/

# Examples

Check the code in this repo for a super simple that you can tinker with and see what happens.

# Discussion

*Wait, `logging.basicConfig()`, really?!?*

If you're a seasoned Python programmer, you might be surprised/shocked to see that I'd
recommend to use that.

Well, truth is, a lot of Python programmers don't have the time or energy to write
a 30-line dict to configure logging in their app. Or, in midsize teams, nobody feels
confident enough to take ownership of that and drive a refactor of the logging code.
As a result, we still see a lot of `print()` out there, and my priority is to turn
these into logging calls.
Then later we can discuss how to best configure the logging handlers etc.

*But we should write logs to files, and and and*

No we shouldn't. I mean, maybe you should, and that's totally okay, but a lot of folks
these days run their stuff in containers. In containers, the standard is to write on
stdout/stderr and the container engine will capture that and store/forward it somewhere.
If I'm responsible for running your code in containers, and your logging system astutely writes
to log files, the first thing I'll do is rip it apart to write on stdout/stderr.
It'll pain me but I'll do it nonetheless 🤷🏻

*Have you ever heard of our lord and savior JSON*

I do appreciate stuff that generates JSON! But only when the logging pipeline
handles it. If the rest of the infrastructure and team consumes logs with `docker logs`
and `kubectl logs`, I'm not going to generate JSON because it's going to make everyone's
life miserable. However, if we have a proper logging pipeline that forwards stuff to e.g.
some ELK/EFK/whatever, *and* our devs know how to access (and use!) Kibana (or whatever
frontend the logging system has), then yes by all means, JSON all the things for the win!
But not before.

Thank you!
