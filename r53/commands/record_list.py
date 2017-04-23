from r53.commands.base import Route53Base
import r53.util as util
import boto3
import os, json

class Record_list(Route53Base):
  def __init__(self):
    super().__init__()
    self.r53client = boto3.client('route53')

  def run(self):
    self.list_()

  def list_(self):
    # log env vars for debug:
    # self.response.debug(json.dumps(dict(os.environ)))
    results = []
    types = self.request.get_optional_option('TYPE')
    name_filter = self.request.get_optional_option('NAME')
    # types is optional, types can be a list or string
    types = types if not isinstance(types, str) else [types]
    zones = self.request.options['ZONE']
    # zones can be string or tuple
    for zone in zones if not isinstance(zones, str) else [zones]:
      paginator = self.r53client.get_paginator('list_resource_record_sets')
      response_iterator = paginator.paginate(HostedZoneId=zone)
      if name_filter is not None:
        response_iterator = response_iterator.search(
          "ResourceRecordSets[?contains(@.Name,'%s')]" % name_filter)
      else:
        # unpack to match same response format
        response_iterator = response_iterator.search("ResourceRecordSets[]")
      for r in response_iterator:
        self.parse_record_(r, zone, types, results)
    self.response.content(results, template='records_list').send()

  # apply type filter and parse record into result object
  def parse_record_(self, r, zone, types, results):
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
