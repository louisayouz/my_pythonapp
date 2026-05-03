<script  type="text/javascript">
  function editQuotePopup(rowid) {
    tds = $("#rowid-"+rowid).find('td');

    tds.each( function(idx, item){
      cls = $(item).attr('class');
      switch (cls) {
        case 'symbol':
          $('#edit_symbol').html($(item).data('symbol'));
          $('#edit_quoteid').val($(item).data('quoteid'));
        case 'price':
          $('#edit_price').val($(item).attr('price'));console.log($(item).attr('price')); break;
          break;
        case 'quantity':
          quantity = $(item).data('qnt');
          $('#edit_quantity').val(quantity); $('#e_qnt').html(quantity); break;
        case 'from_month':
          $('#edit_to_month').val('');
          to_month = parseInt($(item).attr('tomonthattr'), 10);
          if(to_month != 0 ){
             $('#edit_to_month').val(to_month);
          }
          from_month = $(item).attr('frommonthattr');
          $('#edit_from_month').val(from_month); console.log(from_month); break;
      }
    });

    const modal = new bootstrap.Modal(document.getElementById('editModal'));
    modal.show();
  }

  function addNewQuoteModal(){
    const modal = new bootstrap.Modal(document.getElementById('addNewQuoteModal'));
    modal.show();
  }

  function AddNewQuoteCount(rowid)
  {
    let tooltip = $('#tooltip_add');
    tds = $("#rowid-"+rowid).find('td')
    tomonth  = $("#rowid-"+rowid).find('.from_month').attr('tomonthattr');
    if(tomonth == 0){
    //if ($(tomonthObj).html().trim().length == 0){
      tooltip.text("'To month' value is empty! Edit 'To month' value and click on 'Add' again.");
      tooltip.attr("style", "display:inline-block");
      $(".content_add_block").attr("style", "display:none");
    }
    else
    {

      tooltip.text("");
      tooltip.attr("style", "display:none");

      $(".content_add_block").attr("style", "display:block");

      tds.each(function(idx, item){
        cls = $(item).attr('class');
        switch (cls){
          case 'symbol':
            $('#add_quoteid').val($(item).data('quoteid'));
            $('#add_symbol').html($(item).data('symbol'));//for show only
            $('#addsymbol').val($(item).data('symbol')); //form data
          case 'price':
            price = $(item).html();  $('add_price').val($(item).html()); console.log(price); break;
          case 'quantity':
            //quantity = $(item).data('qnt');
            //$('#add_quantity').val(quantity); console.log(quantity); break;
          case 'from_month':
            var to_month = $("#rowid-"+rowid).find('.from_month').attr('tomonthattr');
            var from_month = parseInt(to_month) + 1;
            $('#add_from_month').val(from_month);
            $('#add_to_month').val(12); break;
        }
      });
    }
      const modal = new bootstrap.Modal(document.getElementById('addModal'));
      modal.show();
    }

    function ShowDividends(quote='', foryear=0, frommonth=0, tomonth=0){
       $('#tableContainer').empty();
       if (quote != ''){
          getDivReq(quote, foryear, frommonth, tomonth );
       }

       const modal = new bootstrap.Modal(document.getElementById('dividendlist'));
       modal.show();
    }

  function getDivReq(quote, foryear, frommonth, tomonth ){
    $.ajax({
      url: "/getquotedivs/"+quote+"/"+foryear+"/"+frommonth+"/"+tomonth,
      method: "GET",
      success: function (response) {

        console.log("ajax Fetched data:", response);

        fillDivTable(response);

      },
      error: function () {
        console.log("Failed to fetch data");
      }});
  };

  function fillDivTable(data){
      var table = $('<table class="table">');
      // Create header
      var thead = $('<thead>');
      var headerRow = $('<tr>');
      headerRow.append('<th>Month</th>');
      headerRow.append('<th>Price</th>');
      thead.append(headerRow);
      table.append(thead);

      // Create body
      var tbody = $('<tbody>');
      $.each(data, function(index, item) {
        var row = $('<tr>');
        row.append('<td>' + item.month + '</td>');
        row.append('<td>' + item.price + '</td>');
        tbody.append(row);
      });
      table.append(tbody);

      // Append table to container
      $('#tableContainer').append(table);
  }


  function copyQuotes(){
    $.ajax({
      url: "/copy_portfolio/{{portfolioid}}",
      method: "POST",
      success: function (response) {
        console.log("refrefreshed", response);
        window.location.href = "/quotes/{{portfolioid}}/{{for_year}}";
      },
      error: function (){
        console.log("Failed to copy quotes");
      }});
  };

</script>