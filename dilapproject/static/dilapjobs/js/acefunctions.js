$('.row .btn').on('click', function(e) {
	e.preventDefault();
	var $this = $(this);
	var $collapse = $this.closest('.collapse-group').find('.collapse');
	$collapse.collapse('toggle');
});

$("tableX").each(function() {
	var $this = $(this);
	var newrows = [];

	$this.find("tr").each(function(){
		var i = 0;

		$(this).find("td").each(function(){
			i++;
			if(newrows[i] === undefined) { newrows[i] = $(""); }
			newrows[i].append($(this));
		});
	});

	$this.find("tr").remove();
	$.each(newrows, function(){
		$this.append(this);
	});
});

function add(type){
	var foo = document.getElementById(type);

	var element = document.createElement("input");

	element.setAttribute("type", "text");
	element.setAttribute("placeholder", "Enter Neighbouring Property");

	if (type == "fooBar_e"){
		element.setAttribute("name", "neighbours_e[]");
		element.setAttribute("style", "width: 100%");
	} else {
		element.setAttribute("name", "neighbours[]");
		element.setAttribute("style", "width: 30%; margin-right: 4px");
	}
	element.setAttribute("class", "form-control");

	foo.appendChild(element);
	count = 0;
	while (count < 3){

		var elementl = document.createElement("input");

		elementl.setAttribute("type", "text");
		if (type == "fooBar_e"){
			elementl.setAttribute("name", "letters_e[]");
			elementl.setAttribute("style", "width: 20%; float: left");
		} else {
			elementl.setAttribute("name", "letters[]");
			elementl.setAttribute("style", "width: 14%; margin-right: 4px");
		}
		elementl.setAttribute("class", "form-control datepicker");
		elementl.setAttribute("value", "none");

		foo.appendChild(elementl);


		var sel = document.createElement("select");

		if (type == "fooBar_e"){
			sel.setAttribute("name", "letters_e[]");
			sel.setAttribute("style", "float: left");
		} else {
			sel.setAttribute("name", "letters[]");
			sel.setAttribute("style", "margin-right: 4px")
		}

		var option0 = document.createElement("option");
		var option1 = document.createElement("option");
		var option2 = document.createElement("option");
		var option3 = document.createElement("option");
		var option4 = document.createElement("option");
		var option5 = document.createElement("option");
		option0.text = ""
		option1.text = "RM"
		option2.text = "AP"
		option3.text = "HD"
		option4.text = "STR"
		option5.text = "EMA"
		sel.add(option0)
		sel.add(option1)
		sel.add(option2)
		sel.add(option3)
		sel.add(option4)
		sel.add(option5)

		foo.appendChild(sel);

		count = count + 1;

		$(".datepicker").each(function() {
			$(this).datepicker({constrainInput: false, dateFormat: 'dd/mm/yy'});
		});
	}
}

function addC(type){
	var foo = document.getElementById(type);

	var element = document.createElement("input");

	element.setAttribute("type", "text");
	element.setAttribute("placeholder", "Enter Council Asset");

	if (type == "fooBar_ce"){
		element.setAttribute("name", "councilassets_e[]");
		element.setAttribute("style", "width: 100%");
	} else {
		element.setAttribute("name", "councilassets[]");
		element.setAttribute("style", "width: 90%");
	}
	element.setAttribute("class", "form-control");
	foo.appendChild(element);
}

function fillup(id){
	var details = document.getElementById(id);

	var jobNum = details.getAttribute('data-job');
	var client = details.getAttribute('data-client');
	var address = details.getAttribute('data-address');
	var notes = details.getAttribute('data-notes');
	var councilassets = details.getAttribute('data-councilassets');
	var neighbours = details.getAttribute('data-neighbours');
	var letters = details.getAttribute('data-letters');

	document.getElementsByName("old_jobnumber_e")[0].setAttribute("value", jobNum);
	document.getElementsByName("jobnumber_e")[0].setAttribute("value", jobNum);
	document.getElementsByName("client_e")[0].setAttribute("value", client);
	document.getElementsByName("address_e")[0].setAttribute("value", address);
	document.getElementsByName("notes_e")[0].setAttribute("value", notes);

	////////////////// generate council assets
	if (councilassets == ""){
		var lenc = 0;
	} else {
		var councilassets_a = councilassets.split('|');
		var lenc = councilassets_a.length;
	}
	var tmpc = document.getElementsByName("councilassets_e[]").length;
	while (tmpc < lenc){
		addC('fooBar_ce');
		tmpc = tmpc + 1;
	}
	var t = 0;
	while (t < councilassets_a.length){
		document.getElementsByName("councilassets_e[]")[t].setAttribute("value", councilassets_a[t]);
		t = t + 1;
	}
	////////////////// generate letters and neighbours
	var letters_combined_a = letters.split('|');
	if (neighbours == ""){
		var len = 0;
	} else {
		var neighbours_a = neighbours.split('|');
		var len = neighbours_a.length;
	}
	
	var tmp = document.getElementsByName("neighbours_e[]").length;
	while (tmp < len){
		add('fooBar_e');
		tmp = tmp + 1;
	}
	var i = 0;
	var l = 0;
	while (i < len){
		var letters_a = letters_combined_a[i].split(" ");
		document.getElementsByName("neighbours_e[]")[i].setAttribute("value", neighbours_a[i]);

		document.getElementsByName("letters_e[]")[l].setAttribute("value", letters_a[0]);
		document.getElementsByName("letters_e[]")[l+1].value = letters_a[1];
		document.getElementsByName("letters_e[]")[l+2].setAttribute("value", letters_a[2]);
		document.getElementsByName("letters_e[]")[l+3].value = letters_a[3];
		document.getElementsByName("letters_e[]")[l+4].setAttribute("value", letters_a[4]);
		document.getElementsByName("letters_e[]")[l+5].value = letters_a[5];
		i = i + 1;
		l = l + 6;
	}
}

$(document).ready(function(){
	$(".datepicker").each(function() {
		$(this).datepicker({constrainInput: false, dateFormat: 'dd/mm/yy'});
	});
	$(".no-space").keypress(function(key){
		if (key.charCode == 32) return false;
	});
	$('#oneclick').click(function(){
		$(this).attr('disabled', true);
		document.getElementById("create_form").submit();
	});
	$('#oneclick_e').click(function(){
		$(this).attr('disabled', true);
		document.getElementById("edit_form").submit();
	});
});