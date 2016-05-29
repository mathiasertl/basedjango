django.jQuery(document).ready(function() {
    console.log('yay!');
    django.jQuery('.basedjango-lang-selector').change(function(e) {
        var val = django.jQuery(e.target).val();
        django.jQuery(e.target).parent().find('[data-lang="' + val + '"]').show();
        django.jQuery(e.target).parent().find('[data-lang][data-lang!="' + val + '"]').hide();

    });
});
