from django.contrib import admin

from dashboard.models import Token, CollectedToken, Reward, CollectedReward


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass


@admin.register(CollectedToken)
class CollectedTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    pass


@admin.register(CollectedReward)
class CollectedRewardAdmin(admin.ModelAdmin):
    pass
