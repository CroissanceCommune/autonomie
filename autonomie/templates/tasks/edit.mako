<%doc>
    Template for estimation and invoice edition/creation
</%doc>
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%namespace file="/base/utils.mako" import="address"/>
<%block name='css'>
<link href="${request.static_url('autonomie:static/css/task.css')}" rel="stylesheet"  type="text/css" />
</%block>
<%block name='content'>
    <dl class="dl-horizontal">
        <dt>Prestataire</dt>
        <dd>${address(company, 'company')}</dd>
        </dl>
${form|n}
    <div style="display:none;" id='discount_popup'>
        <form id="discount_temp" class="form-horizontal">
            <div class="control-group">
                <div class="controls">
            <select id="discount_type_select">
                <option value="value" selected="true">En montant fixe</option>
                <option value="percent">En pourcentage</option>
            </select>
             </div>
         </div>
            <div class="control-group">
                <label class='control-label' for="discount_temp_description">Description</label>
                <div class="controls">
                    <textarea name="discount_temp_description" rows="2"></textarea>
                </div>
            </div>
            <div id='value_configuration'>
                <div class="control-group">
                    <label class='control-label' for="discount_temp_value">Montant</label>
                    <div class="controls">
                        <input type="text" name="discount_temp_value">
                    </div>
                </div>
                <div class="control-group">
                    <label class='control-label' for="discount_temp_tva">Tva</label>
                    <div class="controls">
                        <select id="discount_temp_tva" name="tva">
                            % for tva in tvas:
                                <option value="${tva.value}"
                                % if tva.default == 1:
                                    selected="on"
                                % endif
                                >${tva.name}</option>
                            % endfor
                        </select>
                    </div>
                </div>
            </div>
            <div id='percent_configuration' style='display:none'>
                <div class="control-group">
                    <label class='control-label' for="discount_temp_percent">Pourcentage</label>
                    <div class="controls">
                        <div class="input-append">
                            <!-- Important : ici le span et l'input sont sur la même ligne (les espaces font bugger le rendu -->
                            <input type="text" name="discount_temp_percent" class="span2" style="z-index:2500;"><span class="add-on">%</span>
                        </div>
                    </div>
                </div>
            </div>
        </form>
        <div class='form-actions'>
            <button  class='btn btn-primary' type='button' onclick="discount.validate()">Valider</button>
            <button  class='btn btn-primary' type='button' onclick="discount.close()">Annuler</button>
        </div>
    </div>
    <script type='text/javascript'>
        setPopUp('discount_popup', "Remise");
    </script>
</%block>
<%block name='footerjs'>
initialize();
</%block>
