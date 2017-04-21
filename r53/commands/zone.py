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
    response = self.r53client.list_hosted_zones(MaxItems='100')
    self.parse_zones(response,results)
    while response["IsTruncated"]:
      response = self.r53client.list_hosted_zones(Marker=response["NextMarker"], MaxItems='100')
      self.parse_zones(response,results)
    self.response.content(results, template="zones_list").send()

  # parse response into result object
  def parse_zones(self,response,results):
    for z in response["HostedZones"]:
        zone = {
          "Id":z["Id"],
          "Name":z["Name"],
          "Private":z["Config"]["PrivateZone"],
          "Color": "red" if z["Config"]["PrivateZone"] else "green"
        }
        results.append(zone)

  def parse_subcommand_(self):
    if self.request.args == None:
      return self.list
    if self.request.args[0] == "list":
      return self.list
    self.fail("Unknown subcommand: '%s'" % self.request.args[0])
