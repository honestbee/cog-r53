# Route53 bundle for Cog

## TL;DR
no support for `HealthCheckId` atm.
no support for `Weighted` records atm.

```
!r53:zone create example.com --comment 'hosted zone'
!r53:zone list
!r53:record create example.com 'www 60 A 192.168.0.1'
```

## Zones

List should return a table similar to:

```
aws route53 list-hosted-zones \
    --query "HostedZones[].[Id,Name,Config.PrivateZone]" \
    --output table
```

Behind the scenes using the `change-resource-record-set` API endpoint:

set default `Hosted Zone ID` as part of dynamic config of bundle?

## Basic

```
!r53:record create
  --comment "optional comment about the changes"
  --zone-id <zone-id> (default: "zone-id from config")
  --TTL "time to live in seconds"
  --type "SOA|A|TXT|NS|CNAME|MX|PTR|SRV|SPF|AAAA" (default: "A")
  <dns name> <values (csv list)>
```

## Alias

See [Choosing between Alias and Non-Alias](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)

```
!r53:record create
  --comment "optional comment about the changes"
  --zone-id <zone-id>
  --type "SOA|A|TXT|NS|CNAME|MX|PTR|SRV|SPF|AAAA" (default: "A")
  --alias-target-zone-id <zone-id>
  <dns name>
```

## References

- [Route53 docs](http://docs.aws.amazon.com/cli/latest/reference/route53/change-resource-record-sets.html?highlight=route53)

# Installing

In chat:

```
@cog bundle install statuspage
```

From the command line:

```
cogctl bundle install statuspage
```

# Configuring

The `r53` bundle requires aws credentials, default region and zoneid.

You can set these variables with Cog's dynamic config feature:

```bash
echo '"AWS_ACCESS_KEY_ID": <YOUR_ACCESS_KEY_ID>' >> config.yaml
echo '"AWS_SECRET_ACCESS_KEY": <YOUR_SECRET_ACCESS_KEY>' >> config.yaml
echo '"AWS_REGION": <YOUR_REGION>' >> config.yaml
echo '"AWS_ZONE_ID": <YOUR_ZONE_ID>' >> config.yaml
cogctl dynamic-config create r53 config.yaml --layer=base
```

# Building

To build the Docker image, simply run:

    $ make docker

Requires Python 3.5.x, pip, make, and Docker.
