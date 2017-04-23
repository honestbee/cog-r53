#resource record set change batch

class ChangeBatch():
    def __init__(self, comment='comment'):
        self.Comment = comment
        self.Changes = []

    def add_change_(self, change):
        self.Changes.append(change)

    def add_upsert_basic(self, name, type, ttl, values):
        change = {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': name,
                'Type': type,
                'TTL': ttl, #seconds
                'ResourceRecords': [{ 'Value': x} for x in values]
            }
        }
        self.add_change_(change)

    def add_upsert_alias(self, name, type, target_zone_id, target_dns_name):
        change = {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': name,
                'Type': type,
                'AliasTarget': {
                    'HostedZoneId': target_zone_id,
                    'DNSName': target_dns_name
                }
            }
        }
        self.add_change_(change)
