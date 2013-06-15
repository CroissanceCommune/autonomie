<%inherit file="base.mako" ></%inherit>
<%block name='content'>
<style>
    .form-horizontal .form-actions{
        padding:15px 30px;
    }
    .form-actions .btn{
        width:100%;
        padding:5px;
    }
    .loginbox{
        border:1px solid #ddd;
        overflow:hidden;
        border-radius: 4px 4px 4px 4px;
        margin-top:10px;
        background-color:#efefef;
        padding-top:5px;
    }
    .loginbox legend{
        text-align:center;
    }
</style>
<div class='row'>
    <div class='span6 offset3 loginbox'>
        <div style='text-align:center;'>
            <img src="/assets/main/logo.png" alt='Votre CAE' />
        </div>
        ${html_form|n}
    </div>
</div>
</%block>
