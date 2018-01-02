# Copyright (c) 2012-2016 Seafile Ltd.
from django.db import models

from .settings import ORG_MEMBER_QUOTA_DEFAULT

class OrgMemberQuotaManager(models.Manager):
    def get_quota(self, org_id):
        try:
            return self.get(org_id=org_id).quota
        except self.model.DoesNotExist:
            return ORG_MEMBER_QUOTA_DEFAULT

    def set_quota(self, org_id, quota):
        try:
            q = self.get(org_id=org_id)
            q.quota = quota
        except self.model.DoesNotExist:
            q = self.model(org_id=org_id, quota=quota)
        q.save(using=self._db)
        return q

class OrgMemberQuota(models.Model):
    org_id = models.IntegerField(db_index=True)
    quota = models.IntegerField()

    objects = OrgMemberQuotaManager()
