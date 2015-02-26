<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name='content'>
    % if errors:
        % if "mails" in errors:
            <div class="alert alert-error">
                Veuillez sélectionner au moins un fichier à envoyer
                % if force == False:
                    (si vous désirez forcer l'envoi de documents, vous devez cocher l'option "Forcer l'envoi des documents déjà expédiés ?")
                % endif
            </div>
        % endif
        % if "mail_subject" in errors or "mail_message" in errors:
            <div class="alert alert-error">
                Le sujet et le contenu du mail ne peuvent être vide
            </div>
        % endif

    % endif
    <form accept-charset="utf-8" enctype="multipart/form-data" method="POST" action="">
        <div class='row-fluid'>
        <div class='span12'>
            <span class='help-block'>
                <i class='fa fa-question-circle fa-2x'></i>
                Depuis cette interface, vous pouvez envoyer des documents par e-mail.
                <ul>
                    <li>Sélectionner les documents que vous voulez envoyer</li>
                    <li>Composer votre message</li>
                    <li>Envoyer</li>
                </ul>
            </span>

            <table class="table table-striped table-bordered">
                <caption>Sélection des documents</caption>
                <thead>
                    <th class="span2"><label class='checkbox inline'><input type="checkbox" id="check_all"></input><b>Tous</b></label></th>
                    <th>Entreprise</th>
                    <th>Adresse de l'entreprise</th>
                    <th>Nom du fichier</th>
                    <th>Déjà envoyé ?</th>
                </thead>
                <tbody>
                    <input type="hidden" name="__start__" value="mails:sequence" />
            % for data in datas.values():
                % for file_dict in data:
                    <tr>
                        <% file_obj = file_dict['file'] %>
                        <% filename = file_obj.name %>
                        <% id_ = file_dict['company'].id %>
                        <td>
                            % if file_dict['company'].email:
                            <input type="hidden" name="__start__" value="mail:mapping"/>
                            <input type="hidden" name="company_id" value="${file_dict['company'].id}" />
                            <input type="checkbox"
                                    name="attachment"
                                    value="${filename}"
                                    % if {'company_id': id_, 'attachment': filename} in mails:
                                        checked
                                    % endif
                            >
                                    </input>
                            <input type="hidden" name="__end__" value="mail:mapping"/>
                            % else:
                               e-mail non renseigné
                            % endif
                        </td>
                        <td>${file_dict['company'].name}</td>
                        <td>${file_dict['company'].email}</td>
                        <td>
                            <a href="${file_obj.url(request, company_id=id_)}" title="Visualisez le fichier">
                                ${filename}&nbsp;<i class="fa fa-file-pdf-o fa-1x"></i>
                            </a>
                        </td>
                        <td>
                            % if file_obj.is_in_mail_history(file_dict['company']):
                                <i class="fa fa-check-circle-o fa-1x"></i>
                            % endif
                        </td>
                    </tr>
                % endfor
            % endfor
            <input type="hidden" name="__end__" value="mails:sequence" />
            </tbody>
            </table>
            <div class="well span12">
                <label for="subject">Objet de l'e-mail</label>
                <input type='text' class='span10' name="mail_subject" value="${mail_subject}"></input>
                <label for="mail_message">Message</label>
                <textarea name="mail_message" class='span10'>${mail_message}</textarea>
                <span class="help-block">Le contenu du message (les variables entre {} seront remplacées par les variables correspondantes):
                    <ul class='unstyled'>
                        <li>{company.name} : Nom de l'entreprise</li>
                        <li>{company.employees[0].lastname} : Nom du premier employé de l'entreprise</li>
                        <li>{company.employees[0].firstname} : Prénom du premier employé de l'entreprise</li>
                        <li>{month} : mois du bulletin de salaire</li>
                        <li>{year} : année du bulletin de salaire</li>
                    </ul>
                </span>
                <label for="force">Forcer l'envoi des documents déjà expédiés ?</label>
                <input type="checkbox" value="force" name="force"
                % if force:
                    checked
                % endif
                />
                <span class="help-block">
                    Si vous ne cochez pas cette case seul les documents qui \
                    n'ont pas encore été expédiés seront envoyés.
                </span>
            </div>
        </div>
    </div>
    <div class="row-fluid">
        <div class="span12">
            <div class="form-actions">
                <button class="btn btn-primary"
                    type="submit"
                    name="submit"
                    title="Envoyer ces documents par mail">
                    <i class="fa fa-envelope fa-2x"></i>
                    Envoyer
                </button>
            </div>
        </div>
    </div>
    </form>
</%block>
<%block name="footerjs">
$('#check_all').change(
    function(){
    $('input[name=attachment]').prop('checked', this.checked);
    }
);
</%block>
