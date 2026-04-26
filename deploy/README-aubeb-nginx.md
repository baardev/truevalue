---
doc_id: deploy_readme_aubeb_nginx
title: AUBEB Nginx Password Gate
type: readme
status: active
domain: blue_economy
layer: operations
projects:
  - aubeb
tags:
  - aubeb
  - blue_economy
  - operations
related_docs:
  []
key_claims:
  []
---

# AUBEB Nginx Password Gate

This keeps the current static Python server and places Nginx in front of it.
Nginx handles the public request and blocks AUBEB paths unless the browser
provides a valid Basic Auth username and password.

## Request Flow

```text
Browser
  -> tvf.tholonia.com on Nginx port 80
  -> Python static server on 127.0.0.1:8000
  -> /home/jw/src/tv
```

## Protected Paths

The template protects:

```text
/frontend/project/aubeb/
/viewable/frontend/project/aubeb/
```

That covers the visible AUBEB pages, project-local JSON, source YAML, CSV files,
and generated viewable mirrors. Public index files may still mention AUBEB unless
the project is also removed from the public navigation.

## Named Virtual Host

Nginx can serve multiple domains on the same public port 80. The existing
`dev.tholonia.com` site can keep serving `/home/jw/vhsx`, while this template
serves the TV project only when the requested host is `tvf.tholonia.com`:

```text
dev.tholonia.com:80    -> existing /home/jw/vhsx site
tvf.tholonia.com:80    -> Nginx AUBEB password gate
127.0.0.1:8000         -> Python static backend for /home/jw/src/tv
```

Only one Nginx process binds port 80, but it may contain multiple `server`
blocks with different `server_name` values.

If another process currently owns port 80 for `dev.tholonia.com`, move that
host into Nginx too. Use `deploy/nginx-dev-and-tvf.conf.template` for the
combined setup:

```text
dev.tholonia.com:80 -> Nginx static root /home/jw/vhsx
tvf.tholonia.com:80 -> Nginx proxy to 127.0.0.1:8000
```

## DNS

In Cloudflare, add:

```text
Type: A
Name: tvf
Content: <your server public IP>
Proxy status: Proxied or DNS only
```

Use `DNS only` while testing if Cloudflare proxy behavior gets in the way. Once
the host works, `Proxied` is fine.

## Install Steps

### Manjaro / Arch quick path

Your system needs Nginx installed before `/etc/nginx/conf.d/` and the
`nginx.service` unit exist:

```bash
sudo pacman -S nginx apache
sudo mkdir -p /etc/nginx/conf.d
```

If this is a fresh Nginx install, use the repo's Manjaro main config so
`/etc/nginx/conf.d/*.conf` is loaded:

```bash
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
sudo cp /home/jw/src/tv/deploy/nginx-main-manjaro.conf.template /etc/nginx/nginx.conf
```

Run the Python server bound to localhost:

```bash
cd /home/jw/src/tv
python3 -m http.server 8000 --bind 127.0.0.1
```

Create the Nginx password file. If `htpasswd` says `password verification error`,
the two typed passwords did not match. Re-run the command:

```bash
sudo htpasswd -c /etc/nginx/tv-aubeb.htpasswd aubeb
```

Install and enable the Nginx site. If Nginx is only serving `tvf.tholonia.com`,
install `nginx-tv-aubeb.conf.template`:

```bash
sudo cp /home/jw/src/tv/deploy/nginx-tv-aubeb.conf.template /etc/nginx/sites-available/tv-aubeb
sudo ln -s /etc/nginx/sites-available/tv-aubeb /etc/nginx/sites-enabled/tv-aubeb
sudo nginx -t
sudo systemctl reload nginx
```

If your Nginx install does not use `sites-available` and `sites-enabled`, copy
the template to `/etc/nginx/conf.d/tv-aubeb.conf` instead:

```bash
sudo mkdir -p /etc/nginx/conf.d
sudo cp /home/jw/src/tv/deploy/nginx-tv-aubeb.conf.template /etc/nginx/conf.d/tv-aubeb.conf
sudo nginx -t
sudo systemctl enable --now nginx
```

If Nginx should serve both `dev.tholonia.com` and `tvf.tholonia.com`, install
the combined template instead:

```bash
sudo rm -f /etc/nginx/conf.d/tv-aubeb.conf
sudo cp /home/jw/src/tv/deploy/nginx-dev-and-tvf.conf.template /etc/nginx/conf.d/dev-and-tvf.conf
sudo nginx -t
sudo systemctl enable --now nginx
```

After later config changes, reload instead of enable:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Verification

Open a public page and confirm it loads without a password:

```text
http://tvf.tholonia.com/
```

Open AUBEB and confirm the browser asks for credentials:

```text
http://tvf.tholonia.com/frontend/project/aubeb/index.html
```

Confirm direct Python access is not exposed externally. The Python server should
only bind to `127.0.0.1:8000`, not `0.0.0.0:8000`.
