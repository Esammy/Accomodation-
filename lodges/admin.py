from django.contrib import admin
from .models import Profile, LodgeProperties, Lodge, NewPayment, Pop_searched, Contact #, AgentPersonalInfo, AgentProperties #, Payment

admin.site.register(Profile)
admin.site.register(LodgeProperties)
admin.site.register(Lodge)
# admin.site.register(AgentPersonalInfo)
# admin.site.register(AgentProperties)
admin.site.register(NewPayment)
admin.site.register(Pop_searched)
admin.site.register(Contact)