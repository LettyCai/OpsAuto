# -*- coding: utf-8 -*-
__author__ = 'clj'
__date__ = '2019/3/13 13:59'

from .models import HostsInfo
from django import forms

class HostInfoForm(forms.ModelForm):
    class Meta:
        model = HostsInfo
        fields = ['ip','ssh_passwd','hostname','mac_address','mathine_type','sn_key','system_ver']

    #验证数据是否合法
    """
    def clead_ip(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
    """