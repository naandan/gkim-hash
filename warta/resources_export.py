from import_export import resources
from warta.models import Warta, Announcement

class WartaResource(resources.ModelResource):
    class Meta:
        model = Warta
        fields = ('created_at', 'name', 'file', 'status', 'highlight', 'order', 'contents', )
        export_order = fields

    def get_export_headers(self):
        return ['Tanggal', 'Judul', 'File', 'Status', 'Highlight', 'Order', 'Content', ]
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y")
    def dehydrate_status(self, obj):
        return 'Dipublish' if obj.status else 'Tidak Dipublish'
    
class AnnouncementResource(resources.ModelResource):
    class Meta:
        model = Announcement
        fields = ('created_at', 'name', 'file', 'status', 'highlight', 'order', 'url', )
        export_order = fields

    def get_export_headers(self):
        return ['Tanggal', 'Judul', 'File', 'Status', 'Highlight', 'Order', 'Url', ]
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y")
    def dehydrate_status(self, obj):
        return 'Dipublish' if obj.status else 'Tidak Dipublish'