from flask import (
Flask, redirect, url_for, render_template,
Blueprint, request, session, flash
)
from userhub import genericRepository
from userhub.t_tags import forms as t_tagsforms
from userhub.models import TTags,BibTagTypes, TApplications
from userhub.utils.utilssqlalchemy import json_resp
from userhub.env import db

route =  Blueprint('tags',__name__)

@route.route('/tags', methods=['GET','POST'])
def tags():
    entete =['ID','ID type', 'CODE', 'Nom', 'Label', 'Description']
    colonne = ['id_tag','id_tag_type','tag_name','tag_name','tag_label','tag_desc']
    contenu = TTags.get_all(colonne)
    return render_template('affichebase.html' ,entete = entete ,ligne = colonne,  table = contenu,  cle = 'id_tag', cheminM = '/t_tags/tag/', cheminS = '/t_tag/tag/delete/')

@route.route('/tag', methods=['GET','POST'])
def tag():
    form = t_tagsforms.Tag()
    form.id_tag_type.choices =BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if request.method =='POST':
        if form.validate() and form.validate_on_submit():
            form_tag = form.data
            form_tag.pop('csrf_token')
            form_tag.pop('submit')
            form_tag.pop('id_tag')
            TTags.post(form_tag)
            return redirect(url_for('tags.tags'))
        else:
            flash(form.errors)
    return render_template('tag.html', form = form)

@route.route('/tag/<id_tag>',methods=['GET','POST'])
def update(id_tag):
    tag = TTags.get_one(id_tag)
    form = t_tagsforms.Tag()
    form.id_tag_type.choices = BibTagTypes.choixSelect('id_tag_type','tag_type_name')
    if request.method == 'GET':
        form.id_tag_type.process_data(tag['id_tag_type'])
    if request.method == 'POST':
        if form.validate() and form.validate_on_submit():
            form_tag = form.data
            form_tag.pop('csrf_token')
            form_tag.pop('submit')
            form_tag['id_tag'] = tag['id_tag']
            TTags.update(form_tag)
            return redirect(url_for('tags.tags'))
        else:
            flash(form.errors)
    return render_template('tag.html', form = form, code = tag['tag_code'], name = tag['tag_name'], label = tag['tag_label'], desc = tag['tag_desc'])


@route.route('/tag/delete/<id_tag>',methods=['GET','POST'])
def delete(id_tag):
    TTags.delete(id_tag)
    return redirect(url_for('tags.tags'))