from r53.commands.base import Route53Base
import r53.util as util
import boto3
import os, json

class Record(Route53Base):
  def __init__(self):
    super().__init__()
    self.r53client = boto3.client('route53')

  def run(self):
    handler = self.parse_subcommand_()
    handler()

  def list(self):
    # log env vars for debug:
    # self.response.debug(dict(os.environ))
    results = []
    types = self.request.get_optional_option('TYPE')
    # types is optional, types can be a list or string
    types = types if not isinstance(types, str) else [types]
    zones = self.request.options['ZONE']
    # zones can be string or tuple
    for zone in zones if not isinstance(zones, str) else [zones]:
      response = self.r53client.list_resource_record_sets(
        HostedZoneId=zone,
        MaxItems='100')
      self.parse_records(response, zone, types, results)
      while response["IsTruncated"]:
        response = self.r53client.list_resource_record_sets(
          HostedZoneId=zone,
          StartRecordName=response['NextRecordName'],
          MaxItems='100')
        self.parse_records(response, zone, types, results)
    self.response.content(results, template='records_list').send()

  # parse response into result object
  def parse_records(self, response, zone, types, results):
    for r in response["ResourceRecordSets"]:
        if types is None or r["Type"] in types:
          values = []
          if "ResourceRecords" in r.keys():
              for v in r["ResourceRecords"]:
                values.append(v["Value"])
          record = {
            "Zone":zone,
            "Name":r["Name"],
            "Type":r["Type"],
            "AliasTarget":r["AliasTarget"] if "AliasTarget" in r.keys() else None,
            "ResourceRecords": ",".join(values) if "ResourceRecords" in r.keys() else None
          }
          results.append(record)

  def parse_subcommand_(self):
    if self.request.args == None:
      return self.list
    if self.request.args[0] == "list":
      return self.list
    self.fail("Unknown subcommand: '%s'" % self.request.args[0])
