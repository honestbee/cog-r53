# Route53 bundle for Cog

Early trial of a bundle to manage Route53 records from Slack.

Primary use case is to create CNAME records by marketing for SaaS marketing platform.

## TL;DR

no support for `HealthCheckId` atm.
no support for `Weighted` records atm.

```
# list zones
!r53:zone

# list records (with option to filter down to records containing <name-filter>)
!r53:record list -z <zone-id> [-t <record-type>] [-n <name-filter>]

# create basic record
!r53:record create -z <zone-id> -t <record-type> <name> <record>[, <record>, ...]

# create alias record
!r53:record create -z <zone-id> -t <record-type> -a <alias-zone-id> <name> <dnsname> <record>
```

## Zones

Returns a table similar to:

```
aws route53 list-hosted-zones \
    --query "HostedZones[].[Id,Name,Config.PrivateZone,ResourceRecordSetCount]" \
    --output table
```

Color coded as follows:

- blue: public zones
- yellow: private zones

## Records

### Basic

```
!r53:record create
  --comment "optional comment about the changes"
  --zone-id <zone-id> (default: "zone-id from config")
  --TTL "time to live in seconds"
  --type "SOA|A|TXT|NS|CNAME|MX|PTR|SRV|SPF|AAAA" (default: "A")
  <name> <values>
```

### Alias

See [Choosing between Alias and Non-Alias](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)

```
!r53:record create
  --comment "optional comment about the changes"
  --zone-id <zone-id>
  --type "SOA|A|TXT|NS|CNAME|MX|PTR|SRV|SPF|AAAA" (default: "A")
  --alias-target-zone-id <zone-id>
  <name> <dns name> <value>
```

## References

- [Route53 docs](http://docs.aws.amazon.com/cli/latest/reference/route53/change-resource-record-sets.html?highlight=route53)

# Installing

From GitHub repository:

```
wget -qO- https://github.com/honestbee/cog-r53/raw/master/config.yaml |
 cogctl bundle install -er default - --force
```

If available from Cog Warehouse:

In chat:

```
@cog bundle install r53
```

From the command line:

```
cogctl bundle install r53
```

# Configuring

The `r53` bundle requires aws credentials with route53 Full permissions.

You can set these variables with Cog's dynamic config feature:

```bash
echo '"AWS_ACCESS_KEY_ID": <YOUR_ACCESS_KEY_ID>' >> config.yaml
echo '"AWS_SECRET_ACCESS_KEY": <YOUR_SECRET_ACCESS_KEY>' >> config.yaml
cogctl dynamic-config create r53 config.yaml --layer=base
```

# Development

## Building

To build the Docker image, simply run:

    $ make docker

Requires Python 3.5.x, pip, make, and Docker.

## Testing Locally

Test commands locally:

Create `.env`:
```
COG_BUNDLE=r53

AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

Confirm environment is set properly:

```
docker-compose config
```

Run `zone` command:
```
docker-compose run -e COG_COMMAND=zone command
```

Test Options (in .env file):
```
# all passed in option flags
COG_OPTS=zone,type

# type as string option
COG_OPT_TYPE=A

# zone as list option
COG_OPT_ZONE_COUNT=2
COG_OPT_ZONE_0=Z1...
COG_OPT_ZONE_1=ZV...
```

Test basic record-create
```
COG_COMMAND=record-create

COG_OPTS=zone,type,alias-target-zone
COG_OPTS=zone,type

COG_OPT_ZONE=Z1NL520TLGD8CP
COG_OPT_TYPE=A

COG_ARGC=3
COG_ARGV_0=record_name
COG_ARGV_1=resource_1
COG_ARGV_2=resource_2
```

Test alias record-create
```
COG_COMMAND=record-create
COG_OPTS=zone,type,alias-target-zone

COG_OPT_ZONE=Z1...
COG_OPT_ALIAS-TARGET-ZONE=Z1...
COG_OPT_TYPE=A

COG_ARGC=3
COG_ARGV_0=record_name
COG_ARGV_1=alias-target
```
