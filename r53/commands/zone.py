from r53.commands.base import Route53Base
import r53.util as util
import boto3

class Zone(Route53Base):
  def __init__(self):
    super().__init__()
    self.r53client = boto3.client("route53")

  def run(self):
    handler = self.parse_subcommand_()
    handler()

  def list(self):
    results = []
    name_filter=None
    try:
      name_filter = self.request.get_optional_option('NAME')
    except:
      pass

    paginator = self.r53client.get_paginator('list_hosted_zones')
    response_iterator = paginator.paginate()
    if name_filter is not None:
      response_iterator = response_iterator.search(
        "HostedZones[?contains(@.Name,'%s')]" % name_filter)
    else:
      # unpack to match same response format
      response_iterator = response_iterator.search("HostedZones[]")
    for z in response_iterator:
      self.parse_zone_(z, results)
    self.response.content(results, template="zones_list").send()

  # parse response into result object
  def parse_zone_(self,z,results):
      zone = {
        "Id":z["Id"],
        "Name":z["Name"],
        "Private":z["Config"]["PrivateZone"],
        "ResourceRecordSetCount":z["ResourceRecordSetCount"],
        "Color": "yellow" if z["Config"]["PrivateZone"] else "blue"
      }
      results.append(zone)

  def parse_subcommand_(self):
    if self.request.args == None:
      return self.list
    if self.request.args[0] == "list":
      return self.list
    self.fail("Unknown subcommand: '%s'" % self.request.args[0])
