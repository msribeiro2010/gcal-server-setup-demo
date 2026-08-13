# /app/data on server

Target directory created on the remote VPS (203.0.113.42, user `deploy`):

```
deploy@203.0.113.42:~$ mkdir -p /app/data
deploy@203.0.113.42:~$ ls -ld /app/data
drwxr-xr-x 2 deploy deploy 4096 Aug 13 08:41 /app/data
```

Purpose: stores the transferred Google Calendar OAuth token
(`google_calendar_token.json`) and any credential-derived artifacts.
