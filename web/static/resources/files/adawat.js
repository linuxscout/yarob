/* strip tashkeel*/
//~ var body = $('body');

function isCharTashkeel(letter) {
    var CHARCODE_SHADDA = 1617;
    var CHARCODE_SUKOON = 1618;
    var CHARCODE_SUPERSCRIPT_ALIF = 1648;
    var CHARCODE_TATWEEL = 1600;
    var CHARCODE_ALIF = 1575;
  if (typeof(letter) == "undefined" || letter == null) return false;
  var code = letter.charCodeAt(0);
  //1648 - superscript alif
  //1619 - madd: ~
  return (code == CHARCODE_TATWEEL || code == CHARCODE_SUPERSCRIPT_ALIF || code >= 1611 && code <=
    1631); //tashkeel
}

function strip_tashkeel(input) {
  var output = "";
  //todo consider using a stringbuilder to improve performance
  for (var i = 0; i < input.length; i++) {
    var letter = input.charAt(i);
    if (!isCharTashkeel(letter)) //tashkeel
      output += letter;
  }
  return output;
}

function ajust_ligature(input) {
  return x = input.replace("لَا", "لاَ");
}


// draw Inflection area
function draw_inflection_results(d) {
        var text = "";
        var id = parseInt(d.order);
        var div_inflect =  document.createElement("div");
        for (var i = 0; i < d.result.length; i++) {
          item = d.result[i];
          var currentId = id * 100 + i;
            var pattern = /[-[\]{}()*+?.,،:\\^$|#\s]/;
            if (!pattern.test(item.chosen)) text += " ";
            var word_to_display = item.chosen;
            // create a span
            var line = document.createElement("span");
            line.setAttribute("class", "inflect");
//            line.appendChild(document.createTextNode(item.chosen));
//            line.appendChild(document.createTextNode(" "));
//            line.appendChild(document.createTextNode(item.inflect));


            // select:
            var select = document.createElement("select");
            select.setAttribute("class", "inflect");
            console.log(item.features);
            for(const key in item.features)
            { // draw a select for each word,
            console.log(item.features[key]);
            var voc_infl_list = item.features[key];
            console.log(voc_infl_list[0]);

            for(var ki =0; ki<voc_infl_list.length;ki++)
            {
                var option = document.createElement("option");
                const vocalized = voc_infl_list[ki].vocalized;
                const tagscode  = voc_infl_list[ki].tagscode;
                const inflect =  voc_infl_list[ki].inflect;
                if(vocalized == item.chosen)
                    option.setAttribute("selected", "selected");
                option.setAttribute("value", vocalized);
                option.setAttribute("title", tagscode);
                option.appendChild(document.createTextNode(vocalized +": " + inflect + "["+tagscode+"]"));
                select.appendChild(option);
            }
            }

//            text += item.chosen + "  " + item.inflect + "<br/>";
            div_inflect.append(line);
            div_inflect.append(select);
            div_inflect.appendChild(document.createElement("br"));
            $('#result').data(currentId.toString(), item);
        }
        // display the result
        $("#result").append(div_inflect);
//        $("#result").html($("#result").html() + "****************<br/><div class=\'word-inflections\'>" + text +
//          "</div>");

      }
// draw tashkeel area
function draw_tashkeel_results(d) {

        // Grammar graph
        //draw_graph();
        var text = "";
        var id = parseInt(d.order);
        var openColocation = 0;
        for (var i = 0; i < d.result.length; i++) {

          item = d.result[i];
          var currentId = id * 100 + i;
//          console.log(item.chosen);
          if (item.chosen.indexOf("~~") >= 0) { // handle collocations
            openColocation = 0;
            text += "</span><span class='collocation' title='دقّق تشكيل هذه العبارة'>" +
              item.chosen.replace("~~", "");
          } else if (item.chosen.indexOf("~") >= 0) { // handle collocations
            if (openColocation == 0) {
              openColocation = 1;
              text += item.chosen.replace("~", "") +
                " <span class='collocation' title='دقّق تشكيل هذه العبارة'>";
            } else {
              openColocation = 0;
              text += "</span>" + item.chosen.replace("~", "");
            }
          } else {
            var pattern = /[-[\]{}()*+?.,،:\\^$|#\s]/;
            if (!pattern.test(item.chosen)) text += " ";
            var word_to_display = item.chosen.replace('\n',"<br/>");
            if (document.NewForm.LastMark.checked == 0) word_to_display = item.semi;
            text += "<span class='vocalized' id='" + currentId + "' inflect='" + item.inflect.replace(/:+/g, ', ') +
              "' suggest='" + item.suggest.replace(/;/g, '، ') + "' rule='" + item.rule +
              "' link='" + item.link + "'>" + word_to_display + "</span>";
            //~ $('#result').data(currentId.toString(), item.suggest);
            $('#result').data(currentId.toString(), item);
          }
        }
        // display the result
        $("#loading").data(d.order, text);
        $("#result").html($("#result").html() + "<div class=\'tashkeel\'>" + text +
          "</div>");
        // dela dot, to count the phrase executed
        //~ $("#loading").html($("#loading").html().replace('.', ''));
        //~ if ($("#loading").html().indexOf('.') < 0) { // if no dot, the work is terminated
          //~ // redraw the text result with order
          //~ var ordredtext = "";
          //~ for (var j = 0; j < $("#loading").data('length'); j++) {
            //~ ordredtext += $("#loading").data(j.toString());
          //~ }
          //~ console.log("oder");
            //~ $('#result').data("count",d.result.length);
            //~ $('#result').html("<div class=\'tashkeel\'>" + ordredtext + "</div>");
            //~ $("#loading").hide();
        //~ }
      }
//
//function draw_graph(d){
////alert("Hello");
//var cy = cytoscape({
//  container: $('#result'),
//  layout: { name: 'grid'},
// style: [
//    {
//      selector: 'node',
//      style: {
//        'content': 'data(label)',
//        'background-color':'data(color)',
//        'shape': 'data(faveShape)',
//        'font-family':'Droid Arabic Naskh',
//        'font-size':'14pt',
//
//
//          }
//    },
//    {
//      selector: 'edge',
//      style: {
//        'content': 'data(label)',
//        'opacity': 1,
//        'width': 'mapData(strength, 70, 100, 2, 6)',
//        'line-color': 'data(color)',
//        'curve-style': 'data(curve)',
//      }
//    },
//
//    {
//      selector: ':parent',
//      style: {
//        'background-opacity': 0.6
//      }
//    }
//  ]
//
//});
//cy.zoomingEnabled( true );
//cy.layout({ name: 'grid' });
//var layout = cy.makeLayout({
//  name: 'grid'
//});
//
//layout.run();
//for (k in d.result) {
//    if (d.result[k].length != 0) {
//// create the actual word node
//    var word = d.result[k][0]['word'];
//    //alert ("n"+ k.toString());
//    var id_parent = k.toString();
//    cy.add([
//     // { group: "nodes", data: { id: id_parent , label :word} } ,
//  { group: "nodes", data: { id: id_parent , label :word,  color:"#ddd", faveShape:"rectangle"}, position: { x: 80*(k+1), y: 30 } },
//    ]);
//    for (j in d.result[k])
//        {
//        var color = "#ddd";
//        var faveShape = 'ellipse';
//        var item = d.result[k][j];
//        var vocalized = item['vocalized'];
//        //extract syntaxic relations,
//        // ToDo improve relations extraction
//        var synt = item["syntax"];
//
//        if (item['type'].indexOf("Verb") !=-1)
//            {
//            color = "#6FB1FC";
//            faveShape = "octagon";
//            }
//        else if (item['type'].indexOf("STOPWORD") !=-1)
//            {
//            color = "#EDA1ED";
//            faveShape = "triangle";
//            }
//        var cur_id = k.toString()+"-"+j.toString();
//         var node = cy.add([
//      { group: "nodes", data: { id: cur_id , label : vocalized , parent:id_parent, color:color, faveShape:faveShape}, position: { x: 50+10*(k+1), y: 50+10*(j+1) } },
//            ]);
//
//        // if have previous we can represent all connections
//        if (k-1 >= 0)
//        {
//        // syntaxic
//        for( h in synt['P'])
//        {
//        var previous = (k-1).toString()+"-"+h.toString();
//        var edge_color = "#6FB1FC";
//        if(h%3 ==1)
//            edge_color = "#EDA1ED";
//        else if (h% 3 ==2)
//            edge_color = "#86B342";
//
//        cy.add([
//          { group: "edges", data: { id: "e"+cur_id+"-"+previous, source: previous, target: cur_id , label:synt['P'][h], color:edge_color, curve: 'bezier'} },
//        ]);
//        }
//
//        // sementic
//        for( h in synt['SP'])
//        {
//        var previous = (k-1).toString()+"-"+h.toString();
//        var edge_color = "#ff0000";
//        cy.add([
//          { group: "edges", data: { id: "e"+cur_id+"-"+previous, source: previous, target: cur_id , label:synt['SP'][h], color:edge_color, curve: 'haystack'} },
//        ]);
//        }
//        }
//
//
//        }//for j
//
//       } //end if
//
//    } //end for k
//layout.run();
//}




// randomMaqola_handler
//var randomMaqola_handler = function(e) {
//    e.preventDefault()
//    $.getJSON("http://maqola.org/site/widget?nolayout", function(d) {
//      // $("#InputText").text(d.result+"Taha");
//      if (d) document.NewForm.InputText.value = d.body.replace(/<\/?[^>]+(>|$)/g, " ");
//      else document.NewForm.InputText.value = "TZA";;
//      //"#result").text(d.time);
//    });
//  }
//
//

var random_click = function(e) {
    e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: '',
      action: "RandomText"
    }, function(data) {
      if (data) document.NewForm.InputText.value = data.result;
      else document.NewForm.InputText.value = "TZA";
    });
  }

// signal a problem
var signal_click = function(e) {
    e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: "",
      action: "Signal",
      problem: document.signalForm.signal.value,
      message : document.signalForm.message.value
    }, function(data) {
    alert("شكرا لك على التنبيه،  سنراجع المشكلة."
    +"\n"+ data.result);
    });
  }

 // aks for expert button
var ask_click = function(e) {
    e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: document.askForm.phrase.value,
      action: "Ask",
      email: document.askForm.email.value,
      askby : document.askForm.askby.value
    }, function(data) {
    alert("شكرا لك، سنجيبك في أقرب وقت."
    +"\n"+ data.result);
    });
  }

 // Contact Form
var contact_click = function(e) {
    e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: "",
      action: "Contact",
      name: document.contactForm.name.value,
      subject: document.contactForm.subject.value,
      email: document.contactForm.email.value,
      message : document.contactForm.message.value
    }, function(data) {
    alert("شكرا لك على رسالتك،."
    +"\n"+ data.result);
    });
  }


 // Edit Form
var edit_click = function(e) {
    e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: "",
      action: "Edit",
      id_phrase: document.editForm.id_phrase.value,
      phrase: document.editForm.phrase.value,
      inflection: document.editForm.inflection.value,
      phrase_type: document.editForm.phrase_type.value,
      source: document.editForm.source.value,
      state: document.editForm.state.value,
      date: document.editForm.date.value,
      keywords: document.editForm.keywords.value,
    }, function(data) {
    alert("شكرا لك على مساهمتك،."
    +"\n"+ data.result);
    });
  }

var stripharakat_click = function(e) {
        e.preventDefault()
        $("#result").html(strip_tashkeel(document.NewForm.InputText.value));
  }
  
//var csv2data_click = function(e) {
//        e.preventDefault()
//    $.getJSON(script + ")s/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "CsvToData"
//    }, function(d) {
//      $("#result").html("<pre>" + d.result + "</pre>");
//      //"#result").text(d.time);
//    });
//  }

//--------------------------------------
//var number_click = function(e) {
//      e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "NumberToLetters"
//    }, function(d) {
//      $("#result").html("<p>" + d.result + "</p>");
//      //"#result").text(d.time);
//    });
//  }
  
  
  // extact named enteties 
//var named_click = function(e) {
//        e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "extractNamed"
//    }, function(d) {
//      $("#result").html("<p>" + d.result + "</p>");
//      //"#result").text(d.time);
//    });
//  }
  
  // extact numbers enteties 
//var numbred_click = function(e) {
//        e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "extractNumbered"
//    }, function(d) {
//      $("#result").html("<p>" + d.result + "</p>");
//      //"#result").text(d.time);
//    });
//  }

  // extact enteties 
//var extractEnteties_click = function(e) {
//      e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "extractEnteties"
//    }, function(d) {
//      $("#result").html(d.result +"<br/><hr/><span class='coll'>متلازمات</span> <span class='named'>مسميات</span> <span class='number'>معدودات</span> ");
//
//    });
//  }

//----------Tabs----------------------  
var more_click = function(e) {
      e.preventDefault()
    $("#moresection").slideToggle();
  }

  var vocalize_group_click = function(e) {
        e.preventDefault()
    $("#vocalizesection").slideToggle();
    $("#moresection").hide();
  }
  //Unshape text 
//  var unshape_click = function(e) {
//        e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Unshape"
//    }, function(d) {
//      $("#result").html("<p>" + d.result + "</p>");
//    });
//  }
  //move result into input 
  var move_click = function(e) {
        e.preventDefault()
    $(".txkl").change(e);
    document.NewForm.InputText.value = $("#result").text();
  }
  //copy result into clipboard
  var copy_click = function(e) {
        e.preventDefault()
    $(".txkl").change();
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($("#result").text()).select();
    document.execCommand("copy");
    $temp.remove();
    alert("نسخت البيانات في الحافظة.");
    //document.NewForm.InputText.value = $("#result").text();
  }

  //copy result into clipboard
  var copy_card_click = function(e) {
        e.preventDefault()
     var card = $(this).closest(".card");

      // Find the content to copy (for example, the text in a <p> element inside the card)
      var contentToCopy = card.find("[id^='phrase_clone']").text();
//      console.log("Content To copy", contentToCopy)
      contentToCopy += " \n "+card.find("p").text();

      // Create a temporary input element to hold the text to copy
      var tempInput = $("<textarea>");
      // Set the input's value to the content to copy
      tempInput.val(contentToCopy);

      // Append the input element to the document
      $("body").append(tempInput);

      // Select the input element's content
      tempInput.select();

      // Copy the selected text to the clipboard
      document.execCommand("copy");

      // Remove the temporary input element from the document
      tempInput.remove();

      // Optional: Show a success message or provide visual feedback to the user
    alert("نسخت البيانات في الحافظة.");
  }


// morphology analysis by Al-Qalsadi
//  var stem_click = function(e) {
//        e.preventDefault()
//    $("#loading").slideDown();
//    var $table = $('<table/>');
//    var table = $table.attr("border", "1")[0];
//    var headers = ["<tr>", "<th>المدخل</th>", "<th>تشكيل</th>", "<th>الأصل</th>",
//      "<th>الزوائد</th>", "<th>الجذع</th>",
//      "<th style='white-space:nowrap;'>الحالة الإعرابية</th>",
//      "<th>النوع</th><th>النحوي</th>", "<th>شيوع</th>", "</tr>"
//    ].join('');
//    $table.append(headers);
//    var item = "";
//    $("#result").html("");
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "LightStemmer"
//    }, function(d) {
//      for (k in d.result) {
//        var tbody = document.createElement('tbody');
//        if (d.result[k].length == 0) {
//          var tr = document.createElement('tr');
//          var td = document.createElement('td');
//          td.appendChild(document.createTextNode(k));
//          tr.appendChild(td);
//          for (j = 0; j < 7; j++) {
//            var td = document.createElement('td');
//            td.appendChild(document.createTextNode("-"));
//            tr.appendChild(td);
//          }
//          tbody.appendChild(tr);
//        } else {
//          for (i = 0; i < d.result[k].length; i++) {
//            var tr = document.createElement('tr');
//            item = d.result[k][i];
//            var td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['word']));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['vocalized']));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['original']));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['affix']));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['stem']));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['tags'].replace(/:/g, ': ')));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['type']));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(JSON.stringify(item['syntax'])));
//            tr.appendChild(td);
//            td = document.createElement('td');
//            td.appendChild(document.createTextNode(item['freq']));
//            tr.appendChild(td);
//            tbody.appendChild(tr);
//          }
//        }
//        table.appendChild(tbody);
//      }
//      $("#result").append($table);
//    });
//    $("#loading").slideUp();
//  }
//  var tokenize_click = function(e) {
//        e.preventDefault()
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Tokenize"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        $("#result").append(d.result[i] + "<br/>");
//      }
//    });
//  }
// Gramatical Analysis

  
  // extract chunks from text
//    var chunk_click = function(e) {
//          e.preventDefault()
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "chunk"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        $("#result").append(d.result[i] + "<br/>");
//      }
//    });
//  }
  
    // extract chunks from text
//    var bigrams_click = function(e) {
//          e.preventDefault()
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "bigrams"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        $("#result").append(d.result[i] + "<br/>");
//      }
//    });
//  }
  // inverse order
//  var inverse_click = function(e) {
//        e.preventDefault()
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Inverse"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        $("#result").append(d.result[i] + "<br/>");
//      }
//    });
//  }
  // Ajust an Arabic poetry in two columns  
//  var poetry_click = function(e) {
//        e.preventDefault()
//    var $table = $('<table/>');
//    var table = $table.attr("border", "0")[0];
//    //~ $table.addClass('poemtryJustifyCSS3');
//    $table.addClass('poem');
//    var item;
//    $("#result").html("");
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Poetry"
//    }, function(d) {
//      for (i = 0; i < d.result.length; i++) {
//        var tr = document.createElement('tr');
//        item = d.result[i];
//        var td = document.createElement('td');
//        td.setAttribute('class','poem');
//        td.appendChild(document.createTextNode(item[0]));
//        tr.appendChild(td);
//        td = document.createElement('td');
//        td.setAttribute('class','poem');
//        td.appendChild(document.createTextNode(item[1]));
//        tr.appendChild(td);
//        table.appendChild(tr);
//      }
//      $("#result").append($table);
//    });
//  }

//  var romanize_click = function(e) {
//        e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Romanize"
//    }, function(d) {
//      $("#result").html("<p>" + d.result + "</p>");
//    });
//  }
  var contribute_click = function(e) {
        e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: $("#result").text(),
      action: "Contribute"
    }, function(d) {
      alert(d.result);
    });
  }
//  // normalize text
//  var normalize_click = function(e) {
//        e.preventDefault()
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Normalize"
//    }, function(d) {
//      $("#result").html(d.result);
//    });
//  }
//  var wordtag_click = function(e) {
//        e.preventDefault()
//    var $table = $('<table/>');
//    var $div = $('<div/>');
//    var div = $div[0];
//    var table = $table.attr("border", "0")[0];
//    $table.attr("width", '600');
//    //$table.attr( "style",'text-align: justify; text-justify: newspaper; text-kashida-space: 100;”);
//    var headers = ["<tr>", "<th>الكلمة</th>", "<th>تصنيفها</th>", "</tr>"].join('');
//    $table.append(headers);
//    $("#result").html("");
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Wordtag"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        item = d.result[i];
//        var span = document.createElement('span');
//        span.setAttribute('class', item.tag);
//        span.appendChild(document.createTextNode(" " + item.word));
//        div.appendChild(span);
//        //display as table
//        var tr = document.createElement('tr');
//        var td = document.createElement('td');
//        td.appendChild(document.createTextNode(item.word));
//        tr.appendChild(td);
//        td = document.createElement('td');
//        td.setAttribute('class', item.tag);
//        td.appendChild(document.createTextNode(item.tag));
//        tr.appendChild(td);
//        table.appendChild(tr);
//      }
//      $("#result").append($div);
//      $("#result").append($table);
//    });
//  }
//  var language_click = function(e) {
//        e.preventDefault()
//    var $div = $('<div/>');
//    var div = $div[0];
//    $("#result").html("");
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Language"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        item = d.result[i];
//        var span = document.createElement('span');
//        span.setAttribute('class', item[0]);
//        span.appendChild(document.createTextNode(item[1]));
//        div.appendChild(span);
//      }
//      $("#result").append($div);
//    });
//  }


  // generate all affixation form of a word  
//  var affixate_click = function(e) {
//        e.preventDefault()
//    var $table = $('<table/>');
//    var table = $table.attr("border", "0")[0];
//    $table.attr("width", '600');
//    //$table.attr( "style",'text-align: justify; text-justify: newspaper; text-kashida-space: 100;”);
//    var headers = ["<tr>", "<th>الكلمة</th>", "<th>تقطيعها</th>", "</tr>"].join('');
//    $table.append(headers);
//    $("#result").html("");
//    var item;
//    $.getJSON(script + "/ajaxGet", {
//      text: document.NewForm.InputText.value,
//      action: "Affixate"
//    }, function(d) {
//      $("#result").html("");
//      for (i = 0; i < d.result.length; i++) {
//        var tr = document.createElement('tr');
//        item = d.result[i];
//        var td = document.createElement('td');
//        td.appendChild(document.createTextNode(item.standard));
//        tr.appendChild(td);
//        td = document.createElement('td');
//        td.appendChild(document.createTextNode(item.affixed));
//        tr.appendChild(td);
//        table.appendChild(tr);
//        //      $("#result").append(+"  "++"<br/>" );
//      }
//      $("#result").append($table);
//    });
//  }

  var tashkeel2_click = function(e) {
        e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: ocument.NewForm.InputText.value,
      action: "Tashkeel"
    }, function(d) {
      $("#result").html("<div class=\'tashkeel\'>" + d.result + "</div>");
      $("#contributeSection").show();
    });
  }
  var reducetashkeel_click = function(e) {
        e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "ReduceTashkeel"
    }, function(d) {
      $("#result").html("<div class=\'tashkeel\'>" + d.result + "</div>");
      $("#contributeSection").show();
    });
  }
  var comparetashkeel_click = function(e) {
        e.preventDefault()
    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "CompareTashkeel"
    }, function(d) {
      var table = d.result;
      $("#result").html("<div class=\'tashkeel\'>" + table + "</div>");
    });
  }
  var showCollocations_click = function(e) {
        e.preventDefault()
    $.getJSON(script + "/ajaxGet", {text: document.NewForm.InputText.value,
      action: "showCollocations"
    }, function(d) {$("#result").html(d.result);});
  }



  var tashkeel_click = function(e) {
    var collocation = 1;
    var vocalizewWordsEnds = "0";
    if (document.NewForm.LastMark.checked == 1) vocalizewWordsEnds = "1";
    var inputText = document.NewForm.InputText.value;
    inputText = inputText.replace(/(\.+)/g, "\$1\n");
    // replace all spaces to save it in the output
    //~ var textlistOne = inputText.split('\n');
    // use only one text string, make it like this just for compatibility
    
    var textlistOne = inputText.split('######');
   $("#loading").hide();    
    $("#result").html("");
    $("#loading").show();
    $('#loading').data('length', 0);
    
    var textlist = new Array();
    for (var i = 0; i < textlistOne.length; i++) {
      if (textlistOne[i] != "") textlist.push(textlistOne[i]);
    }
    $('#loading').data('length', textlist.length);
    for (var i = 0; i < textlist.length; i++) {
      // split inputtext into lines and clauses
      // add dots to save the phrases number.
      $("#loading").html($("#loading").html() + ".");
      $.getJSON(script + "/ajaxGet", {
        text: textlist[i],
        action: "Tashkeel2",
        order: i.toString(),
        lastmark: vocalizewWordsEnds
      }, function(d) {
      draw_tashkeel_results(d);
      });
    } // end for i intextlist
       $("#loading").hide(); 
    $("#contributeSection").show();
  }
  

  var inflect_click = function(e) {
    var collocation = 1;
    var vocalizewWordsEnds = "0";
    if (document.NewForm.LastMark.checked == 1) vocalizewWordsEnds = "1";
    var inputText = document.NewForm.InputText.value;
    inputText = inputText.replace(/(\.+)/g, "\$1\n");
    // replace all spaces to save it in the output
    //~ var textlistOne = inputText.split('\n');
    // use only one text string, make it like this just for compatibility
    
    var textlistOne = inputText.split('######');
   $("#loading").hide();    
    $("#result").html("");
    $("#loading").show();
    $('#loading').data('length', 0);
    
    var textlist = new Array();
    for (var i = 0; i < textlistOne.length; i++) {
      if (textlistOne[i] != "") textlist.push(textlistOne[i]);
    }
    $('#loading').data('length', textlist.length);
    for (var i = 0; i < textlist.length; i++) {
      // split inputtext into lines and clauses
      // add dots to save the phrases number.
      $("#loading").html($("#loading").html() + ".");
      $.getJSON(script + "/ajaxGet", {
        text: textlist[i],
        action: "Inflect",
        order: i.toString(),
        lastmark: vocalizewWordsEnds
      }, function(d) {
      // draw tashkeel results
      draw_tashkeel_results(d);
      // draw a list of word: inflection
      draw_inflection_results(d);

      });
    } // end for i intextlist
       $("#loading").hide(); 
  }
  

var vocalized_click =function(e) {
       e.preventDefault();
    $(".txkl").change(e);
    var myword = $(this);
    var nextword = $(this).next();
    var id = myword.attr('id');

    var list = $("#result").data(id).suggest.split(';');
    console.log( $("#result").data(id).features)
    //~ var text = "<form><select class='txkl' id='" + id + " size=3'>";
    var text = "<select class='txkl' id='" + id + "' value='"+myword.text()+"'>";
    var cpt = 0;
    for (i in list) {
      if (list[i] != "") {
        if (myword.text() != list[i]) text += "<option>" + list[i] + "</option>";
        else text += "<option selected=" + list[i] + ">" + list[i] + "</option>";
        cpt += 1;
      }
    }
    text += "<option><strong>تعديــل...</strong></option>";
    text += "<option><strong>××إلغاء××</strong></option>";
    text += "</select>";
    // multiple suggestions
    if (cpt > 1) {
        console.log(text)
      myword.replaceWith(text);

    } else {
        // unique suggestions
      text = "<input type='text' class='txkl'  size='10' id='" + myword.attr('id') +
        "' value='" + myword.text() + "'/>";
      myword.replaceWith(text);
    }
//    console.log(myword.text()+";;"+nextword.text())
}


  // spell checking
  var spellcheck_click = function(e) {
    var collocation = 1;
    var vocalizewWordsEnds = "0";
    if (document.NewForm.LastMark.checked == 1) vocalizewWordsEnds = "1";
    var inputText = document.NewForm.InputText.value;
    inputText = inputText.replace(/(\.+)/g, "\$1\n");
    // replace all spaces to save it in the output
    // in order to keep the same typography 
    var textlistOne = inputText.split('\n');
    $("#result").html("");
    $("#loading").show();
    $('#loading').data('length', 0);
    var textlist = new Array();
    for (var i = 0; i < textlistOne.length; i++) {
      if (textlistOne[i] != "") textlist.push(textlistOne[i]);
    }
    $('#loading').data('length', textlist.length);
    for (var i = 0; i < textlist.length; i++) {
      // split inputtext into lines and clauses
      // add dots to save the phrases number.
      $("#loading").html($("#loading").html() + ".");
      $.getJSON(script + "/ajaxGet", {
        text: textlist[i],
        action: "SpellCheck",
        order: i.toString(),
        lastmark: vocalizewWordsEnds
      }, function(d) {
//        console.log(d);
        var text = "";
        var id = parseInt(d.order);
        var openColocation = 0;
        for (var i = 0; i < d.result.length; i++) {
          item = d.result[i];
          var currentId = id * 100 + i;
          //text+=currentId.toString();
          if (item.chosen.indexOf("~~") >= 0) { // handle collocations
            openColocation = 0;
            text += "</span><span class='collocation' title='دقّق تشكيل هذه العبارة'>" +
              item.chosen.replace("~~", "");
          } else if (item.chosen.indexOf("~") >= 0) { // handle collocations
            if (openColocation == 0) {
              openColocation = 1;
              text += item.chosen.replace("~", "") +
                " <span class='collocation' title='دقّق تشكيل هذه العبارة'>";
            } else {
              openColocation = 0;
              text += "</span>" + item.chosen.replace("~", "");
            }
          } else {
            var pattern = /[-[\]{}()*+?.,،:\\^$|#\s]/;
            if (!pattern.test(item.chosen)) text += " ";
            if (item.suggest != '') text += "<span class='spelled-incorrect' id='" +
              currentId + "'>" + item.chosen + "</span>";
            else text += "<span class='spelled' id='" + currentId + "'>" + item.chosen +
              "</span>";
            $('#result').data(currentId.toString(), item.suggest);
          }
        }
        // display the result
        $("#loading").data(d.order, text);
        $("#result").html($("#result").html() + "<p class=\'spellStyle\'>" + text +
          "</p>");
        // dela dot, to count the phrase executed
        $("#loading").html($("#loading").html().replace('.', ''));
        if ($("#loading").html().indexOf('.') < 0) { // if no dot, the work is terminated
          // redraw the text result with order
          var ordredtext = "";
          for (var j = 0; j < $("#loading").data('length'); j++) {
            ordredtext += "<br/>" + $("#loading").data(j.toString());
          }
          $('#result').html("<p class=\'spellStyle\'>" + ordredtext + "</p>");
          $("#loading").hide();
        }
      });
    } // end for i intextlist
    $("#contributeSection").show();
  }

// Handle misspelled words
  var spelled_incorrect_click = function(e) {
      e.preventDefault();
    $(".spld").change(e);
    var myword = $(this);
    var id = myword.attr('id');
    var list = $("#result").data(id).split(';');
    var text = "<select class='spld' id='" + id + "'>";
    var cpt = 0;
    for (i in list) {
      if (list[i] != "") {
        if (myword.text() != list[i]) text += "<option>" + list[i] + "</option>";
        else text += "<option selected=" + list[i] + ">" + list[i] + "</option>";
        cpt += 1;
      }
    }
    text += "<option><strong>تعديــل...</strong></option>";
    text += "</select>";
    // disable others suggestion lists  
    if (cpt > 1) {
      myword.replaceWith(text);
    } else {
      text = "<input type='text' class='spld'  size='10' id='" + myword.attr('id') +
        "' value='" + myword.text() + "'/>";
      myword.replaceWith(text);
    }
  }
  
  var spld_change = function(e) {
      e.preventDefault();
    if ($(this).val() != "تعديــل...") {
      var text = "<span id='" + $(this).attr('id') + "'>" + $(this).val() +
        "</span>";
      $(this).replaceWith(text);
    } else // case of editing other choice
    {
      var list = $("#result").data($(this).attr('id')).suggest.split(';');
      var text = "<input type='text' class='spld'  size='10' id='" + $(this).attr('id') +
        "' value='" + list[0] + "'/>";
      $(this).replaceWith(text);
//       console.log($(this).text()+"-"+$(this).next().text());
    }
 }

  // change diff 
var diff_hover = function() {
    var text = $(this).text() + " : " + $(this).attr('original') + "<br/>"+$(this).attr('inflect')  + "<br/>ق[" + $(this).attr('rule') + "] " + $(this).attr('link') ;
    if ($('#result').data("count")>20) {$('#hint').html(text);  $('#hint').show(); $('#small_hint').hide();}
    else  {$('#small_hint').html(text); $('#small_hint').show();$('#hint').hide();}

  }
  // change diff 
var diff_mouseleave = function() {
    $('#small_hint').html("");
    $('#small_hint').hide();
  }


  // display infos on vocalized  
var vocalized_hover = function(e) {
       e.preventDefault();
    var text = $(this).text() + " : " + $(this).attr('inflect')  + "<br/>ق[" + $(this).attr('rule') + "] " + $(this).attr('link') + "<br/>" + $(this).attr('suggest');
    if ($('#result').data("count")>20)
     {$('#hint').html(text); 
     $('#hint').show();
     $('#small_hint').hide();
     }
    else
    { $('#small_hint').html(text);
    $('#small_hint').show();
    $('#hint').hide();
    }
  }
  // change diff 
var vocalized_mouseleave = function(e) {
       e.preventDefault();
    $('#hint').hide("");
    $('#small_hint').hide("");
        $(".txkl").change(e);
  }
var txkl_mouseleave = function(e) {
       e.preventDefault();
        $(".txkl").change(e);
  }

var txkl_select = function(e) {
       e.preventDefault();
    $(".txkl").change(e);
  }
  
var txkl_pressed = function(e)
{
    e.preventDefault();
    if ((e.which == 27) || (e.which == 13))
    {
      var item = $("#result").data($(this).attr('id'));
      var text = "<span class='vocalized' id='" + $(this).attr('id') + "' suggest='" + item.suggest.replace(/;/g, '، ') +
         "' inflect='معدّل يدويا'rule='معدّل يدويا' link='N/A' >" + $(this).attr('value') + "</span>";
      $(this).replaceWith(text);
      //~ alert('txkl_pressed');
    }
}
    
var txkl_change = function(e) {
    e.preventDefault();

    if ($(this).val() != "تعديــل..." && ($(this).val() != "××إلغاء××")) {
      var item = $("#result").data($(this).attr('id'));
      if("features" in item)
      {var new_inflect = "["+item.features[$(this).val()][0].tagscode+"]{"+item.features[$(this).val()][0].inflect+"}#"+ item.features[$(this).val()][0].tags;
//      console.log("val "+item.features[$(this).val()]);
//      console.log("tags "+item.features[$(this).val()][0]['tags']);
//      console.log("tags "+item.features[$(this).val()][0].tags);
//      console.log("tagscode "+item.features[$(this).val()][0].tagscode);
//      console.log("inflect "+item.features[$(this).val()][0].inflect);
//      console.log("type "+item.features[$(this).val()][0].type);
      }
      else
      {var new_inflect = "معدّل يدويا*";
      }
      var text = "<span class='vocalized' id='" + $(this).attr('id') + "' suggest='" + item.suggest.replace(/;/g, '، ') +
         "' inflect='"+new_inflect+"'rule='معدّل يدويا' link='N/A' >" + $(this).val() + "</span>";

      $(this).replaceWith(text);

    } else if ($(this).val() == "××إلغاء××")
    {
      var item = $("#result").data($(this).attr('id'));
      var text = "<span class='vocalized' id='" + $(this).attr('id') + "' suggest='" + item.suggest.replace(/;/g, '، ') +
         "' inflect='معدّل يدويا'rule='معدّل يدويا' link='N/A' >" + $(this).attr('value') + "</span>";
      $(this).replaceWith(text);
    }
    else // case of editing other choice
    {
      var list = $("#result").data($(this).attr('id')).suggest.split(';');
      text = "<input type='text' class='txkl'  size='10' id='" + $(this).attr('id') +
        "' value='" + list[0] + "'/>";
      $(this).replaceWith(text);
//       console.log($(this).text()+"-"+$(this).next().text());
    }
 }

function draw_inflection_card(i,item)
{
var clonedCard = $("#CardToClone").clone();
clonedCard.attr("id","cardtoclone"+i);
var ph = clonedCard.find("#PHRASE_CLONE")
ph.attr("id","phrase_clone"+i);
ph.html(item.phrase);
clonedCard.find("#INFLECTION_CLONE").html(item.inflection);
clonedCard.find("#collapseContainer").attr("id","collapseContainer"+i);

var x = clonedCard.find(".card-header");
x.attr("data-target", "#collapseContainer"+i);
console.log("X cardheadr: : "+x.attr("data-target"));
//clonedCard.find(".card-header").attr("data-target","#collapseContainer"+i);
return clonedCard;
}

var  lookup_click = function(e) {
        e.preventDefault()

    $("#result").html("");
    var item;

    $.getJSON(script + "/ajaxGet", {
      text: document.NewForm.InputText.value,
      action: "Lookup"
    }, function(d) {
      $("#result").html("");
      for (i = 0; i < d.result.length; i++) {
        item = d.result[i];
//        console.log(i);

        var div_item = draw_inflection_card(i, item );
      $("#result").append(div_item);
      }

    });
  }
// ready document

$().ready(function() {

//  $(document).on( 'click', '#randomMaqola', randomMaqola_handler);
//  $(document).on( 'click', '#affixate', affixate_click );
//  $(document).on( 'click', '#bigrams', bigrams_click );
//  $(document).on( 'click', '#chunk', chunk_click );
//  $(document).on( 'click', '#comparetashkeel', comparetashkeel_click );
  $(document).on( 'click', '#contribute', contribute_click );
  $(document).on( 'click', '#copy', copy_click );
//  $(document).on( 'click', '#csv2data', csv2data_click );
//  $(document).on( 'click', '#extractEnteties', extractEnteties_click );
//  $(document).on( 'click', '#inverse', inverse_click );
//  $(document).on( 'click', '#language', language_click );
  $(document).on( 'click', '#more', more_click );
  $(document).on( 'click', '#move', move_click );
//  $(document).on( 'click', '#named', named_click );
//  $(document).on( 'click', '#normalize', normalize_click );
//  $(document).on( 'click', '#number', number_click );
//  $(document).on( 'click', '#numbred', numbred_click );
//  $(document).on( 'click', '#poetry', poetry_click );
  $(document).on( 'click', '#random', random_click );
//  $(document).on( 'click', '#reducetashkeel', reducetashkeel_click );
//  $(document).on( 'click', '#showCollocations', showCollocations_click );
  $(document).on( 'click', '#stripharakat', stripharakat_click );
//  $(document).on( 'click', '#spellcheck', spellcheck_click );

//  $(document).on( 'click', '#tashkeel2', tashkeel2_click );
  $(document).on( 'click', '#tashkeel', tashkeel_click );
//  $(document).on( 'click', '#tokenize', tokenize_click );
//  $(document).on( 'click', '#unshape', unshape_click );
  $(document).on( 'click', '#vocalize_group', vocalize_group_click );
//  $(document).on( 'click', '#stem', stem_click );
//  $(document).on( 'click', '#wordtag', wordtag_click );
//  $(document).on( 'click', '.spelled-incorrect', spelled_incorrect_click );
//  $(document).on( 'change', '.spld', spld_change );
//  $(document).on( 'mouseleave', '#diff', diff_mouseleave );
//  $(document).on( 'mouseover', '#diff', diff_hover );
  $(document).on( 'mouseover', '.vocalized', vocalized_hover );
  $(document).on( 'change', '.txkl', txkl_change );
  $(document).on( 'keyup', '.txkl', txkl_pressed );
  $(document).on( 'click', '.vocalized', vocalized_click );
  
  $(document).on( 'click', '#synt', inflect_click );
  $(document).on( 'click', '#lookup', lookup_click );

  // forms
  // ask for expert form
  $(document).on( 'click', '#submit-ask', ask_click);
  $(document).on( 'click', '#submit-signal', signal_click);
  $(document).on( 'click', '#submit-contact', contact_click);
  $(document).on( 'click', '#submit-edit', edit_click);

  $(document).on( 'click', '#copy-card', copy_card_click );
});

