from import_export import resources
from structural.models import NonStructural

class NonStructuralResource(resources.ModelResource):
    class Meta:
        model = NonStructural
        fields = (
            'created_at',
            'role',
        )
        export_order = fields

    def get_export_headers(self):
        return ["Tanggal", 'Nama Role']
        
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')