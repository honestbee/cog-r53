from r53.commands.base import Route53Base
import r53.util as util
import boto3
import os, json

class Record_create(Route53Base):
  def __init__(self):
    super().__init__()
    self.r53client = boto3.client('route53')

  def run(self):
    self.create_()

  def create_(self):
    # dump environment
    # self.response.info(json.dumps(dict(os.environ)))
    # dump arguments
    # self.response.info('Arguments: %s' % self.request.args)
    # prepare create
    type = self.request.options['TYPE']
    zone = self.request.options['ZONE']
    alias_zone = self.request.get_optional_option('ALIAS-TARGET-ZONE')
    name = self.request.args[0]
    values = self.request.args[1:]
    changes = util.ChangeBatch()
    if alias_zone is None:
        ttl = self.request.get_optional_option('TTL')
        if ttl is None:
            ttl = 60
        else:
            ttl = int(ttl)
        self.response.info('Creating basic %s record: %s -> %s' % (type, name, values))
        changes.add_upsert_basic(name,type,ttl, values)
    else:
        # only take first argument
        self.response.info('Creating alias %s record: %s -> %s' % (type, name, values[0]))
        changes.add_upsert_alias(name,type,alias_zone,values[0])

    # dump changebatch dict as json
    self.response.info(json.dumps(vars(changes)))
    self.response.content({'Message': 'record-create is not fully implemented, check Relay logs'}).send()
