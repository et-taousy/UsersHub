from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from app import genericRepository
from app.t_tags import forms as t_tagsforms
from app.models import TTags,BibTagTypes, TApplications, CorRoleTag, TRoles, CorOrganismeTag, Bib_Organismes, CorApplicationTag
from app.utils.utilssqlalchemy import json_resp
from app.env import db

route =  Blueprint('tags',__name__)

@route.route('tags/list', methods=['GET','POST'])
def tags():
    fLine =['ID','ID_type', 'CODE', 'Nom', 'Label', 'Description']
    columns = ['id_tag','id_tag_type','tag_code','tag_name','tag_label','tag_desc']
    contents = TTags.get_all(columns)
    return render_template('table_database.html' ,fLine = fLine ,line = columns,  table = contents,  key = 'id_tag', pathU = '/tag/update/', pathD = '/tags/delete/', pathA = '/tag/add/new',pathP = "/tag/users/",pathO = "/tag/organisms/",pathApp = "/tag/applications/",name = "un tag", name_list = "Liste des Tags", Members= "Utilisateurs", otherCol = 'True', tag_orga = 'True', Organismes = 'Organismes', tag_app = 'True', App = "Application")


@route.route('tags/delete/<id_tag>',methods=['GET','POST'])
def delete(id_tag):
    TTags.delete(id_tag)
    return redirect(url_for('tags.tags'))


@route.route('tag/add/new',defaults={'id_tag': None}, methods=['GET','POST'])
@route.route('tag/update/<id_tag>',methods=['GET','POST'])
def addorupdate(id_tag):
    form = t_tagsforms.Tag()
    form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if id_tag == None:
        if request.method =='POST':
            if form.validate() and form.validate_on_submit():
                form_tag = pops(form.data)
                form_tag.pop('id_tag')
                TTags.post(form_tag)
                return redirect(url_for('tags.tags'))
            else:
                flash(form.errors)
        return render_template('tag.html', form = form)
    else:
        tag = TTags.get_one(id_tag)
        if request.method == 'GET':
            form = process(form,tag)
        if request.method == 'POST':
            if form.validate() and form.validate_on_submit():
                form_tag = pops(form.data)
                form_tag['id_tag'] = tag['id_tag']
                TTags.update(form_tag)
                return redirect(url_for('tags.tags'))
            else:
                flash(form.errors)
        return render_template('tag.html',form = form)

@route.route('tag/users/<id_tag>', methods=['GET','POST'])
def tag_users(id_tag):
    users_in_tag = TRoles.test_group(TRoles.get_user_in_tag(id_tag))
    users_out_tag = TRoles.test_group(TRoles.get_user_out_tag(id_tag))
    header = [ 'ID', 'Nom']
    data = ['id_role','full_name']
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        new_users_in_tag = data["tab_add"]
        new_users_out_tag = data["tab_del"]
        CorRoleTag.add_cor(id_tag,new_users_in_tag)
        CorRoleTag.del_cor(id_tag,new_users_out_tag)

    return render_template('tobelong.html', fLine = header, data = data, table = users_out_tag, table2 = users_in_tag, group = 'groupe')


@route.route('tag/organisms/<id_tag>', methods=['GET','POST'])
def tag_organismes(id_tag):
    organismes_in_tag = Bib_Organismes.get_orgs_in_tag(id_tag)
    organismes_out_tag = Bib_Organismes.get_orgs_out_tag(id_tag)
    header = ['ID','Nom']
    data = ['id_organisme','nom_organisme']
    if request.method == 'POST':
        data = request.get_json()
        new_orgs_in_tag = data["tab_add"]
        new_orgs_out_tag = data["tab_del"]
        CorOrganismeTag.add_cor(id_tag,new_orgs_in_tag)
        CorOrganismeTag.del_cor(id_tag,new_orgs_out_tag)
        print("ajout : ")
        print(new_orgs_in_tag)
        print("supp : ")
        print( new_orgs_out_tag )
    return render_template('tobelong.html', fLine = header, data = data, table = organismes_out_tag, table2 = organismes_in_tag)


@route.route('tag/applications/<id_tag>',  methods=['GET','POST'])
def tag_applications(id_tag):
    applications_in_tag = TApplications.get_applications_in_tag(id_tag)
    applications_out_tag = TApplications.get_applications_out_tag(id_tag)
    header = ['ID','Nom']
    data = ['id_application','nom_application']
    if request.method == 'POST':
        data = request.get_json()
        new_apps_in_tag = data["tab_add"]
        new_apps_out_tag = data["tab_del"]
        CorApplicationTag.add_cor(id_tag,new_apps_in_tag)
        CorApplicationTag.del_cor(id_tag,new_apps_out_tag)
        print("ajout : ")
        print(new_apps_in_tag)
        print("supp : ")
        print( new_apps_out_tag )
    return render_template('tobelong.html', fLine = header, data = data, table = applications_out_tag, table2 = applications_in_tag)



def pops(form):
    form.pop('csrf_token')
    form.pop('submit')
    return form

def process(form,tag):
    form.id_tag_type.process_data(tag['id_tag_type'])
    form.tag_name.process_data(tag['tag_name'])
    form.tag_label.process_data(tag['tag_label'])
    form.tag_code.process_data(tag['tag_code'])
    form.tag_desc.process_data(tag['tag_desc'])
    return form



# NON UTILISE
# @route.route('/tag', methods=['GET','POST'])
# def tag():
#     form = t_tagsforms.Tag()
#     form.id_tag_type.choices =BibTagTypes.choixSelect('id_tag_type','tag_type_name')
#     if request.method =='POST':
#         if form.validate() and form.validate_on_submit():
#             form_tag = form.data
#             form_tag.pop('csrf_token')
#             form_tag.pop('submit')
#             form_tag.pop('id_tag')
#             TTags.post(form_tag)
#             return redirect(url_for('tags.tags'))
#         else:
#             flash(form.errors)
#     return render_template('tag.html', form = form)


# @route.route('tags/update/<id_tag>',methods=['GET','POST'])
# def update(id_tag):
#     entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
#     colonne = ['id_tag','id_tag_type','tag_code','tag_name','tag_label','tag_desc']
#     contenu = TTags.get_all(colonne)
#     # test
#     tag = TTags.get_one(id_tag)
#     form = t_tagsforms.Tag()
#     form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
#     if request.method == 'GET':
#         form.id_tag_type.process_data(tag['id_tag_type'])
#     if request.method == 'POST':
#         if form.validate() and form.validate_on_submit():
#             form_tag = form.data
#             form_tag.pop('csrf_token')
#             form_tag.pop('submit')
#             form_tag['id_tag'] = tag['id_tag']
#             TTags.update(form_tag)
#             return redirect(url_for('tags.tags'))
#         else:
#             flash(form.errors)
#     return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/tags/update/', cheminS = '/tags/delete/', test ='tag.html', form = form, code = tag['tag_code'], name = tag['tag_name'], label = tag['tag_label'], desc = tag['tag_desc'])