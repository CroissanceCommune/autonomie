# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Userdatas related form informations
"""
import deform
import colander
import functools

from colanderalchemy import SQLAlchemySchemaNode

from autonomie_base.consts import (
    SEX_OPTIONS,
    CIVILITE_OPTIONS,
)

from autonomie.models.user.userdatas import (
    CaeSituationOption,
    UserDatas,
    AntenneOption,
    ZoneOption,
    ZoneQualificationOption,
    StudyLevelOption,
    SocialStatusOption,
    ActivityTypeOption,
    PcsOption,
    PrescripteurOption,
    NonAdmissionOption,
    ParcoursStatusOption,
    STATUS_OPTIONS,
    CONTRACT_OPTIONS,
    UserDatasSocialDocTypes,
)
from autonomie.models.company import CompanyActivity
from autonomie.forms.widgets import CleanMappingWidget
from autonomie.forms.lists import BaseListsSchema
from autonomie.forms.user import (
    conseiller_filter_node_factory,
    get_deferred_user_choice,
)
from autonomie.forms import (
    customize_field,
    get_deferred_select,
    get_select,
    get_select_validator,
    mail_validator,
)


USERDATAS_FORM_GRIDS = {
    u"Synthèse": (
        (
            ('situation_follower_id',6), 
            ('situation_antenne_id',6), 
        ),
        (
            ('parcours_prescripteur_id', 6),
            ('parcours_prescripteur_name', 6),
        ),
        (
            ('parcours_date_info_coll', 3),
            ('situation_societariat_entrance',3),
            ('parcours_non_admission_id', 6),
        ),
    ),
    u"Coordonnées": (
        (
            ('coordonnees_civilite', 3),
            ('coordonnees_lastname', 3),
            ('coordonnees_firstname', 3),
            ('coordonnees_ladies_lastname', 3)
        ),
        (
            ('coordonnees_email1', 3),
            ('coordonnees_email2', 3),
        ),
        (
            ('coordonnees_tel', 3),
            ('coordonnees_mobile', 3),
        ),
        (
            ('coordonnees_address', 3),
            ('coordonnees_zipcode', 3),
            ('coordonnees_city', 3),
        ),
        (
            ('coordonnees_zone_id', 3),
            ('coordonnees_zone_qual_id', 3),
        ),
        (
            ('coordonnees_sex', 3),
            ('coordonnees_birthday', 3),
            ('coordonnees_birthplace', 3),
            ('coordonnees_birthplace_zipcode', 3),
        ),
        (
            ('coordonnees_nationality', 3),
            ('coordonnees_resident', 3),
        ),
        (
            ('coordonnees_secu', 3),
        ),
        (
            ('coordonnees_family_status', 3),
            ('coordonnees_children', 3),
            ('coordonnees_study_level_id', 3),
        ),
        (
            ('coordonnees_emergency_name', 3),
            ('coordonnees_emergency_phone', 3),
        ),
        (
            ('coordonnees_identifiant_interne', 3),
        ),
    ),
    u"Statut": (
        (
            ('social_statuses', 12),
        ),
        (
            ('today_social_statuses', 12),
        ),
        (
            ('statut_end_rights_date', 4),
        ),
        (
            ('statut_handicap_allocation_expiration', 4),
        ),
        (
            ('statut_external_activity', 12),
        ),
    ),
    u"Activité": (
        (
            ('activity_typologie_id', 12),
        ),
        (
            ('activity_pcs_id', 12),
        ),
        (
            ('activity_companydatas', 12),
        ),
        (
            ('parcours_goals', 12),
        ),
        (
            ('parcours_status_id', 12),
        ),
        (
            ('parcours_medical_visit', 3),
            ('parcours_medical_visit_limit', 3),
        ),
    ),

}


@colander.deferred
def deferred_situation_select(node, kw):
    values = [('', u"Sélectionner un statut")]
    options = CaeSituationOption.query()
    for option in options:
        values.append((option.id, option.label))
    return deform.widget.SelectWidget(values=values)


@colander.deferred
def deferred_situation_id_validator(node, kw):
    return colander.OneOf(
        [option.id for option in CaeSituationOption.query()]
    )


def customize_schema(schema):
    """
    Customize the form schema
    :param obj schema: A UserDatas schema
    """
    customize = functools.partial(customize_field, schema)

    customize(
        'situation_antenne_id',
        get_deferred_select(AntenneOption)
    )

    customize(
        'situation_follower_id',
        get_deferred_user_choice(
            roles=['admin', 'manager'],
            widget_options={
                'default_option': ('', ''),
            }
        )
    )

    customize(
        'coordonnees_civilite',
        get_select(CIVILITE_OPTIONS)
    )

    customize('coordonnees_email1', validator=mail_validator())
    customize('coordonnees_email2', validator=mail_validator())

    customize(
        'coordonnees_address',
        deform.widget.TextAreaWidget(),
    )

    customize(
        "coordonnees_zone_id",
        get_deferred_select(ZoneOption),
    )

    customize(
        "coordonnees_zone_qual_id",
        get_deferred_select(ZoneQualificationOption),
    )

    customize(
        "coordonnees_sex",
        get_select(SEX_OPTIONS),
        get_select_validator(SEX_OPTIONS)
    )

    customize(
        "coordonnees_birthplace",
        deform.widget.TextAreaWidget(),
    )

    customize(
        "coordonnees_family_status",
        get_select(STATUS_OPTIONS),
        get_select_validator(STATUS_OPTIONS),
    )

    customize(
        "coordonnees_children",
        get_select(zip(range(20), range(20)))
    )

    customize(
        "coordonnees_study_level_id",
        get_deferred_select(StudyLevelOption),
    )

    customize(
        "statut_social_status_id",
        get_deferred_select(SocialStatusOption),
    )

    customize(
        "statut_social_status_today_id",
        get_deferred_select(SocialStatusOption),
    )

    customize(
        "activity_typologie_id",
        get_deferred_select(ActivityTypeOption)
    )

    customize(
        "activity_pcs_id",
        get_deferred_select(PcsOption)
    )

    customize(
        "parcours_prescripteur_id",
        get_deferred_select(PrescripteurOption),
    )

    customize(
        "parcours_non_admission_id",
        get_deferred_select(NonAdmissionOption),
    )

    if 'social_statuses' in schema:
        child_schema = schema['social_statuses'].children[0]
        child_schema.widget = CleanMappingWidget()
        customize_field(
            child_schema,
            'social_status_id',
            widget=get_deferred_select(SocialStatusOption)
        )
        customize_field(
            child_schema,
            'step',
            widget=deform.widget.HiddenWidget(),
            default="entry"
        )

    if 'today_social_statuses' in schema:
        child_schema = schema['today_social_statuses'].children[0]
        child_schema.widget = CleanMappingWidget()
        customize_field(
            child_schema,
            'social_status_id',
            widget=get_deferred_select(SocialStatusOption)
        )
        customize_field(
            child_schema,
            'step',
            widget=deform.widget.HiddenWidget(),
            default="today"
        )

    if 'statut_external_activity' in schema:
        child_schema = schema['statut_external_activity'].children[0]
        child_schema.widget = CleanMappingWidget()
        customize_field(
            child_schema,
            'statut_external_activity',
            widget=get_select(CONTRACT_OPTIONS),
        )

    if 'activity_companydatas' in schema:
        child_schema = schema['activity_companydatas'].children[0]
        child_schema.widget = CleanMappingWidget()
        customize_field(
            child_schema,
            'activity_id',
            widget=get_deferred_select(CompanyActivity)
        )

    customize("parcours_goals", deform.widget.TextAreaWidget())
    customize('parcours_status_id', get_deferred_select(ParcoursStatusOption))


def get_add_edit_schema():
    """
    Build a colander schema for UserDatas add edit
    :returns: A colander schema
    """
    schema = SQLAlchemySchemaNode(
        UserDatas,
        excludes=('name', '_acl', 'user_id')
    )
    customize_schema(schema)
    return schema


def get_list_schema():
    """
    Return a list schema for user datas
    """
    schema = BaseListsSchema().clone()

    schema['search'].description = u"Nom, prénom, entreprise"

    schema.insert(0, colander.SchemaNode(
        colander.Integer(),
        name='situation_situation',
        widget=deferred_situation_select,
        validator=deferred_situation_id_validator,
        missing=colander.drop,
    )
    )

    schema.insert(0, conseiller_filter_node_factory())
    return schema


def get_doctypes_schema(userdatas_model):
    """
    Build a form schema for doctypes registration

    :param obj userdatas_model: An instance of userdatas we're building 
    the form for
    """
    registered = userdatas_model.doctypes_registrations
    node_schema = SQLAlchemySchemaNode(UserDatasSocialDocTypes)
    node_schema.widget = deform.widget.MappingWidget(
        template="clean_mapping.pt"
    )
    node_schema['status'].widget = deform.widget.CheckboxWidget()

    form_schema = colander.Schema()
    for index, entry in enumerate(registered):
        node = node_schema.clone()
        name = 'node_%s' % index
        node.name = name
        node.title = u''
        node['status'].title = u''
        node['status'].label = entry.doctype.label
        form_schema.add(node)

    return form_schema
