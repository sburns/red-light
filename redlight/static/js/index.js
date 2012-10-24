$(document).ready(function () {
  var fields;

  var clear_credentials = function() {
    $(".typeahead").each(function() {
      var ta = $(this).typeahead();
      ta.data('typeahead').source = [];
    });
    $("small#credentialCheck").text("");
  };

  $('input#inputURL').focusin(function () {
    clear_credentials();
  });

  $('input#inputAPI').focusin(function () {
    clear_credentials();
  });


  function load_ta(elem) {
    var ta = elem.typeahead();
    elem.data('active', true);
    ta.data('typeahead').source = [];
    ta.data('typeahead').source = fields;
    ta.data('typeahead').items = 12;
    ta.data('typeahead').minLength = 0;
    elem.data('active', false);
    elem.trigger('keyup');
  }

  $("input.search").focus(function () {
    load_ta($(this));
  });


  //Load up typeahead
  $('input#inputAPI').focusout(function () {
    $.getJSON($SCRIPT_ROOT + '/v1/columns.json',
      $.param({
        url: $("#inputURL").val(),
        api: $("#inputAPI").val()
      }, true),
      function(d) {
        if (d.err.length > 0) {
          $("small#credentialCheck").removeClass("text-success").addClass("text-error").text("There was an error accessing your REDCap, try again with your credentials");
          return;
        } else {
          $("small#credentialCheck").removeClass("text-error").addClass("text-success").text("REDCap access successful");
          fields = d.columns;
      }
    });
  });

  // Add filter
  $('a#addFilt').click(function () {
    var num = $('.clonedFilter').length;
    var newNum = (num + 1);
    var newFilter = $('#filter' + num).clone().attr('id', 'filter' + newNum);
    // Update each child
    newFilter.children('input[id*="field"]').attr('id', 'field' + newNum);
    newFilter.children('select[id*="select"]').attr('id', 'select' + newNum);
    newFilter.children('input[id*="value"]').attr('id', 'value' + newNum);
    $('#filter' + num).after(newFilter);
    $('a#removeFilt').removeClass('disabled');
    load_ta($("#field" + newNum));
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
    var newOutput = $('#outcol' + num).clone().attr('id', 'outcol' + newNum);
    // Update each child
    newOutput.children('input[id*="col"]').attr('id', 'col' + newNum);
    $('#outcol' + num).after(newOutput);
    $('a#removeOut').removeClass('disabled');
    load_ta($("#col" + newNum));
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
    $('#resultAlert').removeClass('alert-success').removeClass('alert-error').addClass('alert-info');
    var fields = [];
    var verbs = [];
    var values = [];
    var outputs = [];
    $(".field").each(function() {
      fields.push($(this).val());
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
    $.getJSON($SCRIPT_ROOT + '/v1/filter.json',
    $.param({
      url: $("#inputURL").val(),
      api: $("#inputAPI").val(),
      fields: fields,
      verbs: verbs,
      values: values,
      outputs: outputs
    }, true),
    function(d) {
      if (d.err.length > 0) {
        $('#resultText').text(d.err);
        $('#resultAlert').removeClass('alert-info').addClass('alert-error');
        return;
      } else {
        $('#resultText').text(d.result.length + ' records matched the specified filters.');
        $('#resultAlert').removeClass('alert-info').addClass('alert-success');
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