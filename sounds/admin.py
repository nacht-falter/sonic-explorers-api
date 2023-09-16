from django.contrib import admin
from sounds.models import Sound
import tagulous.admin

admin.site.register(Sound)
tagulous.admin.register(Sound.tags)
