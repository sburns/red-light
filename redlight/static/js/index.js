$(document).ready(function () {

  // Add filter
  $('a#addFilt').click(function () {
    var num = $('.clonedFilter').length;
    var newNum = (num + 1);
    var newFilter = $('#filter' + num).clone().attr('id', 'filter' + newNum);
    // Update each child
    newFilter.children('input[id*="key"]').attr('id', 'key' + newNum);
    newFilter.children('select[id*="select"]').attr('id', 'select' + newNum);
    newFilter.children('input[id*="value"]').attr('id', 'value' + newNum);
    $('#filter' + num).after(newFilter);
    $('a#removeFilt').removeClass('disabled');
  });


  // Remove Filter
  $('a#removeFilt').click(function () {
    var num = $('.clonedFilter').length;
    if (num - 1 === 0)
      // don't remove the only filter :)
      return;
    $('#filter' + num).remove();
    if (num - 1 == 1)
      $('a#removeFilt').addClass('disabled');
  });

  // Add Output Column
  $('a#addOut').click(function () {
    var num = $('.clonedOutputColumn').length;
    var newNum = (num + 1);
    var newFilter = $('#outcol' + num).clone().attr('id', 'outcol' + newNum);
    // Update each child
    newFilter.children('input[id*="col"]').attr('id', 'col' + newNum);
    $('#outcol' + num).after(newFilter);
    $('a#removeOut').removeClass('disabled');
  });


  // Remove Output
  $('a#removeOut').click(function () {
    var num = $('.clonedOutputColumn').length;
    if (num - 1 === 0)
      // don't remove the only filter :)
      return;
    $('#outcol' + num).remove();
    if (num - 1 === 1)
      $('a#removeOut').addClass('disabled');
  });



  // Run Filter
  $('a#filter').click(function () {
    $('#results').empty();
    $('#resultText').text("Searching...");
    $('#resultText').removeClass('label-success').addClass('label-info');
    var keys = [];
    var verbs = [];
    var values = [];
    var outputs = [];
    $(".key").each(function() {
      keys.push($(this).val());
    });
    $(".value").each(function () {
      values.push($(this).val());
    });
    $(".verb").each(function (){
      verbs.push($(this).val());
    });
    $(".outcol").each(function (){
      outputs.push($(this).val());
    });
    keystring = keys.join(',');
    verbstring = verbs.join(',');
    valuestring = values.join(',');
    outstring = outputs.join(',');
    $.getJSON($SCRIPT_ROOT + '/api/1/filter.json',
    $.param({
      url: $("#inputURL").val(),
      api: $("#inputAPI").val(),
      keys: keys,
      verbs: verbs,
      values: values,
      outputs: outputs
    }, true),
    function(d) {
      if (d.err.length > 0) {
        $('#resultText').text(d.err);
        $('#resultText').removeClass('label-info').addClass('label-important');
        return;
      } else {
        $('#resultText').text('Results (' + d.result.length + ' found)');
        $('#resultText').removeClass('label-info').addClass('label-success');
        var content = '<table class="table table-striped"><thead><tr>';
        $.each(d.header, function(ind, val) {
          content += '<th>' + val + '</th>';
        });
        var headlen = d.header.length;
        content += '</tr></thead><tbody>'; // finish row and header
        $.each(d.result, function(ind, val) {
          var rowstr = "";
          for (i = 0; i < headlen; i++) {
            rowstr += '<td>' + val[d.header[i]] + '</td>';
          }
          content += '<tr>' + rowstr + '</tr>';
        });
        content += '</tbody></table>';
        $('div#results').append(content);
      }
    });
  });


  $('li#navSearch').addClass('active');

  // Init the remove buttons as disabled
  $('a#removeFilt').addClass('disabled');
  $('a#removeOut').addClass('disabled');
});