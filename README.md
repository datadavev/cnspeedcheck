# cnspeedcheck

Python script using speedcheck-cli library to generate JSON log output.

Intended for placement on the DataONE CNs to track network load.

Given output to `/var/log/speedcheck/speedcheck.log`, a CSV summary can be produced:

```
</var/log/speedcheck/speedcheck.log jq  -r '. | [.timestamp, .download, .upload] | @csv'
```

With columns `timestamp`, `download MB/sec`, and `upload MB/sec`

