# Google Domains DDNS

`google-domains-ddns` provides a mechanism for automagically updating Google Dynamic DNS records.

## Configuration

`google_domains_ddns` is configured via environment variables

### Required
* `USERNAME`: Generated username from DDNS entry
* `PASSWORD`: Generated password from DDNS entry
* `DOMAIN`: Domain which is being updated

### Optional
* `INTERVAL`: An ISO8601 Duration string, defaults to `PT30M`
* `LOG_LEVEL`: Python log level, defaults to `INFO`; examples are `DEBUG`, `INFO`, `WARNING`, `ERROR`

## Development

Container can be build and test via `./test.sh`

## Publish
```
    docker buildx create --platform linux/amd64,linux/arm/v7 --use
    docker run --privileged --rm tonistiigi/binfmt --install all

    ./publish.sh
```
