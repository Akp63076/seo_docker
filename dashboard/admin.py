from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import   description_table, domain_table, keyword_tag_table, keyword_rel_question_table, keyword_rel_search_table, keyword_table, keyword_brand_table, question_table, rel_question_table, rel_search_table, tag_table, sitelink_table, brand_table,keyword_frequency_table,frequency_table




@admin.register(keyword_table)
class keyword_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','keyword','req_url','with_year','search_volume','category')
@admin.register(domain_table)
class domain_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','domain')

@admin.register(description_table)
class description_tableAdmin(ImportExportModelAdmin):
    list_display = ('desc_id','url','date','pos','title','description','pos_overall','url_shown','domain_id','keyword_id')

@admin.register(rel_search_table)
class rel_search_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','rel_search')

@admin.register(keyword_rel_search_table)
class keyword_rel_search_tableAdmin(ImportExportModelAdmin):
    list_display = ('keyword_id','rel_search_id','date')
  

@admin.register(brand_table)
class brand_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','brand')

@admin.register(keyword_brand_table)
class keyword_brand_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','keyword_id','brand_id')

@admin.register(rel_question_table)
class rel_question_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','rel_question','pos','answer','source_url','source_title','url_shown','domain_id')


@admin.register(tag_table)
class tag_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','tag')



@admin.register(keyword_tag_table)
class keyword_tag_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','keyword_id','tag_id')

@admin.register(frequency_table)
class frequency_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','frequency')



@admin.register(keyword_frequency_table)
class keyword_frequency_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','keyword_id','frequency_id')

@admin.register(keyword_rel_question_table)
class keyword_rel_question_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','date','keyword_id','question_id')

@admin.register(question_table)
class question_tableAdmin(ImportExportModelAdmin): 
    list_display = ('id','question','pos','desc')

@admin.register(sitelink_table)
class sitelink_tableAdmin(ImportExportModelAdmin):
    list_display = ('id','url_type','url','title','desc')
