/*
  Get a list of url parameters, allows multiple values for one key
 */
function get_url_params() {
  var query = location.search.substr(1);
  var params = query.split("&");
  var result = {};
  for (var i = 0; i < params.length; i++) {
    var item = params[i].split("=");
    result[item[0]] = result[item[0]] || [];
    result[item[0]].push(item[1]);
  }
  return result;
}

/*
  Handles filter specific functionality, such as checking the checkboxes and
  replacing the content via ajax (if that is set in the settings)
 */
var init_filter = function ($content) {
  /* Make sure that form fields are pre-filled (when there is a page reload) */
  $content.find('form.events_filter').each(function () {
    var $form = $(this);
    var url_params = get_url_params();

    // check search bar
    if (url_params.hasOwnProperty('search')) {
      $form.find('input[name="search"]').val(url_params['search']);
    }

    // check tag checkboxes
    if (url_params.hasOwnProperty('tags')) {
      $.each(url_params['tags'], function (index, value) {
        $form.find('input[name="tags"][value="' + value + '"]').attr('checked', 'checked');
      });
    }
  });

  /* Stop pagereload, get and replace content via ajax instead. */
  $content.find('form.events_filter.ajax_filter').each(function () {
    var $form = $(this);
    $form.find('button[type=submit]').on('click', function (e) {
      e.preventDefault();
      var url = window.location.pathname;

      $.ajax({
        url: url,
        data: $form.serialize(),
        method: 'GET'
      }).success(function (res, status, xhr, form) {
        // replace content
        var $new_content = $(res).find('.events_list');
        $content.find('.events_list').replaceWith($new_content);
      }).error(function (res, status, xhr, form) {
        console.log(res, status, xhr, form);
      });
    });
  });
};

$(document).ready(function () {
  var $body = $('body');
  init_filter($body);
});
