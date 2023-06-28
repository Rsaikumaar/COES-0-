function going(){
	if(document.getElementById('Upload').checked)
	{
		document.getElementById('goto').action='/go';
		document.getElementById('goto').method='post';
	}
	else if(document.getElementById('Import').checked)
	{
		document.getElementById('goto').action='/goim';
		document.getElementById('goto').method='post';
	}
}


/*
	Second radio button
*/
function change1(){
		if(document.getElementById('v-r').checked)
		{
			let text="<h1>Open the Exam of v-r</h1>";
				document.getElementById('add1').innerHTML=text;
		}
		else if(document.getElementById('r-v').checked)
		{
			let text="<h1>Open the Exam of r-v</h1>";
				document.getElementById('add1').innerHTML=text;	
				change3();
		}
		else if(document.getElementById('v-v').checked)
		{
			let text="<h1>Open the Exam of v-v</h1>";
				document.getElementById('add1').innerHTML=text;
		}
		
	}
		function change2(){
			if(document.getElementById('fill').checked)
		{
			let text="<h1>Open the Exam of fill</h1>"+
			"Formate of Excel :|subject|question|ans";
				document.getElementById('add1').innerHTML=text;
		}
			else if(document.getElementById('MCQ').checked)
		{
			let text="<h1>Open the Exam of MCQ</h1>"+
			"Formate of Excel :subject|question|opt1|opt2|opt3|opt4|main";
				document.getElementById('add1').innerHTML=text;
		}
		


}

/*
	First radio button
*/
function change(){
			if(document.getElementById('voice').checked)
			{let text="<h1>Open the Exam of voice</h1>Formate of Excel :|subject|question";
/*let text="<div >"+
		 "<label for='cat'><b>Select catogary</b></label><br>"+
		 "<input type='radio'  name='vexam' onclick='change1()' id='v-r' required>"+
		 "<label for'exm'>(1)Listen Voice and Written</label><br>"+
		 "<input type='radio'  name='vexam' onclick='change1()' id='r-v' required>"+
		 "<label for'exm'>(2)See and Read </label><br>"+
		 "<input type='radio'  name='vexam' onclick='change1()' id='v-v' required>"+
		 "<label for'exm'>(3)Listen and Read </label><br>"+
		 "</div>";*/
		 		document.getElementById('add1').innerHTML="";
				document.getElementById('add').innerHTML=text;
			}
			else 
				if(document.getElementById('nvoice').checked)
			{
let text="<div >"+
		 "<label for='cat'><b>Select catogary</b></label><br>"+
		 "<input type='radio' name='nvexam' value='fill' onclick='change2()' id='fill' required>"+
		 "<label for'exm'>(1)Fill In The Blanks</label><br>"+
		 "<input type='radio'  name='nvexam' value='MCQ' onclick='change2()' id='MCQ' required>"+
		 "<label for'exm'>(2)Multiple Choice </label><br>"+
		 "</div>";
		 		document.getElementById('add1').innerHTML="";
				document.getElementById('add').innerHTML=text;
			}
		}
